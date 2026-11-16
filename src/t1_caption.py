"""A0-ESC T1 caption arm (predictions.md "A0-ESC" T1/P1): one fresh llava:latest caption per draw of runs/t1_caption/draws.json.

    .venv/bin/python -m src.t1_caption [--config configs/esc_c_runpod.yaml] [--parallel 8]

The captioner is the runner's own OllamaCaptioner with A0's captioner settings and temperature taken from the config (Hintze's
verbatim instruction, options={"temperature": 0.9} only, digest pinned to 8dd30f6b0cb1), so every caption is made exactly as in a
loop step. Output: runs/t1_caption/captions.jsonl, one JSON line per draw, appended and flushed as each caption returns; on restart,
draws already present are skipped (append-only; a torn last line is closed with a newline and that draw is redone). A caption is
`churchless` if it matches none of the A0-ESC church vocabulary. Progress: runs/t1_caption/progress.json; log: logs/t1_caption.log.
"""
import argparse, concurrent.futures as cf, json, logging, os, pathlib, re, threading, time
from .config import load_config
from .captioners.ollama_llava import OllamaCaptioner
from .store import atomic_write_json
from .runner import ROOT, git_commit

CHURCH = re.compile(r"cathedral|church|\bnave\b|stained|chapel|basilica|altar|\bpews?\b|gothic|abbey|cloister|monaster|notre|spire", re.I)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", default="configs/esc_c_runpod.yaml"); ap.add_argument("--parallel", type=int, default=8)
    ap.add_argument("--dir", help="test only: a scratch copy of the pool dir"); ap.add_argument("--limit", type=int, help="test only: first N draws")
    a = ap.parse_args()
    cfg = load_config(a.config); D = pathlib.Path(a.dir) if a.dir else ROOT / "runs" / "t1_caption"; out = D / "captions.jsonl"
    (ROOT / "logs").mkdir(exist_ok=True)
    logging.basicConfig(filename=ROOT / "logs" / "t1_caption.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    log = logging.getLogger("t1"); cap = OllamaCaptioner(cfg["captioner"], cfg["temperature"], log); info = cap.info()
    pool = json.loads((D / "pool.json").read_text())["pool"]; draws = json.loads((D / "draws.json").read_text())[: a.limit]
    done = set()
    if out.exists():
        raw = out.read_bytes()
        if raw and not raw.endswith(b"\n"):
            with open(out, "ab") as f: f.write(b"\n")
        for line in out.read_text().splitlines():
            try: done.add(json.loads(line)["i"])
            except Exception: pass  # noqa: BLE001  (torn line: its draw is redone)
    todo = [d for d in draws if d["i"] not in done]; lock = threading.Lock(); n0 = len(done); t0 = time.time(); git = git_commit()
    log.info("t1_caption: %d of %d draws done, %d to do, parallel %d, captioner %s %s", n0, len(draws), len(todo), a.parallel, info["model"], info["digest"])
    f = open(out, "a", encoding="utf-8"); state = {"n": 0, "churchless": 0}

    def one(d):
        p = pool[d["pool"]]; text, meta = cap.caption(D / p["file"], keep_alive=cfg["captioner"].get("keep_alive_during_pass"))
        rec = {"i": d["i"], "pool": d["pool"], "bin": d["bin"], "run": p["run"], "traj": p["traj"], "step": p["step"], "dist": p["dist"],
               "caption": text, "churchless": not CHURCH.search(text), **meta, "captioner": info, "captioned_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "pipeline_git": git, "config_sha256": cfg["_config_sha256"]}
        with lock:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush(); state["n"] += 1; state["churchless"] += rec["churchless"]
            if state["n"] % 100 == 0:
                os.fsync(f.fileno()); el = time.time() - t0; rate = el / state["n"]
                atomic_write_json(D / "progress.json", {"state": "running", "done": n0 + state["n"], "total": len(draws), "s_per_caption": round(rate, 3),
                                                        "eta_hours": round(rate * (len(todo) - state["n"]) / 3600, 2), "churchless_so_far": state["churchless"],
                                                        "updated": time.strftime("%Y-%m-%dT%H:%M:%S")})
                log.info("%d / %d captions, %.2f s per caption, churchless so far %d", n0 + state["n"], len(draws), rate, state["churchless"])

    with cf.ThreadPoolExecutor(a.parallel) as ex:
        for fut in cf.as_completed([ex.submit(one, d) for d in todo]): fut.result()
    f.close()
    atomic_write_json(D / "progress.json", {"state": "finished", "done": n0 + state["n"], "total": len(draws), "churchless_this_session": state["churchless"],
                                            "updated": time.strftime("%Y-%m-%dT%H:%M:%S")})
    log.info("t1_caption finished: %d captions this session, %d churchless", state["n"], state["churchless"])


if __name__ == "__main__":
    main()
