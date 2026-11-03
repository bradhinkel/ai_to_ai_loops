"""E3-S2: second 100-seed Haiku sample against predictions.md "E3 second sample and projections" (2026-11-03), R1-R4.
A = first sample (e3_1_haiku_100), B = second (e3_1_haiku_100b). Atlas rules as e3s_report.py (radius 0.15, hysteresis 1.25, dwell >= 5,
>= 3 persistent visits, k = 40 per 2,000 trajectory-steps; anonymised = names -> X). R2/R4 use the joint 200-trajectory atlas (k 396).

Usage: .venv/bin/python analysis/e3s2_report.py [--a e3_1_haiku_100] [--b e3_1_haiku_100b] [--no-embed]
Writes reports/e3/s2.md, s2.json and the second sample's own sheets sw_cluster_<b>_{raw,anon}.md.
"""
import argparse, itertools, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, MODELS, Cache, cpu_only, package_versions  # noqa: E402
from gravity import visits  # noqa: E402
from e3_report import load_records, embed_all, unit  # noqa: E402
from e3s_report import ATLAS, k_for, atlas_pairs, anon_embed, cell_stats, cluster_sheet  # noqa: E402
from e3_projection import fit_reference, label  # noqa: E402

OUT = ROOT / "reports" / "e3"


def persistent_sets(L, cluster_ids, offset=0):
    """cluster id -> set of trajectory indices (plus offset) with a dwell >= 5 visit."""
    out = {}
    for c in cluster_ids:
        ts = set()
        for ti in range(L.shape[0]):
            if any(length >= ATLAS["min_dwell"] for length, _ in visits(L[ti] == c)): ts.add(ti + offset)
        out[int(c)] = ts
    return out


