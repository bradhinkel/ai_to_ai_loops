"""A0-ESC T1 continuation stage: seed one chain per churchless T1 caption (predictions.md "A0-ESC" T1/P1).

    .venv/bin/python scripts/t1_seed.py [--target t1_cont] [--dry-run]

Every caption in runs/t1_caption/captions.jsonl with churchless = true is a *candidate*. Candidate n (in draw order i) becomes chain n
of runs/<target>, step 0:
  step_000.png       the pool image, byte-identical (sha256 checked against the pool record and the source gen record)
  step_000.gen.json  the source step's gen record, byte-identical
  step_000.json      the source step's caption record with `caption` replaced by the candidate's fresh T1 caption; the source caption is
                     kept as `source_caption` and the T1 caption line (draw i, captioner, digest, time) as `t1_caption`
so the runner makes step 1 from the churchless caption and continues 30 steps (config steps 31) with sdxl_seed = base + chain*10000 + step.
Also writes runs/<target>/seed_table.json (the runner's JSON seed table: one entry per chain, prompt = the T1 caption, attrs = the
draw) and runs/<target>/seed_states.json (chain -> draw, pool image, source run/traj/step, bin, distance). Nothing in the source runs
is touched; the target must not exist (runs/ is append-only).
"""
import argparse, datetime, hashlib, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
T1 = ROOT / "runs" / "t1_caption"


def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--target", default="t1_cont"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(); dst = ROOT / "runs" / a.target
    if dst.exists(): sys.exit(f"{dst} exists; runs/ is append-only, choose a new target")
    pool = json.loads((T1 / "pool.json").read_text())["pool"]
    lines = [json.loads(l) for l in (T1 / "captions.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len({x["i"] for x in lines}) == len(lines), "duplicate draws in captions.jsonl"
    cands = sorted((x for x in lines if x["churchless"]), key=lambda x: x["i"])
    print(f"{len(lines)} captions, {len(cands)} candidates, {len({c['pool'] for c in cands})} distinct pool images; "
          f"by bin {[sum(c['bin'] == b for c in cands) for b in range(4)]}")
    if a.dry_run: return
    table, states = [], []
    for n, c in enumerate(cands):
        p = pool[c["pool"]]; sd = ROOT / "runs" / p["run"] / f"traj_{p['traj']:03d}"; td = dst / f"traj_{n:03d}"
        png, gen = T1 / p["file"], sd / f"step_{p['step']:03d}.gen.json"
        g = json.loads(gen.read_text())
        if not (sha256(png) == p["image_sha256"] == g["image_sha256"]): sys.exit(f"{png}: sha256 mismatch")
        rec = json.loads((sd / f"step_{p['step']:03d}.json").read_text(encoding="utf-8"))
        rec["source_caption"] = rec["caption"]; rec["caption"] = c["caption"]
        rec["t1_caption"] = {k: c[k] for k in ("i", "pool", "bin", "dist", "captioned_at", "captioner", "eval_count", "done_reason") if k in c}
        rec["seeded_into"] = {"run": a.target, "chain": n}
        td.mkdir(parents=True, exist_ok=False)
        for src, name in ((png, "step_000.png"), (gen, "step_000.gen.json")):
            shutil.copy2(src, td / (name + ".tmp")); (td / (name + ".tmp")).replace(td / name)
        (td / "step_000.json.tmp").write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding="utf-8"); (td / "step_000.json.tmp").replace(td / "step_000.json")
        attrs = {"draw": c["i"], "pool": c["pool"], "bin": c["bin"], "dist": c["dist"], "source_run": p["run"], "source_traj": p["traj"], "source_step": p["step"]}
        table.append({"id": f"t1_draw_{c['i']:05d}", "prompt": c["caption"], "reps": 1, "set": "t1_cont", "attrs": attrs})
        states.append({"chain": n, **attrs, "image_sha256": p["image_sha256"], "caption": c["caption"]})
    (dst / "seed_table.json").write_text(json.dumps({"seeds": table}, indent=1, ensure_ascii=False), encoding="utf-8")
    (dst / "seed_states.json").write_text(json.dumps({"created": datetime.datetime.now().isoformat(timespec="seconds"),
        "captions_sha256": sha256(T1 / "captions.jsonl"), "pool_sha256": sha256(T1 / "pool.json"), "n_captions": len(lines),
        "states": states}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{a.target}: {len(states)} chains seeded at step 0")


if __name__ == "__main__":
    main()
