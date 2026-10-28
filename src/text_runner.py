"""Lockstep runner for the E3 text loops (SPEC2 §4 E3, amended 2026-10-28).

State = the story. Two loops:
  compress_expand (E3-1): story_k -> summary_k (compress instruction) ; story_{k+1} = expand(summary_k)   [caption -> image -> caption analog]
  rewrite         (E3-2): story_{k+1} = rewrite(story_k)                                                   [no bottleneck]
Step 0 is expand(seed) for both loops; a rewrite run normally copies step 0 from its compress_expand sibling (step0.source) so the two
loops of one model start from identical stories. One record per (trajectory, step), written atomically after every call of the step
has returned; resume is by file presence, so the process can be killed at any moment and restarted with the same command.
Controls: runs/<run>/control.json {"state": running|paused|stopped} read between waves.

    .venv/bin/python -m src.text_runner configs/e3_1_qwen_smoke.yaml [--steps N] [--count N]
"""
import argparse, copy, datetime, hashlib, json, logging, os, pathlib, pickle, signal, socket, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

import yaml
from .config import deep_merge
from .store import TextTrajStore, atomic_write_json, append_jsonl, read_json, sha256_bytes
from .gpu_log import GpuLogger
from .runner import git_commit, package_versions, now

ROOT = pathlib.Path(__file__).resolve().parents[1]

TEXT_DEFAULTS = {
    "run_name": None,
    "arm": "E3-1",
    "loop": "compress_expand",          # compress_expand (E3-1) | rewrite (E3-2)
    "steps": 100,                       # stories per trajectory; story 0 = expand(seed)
    "trajectories": {"first": 0, "count": 20},
    "temperature": 0.9,
    "seeds": {"file": "hintze_osf/Generation Scripts For HPCC/reservoir_100.pkl"},
    "step0": {"source": None},          # run name whose step_000 stories are copied (rewrite runs); None = generate step 0 here
    "instructions": {                   # SPEC2 §4 E3; the text follows the instruction after a blank line
        "expand": "Write a short story of about 500 words based on the following description. Return only the story. Do not explain.",
        "compress": "Summarize this story. The summary must be 50 words or fewer. Do not exceed the limit. Return only the summary. Do not explain.",
        "rewrite": "Rewrite this story, same length. Return only the story. Do not explain.",
    },
    "model": {
        "backend": "ollama",            # ollama | anthropic
        "model": "qwen2.5vl:7b",
        "digest_prefix": "5ced39dfa4ba",
        "host": "http://127.0.0.1:11434",
        "keep_alive": "10m",
        "unload_at_exit": True,
        "timeout_s": 600,
        "retries": 5,
        "parallel": 1,                  # trajectories advanced concurrently (Ollama: pair with OLLAMA_NUM_PARALLEL)
        "max_tokens_story": 4000,       # anthropic only (thinking counts against it); Ollama has no cap, as in the caption loop
        "max_tokens_summary": 1000,
        "effort": "low",                # anthropic only
    },
    "gpu_log": {"interval_s": 10, "path": "logs/gpu.csv"},
}


def load_text_config(path):
    path = pathlib.Path(path); raw = path.read_bytes()
    cfg = deep_merge(TEXT_DEFAULTS, yaml.safe_load(raw) or {})
    if not cfg.get("run_name"): cfg["run_name"] = path.stem
    if cfg["loop"] not in ("compress_expand", "rewrite"): raise ValueError(f"loop must be compress_expand or rewrite, not {cfg['loop']!r}")
    cfg["_config_path"] = str(path); cfg["_config_sha256"] = hashlib.sha256(raw).hexdigest()
    return cfg


def words(t): return len(t.split())


