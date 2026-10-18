"""Two-pass lockstep runner for the caption->image->caption loop (SPEC §8).

For each step t: SDXL pass over every trajectory that lacks image t, release the GPU, LLaVA pass over every trajectory
that lacks caption t, unload LLaVA, next step. Resume is by file presence (src/store.py), so the process can be killed
at any moment and restarted with the same command. Controls come from runs/<run>/control.json at pass boundaries.

    .venv/bin/python -m src.runner configs/a0_pilot.yaml [--steps N] [--count N]
"""
import argparse, datetime, hashlib, json, logging, os, pathlib, pickle, signal, socket, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

from .config import load_config
from .store import TrajStore, atomic_write_json, append_jsonl, read_json
from .gpu_log import GpuLogger, vram_used_mb

ROOT = pathlib.Path(__file__).resolve().parents[1]


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def git_commit():
    """HEAD of the repo; on a pod without .git, the GIT_COMMIT file written by scripts/runpod_sync.sh push."""
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if out:
            return out
    except Exception:  # noqa: BLE001
        pass
    f = ROOT / "GIT_COMMIT"
    return f.read_text().strip() if f.exists() else None


def package_versions():
    import importlib.metadata as md
    return {p: md.version(p) for p in ("torch", "torchvision", "diffusers", "transformers", "accelerate", "safetensors", "pillow", "numpy", "ollama")}


