"""E3-S2 post-hoc measurement check for R2 (predictions.md decision rule: "R2 failing sends the thread back to the measurement").
The pre-registered R2 count refits a joint 200-trajectory atlas (k 396) and asks whether the joint cluster nearest each first-sample well
receives a persistent visit from a second-sample trajectory; the refit can split a family of plots across clusters. This check keeps the
first sample's own k-198 anonymised atlas fixed and labels the second sample's steps against it with no refit (the E3-P method), then counts
first-sample shared wells with a persistent (dwell >= 5) second-sample visit; and the reverse. Written 2026-11-03 after the joint-refit count
(6 of 13) was seen, so it is post hoc and is reported as such.
    .venv/bin/python analysis/e3s2_projection_check.py  -> reports/e3/s2_projection_check.json
"""
import sys, pathlib, json
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, Cache, cpu_only  # noqa: E402
from e3_report import unit  # noqa: E402
from e3s_report import k_for, ATLAS  # noqa: E402
from e3_projection import fit_reference, label  # noqa: E402
from gravity import visits  # noqa: E402


def main(a="e3_1_haiku_100", b="e3_1_haiku_100b"):
    cpu_only()
    A = unit(Cache(a).load("minilm_anon")["X"].astype(np.float64)[:, 1:]); B = unit(Cache(b).load("minilm_anon")["X"].astype(np.float64)[:, 1:])
    k = k_for(A.shape[0] * A.shape[1]); C, LA, pers, shared = fit_reference(A, k); LB = label(C, B); wells = {}
    for c, ts, nv in shared:
        bt = [ti for ti in range(B.shape[0]) if any(l >= ATLAS["min_dwell"] for l, _ in visits(LB[ti] == c))]
        wells[int(c)] = dict(a_trajs=ts, b_persistent=bt, b_touching=int(sum((LB[ti] == c).any() for ti in range(B.shape[0]))))
    Cb, LBb, persb, sharedb = fit_reference(B, k); LAb = label(Cb, A)
    rev = {int(c): [ti for ti in range(A.shape[0]) if any(l >= ATLAS["min_dwell"] for l, _ in visits(LAb[ti] == c))] for c, ts, nv in sharedb}
    res = dict(method="label the other sample's anonymised steps against one sample's own k-198 atlas, no refit (E3-P method)", k=k,
               a_shared=len(shared), a_wells_visited_persistently_by_b=sum(bool(v["b_persistent"]) for v in wells.values()), wells=wells,
               reverse=dict(b_shared=len(sharedb), b_wells_visited_persistently_by_a=sum(bool(v) for v in rev.values()), wells=rev))
    (ROOT / "reports" / "e3" / "s2_projection_check.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "wells"}, default=str)[:600])


if __name__ == "__main__":
    main()
