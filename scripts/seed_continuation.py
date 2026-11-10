"""Seed a continuation run from a finished run's records (DEVIATIONS D20; predictions.md A0-1000).

    .venv/bin/python scripts/seed_continuation.py [--source a0_core] [--target a0_1000] [--through 99] [--first 0] [--count 100] [--png-from 0]

Copies step_000..step_<through> of each chosen trajectory (step_NNN.json, step_NNN.gen.json and, from --png-from on, step_NNN.png)
from runs/<source>/traj_TTT into runs/<target>/traj_TTT, verifying every image against the sha256 in its gen record. The runner
then resumes the target at step <through>+1 (prompt = caption of step <through>). Nothing in the source is touched and nothing in
the target is ever overwritten: a target file that already exists must be byte-identical or the script stops. Provenance is appended
to runs/<target>/continuation.jsonl (one line per invocation). --png-from 99 makes a pod copy that carries only the image the
runner needs; the laptop copy (--png-from 0) is the complete record.
"""
import argparse, datetime, hashlib, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="a0_core"); ap.add_argument("--target", default="a0_1000")
    ap.add_argument("--through", type=int, default=99, help="last step copied; the runner resumes at through+1")
    ap.add_argument("--first", type=int, default=0); ap.add_argument("--count", type=int, default=100)
    ap.add_argument("--png-from", type=int, default=0, help="copy images only from this step on (records are always copied)")
    a = ap.parse_args()
    src = ROOT / "runs" / a.source; dst = ROOT / "runs" / a.target
    if not src.exists(): sys.exit(f"source run {src} not found")
    if a.source == a.target: sys.exit("source and target must differ (runs/ is append-only)")
    sm = json.loads((src / "manifest.json").read_text())
    copied = 0; identical = 0; endpoints = {}
    for t in range(a.first, a.first + a.count):
        sd = src / f"traj_{t:03d}"; td = dst / f"traj_{t:03d}"
        for s in range(a.through + 1):
            if not (sd / f"step_{s:03d}.json").exists(): sys.exit(f"{sd} is not complete through step {a.through} (step {s} missing)")
        gen = json.loads((sd / f"step_{a.through:03d}.gen.json").read_text())
        png = sd / f"step_{a.through:03d}.png"
        if sha256(png) != gen["image_sha256"]: sys.exit(f"{png}: sha256 does not match its gen record")
        endpoints[t] = gen["image_sha256"]
        td.mkdir(parents=True, exist_ok=True)
        for s in range(a.through + 1):
            names = [f"step_{s:03d}.json", f"step_{s:03d}.gen.json"] + ([f"step_{s:03d}.png"] if s >= a.png_from else [])
            for n in names:
                sp, tp = sd / n, td / n
                if tp.exists():
                    if sha256(sp) != sha256(tp): sys.exit(f"{tp} exists and differs from {sp}; runs/ is append-only, stopping")
                    identical += 1; continue
                shutil.copy2(sp, td / (n + ".tmp")); (td / (n + ".tmp")).replace(tp); copied += 1
    dst.mkdir(parents=True, exist_ok=True)
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "source_run": a.source, "source_manifest": {k: sm.get(k) for k in ("created", "host", "git_commit", "config_sha256", "seeds_file_sha256")},
           "through_step": a.through, "trajectories": list(range(a.first, a.first + a.count)), "png_from": a.png_from,
           "files_copied": copied, "files_already_present": identical, "endpoint_image_sha256": endpoints}
    with open(dst / "continuation.jsonl", "a", encoding="utf-8") as f: f.write(json.dumps(rec) + "\n")
    print(f"{a.target}: trajectories {a.first}-{a.first + a.count - 1} seeded from {a.source} through step {a.through}; {copied} files copied, {identical} already present")


if __name__ == "__main__":
    main()
