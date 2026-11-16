"""A0-ESC T1 caption arm: the stratified pool and the 30,000 draws (predictions.md "A0-ESC" T1/P1; 30,000 captions approved 2026-11-16).

    .venv/bin/python analysis/t1_pool.py          -> runs/t1_caption/{pool/*.png, pool.json, draws.json}

Pool: every post-entry image (first cathedral entry to the end of the record) of the 43 distinct SDXL + llava:latest cathedral
entrants (same runs, labels and de-duplication as analysis/esc_c_states.py: A0-core archive centroids, radius 0.20, hysteresis 1.25).
Bins by DINOv2 distance to the A0-core cathedral centroid: [0, 0.2), [0.2, 0.35), [0.35, 0.6), [0.6, inf). Allocation, fixed
before any caption exists: 15,000 / 9,000 / 3,000 / 3,000 draws (outer bins oversampled); within a bin images are drawn uniformly
with replacement (numpy default_rng(20261116)). Weights for the rate = each bin's share of the pool (recorded in pool.json).
Images are copied byte-identical (sha256 checked against their gen records) to pool/<run>__traj_TTT__step_SSS.png.
runs/t1_caption must not exist (runs/ is append-only). DINOv2 only; CLIP is not used.
"""
import hashlib, json, pathlib, shutil, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, ROOT  # noqa: E402
from gravity import label_steps  # noqa: E402
from esc_c_states import RUNS, CAT  # noqa: E402

BINS, ALLOC, RNG, OUT = [0.0, 0.2, 0.35, 0.6, np.inf], [15000, 9000, 3000, 3000], 20261116, ROOT / "runs" / "t1_caption"


def main():
    if OUT.exists(): sys.exit(f"{OUT} exists; runs/ is append-only")
    CA = np.load(ROOT / "archive/a0_core_centroids.npz", allow_pickle=True)["centroid_dinov2"].astype(np.float64)
    CA /= np.linalg.norm(CA, axis=1, keepdims=True); pool = []
    for run in RUNS:
        B = Cache(run).arrays("dinov2"); M = B["mask"]; X = np.nan_to_num(B["X"].astype(np.float64))
        X /= np.where((n := np.linalg.norm(X, axis=-1, keepdims=True)) > 0, n, 1)
        D = 1 - np.einsum("kd,tsd->kts", CA, X); D[:, ~M] = 9; L = label_steps(D, np.full(len(CA), 0.20), 1.25)
        for i, t in enumerate(B["trajs"]):
            t = int(t)
            if (run == "a0_core" and t < 20) or (run == "a0_1000" and t >= 20) or not (L[i] == CAT).any(): continue
            f = int(np.argmax(L[i] == CAT))
            for j in range(f, L.shape[1]):
                if M[i, j]:
                    d = float(D[CAT, i, j]); pool.append({"run": run, "traj": t, "step": int(B["steps"][j]), "dist": round(d, 4),
                                                          "bin": int(np.searchsorted(BINS, d, side="right") - 1)})
    counts = [sum(p["bin"] == b for p in pool) for b in range(4)]; weights = [c / len(pool) for c in counts]
    rng = np.random.default_rng(RNG); draws = []
    for b, k in enumerate(ALLOC):
        members = [i for i, p in enumerate(pool) if p["bin"] == b]
        for i in rng.choice(members, size=k, replace=True): draws.append({"pool": int(i), "bin": b})
    order = rng.permutation(len(draws)); draws = [{"i": n, **draws[o]} for n, o in enumerate(order)]   # interleave bins so a partial run is balanced
    used = sorted({d["pool"] for d in draws}); (OUT / "pool").mkdir(parents=True)
    for i in used:
        p = pool[i]; sd = ROOT / "runs" / p["run"] / f"traj_{p['traj']:03d}"
        gen = json.loads((sd / f"step_{p['step']:03d}.gen.json").read_text()); png = sd / f"step_{p['step']:03d}.png"
        if hashlib.sha256(png.read_bytes()).hexdigest() != gen["image_sha256"]: sys.exit(f"{png}: sha256 mismatch")
        p["file"] = f"pool/{p['run']}__traj_{p['traj']:03d}__step_{p['step']:03d}.png"; p["image_sha256"] = gen["image_sha256"]
        shutil.copy2(png, OUT / p["file"])
    (OUT / "pool.json").write_text(json.dumps({"bins": [0, 0.2, 0.35, 0.6, None], "allocation": ALLOC, "rng": RNG, "counts": counts,
                                               "weights": weights, "n_pool": len(pool), "pool": pool}, indent=0))
    (OUT / "draws.json").write_text(json.dumps(draws))
    print(f"pool {len(pool)} images, bins {counts}, weights {[round(w, 4) for w in weights]}; {len(draws)} draws over {len(used)} distinct images")


if __name__ == "__main__":
    main()
