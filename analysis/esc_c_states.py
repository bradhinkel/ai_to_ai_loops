"""ESC-C start states (predictions.md "ESC", approved 2026-11-15): 100 cathedral states from the distinct SDXL + llava:latest entrants.

    .venv/bin/python analysis/esc_c_states.py        -> data/esc_c_states.json (then scripts/seed_states.py --states-file ...)

Labels: A0-core's 8 archive centroids (archive/a0_core_centroids.npz), radius 0.20 DINOv2, exit hysteresis 1.25 (gravity.label_steps);
cathedral = archive index 0. Runs: a0_pilot, a0_core, a0_core2, a0_photo, a0_1000. A0-1000 trajectories 0-19 are a0_core's 0-19
continued (steps 0-99 are byte copies), so an a0_core entrant among 0-19 is taken from a0_1000 (its longer record) and counted once;
a0_1000 trajectories 20-99 are only a0_core's copies and are skipped. Each entrant gets 100 // n chains, the first 100 mod n entrants
(in run, trajectory order) one more; its inside steps are cut into that many equal blocks and one step is drawn from each block
(numpy default_rng(20261115)). DINOv2 only; CLIP is not used.
"""
import json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, ROOT  # noqa: E402
from gravity import label_steps  # noqa: E402

RUNS, CAT, CHAINS, RNG = ["a0_pilot", "a0_core", "a0_core2", "a0_photo", "a0_1000"], 0, 100, 20261115


def main():
    CA = np.load(ROOT / "archive/a0_core_centroids.npz", allow_pickle=True)["centroid_dinov2"].astype(np.float64)
    CA /= np.linalg.norm(CA, axis=1, keepdims=True); entrants = []
    for run in RUNS:
        B = Cache(run).arrays("dinov2"); M = B["mask"]; X = np.nan_to_num(B["X"].astype(np.float64))
        X /= np.where((n := np.linalg.norm(X, axis=-1, keepdims=True)) > 0, n, 1)
        D = 1 - np.einsum("kd,tsd->kts", CA, X); D[:, ~M] = 9; L = label_steps(D, np.full(len(CA), 0.20), 1.25)
        for i, t in enumerate(B["trajs"]):
            t = int(t)
            if run == "a0_core" and t < 20: continue            # taken from a0_1000
            if run == "a0_1000" and t >= 20: continue           # copies of a0_core only
            inside = [int(B["steps"][j]) for j in np.where(L[i] == CAT)[0]]
            if inside: entrants.append((run, t, inside))
    rng = np.random.default_rng(RNG); n = len(entrants); states = []
    for e, (run, t, inside) in enumerate(entrants):
        for block in np.array_split(np.array(inside), CHAINS // n + (e < CHAINS % n)): states.append({"run": run, "traj": t, "step": int(rng.choice(block))})
    (ROOT / "data" / "esc_c_states.json").write_text(json.dumps(states, indent=0))
    print(f"{n} entrants ({', '.join(f'{r}: {sum(e[0] == r for e in entrants)}' for r in RUNS)}), {len(states)} states, "
          f"{sum(len(e[2]) for e in entrants)} inside steps -> data/esc_c_states.json")


if __name__ == "__main__":
    main()
