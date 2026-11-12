"""FAST-100 pilot grading (predictions.md "FAST-100", 2026-11-12). DINOv2 only; CLIP is not used.

    .venv/bin/python analysis/fast_report.py [--cross fast_x_llava]

States: (a) A0-core's 8 step-99 centroids (archive/a0_core_centroids.npz), radius 0.20, exit hysteresis 1.25x (gravity.py's
label_steps); (b) each run's own attractors: k-means at the elbow on its steps 50-99, same radius and hysteresis; an attractor is
persistent if it has >= 3 visits of >= 5 steps. F1: overlap / new / A0-share band. F2: total-variation distance of the
occupancy over {8 A0-core attractors, outside} on steps 50-99 against A0-core trajectories 0-19. F3: no persistent own
attractor entered by >= 3 trajectories holds all of them to step 99 (left = visits another own attractor after entry, or ends
>= 10 steps outside), and none holds > 30 % of step-99 endpoints.
Writes reports/fast_100_metrics.json and figures/fast_100_*.jpg.
"""
import argparse, json, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, kmeans, elbow_k, ROOT  # noqa: E402
from gravity import label_steps, visits  # noqa: E402

R0, EXIT, LO, HI = 0.20, 1.25, 50, 100


def load(run, trajs=(0, 20)):
    B = Cache(run).arrays("dinov2"); steps = list(B["steps"]); T = list(B["trajs"])
    ti = [i for i, t in enumerate(T) if trajs[0] <= t < trajs[1]]; sj = [steps.index(s) for s in range(0, HI)]
    X = B["X"][ti][:, sj].astype(np.float64); assert B["mask"][ti][:, sj].all(), f"{run}: missing embeddings"
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def labels(C, X):
    C = C / np.linalg.norm(C, axis=1, keepdims=True); D = 1 - np.einsum("kd,tsd->kts", C, X)
    return label_steps(D, np.full(len(C), R0), EXIT)


def occupancy(L, K):
    w = L[:, LO:HI].ravel(); return np.array([(w == k).mean() for k in range(K)] + [(w == -1).mean()])


def own_attractors(X):
    E = X[:, LO:HI].reshape(-1, X.shape[-1]); k = elbow_k(E)[0]; km = kmeans(E, k)
    C = np.stack([E[km.labels_ == c].mean(0) for c in range(k)]); C /= np.linalg.norm(C, axis=1, keepdims=True)
    L = labels(C, X); rows = []
    for c in range(k):
        v = [n for t in range(len(L)) for n, _ in visits(L[t] == c)]
        entrants = [t for t in range(len(L)) if (L[t] == c).any()]
        held = []
        for t in entrants:
            first = int(np.argmax(L[t] == c)); after = L[t, first:]
            other = bool(((after >= 0) & (after != c)).any()); tail_out = int((after[::-1] != c).argmax()) if after[-1] != c else 0
            held.append(not other and tail_out < 10)
        rows.append(dict(k=c, size=int((km.labels_ == c).sum()), visits_ge5=sum(n >= 5 for n in v), persistent=sum(n >= 5 for n in v) >= 3,
                         entrants=len(entrants), held_all=bool(entrants) and all(held), n_held=int(sum(held)), endpoints=int((L[:, HI - 1] == c).sum()),
                         occupancy_50_99=float((L[:, LO:HI] == c).mean())))
    return k, C, L, rows


def sheet(run, L, rows, path):
    """One row per own attractor: up to 6 member images (steps 50-99) nearest the centroid order is not needed; first visits suffice."""
    rs = [r for r in rows if r["persistent"]]; W = Image.new("RGB", (6 * 160 + 200, max(1, len(rs)) * 160), "white"); d = ImageDraw.Draw(W)
    for i, r in enumerate(rs):
        d.text((4, i * 160 + 60), f"#{r['k']}  occ {r['occupancy_50_99']:.2f}\nentr {r['entrants']} end {r['endpoints']}", fill="black")
        pts = [(t, s) for t in range(L.shape[0]) for s in range(LO, HI) if L[t, s] == r["k"]]
        seen, pick = set(), []
        for t, s in pts:
            if t not in seen: seen.add(t); pick.append((t, s))
        for j, (t, s) in enumerate(pick[:6]):
            W.paste(Image.open(ROOT / "runs" / run / f"traj_{t:03d}" / f"step_{s:03d}.png").resize((160, 160)), (200 + j * 160, i * 160))
    W.save(path, quality=88)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run", default="fast_100"); ap.add_argument("--cross", default=None); a = ap.parse_args()
    z = np.load(ROOT / "archive/a0_core_centroids.npz", allow_pickle=True); CA = z["centroid_dinov2"].astype(np.float64); KA = len(CA)
    names = json.loads((ROOT / "archive/a0_core_names.json").read_text())
    out = {"definitions": {"radius": R0, "exit_factor": EXIT, "window": [LO, HI - 1], "space": "dinov2"}}
    ref = labels(CA, load("a0_core")); out["a0_core_0_19"] = {"occupancy": occupancy(ref, KA).tolist(), "inside_any": float(1 - occupancy(ref, KA)[-1])}
    figs = ROOT / "reports" / "figures"
    for run in [a.run] + ([a.cross] if a.cross else []):
        X = load(run); LA = labels(CA, X); occ = occupancy(LA, KA)
        k, C, L, rows = own_attractors(X); CAn = CA / np.linalg.norm(CA, axis=1, keepdims=True)
        dmin = (1 - C @ CAn.T).min(1); near = (1 - C @ CAn.T).argmin(1)
        for r in rows: r["nearest_a0"] = names[int(near[r["k"]])]; r["dist_nearest_a0"] = float(dmin[r["k"]])
        pers = [r for r in rows if r["persistent"]]
        res = {"elbow_k": k, "a0_occupancy": occ.tolist(), "a0_inside_any": float(1 - occ[-1]),
               "tv_vs_a0_core": float(0.5 * np.abs(occ - np.array(out["a0_core_0_19"]["occupancy"])).sum()),
               "a0_endpoints": {names[c]: int((LA[:, HI - 1] == c).sum()) for c in range(KA)}, "own": rows,
               "F1_overlap": any(r["dist_nearest_a0"] <= R0 for r in pers), "F1_new": any(r["dist_nearest_a0"] > 0.35 for r in pers),
               "F1_share_in_band": 0.05 <= float(1 - occ[-1]) <= 0.60,
               "F3_none_holds_all": not any(r["entrants"] >= 3 and r["held_all"] for r in pers),
               "F3_max_endpoint_share": max([r["endpoints"] for r in pers], default=0) / X.shape[0]}
        res["F3_pass"] = res["F3_none_holds_all"] and res["F3_max_endpoint_share"] <= 0.30
        out[run] = res; sheet(run, L, rows, figs / f"{run}_attractors.jpg")
    if a.cross: out["F2_pass"] = out[a.cross]["tv_vs_a0_core"] < out[a.run]["tv_vs_a0_core"]
    (ROOT / "reports" / f"{a.run}_metrics.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: (v if k != a.run and k != a.cross else {kk: vv for kk, vv in v.items() if kk != "own"}) for k, v in out.items()}, indent=1))
    for run in [a.run] + ([a.cross] if a.cross else []):
        print(f"\n{run} own attractors:")
        for r in out[run]["own"]: print(r)


if __name__ == "__main__":
    main()
