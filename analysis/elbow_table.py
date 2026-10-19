"""Elbow tracking table (SPEC2 §3, Brad 2026-10-18): one row per endpoint set, rebuilt from the embedding caches after
every run, so variation or patterns in the elbow k can be seen across runs instead of judged one run at a time.

Per set: the knee under the a0_report rule (chord distance on normalised inertia, k = 2..min(25, n-1)), the knee when the
k range is widened (15/20/30/40), the cosine-silhouette maximum, and the sampling spread of the knee: median and 5-95%
range over B random 80% subsamples of the endpoints (without replacement; the same rule each time). Sets: every run's
MiniLM caption endpoints and DINOv2 image endpoints, plus Hintze's own T=0.9 endpoint captions.

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/elbow_table.py a0_pilot a0_core [--boot 200] [--no-hintze]
Writes reports/elbow_table.md and reports/elbow_table.json (overwritten each time; the table is a view of runs/, not data).
"""
import argparse, datetime, json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, cpu_only, final_step_matrix, kmeans, ROOT  # noqa: E402
from elbow_check import knee, curves, hintze_endpoints  # noqa: E402

KMAX_LIST = (15, 20, 25, 30, 40)


def rule_knee(X, kmax=25):
    ks = list(range(2, min(kmax, len(X) - 1) + 1))
    if len(ks) < 4: return None
    return knee(ks, [float(kmeans(X, k).inertia_) for k in ks])


def subsample_spread(X, boot, frac=0.8, seed=0):
    rng = np.random.default_rng(seed); m = max(10, int(round(frac * len(X)))); out = []
    for _ in range(boot):
        idx = rng.choice(len(X), size=m, replace=False)
        k = rule_knee(X[idx])
        if k is not None: out.append(k)
    a = np.array(out)
    return {"B": int(len(a)), "m": m, "median": float(np.median(a)), "p5": float(np.percentile(a, 5)), "p95": float(np.percentile(a, 95)),
            "hist": {int(k): int((a == k).sum()) for k in np.unique(a)}}


def one_set(X, boot):
    n = len(X); kmax_curve = min(40, n - 1)
    ks, inertia, sil = curves(X, kmax_curve)
    by_kmax = {km: knee(ks[:km - 1], inertia[:km - 1]) for km in KMAX_LIST if km <= kmax_curve}
    row = {"n": n, "knee_rule": by_kmax.get(25, by_kmax.get(max(by_kmax))), "knee_by_kmax": by_kmax,
           "silhouette_argmax": int(ks[int(np.argmax(sil))]), "silhouette_top3": [int(ks[i]) for i in np.argsort(sil)[::-1][:3]]}
    if boot: row["subsample"] = subsample_spread(X, boot)
    return row


def main():
    cpu_only()
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--boot", type=int, default=200)
    ap.add_argument("--hintze", default="data/hintze_figshare/temps_0.9/logs"); ap.add_argument("--no-hintze", action="store_true")
    a = ap.parse_args()
    rows = {}
    for run in a.runs:
        cache = Cache(run); run_dir = ROOT / "runs" / run
        for space, label in (("minilm", "captions"), ("dinov2", "images")):
            try:
                _, X, used = final_step_matrix(cache, space, run_dir, step=99)
            except FileNotFoundError:
                print(f"{run}: no {space} cache, skipped"); continue
            name = f"{run} {space} {label}"; print(name, "...", flush=True)
            rows[name] = dict(one_set(X, a.boot), run=run, space=space, step=sorted(set(used.values())))
    if not a.no_hintze:
        from a0_report import embed
        hz = hintze_endpoints(ROOT / a.hintze)
        if hz:
            name = "Hintze T=0.9 minilm captions"; print(name, "...", flush=True)
            rows[name] = dict(one_set(embed(hz).astype(np.float64), a.boot), run="hintze_T0.9", space="minilm", step=[99])
    out = {"built": datetime.date.today().isoformat(), "rule": "knee of normalised inertia (max chord distance), KMeans n_init=10 random_state=0, k=2..min(25,n-1)",
           "subsample": f"{a.boot} random 80% subsamples without replacement, same rule", "rows": rows}
    rep = ROOT / "reports"; rep.mkdir(exist_ok=True)
    (rep / "elbow_table.json").write_text(json.dumps(out, indent=1))
    lines = [f"# Elbow tracking table (built {out['built']})", "",
             "Rule: " + out["rule"] + ". Spread: " + out["subsample"] + ". Rebuilt by `analysis/elbow_table.py` after every run; the SPEC §4.3 reading since 2026-10-18 is 'matches Hintze's T=0.9 data under this rule', and this table is where variation between runs is tracked.", "",
             "| Set | n | knee k (rule) | knee by kmax 15 / 20 / 30 / 40 | silhouette max (top 3) | subsample knee median [5%, 95%] |", "|---|---|---|---|---|---|"]
    for name, r in rows.items():
        bk = r["knee_by_kmax"]; wide = " / ".join(str(bk.get(k, "–")) for k in (15, 20, 30, 40))
        sub = r.get("subsample"); subs = f"{sub['median']:.0f} [{sub['p5']:.0f}, {sub['p95']:.0f}]" if sub else "–"
        lines.append(f"| {name} | {r['n']} | **{r['knee_rule']}** | {wide} | {r['silhouette_argmax']} ({', '.join(map(str, r['silhouette_top3']))}) | {subs} |")
    (rep / "elbow_table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
