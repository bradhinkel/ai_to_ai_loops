"""Seed a run whose step 0 of each chain is a chosen state (trajectory, step) of a finished run (predictions.md "ESC").

    .venv/bin/python scripts/seed_states.py --source fast_1000 --target esc_e --labels reports/fast_1000_labels.npz --attractor 1 \
        --chains 100 --rng 20261115

Picks the start states: every trajectory that enters the attractor (label == attractor in the labels file) gets an equal share of
the chains (the first `chains mod entrants` entrants in trajectory order get one more); each entrant's inside steps are cut into
that many equal consecutive blocks and one step is drawn at random from each block (numpy default_rng(rng)). Each chosen state is
copied byte-identical (step_NNN.png, .gen.json, .json; sha256 checked against the gen record) to runs/<target>/traj_JJJ/step_000.*,
so the runner starts every chain at step 1 with the state's caption as its prompt. The mapping is written to
runs/<target>/seed_states.json. Nothing in the source is touched; the target must not exist yet (runs/ is append-only).
"""
import argparse, datetime, hashlib, json, pathlib, shutil, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]


def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source"); ap.add_argument("--target", required=True)
    ap.add_argument("--labels"); ap.add_argument("--attractor", type=int)
    ap.add_argument("--states-file", help="JSON list of {run, traj, step}: copy exactly these states (several source runs allowed)")
    ap.add_argument("--chains", type=int, default=100); ap.add_argument("--rng", type=int, default=20261115)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    dst = ROOT / "runs" / a.target
    if dst.exists(): sys.exit(f"{dst} exists; runs/ is append-only, choose a new target")
    if a.states_file:
        states = [(d["run"], d["traj"], d["step"]) for d in json.loads((ROOT / a.states_file).read_text())]; entrants = None
    else:
        L = np.load(ROOT / a.labels)["L"]; rng = np.random.default_rng(a.rng)
        entrants = [t for t in range(L.shape[0]) if (L[t] == a.attractor).any()]
        n = [a.chains // len(entrants) + (i < a.chains % len(entrants)) for i in range(len(entrants))]
        states = []
        for t, k in zip(entrants, n):
            inside = np.where(L[t] == a.attractor)[0]
            for block in np.array_split(inside, k): states.append((a.source, t, int(rng.choice(block))))
        print(f"{len(entrants)} entrants, {len(states)} start states; per entrant {dict(zip(entrants, n))}")
    if a.dry_run:
        print(states); return
    out = []
    for j, (run, t, s) in enumerate(states):
        sd, td = ROOT / "runs" / run / f"traj_{t:03d}", dst / f"traj_{j:03d}"
        gen = json.loads((sd / f"step_{s:03d}.gen.json").read_text()); png = sd / f"step_{s:03d}.png"
        if sha256(png) != gen["image_sha256"]: sys.exit(f"{png}: sha256 does not match its gen record")
        td.mkdir(parents=True, exist_ok=False)
        for suf in (".png", ".gen.json", ".json"):
            tmp = td / f"step_000{suf}.tmp"; shutil.copy2(sd / f"step_{s:03d}{suf}", tmp); tmp.replace(td / f"step_000{suf}")
        out.append({"chain": j, "source_run": run, "source_traj": t, "source_step": s, "image_sha256": gen["image_sha256"],
                    "caption": json.loads((sd / f"step_{s:03d}.json").read_text())["caption"]})
    rec = {"created": datetime.datetime.now().isoformat(timespec="seconds"), "source_run": a.source, "labels": a.labels,
           "labels_sha256": sha256(ROOT / a.labels) if a.labels else None, "states_file": a.states_file,
           "states_file_sha256": sha256(ROOT / a.states_file) if a.states_file else None,
           "attractor": a.attractor, "rng": a.rng, "entrants": entrants, "states": out}
    (dst / "seed_states.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(f"{a.target}: {len(out)} chains seeded at step 0 from {sorted({o['source_run'] for o in out})}")


if __name__ == "__main__":
    main()
