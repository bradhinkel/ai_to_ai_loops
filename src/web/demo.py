"""Live / replay grid for the fast-pair demo (AI Tinkerers, 2026-11-13). Mounted by src/web/app.py; page at /demo.

Live: scripts/demo_start.sh <side> runs side^2 chains of the fast pair on the laptop (configs/demo_fast.yaml) into a fresh
runs/demo_<side>x<side>_<stamp>; the page shows each chain's latest completed step and paces the reveals. Replay: any run with images
(fast_100, fast_1000 once pulled, earlier demos) stepped through at a chosen speed.

Display-only safety filter: SDXL-Turbo has no safety checker, so every image is scored on the CPU by an NSFW image classifier
(Falconsai/nsfw_image_detection at a pinned revision) before the page shows it; a flagged image is shown blurred. The loop itself is
never touched (the chain continues from the unblurred caption). Scores are cached in logs/demo_nsfw/<run>.json, never under runs/.
"""
import collections, json, os, pathlib, re, subprocess, threading, time
from fastapi import APIRouter, HTTPException

ROOT = pathlib.Path(__file__).resolve().parents[2]
RUNS, LOGS = ROOT / "runs", ROOT / "logs"
NSFW_MODEL, NSFW_REV, NSFW_THRESHOLD = "Falconsai/nsfw_image_detection", "96cb0d0342c7afb80cab76ecc58b265fa44da256", 0.30
REPLAYABLE = re.compile(r"^(fast_100|fast_x_llava|fast_1000|demo_.*)$")
router = APIRouter()