class Runner:
    def __init__(self, cfg):
        self.cfg = cfg
        self.run_dir = ROOT / "runs" / cfg["run_name"]
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (ROOT / "logs").mkdir(exist_ok=True)
        self.log = logging.getLogger("runner")
        self.log.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        for h in (logging.FileHandler(ROOT / "logs" / f"{cfg['run_name']}.log"), logging.StreamHandler(sys.stdout)):
            h.setFormatter(fmt); self.log.addHandler(h)
        self.stop_requested = False
        signal.signal(signal.SIGTERM, self._on_signal); signal.signal(signal.SIGINT, self._on_signal)

        seeds_path = ROOT / cfg["seeds"]["file"]
        self.seed_prompts = pickle.load(open(seeds_path, "rb"))
        self.seeds_sha = hashlib.sha256(seeds_path.read_bytes()).hexdigest()
        tr = cfg["trajectories"]
        self.traj_ids = list(range(tr["first"], tr["first"] + tr["count"]))
        self.stores = {t: TrajStore(self.run_dir, t, self.seed_prompts[t]) for t in self.traj_ids}

        from .generators.sdxl import SDXLGenerator
        from .captioners.ollama_llava import OllamaCaptioner
        self.gen = SDXLGenerator(cfg["generator"])
        self.cap = OllamaCaptioner(cfg["captioner"], cfg["temperature"], self.log)
        self.gpu = GpuLogger(ROOT / cfg["gpu_log"]["path"], cfg["gpu_log"]["interval_s"], cfg["run_name"])
        self.step_times = []
        self.control_path = self.run_dir / "control.json"
        self.progress_path = self.run_dir / "progress.json"
        self.events_path = self.run_dir / "events.jsonl"
        self._phase = "init"

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, v):
        self._phase = v
        self.gpu.phase = v

    # ---- bookkeeping -------------------------------------------------------------------------------------------
    def _on_signal(self, signum, _frame):
        self.log.warning("signal %s received: finishing the current item, then stopping", signum)
        self.stop_requested = True

    def write_manifest(self):
        path = self.run_dir / "manifest.json"
        resumed_from = {t: s.last_complete_step() for t, s in self.stores.items()}
        if not path.exists():
            atomic_write_json(path, {
                "run_name": self.cfg["run_name"], "arm": self.cfg["arm"], "created": now(), "host": socket.gethostname(),
                "git_commit": git_commit(), "config_path": self.cfg["_config_path"], "config_sha256": self.cfg["_config_sha256"],
                "config": {k: v for k, v in self.cfg.items() if not k.startswith("_")},
                "seeds_file_sha256": self.seeds_sha, "trajectories": self.traj_ids,
                "packages": package_versions(), "python": sys.version.split()[0],
                "captioner": self.cap.info(), "nvidia_smi": subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip(),
            })
            self.log.info("manifest written: %s", path)
        else:
            m = read_json(path)
            if m["config_sha256"] != self.cfg["_config_sha256"]:
                self.log.warning("config hash differs from the manifest's (%s vs %s); the run continues with the manifest's parameters in force for fidelity checks",
                                 self.cfg["_config_sha256"][:8], m["config_sha256"][:8])
        append_jsonl(self.events_path, {"ts": now(), "event": "start", "pid": os.getpid(), "git_commit": git_commit(),
                                        "config_sha256": self.cfg["_config_sha256"], "last_complete_step": resumed_from})
        if not self.control_path.exists():
            atomic_write_json(self.control_path, {"state": "running"})

    def control_state(self):
        try:
            return read_json(self.control_path).get("state", "running")
        except Exception:  # noqa: BLE001
            return "running"

    def progress(self, step, state="running", extra=None):
        latest = {t: s.last_complete_step() for t, s in self.stores.items()}
        rec = {"run_name": self.cfg["run_name"], "state": state, "pid": os.getpid(), "updated": now(), "step": step,
               "phase": self.phase, "steps_total": self.cfg["steps"], "n_traj": len(self.traj_ids),
               "latest_complete_step": latest, "completed_steps": sum(v + 1 for v in latest.values()),
               "total_steps": self.cfg["steps"] * len(self.traj_ids)}
        if self.step_times:
            recent = self.step_times[-5:]
            per_traj_step = sum(x["s_per_traj_step"] for x in recent) / len(recent)
            remaining = rec["total_steps"] - rec["completed_steps"]
            rec.update({"s_per_traj_step": round(per_traj_step, 1), "eta_hours": round(per_traj_step * remaining / 3600, 2),
                        "last_step": self.step_times[-1]})
        if extra: rec.update(extra)
        atomic_write_json(self.progress_path, rec)

    def wait_if_paused(self, step):
        waited = False
        while self.control_state() == "paused" and not self.stop_requested:
            if not waited:
                self.log.info("paused by control.json; GPU released"); self.gen.release(); self.cap.unload(); waited = True
                self.phase = "paused"; self.progress(step, "paused")
            time.sleep(5)
        if self.control_state() == "stopped":
            self.stop_requested = True
        return waited

    def wait_for_vram(self, label):
        thr = self.cfg["vram_free_threshold_mb"]
        for _ in range(60):
            used = vram_used_mb()
            if used < thr:
                return used
            time.sleep(1)
        self.log.warning("%s: VRAM still %.0f MB after 60 s (threshold %d)", label, used, thr)
        return used

    # ---- main loop ---------------------------------------------------------------------------------------------
    def run(self):
        self.write_manifest()
        self.gpu.start()
        self.log.info("run %s: %d trajectories x %d steps, mode=%s, T=%s", self.cfg["run_name"], len(self.traj_ids), self.cfg["steps"], self.cfg["mode"], self.cfg["temperature"])
        two_pass = self.cfg["mode"] == "two_pass"
        if two_pass:
            self.cap.unload()
        gen_info = None
        try:
            for step in range(self.cfg["steps"]):
                todo_cap = [t for t in self.traj_ids if not self.stores[t].is_complete(step)]
                if not todo_cap:
                    continue
                todo_gen = [t for t in todo_cap if not self.stores[t].has_image(step)]
                t_step = time.time()
                self.wait_if_paused(step)
                if self.stop_requested: break

                # ---- pass 1: SDXL ----
                t_gen = time.time(); n_gen = 0
                if todo_gen:
                    self.phase = f"sdxl step {step}"; self.progress(step)
                    if two_pass: self.wait_for_vram("before SDXL")
                    self.gen.load(); gen_info = gen_info or self.gen.info()
                    B = max(1, int(self.cfg["generator"].get("batch", 1)))
                    for i0 in range(0, len(todo_gen), B):
                        chunk = todo_gen[i0:i0 + B]
                        prompts, sources, seeds = [], [], []
                        for t in chunk:
                            prompt, source = self.stores[t].prompt_for(step)
                            prompts.append(prompt); sources.append(source)
                            seeds.append(self.cfg["seeds"]["sdxl_base_seed"] + t * 10000 + step)
                        results = self.gen.generate_batch(prompts, seeds)
                        for t, prompt, source, seed, (image, ginfo) in zip(chunk, prompts, sources, seeds, results):
                            self.stores[t].write_image(step, image, {"run": self.cfg["run_name"], "arm": self.cfg["arm"], "traj": t, "step": step,
                                                                     "prompt": prompt, "prompt_source": source, "prompt_words": len(prompt.split()),
                                                                     "sdxl_seed": seed, "generator": gen_info, "generated_at": now(), **ginfo})
                            n_gen += 1
                            self.log.info("step %3d traj %3d image %5.1fs (batch %d) peak %.2f GB tokens %d%s", step, t, ginfo["gen_time_s"], ginfo["gen_batch_size"],
                                          ginfo["gen_peak_alloc_gb"], ginfo["prompt_tokens_clip"], " (clip-truncated)" if ginfo["prompt_truncated_by_clip"] else "")
                        if self.stop_requested: break
                    if two_pass:
                        left = self.gen.release(); self.log.info("SDXL released, torch alloc %.2f GB, nvidia-smi %.0f MB", left, vram_used_mb())
                gen_s = time.time() - t_gen
                if self.stop_requested: break
                self.wait_if_paused(step)
                if self.stop_requested: break

                # ---- pass 2: LLaVA ----
                t_cap = time.time(); n_cap = 0
                self.phase = f"llava step {step}"; self.progress(step)
                if two_pass: self.wait_for_vram("before LLaVA")
                cap_info = self.cap.info()
                todo_cap = [t for t in todo_cap if not self.stores[t].is_complete(step)]

                def caption_one(t):
                    st = self.stores[t]
                    text, cmeta = self.cap.caption(st.png(step), keep_alive=self.cfg["captioner"]["keep_alive_during_pass"])
                    rec = read_json(st.gen(step))
                    rec.update({"caption": text, "captioner": cap_info, "captioned_at": now(), **cmeta,
                                "pipeline_git": git_commit(), "config_sha256": self.cfg["_config_sha256"]})
                    st.write_record(step, rec)
                    fl = [k for k, v in cmeta["caption_flags"].items() if v]
                    self.log.info("step %3d traj %3d caption %5.1fs %3d words%s", step, t, cmeta["caption_time_s"], cmeta["caption_words"], (" flags=" + ",".join(fl)) if fl else "")
                    return t

                P = max(1, int(self.cfg["captioner"].get("parallel", 1)))
                if P == 1:
                    for t in todo_cap:
                        caption_one(t); n_cap += 1
                        if self.stop_requested: break
                else:
                    with ThreadPoolExecutor(max_workers=P) as ex:
                        for i0 in range(0, len(todo_cap), P):          # submit one wave at a time so a stop request is honoured promptly
                            for _ in ex.map(caption_one, todo_cap[i0:i0 + P]): n_cap += 1
                            if self.stop_requested: break
                if two_pass and self.cfg["captioner"]["unload_after_pass"]:
                    self.cap.unload()
                cap_s = time.time() - t_cap
                n = max(n_gen, n_cap, 1)
                rec = {"step": step, "n_traj": n, "gen_s": round(gen_s, 1), "cap_s": round(cap_s, 1), "step_s": round(time.time() - t_step, 1),
                       "s_per_traj_step": round((time.time() - t_step) / n, 1), "ts": now()}
                self.step_times.append(rec)
                append_jsonl(self.events_path, {"event": "step_done", **rec})
                self.progress(step)
                self.log.info("step %3d done: %.0fs total, %.1fs per trajectory-step (sdxl %.1fs, llava %.1fs per traj); eta %.1f h",
                              step, rec["step_s"], rec["s_per_traj_step"], gen_s / n, cap_s / n, read_json(self.progress_path).get("eta_hours", float("nan")))
                if self.stop_requested: break
        finally:
            self.phase = "exit"
            done = all(s.last_complete_step() >= self.cfg["steps"] - 1 for s in self.stores.values())
            state = "finished" if done else ("stopped" if self.stop_requested else "crashed")
            try:
                self.gen.release(); self.cap.unload()
            except Exception:  # noqa: BLE001
                pass
            self.progress(-1, state)
            append_jsonl(self.events_path, {"ts": now(), "event": state, "pid": os.getpid()})
            self.gpu.stop()
            self.log.info("exit: %s", state)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--run-name")
    ap.add_argument("--steps", type=int)
    ap.add_argument("--count", type=int, help="number of trajectories (override)")
    a = ap.parse_args(argv)
    cfg = load_config(a.config)
    if a.run_name: cfg["run_name"] = a.run_name
    if a.steps: cfg["steps"] = a.steps
    if a.count: cfg["trajectories"]["count"] = a.count
    if cfg["generator"].get("alloc_conf"):
        os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", cfg["generator"]["alloc_conf"])
    Runner(cfg).run()


if __name__ == "__main__":
    main()
