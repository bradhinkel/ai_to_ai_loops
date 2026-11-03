"""E3-P: project the 20-seed text cells into the first 100-seed Haiku sample's atlas (predictions.md "E3 second sample and projections",
2026-11-03, P1-P3 and P4b). The reference atlas is the anonymised (names -> X) MiniLM atlas of e3_1_haiku_100 at k 198 (40 per 2,000
trajectory-steps), radius 0.15, hysteresis 1.25, persistent visit = dwell >= 5, persistent cluster = >= 3 persistent visits, shared well =
persistent cluster visited by >= 2 trajectories. Each projected cell is anonymised the same way and its steps are labelled against the
reference centroids with the same rule; nothing is refit.

Usage: .venv/bin/python analysis/e3_projection.py [--ref e3_1_haiku_100] [--cells e3_1_haiku e3_1_sonnet ...] [--no-embed]
Writes reports/e3/projection.md and projection.json.
"""
import argparse, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, MODELS, Cache, cpu_only, package_versions  # noqa: E402
from gravity import label_steps, visits  # noqa: E402
from e3_report import load_records, embed_all, unit  # noqa: E402
from e3s_report import ATLAS, k_for, anon_embed  # noqa: E402

OUT = ROOT / "reports" / "e3"
CELLS = ["e3_1_haiku", "e3_1_sonnet", "e3_1_mistral", "e3_1_qwen", "e3_1_llava", "e3_d_haiku", "e3_d_mistral"]
LATE = 25  # steps >= 25 count as late for the inside share (prediction text)


def fit_reference(X, k, seed=0):
    from sklearn.cluster import KMeans
    T, S, d = X.shape
    C = unit(KMeans(n_clusters=k, n_init=3, random_state=seed).fit(X.reshape(-1, d)).cluster_centers_.astype(np.float32))
    L = label(C, X); pers, shared = [], []
    for c in range(k):
        nv, ts = 0, set()
        for ti in range(T):
            for length, _ in visits(L[ti] == c):
                if length >= ATLAS["min_dwell"]: nv += 1; ts.add(ti)
        if nv >= ATLAS["min_visits"]:
            pers.append(c)
            if len(ts) >= 2: shared.append((c, sorted(ts), nv))
    return C, L, pers, shared


def label(C, X):
    D = 1.0 - np.einsum("kd,tsd->kts", C, X)
    return label_steps(D, np.full(len(C), ATLAS["radius"]), ATLAS["exit_factor"])


def project(C, pers, shared_ids, X, steps):
    """X unit [T,S,d] for steps[0] >= 1. Per-cell summary of where the cell's steps land in the reference atlas."""
    L = label(C, X); T = X.shape[0]; late = np.array([s >= LATE for s in steps])
    Dsh = 1.0 - np.einsum("kd,tsd->kts", C[shared_ids], X) if shared_ids else None
    in_pers = np.isin(L, pers); inside_late = float(in_pers[:, late].mean())
    per_traj = []
    for ti in range(T):
        pv = {}  # shared well id -> number of persistent visits
        for c in shared_ids:
            n = sum(1 for length, _ in visits(L[ti] == c) if length >= ATLAS["min_dwell"])
            if n: pv[int(c)] = n
        touch = sorted({int(shared_ids[j]) for j in np.where((Dsh[:, ti, :] <= ATLAS["radius"]).any(axis=1))[0]}) if Dsh is not None else []
        per_traj.append(dict(traj=ti, persistent_wells=pv, touched_wells=touch, inside_late=float(in_pers[ti, late].mean())))
    n_pers = sum(1 for p in per_traj if p["persistent_wells"]); n_touch = sum(1 for p in per_traj if p["touched_wells"])
    wells = sorted({w for p in per_traj for w in p["persistent_wells"]})
    nn_late = float(np.median(Dsh[:, :, late].min(axis=0))) if Dsh is not None else None
    return dict(n_traj=T, inside_late=inside_late, traj_with_persistent_shared=n_pers, traj_touching_shared=n_touch, distinct_shared_wells=wells,
                nn_shared_late_median=nn_late, per_traj=per_traj)