def main():
    cpu_only(); ap = argparse.ArgumentParser(); ap.add_argument("--a", default="e3_1_haiku_100"); ap.add_argument("--b", default="e3_1_haiku_100b"); ap.add_argument("--no-embed", action="store_true")
    a = ap.parse_args(); import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    model = None
    if not a.no_embed:
        need = [r for r in (a.a, a.b) if Cache(r).load("minilm") is None]
        if need: embed_all(need, dev)
        from sentence_transformers import SentenceTransformer
        m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    D = {}
    for run in (a.a, a.b):
        recs, T, S = load_records(run); cache = Cache(run); X = cache.load("minilm")["X"].astype(np.float64); Xa, _ = anon_embed(run, recs, T, S, model, cache)
        D[run] = dict(recs=recs, T=T, S=S, raw=unit(X[:, 1:]), anon=unit(Xa[:, 1:]), stats=cell_stats(run, X, Xa, recs, T, S)); print(f"[{run}] loaded", flush=True)
    A, B = D[a.a], D[a.b]; n = len(B["T"]); steps = B["S"][1:]; k1 = k_for(n * len(steps)); R = dict(params=dict(atlas=ATLAS, versions=package_versions()), cells={a.a: A["stats"], a.b: B["stats"]}, verdicts={})
    # R1: B alone
    own = {tag: atlas_pairs(B[tag], k1) for tag in ("raw", "anon")}
    sheets = [(f"sw_cluster_{a.b}_{tag}.md", cluster_sheet(a.b, B["recs"], B["T"], B["S"], own[tag], tag)) for tag in own]
    first = {tag: atlas_pairs(A[tag], k1) for tag in ("raw", "anon")}
    R["R1"] = {tag: dict(shared=own[tag]["shared"], pairs=own[tag]["n_sharing_pairs"], rate=own[tag]["rate"], max_mult=own[tag]["max_mult"], W_hat=own[tag]["W_hat"], persistent=own[tag]["persistent"],
                        first_sample=dict(shared=first[tag]["shared"], pairs=first[tag]["n_sharing_pairs"], rate=first[tag]["rate"], max_mult=first[tag]["max_mult"], W_hat=first[tag]["W_hat"])) for tag in own}
    r1 = R["R1"]["anon"]; R["verdicts"]["R1_law_replicates"] = dict(rate=r1["rate"], rate_in_band=0.003 <= r1["rate"] <= 0.012, shared_ge_8=r1["shared"] >= 8, mult_ge_3=r1["max_mult"] >= 3, raw_shared_ge_3=R["R1"]["raw"]["shared"] >= 3,
                                                               W_in_band=(r1["W_hat"] is not None and 80 <= r1["W_hat"] <= 330))
    R["verdicts"]["R1_law_replicates"]["holds"] = all(v for k, v in R["verdicts"]["R1_law_replicates"].items() if k != "rate")
    # joint anonymised atlas (R2, R3 pooled, R4)
    XJ = np.concatenate([A["anon"], B["anon"]], axis=0); kJ = k_for(XJ.shape[0] * XJ.shape[1]); CJ, LJ, persJ, sharedJ = fit_reference(XJ, kJ); sharedJ_ids = [c for c, _, _ in sharedJ]
    nA = A["anon"].shape[0]; pj = persistent_sets(LJ, persJ)
    # R2: A's own shared wells -> nearest joint cluster -> visited persistently by a B trajectory?
    CA, LA, persA, sharedA = fit_reference(A["anon"], k1); rows2 = []; hit = 0
    for c, ts, nv in sharedA:
        d = 1.0 - CJ @ CA[c]; j = int(np.argmin(d)); dj = float(d[j]); bt = sorted(t - nA for t in pj.get(j, set()) if t >= nA) if dj <= ATLAS["radius"] else []
        at = sorted(t for t in pj.get(j, set()) if t < nA) if dj <= ATLAS["radius"] else []
        ex = A["recs"][(A["T"][ts[0]], 50)].get("summary") or ""
        rows2.append(dict(a_well=int(c), a_trajs=ts, joint_cluster=j, centroid_dist=round(dj, 3), b_trajs=bt, a_trajs_in_joint=at, example=ex[:160])); hit += bool(bt)
    R["R2"] = dict(a_wells=len(sharedA), visited_by_B=hit, rows=rows2); R["verdicts"]["R2_wells_are_the_models"] = dict(visited=hit, of=len(sharedA), holds=hit >= 7, shoebox="grade by hand from the rows")
    # R3: B's own shared wells: new if no A shared well within 0.15; touched by A?
    CB, LB, persB, sharedB = fit_reference(B["anon"], k1); rows3 = []; new = 0; new_touched = 0; CAsh = CA[[c for c, _, _ in sharedA]]
    for c, ts, nv in sharedB:
        d = 1.0 - CAsh @ CB[c]; dmin = float(d.min()); isnew = dmin > ATLAS["radius"]
        touch = sorted(int(t) for t in np.where(((1.0 - np.einsum("d,tsd->ts", CB[c], A["anon"])) <= ATLAS["radius"]).any(axis=1))[0])
        ex = B["recs"][(B["T"][ts[0]], 50)].get("summary") or ""
        rows3.append(dict(b_well=int(c), b_trajs=ts, nearest_a_well_dist=round(dmin, 3), new=isnew, a_trajs_touching=touch, example=ex[:160])); new += isnew; new_touched += isnew and bool(touch)
    pooled_pairs = set()
    for c in sharedJ_ids:
        ts = sorted(pj[c]); pooled_pairs |= set(itertools.combinations(ts, 2))
    nP = (2 * nA) * (2 * nA - 1) // 2; pooled_rate = len(pooled_pairs) / nP
    R["R3"] = dict(b_wells=len(sharedB), new=new, new_touched_by_A=new_touched, rows=rows3, pooled=dict(k=kJ, shared=len(sharedJ), pairs=len(pooled_pairs), rate=pooled_rate))
    R["verdicts"]["R3_new_wells"] = dict(new=new, new_touched=new_touched, pooled_shared=len(sharedJ), pooled_rate=pooled_rate, single_rate=r1["rate"],
                                        holds=new >= 2 and new_touched >= 1 and len(sharedJ) >= 18 and (r1["rate"] > 0 and 1 / 1.5 <= pooled_rate / r1["rate"] <= 1.5))
    # R4: same-seed pairs
    late = slice(49, None)  # steps 50-99 in the step>=1 indexing
    def med_nn(X1, X2): return float(np.median((1.0 - X1[late] @ X2[late].T).min(axis=1)))
    same = [med_nn(A["anon"][t], B["anon"][t]) for t in range(nA)]
    rng = np.random.default_rng(0); diff = [med_nn(A["anon"][t], B["anon"][u]) for t, u in zip(rng.integers(0, nA, 300), rng.integers(0, nA, 300)) if t != u]
    same_share = sum(1 for t in range(nA) if any(t in pj[c] and (t + nA) in pj[c] for c in sharedJ_ids))
    cross = sum(1 for (i, j) in pooled_pairs if (i < nA) != (j < nA)); within = len(pooled_pairs) - cross
    rate_cross = cross / (nA * nA); rate_within = within / (2 * (nA * (nA - 1) // 2))
    R["R4"] = dict(same_seed_median=float(np.median(same)), diff_seed_median=float(np.median(diff)), gap=float(np.median(same) - np.median(diff)), same_seed_pairs_sharing=same_share, cross_rate=rate_cross, within_rate=rate_within)
    R["verdicts"]["R4_seeds_dont_pick_wells"] = dict(same_share=same_share, gap=R["R4"]["gap"], cross_over_within=(rate_cross / rate_within) if rate_within else None,
                                                   holds=same_share <= 3 and R["R4"]["gap"] < 0.02 and rate_within > 0 and 0.5 <= rate_cross / rate_within <= 2.0)
    for name, text in sheets: (OUT / name).write_text(text, encoding="utf-8")
    (OUT / "s2.json").write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")
    V = R["verdicts"]; L_ = [f"# E3-S2: second 100-seed Haiku sample ({a.b}) against the first ({a.a})", "",
          "Predictions: predictions.md \"E3 second sample and projections\" (2026-11-03), R1–R4. Atlas rules as E3-S; anonymised unless stated.", "",
          f"**R1 (law replicates): {'holds' if V['R1_law_replicates']['holds'] else 'fails'}** — second sample alone: anon rate {r1['rate']:.4f} ({r1['pairs']} of 4,950; first sample {R['R1']['anon']['first_sample']['rate']:.4f}), shared wells {r1['shared']} (first {R['R1']['anon']['first_sample']['shared']}), max multiplicity {r1['max_mult']}, W-hat {r1['W_hat'] and round(r1['W_hat'])}, raw shared {R['R1']['raw']['shared']} (first {R['R1']['raw']['first_sample']['shared']}).",
          f"**R2 (wells are the model's): {'holds' if V['R2_wells_are_the_models']['holds'] else 'fails'}** — {hit} of {len(sharedA)} first-sample wells receive a persistent visit from a second-sample trajectory in the joint atlas (k {kJ}).",
          f"**R3 (new rarer wells): {'holds' if V['R3_new_wells']['holds'] else 'fails'}** — second sample has {len(sharedB)} shared wells of which {new} are new (no first-sample well within 0.15), {new_touched} of them touched by a first-sample trajectory; pooled atlas {len(sharedJ)} shared wells, rate {pooled_rate:.4f}.",
          f"**R4 (seeds do not pick wells): {'holds' if V['R4_seeds_dont_pick_wells']['holds'] else 'fails'}** — same-seed pairs sharing a well {same_share} of 100; same-seed vs different-seed late distance {R['R4']['same_seed_median']:.3f} vs {R['R4']['diff_seed_median']:.3f} (gap {R['R4']['gap']:+.3f}); cross-sample rate {rate_cross:.4f} vs within-sample {rate_within:.4f}.", "",
          "## First-sample wells in the joint atlas (R2)", "", "| A well | A trajs | joint cluster (dist) | B trajs visiting | example summary (A, step 50) |", "|---|---|---|---|---|"]
    for r in rows2: L_.append(f"| {r['a_well']} | {r['a_trajs']} | {r['joint_cluster']} ({r['centroid_dist']}) | {r['b_trajs']} | {r['example']} |")
    L_ += ["", "## Second-sample wells (R3)", "", "| B well | B trajs | nearest A well dist | new | A trajs touching | example summary (B, step 50) |", "|---|---|---|---|---|---|"]
    for r in rows3: L_.append(f"| {r['b_well']} | {r['b_trajs']} | {r['nearest_a_well_dist']} | {'yes' if r['new'] else ''} | {r['a_trajs_touching']} | {r['example']} |")
    L_ += ["", "## Cells", "", "| cell | half-life | own seed 10 / 50 | nn-other raw / anon | within 0.15 raw / anon | Vendi story / summary 99 | words 99 | top-10 cover (top name) | modal tuple (share) | woman / hopeful |", "|---|---|---|---|---|---|---|---|---|---|"]
    for run in (a.a, a.b):
        s = R["cells"][run]; th = s["theme"]; nm = s["audit"]["names_50_99"]
        L_.append(f"| {run} | {s['half_life']} | {s['ident_at'].get(10)} / {s['ident_at'].get(50)} | {s['nn_other_median']:.3f} / {s['nn_other_anon_median']:.3f} | {s['within_015']:.3f} / {s['within_015_anon']:.3f} | {s['vendi_story_99']:.1f} / {s['vendi_summary_99'] and round(s['vendi_summary_99'],1)} | {s['words_median_99']:.0f} | {nm['top10_cover']:.2f} ({nm['top10'][0][0]} {nm['top10'][0][1]}) | {' × '.join(th['modal']) if th.get('modal') else ''} ({th.get('modal_share')}) | {th.get('woman_share')} / {th.get('hopeful_share')} |")
    (OUT / "s2.md").write_text("\n".join(L_) + "\n", encoding="utf-8"); print("\n".join(L_[:10]))


if __name__ == "__main__":
    main()
