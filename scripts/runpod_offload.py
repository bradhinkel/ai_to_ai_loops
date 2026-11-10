"""Laptop side: pull one run from the pod, verify the images that arrived, then delete the verified images from the pod so a long
run does not fill the network volume (A0-1000 writes about 40 GB; the volume is 100 GB and holds the models).

    .venv/bin/python scripts/runpod_offload.py a0_1000 [--keep 3] [--no-delete] [--dry-run]

Each call: (1) rsync runs/<run>/ and logs/ from the pod (append-only, never overwrites a newer local file; the pod's deletions never
propagate because there is no --delete); (2) for every step whose record step_NNN.json is complete and that lies more than --keep
steps behind the trajectory's last complete step, check sha256(local png) == gen record's image_sha256; (3) delete those pngs on
the pod, in one ssh call, and remember them in logs/offload_<run>.json so each file is verified once. Records (.json) are never
deleted anywhere, and the newest --keep images of each trajectory stay on the pod (the runner needs step N-1's record, not its
image, to continue, but keeping a few images means a resume after a crash can still regenerate an orphaned step). Needs
RUNPOD_SSH in .env as scripts/runpod_sync.sh does.
"""
import argparse, hashlib, json, os, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
POD_REPO = "/workspace/ai_to_ai_loops"


def env():
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); os.environ.setdefault(k, v.strip().strip('"').strip("'"))
    s = os.environ.get("RUNPOD_SSH") or sys.exit("RUNPOD_SSH missing from .env")
    host, port = s.split()[0], s.split("-p")[-1].strip()
    return host, ["ssh", "-i", str(pathlib.Path.home() / ".ssh" / "claude_runpod"), "-o", "StrictHostKeyChecking=accept-new", "-p", port]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--keep", type=int, default=3); ap.add_argument("--no-delete", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    host, ssh = env(); rd = ROOT / "runs" / a.run; rd.mkdir(parents=True, exist_ok=True); (ROOT / "logs" / "runpod").mkdir(parents=True, exist_ok=True)
    rs = ["rsync", "-az", "--no-o", "--no-g", "--update", "-e", " ".join(ssh)]
    subprocess.run(rs + [f"{host}:{POD_REPO}/runs/{a.run}/", str(rd) + "/"], check=True)
    subprocess.run(rs + [f"{host}:{POD_REPO}/logs/", str(ROOT / "logs" / "runpod") + "/"], check=True)
    state_p = ROOT / "logs" / f"offload_{a.run}.json"
    state = json.loads(state_p.read_text()) if state_p.exists() else {"deleted": [], "verified": []}
    done = set(state["deleted"]); verified = set(state["verified"]); to_delete = []; bad = []
    for td in sorted(rd.glob("traj_???")):
        steps = sorted(int(p.stem.split("_")[1]) for p in td.glob("step_???.json"))
        last = -1
        for s in steps:
            if s != last + 1: break
            last = s
        for s in range(0, last - a.keep + 1):
            rel = f"{td.name}/step_{s:03d}.png"
            if rel in done: continue
            png = td / f"step_{s:03d}.png"; gen = td / f"step_{s:03d}.gen.json"
            if not png.exists() or not gen.exists(): continue
            if rel not in verified:
                if hashlib.sha256(png.read_bytes()).hexdigest() != json.loads(gen.read_text())["image_sha256"]:
                    bad.append(rel); continue
                verified.add(rel)
            to_delete.append(rel)
    n_local = sum(1 for _ in rd.glob("traj_???/step_???.json"))
    print(f"{time.strftime('%FT%T')} {a.run}: {n_local} records local, {len(verified)} images verified, {len(to_delete)} to delete on the pod, {len(bad)} sha mismatches{' (dry run)' if a.dry_run else ''}")
    if bad: print("  sha mismatches (left alone):", bad[:10])
    if to_delete and not a.no_delete and not a.dry_run:
        assert all(re.fullmatch(r"traj_\d{3}/step_\d{3}\.png", r) for r in to_delete)
        lst = "\n".join(f"{POD_REPO}/runs/{a.run}/{r}" for r in to_delete)
        subprocess.run(ssh + [host, "xargs -d '\\n' rm -f"], input=lst, text=True, check=True)
        done.update(to_delete); print(f"  deleted {len(to_delete)} verified images on the pod")
    state = {"deleted": sorted(done), "verified": sorted(verified), "updated": time.strftime("%FT%T")}
    tmp = state_p.with_suffix(".tmp"); tmp.write_text(json.dumps(state)); tmp.replace(state_p)


if __name__ == "__main__":
    main()