# ---------------------------------------------------------------------------------------------------------------- NSFW scoring
class Scorer:
    """One CPU worker thread; requests jump the queue (newest first), results cached per run on disk."""

    def __init__(self):
        self.lock = threading.Lock(); self.queue = collections.deque(); self.queued = set(); self.cache = {}; self.dirty = set()
        self.pipe = None; self.error = None
        threading.Thread(target=self._work, daemon=True).start()

    def _file(self, run): return LOGS / "demo_nsfw" / f"{run}.json"

    def _run_cache(self, run):
        if run not in self.cache:
            try: self.cache[run] = json.loads(self._file(run).read_text())
            except Exception: self.cache[run] = {}  # noqa: BLE001
        return self.cache[run]

    def get(self, run, t, s):
        with self.lock:
            return self._run_cache(run).get(f"{t}/{s}")

    def want(self, items, front=False):
        """items: iterable of (run, t, s). front=True puts them ahead of everything queued (live frames)."""
        with self.lock:
            new = [k for k in items if k not in self.queued and f"{k[1]}/{k[2]}" not in self._run_cache(k[0])]
            for k in (reversed(new) if front else new):
                (self.queue.appendleft if front else self.queue.append)(k); self.queued.add(k)

    def _load(self):
        import torch
        from transformers import pipeline
        torch.set_num_threads(max(1, (os.cpu_count() or 4) // 2))
        self.pipe = pipeline("image-classification", model=NSFW_MODEL, revision=NSFW_REV, device=-1)

    def _flush(self):
        for run in list(self.dirty):
            p = self._file(run); p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(".tmp")
            with self.lock: data = dict(self.cache.get(run, {}))
            tmp.write_text(json.dumps(data)); os.replace(tmp, p)
        self.dirty.clear()

    def _work(self):
        from PIL import Image
        last_flush = time.time()
        while True:
            with self.lock:
                k = self.queue.popleft() if self.queue else None
            if k is None:
                if self.dirty: self._flush()
                time.sleep(0.2); continue
            run, t, s = k
            p = RUNS / run / f"traj_{t:03d}" / f"step_{s:03d}.png"
            try:
                if self.pipe is None: self._load()
                out = self.pipe(Image.open(p).convert("RGB"))
                score = round(float(next((o["score"] for o in out if o["label"].lower() == "nsfw"), 0.0)), 4)
            except FileNotFoundError:
                with self.lock: self.queued.discard(k)
                continue
            except Exception as e:  # noqa: BLE001  (model failed to load: fail closed, every image blurred)
                self.error = repr(e); score = 1.0
            with self.lock:
                self._run_cache(run)[f"{t}/{s}"] = score; self.queued.discard(k); self.dirty.add(run)
            if time.time() - last_flush > 10: self._flush(); last_flush = time.time()


SCORER = Scorer()


# ---------------------------------------------------------------------------------------------------------------- helpers
def _json(p, default=None):
    try: return json.loads(pathlib.Path(p).read_text())
    except Exception: return default  # noqa: BLE001


def _alive(run):
    try:
        os.kill(int((LOGS / f"{run}.pid").read_text().strip()), 0); return True
    except Exception: return False  # noqa: BLE001


def _latest(run, t):
    d = RUNS / run / f"traj_{t:03d}"
    steps = [int(m.group(1)) for f in d.glob("step_*.json") if (m := re.fullmatch(r"step_(\d+)\.json", f.name))] if d.exists() else []
    return max(steps) if steps else -1


def _cell(run, t, s):
    rec = _json(RUNS / run / f"traj_{t:03d}" / f"step_{s:03d}.json", {}) or {}
    sc = SCORER.get(run, t, s)
    return {"traj": t, "step": s, "caption": rec.get("caption") or "", "nsfw": None if sc is None else sc >= NSFW_THRESHOLD}


def _ntraj(run):
    return len(list((RUNS / run).glob("traj_*")))


# ---------------------------------------------------------------------------------------------------------------- API
@router.get("/api/demo/runs")
def demo_runs():
    out = []
    for d in sorted(RUNS.iterdir()) if RUNS.exists() else []:
        if d.is_dir() and REPLAYABLE.match(d.name) and d.name != "demo_base":
            out.append({"run": d.name, "alive": _alive(d.name), "trajs": _ntraj(d.name), "mtime": d.stat().st_mtime})
    return sorted(out, key=lambda r: -r["mtime"])


@router.get("/api/demo/live")
def demo_live():
    """The live demo run: the newest demo_<side>x<side>_* directory, with whether its runner is alive and whether a start is pending."""
    runs = sorted((d for d in RUNS.glob("demo_*x*_*") if d.is_dir()), key=lambda d: d.stat().st_mtime, reverse=True)
    starting = (LOGS / "demo_starting").exists()
    if not runs: return {"run": None, "alive": False, "starting": starting}
    r = runs[0].name; side = int(re.match(r"demo_(\d+)x", r).group(1))
    pr = _json(runs[0] / "progress.json", {}) or {}
    return {"run": r, "side": side, "alive": _alive(r), "starting": starting, "phase": pr.get("phase"), "s_per_traj_step": pr.get("s_per_traj_step")}


@router.get("/api/demo/state/{run}")
def demo_state(run: str, n: int = 9):
    if not (RUNS / run).exists(): raise HTTPException(404)
    cells = [_cell(run, t, _latest(run, t)) for t in range(n)]
    SCORER.want([(run, c["traj"], c["step"]) for c in cells if c["step"] >= 0 and c["nsfw"] is None], front=True)
    return cells


@router.get("/api/demo/frames/{run}")
def demo_frames(run: str, n: int = 9, start: int = 0, count: int = 10):
    """Replay: steps start .. start+count-1 of trajectories 0..n-1 (missing steps are left out). Queues scoring a little further ahead."""
    if not (RUNS / run).exists(): raise HTTPException(404)
    last = {t: _latest(run, t) for t in range(n)}
    frames = {t: [_cell(run, t, s) for s in range(start, min(start + count, last[t] + 1))] for t in range(n)}
    SCORER.want([(run, t, s) for t in range(n) for s in range(start, min(start + count, last[t] + 1)) if SCORER.get(run, t, s) is None], front=True)
    SCORER.want([(run, t, s) for s in range(start + count, start + 4 * count) for t in range(n) if s <= last[t]])
    return {"last": last, "frames": frames}


@router.post("/api/demo/live/{side}")
def demo_start(side: int):
    if side not in (3, 4, 5): raise HTTPException(400, "side must be 3, 4 or 5")
    flag = LOGS / "demo_starting"
    if flag.exists() and time.time() - flag.stat().st_mtime < 600: raise HTTPException(409, "a demo start is already in progress")
    flag.write_text(str(side))
    out = open(LOGS / "demo_start.out", "a")
    subprocess.Popen(["bash", "-c", f"scripts/demo_start.sh {side}; rm -f {flag}"], cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                     stdin=subprocess.DEVNULL, start_new_session=True)
    return {"ok": True, "side": side}


@router.post("/api/demo/stop")
def demo_stop():
    stopped = []
    for p in LOGS.glob("demo_*.pid"):
        r = p.stem
        if _alive(r) and (RUNS / r).exists():
            tmp = RUNS / r / "control.json.tmp"; tmp.write_text(json.dumps({"state": "stopped", "set_at": time.strftime("%Y-%m-%dT%H:%M:%S")}))
            os.replace(tmp, RUNS / r / "control.json"); stopped.append(r)
    return {"ok": True, "stopped": stopped}


@router.get("/api/demo/scorer")
def scorer_status():
    return {"loaded": SCORER.pipe is not None, "queued": len(SCORER.queue), "error": SCORER.error, "threshold": NSFW_THRESHOLD}