def main():
    cpu_only(); ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="e3_1_haiku_100"); ap.add_argument("--cells", nargs="*", default=CELLS); ap.add_argument("--no-embed", action="store_true")
    a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    runs = [a.ref] + [c for c in a.cells if (ROOT / "runs" / c).exists()]
    model = None
    if not a.no_embed:
        need = [r for r in runs if Cache(r).load("minilm") is None]
        if need: embed_all(need, dev)
        from sentence_transformers import SentenceTransformer
        m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    data = {}
    for run in runs:
        recs, T, S = load_records(run); cache = Cache(run); X = cache.load("minilm")["X"].astype(np.float64)
        Xa, _ = anon_embed(run, recs, T, S, model, cache); data[run] = (recs, T, S, unit(X[:, 1:]), unit(Xa[:, 1:]), S[1:])
    R = dict(params=dict(atlas=ATLAS, late_from=LATE, ref=a.ref, versions=package_versions()), reference={}, cells={})
    refs = {}
    for tag, idx in (("anon", 4), ("raw", 3)):
        recs, T, S, _, _, steps = data[a.ref]; X = data[a.ref][idx]; k = k_for(X.shape[0] * X.shape[1])
        C, L, pers, shared = fit_reference(X, k); sh_ids = [c for c, _, _ in shared]
        own = project(C, pers, sh_ids, X, steps)
        R["reference"][tag] = dict(k=k, persistent=len(pers), shared=len(shared), shared_wells={int(c): dict(trajs=ts, visits=nv) for c, ts, nv in shared},
                                   inside_late=own["inside_late"], traj_with_persistent_shared=own["traj_with_persistent_shared"], traj_touching_shared=own["traj_touching_shared"])
        refs[tag] = (C, pers, sh_ids)
        print(f"[{a.ref}] {tag}: k {k}, persistent {len(pers)}, shared {len(shared)}, own inside-late {own['inside_late']:.3f}", flush=True)
    for run in runs[1:]:
        recs, T, S, Xr, Xa, steps = data[run]; R["cells"][run] = {}
        for tag, X in (("anon", Xa), ("raw", Xr)):
            C, pers, sh_ids = refs[tag]; R["cells"][run][tag] = project(C, pers, sh_ids, X, steps)
        p = R["cells"][run]["anon"]
        print(f"[{run}] anon: inside-late {p['inside_late']:.3f}, traj with persistent shared-well visit {p['traj_with_persistent_shared']}, touching {p['traj_touching_shared']}, wells {p['distinct_shared_wells']}, nn-shared late {p['nn_shared_late_median']:.3f}", flush=True)
    # verdicts
    base = R["cells"].get("e3_1_haiku", {}).get("anon", {}); ref_inside = R["reference"]["anon"]["inside_late"]; V = {}
    if base:
        V["P1_same_model"] = dict(traj_persistent=base["traj_with_persistent_shared"], inside=base["inside_late"], ref_inside=ref_inside,
                                  holds=base["traj_with_persistent_shared"] >= 3 and base["inside_late"] >= 0.5 * ref_inside)
        s = R["cells"].get("e3_1_sonnet", {}).get("anon")
        if s:
            ratio = s["inside_late"] / base["inside_late"] if base["inside_late"] else None
            V["P2_sonnet_overlaps"] = dict(traj_persistent=s["traj_with_persistent_shared"], inside_ratio=ratio, wells=s["distinct_shared_wells"],
                                           holds=s["traj_with_persistent_shared"] >= 2 and ratio is not None and 0.2 <= ratio <= 0.8)
        for m in ("e3_1_mistral", "e3_1_qwen", "e3_1_llava"):
            c = R["cells"].get(m, {}).get("anon")
            if c:
                ratio = c["inside_late"] / base["inside_late"] if base["inside_late"] else None
                V[f"P3_{m}"] = dict(traj_persistent=c["traj_with_persistent_shared"], inside_ratio=ratio, holds=c["traj_with_persistent_shared"] <= 1 and (ratio is None or ratio < 0.2))
    dh, dm = R["cells"].get("e3_d_haiku", {}).get("anon"), R["cells"].get("e3_d_mistral", {}).get("anon")
    if dh and dm:
        V["P4b_embedding"] = dict(nn_haiku_d=dh["nn_shared_late_median"], nn_mistral_d=dm["nn_shared_late_median"], haiku_d_touching=dh["traj_touching_shared"],
                                  holds=(dm["nn_shared_late_median"] - dh["nn_shared_late_median"]) >= 0.05 and dh["traj_touching_shared"] >= 5)
    R["verdicts"] = V
    # markdown
    L = ["# E3-P: 20-seed cells projected into the e3_1_haiku_100 atlas", "",
         f"Reference: anonymised MiniLM atlas of {a.ref}, k {R['reference']['anon']['k']}, {R['reference']['anon']['persistent']} persistent clusters, {R['reference']['anon']['shared']} shared wells; "
         f"the reference cell's own late-step inside share is {ref_inside:.3f} and {R['reference']['anon']['traj_with_persistent_shared']} of 100 trajectories make a persistent visit to a shared well "
         f"(raw atlas: k {R['reference']['raw']['k']}, {R['reference']['raw']['shared']} shared wells). Late = steps >= {LATE}. Projected cells are anonymised with their own name filter and labelled against the reference centroids (radius 0.15, hysteresis 1.25); nothing is refit.", "",
         "| cell | inside share, late (anon / raw) | trajectories with a persistent visit to a shared Haiku well (anon / raw) | trajectories touching a shared well at any step | distinct shared wells visited (anon) | median late distance to nearest shared well (anon) |", "|---|---|---|---|---|---|"]
    for run, c in R["cells"].items():
        an, rw = c["anon"], c["raw"]
        L.append(f"| {run} | {an['inside_late']:.3f} / {rw['inside_late']:.3f} | {an['traj_with_persistent_shared']} / {rw['traj_with_persistent_shared']} of {an['n_traj']} | {an['traj_touching_shared']} | {an['distinct_shared_wells']} | {an['nn_shared_late_median']:.3f} |")
    L += ["", "## Verdicts", ""] + [f"- **{k}**: {json.dumps(v)}" for k, v in V.items()]
    L += ["", "## Which wells (anon reference cluster ids, as in `sw_cluster_e3_1_haiku_100_anon.md`)", ""]
    for run, c in R["cells"].items():
        hits = [(p["traj"], p["persistent_wells"]) for p in c["anon"]["per_traj"] if p["persistent_wells"]]
        if hits: L.append(f"- {run}: " + "; ".join(f"traj {t} -> wells {w}" for t, w in hits))
    (OUT / "projection.md").write_text("\n".join(L) + "\n", encoding="utf-8"); (OUT / "projection.json").write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