class TextRunner:
    def __init__(self, cfg):
        self.cfg = cfg
        self.run_dir = ROOT / "runs" / cfg["run_name"]; self.run_dir.mkdir(parents=True, exist_ok=True)
        (ROOT / "logs").mkdir(exist_ok=True)
        self.log = logging.getLogger("text_runner"); self.log.setLevel(logging.INFO); self.log.handlers.clear()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        for h in (logging.FileHandler(ROOT / "logs" / f"{cfg['run_name']}.log"), logging.StreamHandler(sys.stdout)):
            h.setFormatter(fmt); self.log.addHandler(h)
        self.stop_requested = False
        signal.signal(signal.SIGTERM, self._on_signal); signal.signal(signal.SIGINT, self._on_signal)

        seeds_path = ROOT / cfg["seeds"]["file"]
        self.seeds_sha = hashlib.sha256(seeds_path.read_bytes()).hexdigest()
        self.seed_prompts = pickle.load(open(seeds_path, "rb"))
        tr = cfg["trajectories"]
        count = tr["count"] if tr.get("count") is not None else len(self.seed_prompts) - tr["first"]
        self.traj_ids = list(range(tr["first"], tr["first"] + count))
        if self.traj_ids and self.traj_ids[-1] >= len(self.seed_prompts):
            raise ValueError(f"trajectories {tr} exceed the {len(self.seed_prompts)} seeds")
        self.stores = {t: TextTrajStore(self.run_dir, t, self.seed_prompts[t]) for t in self.traj_ids}

        m = cfg["model"]
        if m["backend"] == "anthropic":
            from .textgen.claude_text import ClaudeText
            self.model = ClaudeText(m, cfg["temperature"], self.log)
        else:
            from .textgen.ollama_text import OllamaText
            self.model = OllamaText(m, cfg["temperature"], self.log)
        self.model_info = self.model.info()
        self.step0_dir = None
        if cfg["step0"].get("source"):
            self.step0_dir = ROOT / "runs" / cfg["step0"]["source"]
            src_manifest = read_json(self.step0_dir / "manifest.json")
            sm = src_manifest["model"]
            if (sm.get("model"), sm.get("digest")) != (self.model_info.get("model"), self.model_info.get("digest")):
                raise RuntimeError(f"step0 source {self.step0_dir.name} ran {sm.get('model')} {sm.get('digest')}, this run uses {self.model_info.get('model')} {self.model_info.get('digest')}; step 0 must come from the same model")
            if src_manifest["config"]["instructions"]["expand"] != cfg["instructions"]["expand"]:
                raise RuntimeError("step0 source used a different expand instruction")
        self.gpu = GpuLogger(ROOT / cfg["gpu_log"]["path"], cfg["gpu_log"]["interval_s"], cfg["run_name"])
        self.step_times = []
        self.control_path = self.run_dir / "control.json"; self.progress_path = self.run_dir / "progress.json"; self.events_path = self.run_dir / "events.jsonl"

    def _on_signal(self, signum, _frame):
        self.log.warning("signal %s received: finishing the current wave, then stopping", signum); self.stop_requested = True

    # ---- bookkeeping ----
    def write_manifest(self):
        path = self.run_dir / "manifest.json"
        resumed_from = {t: s.last_complete_step() for t, s in self.stores.items()}
        if not path.exists():
            atomic_write_json(path, {
                "run_name": self.cfg["run_name"], "arm": self.cfg["arm"], "loop": self.cfg["loop"], "created": now(), "host": socket.gethostname(),
                "git_commit": git_commit(), "config_path": self.cfg["_config_path"], "config_sha256": self.cfg["_config_sha256"],
                "config": {k: v for k, v in self.cfg.items() if not k.startswith("_")},
                "seeds_file_sha256": self.seeds_sha, "trajectories": self.traj_ids, "seed_prompts": {t: self.seed_prompts[t] for t in self.traj_ids},
                "packages": package_versions(), "python": sys.version.split()[0], "model": self.model_info,
                "step0_source_manifest_sha256": sha256_bytes((self.step0_dir / "manifest.json").read_bytes()) if self.step0_dir else None,
                "nvidia_smi": subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip(),
            })
            self.log.info("manifest written: %s", path)
        else:
            mf = read_json(path)
            if mf["config_sha256"] != self.cfg["_config_sha256"]:
                self.log.warning("config hash differs from the manifest's (%s vs %s)", self.cfg["_config_sha256"][:8], mf["config_sha256"][:8])
        append_jsonl(self.events_path, {"ts": now(), "event": "start", "pid": os.getpid(), "git_commit": git_commit(), "config_sha256": self.cfg["_config_sha256"], "last_complete_step": resumed_from})
        if not self.control_path.exists(): atomic_write_json(self.control_path, {"state": "running"})

    def control_state(self):
        try: return read_json(self.control_path).get("state", "running")
        except Exception: return "running"  # noqa: BLE001

    def progress(self, step, state="running"):
        latest = {t: s.last_complete_step() for t, s in self.stores.items()}
        rec = {"run_name": self.cfg["run_name"], "state": state, "pid": os.getpid(), "updated": now(), "step": step, "phase": self.gpu.phase,
               "steps_total": self.cfg["steps"], "n_traj": len(self.traj_ids), "latest_complete_step": latest,
               "completed_steps": sum(v + 1 for v in latest.values()), "total_steps": self.cfg["steps"] * len(self.traj_ids)}
        if self.step_times:
            recent = self.step_times[-5:]; per = sum(x["s_per_traj_step"] for x in recent) / len(recent)
            rec.update({"s_per_traj_step": round(per, 1), "eta_hours": round(per * (rec["total_steps"] - rec["completed_steps"]) / 3600, 2), "last_step": self.step_times[-1]})
        atomic_write_json(self.progress_path, rec)

    def wait_if_paused(self, step):
        waited = False
        while self.control_state() == "paused" and not self.stop_requested:
            if not waited:
                self.log.info("paused by control.json"); self.model.unload(); waited = True; self.gpu.phase = "paused"; self.progress(step, "paused")
            time.sleep(5)
        if self.control_state() == "stopped": self.stop_requested = True

    # ---- one trajectory-step ----
    def _call(self, instruction, text, max_tokens):
        return self.model.generate(instruction + "\n\n" + text, keep_alive=self.cfg["model"]["keep_alive"], max_tokens=max_tokens)

    def do_step(self, t, step):
        st = self.stores[t]; cfg = self.cfg; ins = cfg["instructions"]; m = cfg["model"]
        rec = {"run": cfg["run_name"], "arm": cfg["arm"], "loop": cfg["loop"], "traj": t, "step": step, "seed_prompt": st.seed_prompt}
        if step == 0 and self.step0_dir:                      # shared step 0: copy the sibling run's story
            src = read_json(self.step0_dir / f"traj_{t:03d}" / "step_000.json")
            if src["seed_prompt"] != st.seed_prompt: raise RuntimeError(f"traj {t}: seed differs from the step0 source")
            story = src["story"]
            rec.update({"input": st.seed_prompt, "input_source": f"step0_copy:{self.step0_dir.name}", "story": story,
                        "story_sha256": sha256_bytes(story.encode("utf-8")), "story_meta": {"copied_from": src.get("story_sha256"), "time_s": 0.0, "flags": src["story_meta"]["flags"]}})
        else:
            text, source = st.input_for(step, cfg["loop"])
            instruction = ins["rewrite"] if (cfg["loop"] == "rewrite" and step > 0) else ins["expand"]
            story, smeta = self._call(instruction, text, m["max_tokens_story"])
            rec.update({"input": text, "input_source": source, "instruction": instruction, "story": story, "story_sha256": sha256_bytes(story.encode("utf-8")), "story_meta": smeta})
        rec.update({"story_words": words(story), "story_chars": len(story)})
        if step > 0:
            w0 = read_json(st.rec(0))["story_words"]; rec["length_ratio"] = round(rec["story_words"] / w0, 3) if w0 else None
        if cfg["loop"] == "compress_expand":
            summary, cmeta = self._call(ins["compress"], story, m["max_tokens_summary"])
            cmeta["flags"]["over_50_words"] = words(summary) > 50
            rec.update({"compress_instruction": ins["compress"], "summary": summary, "summary_words": words(summary), "summary_meta": cmeta})
        rec.update({"model": self.model_info, "generated_at": now(), "pipeline_git": git_commit(), "config_sha256": cfg["_config_sha256"]})
        st.write_record(step, rec)
        flags = [k for k, v in rec["story_meta"]["flags"].items() if v] + ([f"summary:{k}" for k, v in rec["summary_meta"]["flags"].items() if v] if "summary_meta" in rec else [])
        self.log.info("step %3d traj %3d story %4d words%s%s %5.1fs%s", step, t, rec["story_words"],
                      f" (x{rec['length_ratio']})" if "length_ratio" in rec else "", f", summary {rec['summary_words']} words" if "summary" in rec else "",
                      rec["story_meta"]["time_s"] + (rec["summary_meta"]["time_s"] if "summary_meta" in rec else 0), (" flags=" + ",".join(flags)) if flags else "")
        return t

    # ---- main loop ----
    def run(self):
        self.write_manifest(); self.gpu.start()
        self.log.info("run %s: loop=%s, %d trajectories x %d steps, model=%s %s, T=%s (applied: %s), parallel=%d", self.cfg["run_name"], self.cfg["loop"], len(self.traj_ids),
                      self.cfg["steps"], self.model_info["model"], (self.model_info.get("digest") or "")[:12], self.cfg["temperature"], self.model_info.get("temperature_applied"), self.cfg["model"]["parallel"])
        P = max(1, int(self.cfg["model"]["parallel"]))
        try:
            for step in range(self.cfg["steps"]):
                todo = [t for t in self.traj_ids if not self.stores[t].is_complete(step)]
                if not todo: continue
                t_step = time.time(); self.wait_if_paused(step)
                if self.stop_requested: break
                self.gpu.phase = f"text step {step}"; self.progress(step)
                n = 0
                if P == 1:
                    for t in todo:
                        self.do_step(t, step); n += 1
                        if self.stop_requested: break
                else:
                    with ThreadPoolExecutor(max_workers=P) as ex:
                        for i0 in range(0, len(todo), P):                      # one wave at a time so a stop request is honoured promptly
                            for _ in ex.map(lambda t: self.do_step(t, step), todo[i0:i0 + P]): n += 1
                            if self.stop_requested: break
                rec = {"step": step, "n_traj": n, "step_s": round(time.time() - t_step, 1), "s_per_traj_step": round((time.time() - t_step) / max(n, 1), 1), "ts": now()}
                self.step_times.append(rec); append_jsonl(self.events_path, {"event": "step_done", **rec}); self.progress(step)
                self.log.info("step %3d done: %.0fs, %.1fs per trajectory-step; eta %.2f h", step, rec["step_s"], rec["s_per_traj_step"], read_json(self.progress_path).get("eta_hours", float("nan")))
                if self.stop_requested: break
        finally:
            self.gpu.phase = "exit"
            done = all(s.last_complete_step() >= self.cfg["steps"] - 1 for s in self.stores.values())
            state = "finished" if done else ("stopped" if self.stop_requested else "crashed")
            if self.cfg["model"].get("unload_at_exit"):
                try: self.model.unload()
                except Exception: pass  # noqa: BLE001
            self.progress(-1, state); append_jsonl(self.events_path, {"ts": now(), "event": state, "pid": os.getpid()}); self.gpu.stop()
            self.log.info("exit: %s", state)


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("--run-name"); ap.add_argument("--steps", type=int); ap.add_argument("--count", type=int)
    a = ap.parse_args(argv); cfg = load_text_config(a.config)
    if a.run_name: cfg["run_name"] = a.run_name
    if a.steps: cfg["steps"] = a.steps
    if a.count: cfg["trajectories"]["count"] = a.count
    TextRunner(cfg).run()


if __name__ == "__main__":
    main()
