"""E3-S7B: the 100-seed Mistral and Qwen cells against predictions.md "E3-S7B" (2026-11-03), M1-M4.
Per cell: exclusion rule (fixed in advance: >= 10 CJK-flagged late stories, or late median story length < 150 words -> degenerate, left out of
the atlas and the rate); own raw and anonymised atlases at k 40 per 2,000 trajectory-steps (M1); projection onto the pooled Haiku reference
atlas (first + second 100-seed samples, anonymised, k 396, no refit) (M2); theme-judge field shares vs pooled Haiku (M2); cross-model
same-seed check in a joint atlas with Haiku's first sample (M4).

Usage: .venv/bin/python analysis/e3s7b_report.py [--cells e3_1_mistral_100 e3_1_qwen_100] [--no-embed] [--no-judge]
Writes reports/e3/s7b.md, s7b.json and sw_cluster_<cell>_{raw,anon}.md (kept trajectories only).
"""
import argparse, collections, itertools, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, MODELS, Cache, cpu_only, package_versions  # noqa: E402
from gravity import visits  # noqa: E402
from e3_report import load_records, embed_all, unit  # noqa: E402
from e3s_report import ATLAS, k_for, atlas_pairs, anon_embed, cell_stats, cluster_sheet  # noqa: E402
from e3_projection import fit_reference, label  # noqa: E402
from e3_theme_report import load_judge  # noqa: E402

OUT = ROOT / "reports" / "e3"; HAIKU = ("e3_1_haiku_100", "e3_1_haiku_100b"); LATE = range(50, 100); JFIELDS = ("lead_age", "conflict_type", "setting_place")


def degenerate(recs, T, S):
    out = {}
    for t in T:
        late = [recs[(t, s)] for s in S if s >= 50]
        cjk = sum(1 for r in late if ((r.get("story_meta") or {}).get("flags") or {}).get("cjk")); med = float(np.median([r["story_words"] for r in late]))
        if cjk >= 10 or med < 150: out[t] = dict(cjk_late=cjk, median_words_late=med)
    return out


def field_shares(runs, fields=JFIELDS, late=LATE):
    out = {}
    for f in fields:
        c = collections.Counter()
        for run in runs:
            J, _ = load_judge(run)
            for (t, s), j in J.items():
                if s in late: c[j.get(f)] += 1
        n = sum(c.values()); out[f] = {k: v / n for k, v in c.most_common()} if n else {}
    return out


def same_seed_check(XA, XB, k):
    """Joint atlas of two cells with the same seeds (trajectory t in each): same-seed pairs sharing a persistent well; late-distance gap."""
    nA = XA.shape[0]; XJ = np.concatenate([XA, XB]); C, L, pers, shared = fit_reference(XJ, k); shared_ids = [c for c, _, _ in shared]
    pj = {}
    for c in shared_ids:
        pj[c] = {ti for ti in range(XJ.shape[0]) if any(l >= ATLAS["min_dwell"] for l, _ in visits(L[ti] == c))}
    n = min(nA, XB.shape[0]); same = [t for t in range(n) if any(t in pj[c] and (t + nA) in pj[c] for c in shared_ids)]
    late = slice(49, None); med = lambda X1, X2: float(np.median((1.0 - X1[late] @ X2[late].T).min(axis=1)))  # noqa: E731
    s = [med(XA[t], XB[t]) for t in range(n)]; rng = np.random.default_rng(0)
    d = [med(XA[t], XB[u]) for t, u in zip(rng.integers(0, nA, 300), rng.integers(0, XB.shape[0], 300)) if t != u]
    cross = sum(1 for c in shared_ids for i, j in itertools.combinations(sorted(pj[c]), 2) if (i < nA) != (j < nA))
    return dict(k=k, joint_shared=len(shared), same_seed_pairs_sharing=len(same), same_seeds=same, same_median=float(np.median(s)), diff_median=float(np.median(d)), gap=float(np.median(s) - np.median(d)), cross_pairs=cross)


def main():
    cpu_only(); ap = argparse.ArgumentParser(); ap.add_argument("--cells", nargs="+", default=["e3_1_mistral_100", "e3_1_qwen_100"]); ap.add_argument("--no-embed", action="store_true"); ap.add_argument("--no-judge", action="store_true")
    a = ap.parse_args(); import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    cells = [c for c in a.cells if (ROOT / "runs" / c / "progress.json").exists() and json.loads((ROOT / "runs" / c / "progress.json").read_text()).get("state") == "finished"]
    model = None
    if not a.no_embed:
        need = [r for r in cells if Cache(r).load("minilm") is None]
        if need: embed_all(need, dev)
        from sentence_transformers import SentenceTransformer
        m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    # pooled Haiku reference (anonymised, no refit for projection)
    HX = [unit(Cache(r).load("minilm_anon")["X"].astype(np.float64)[:, 1:]) for r in HAIKU]; XH = np.concatenate(HX); kH = k_for(XH.shape[0] * XH.shape[1])
    CH, LH, persH, sharedH = fit_reference(XH, kH); shH = [c for c, _, _ in sharedH]; print(f"[haiku pooled] k {kH}, shared wells {len(sharedH)}", flush=True)
    haiku_shares = None if a.no_judge else field_shares(HAIKU)
    R = dict(params=dict(atlas=ATLAS, haiku_reference=dict(runs=HAIKU, k=kH, shared=len(sharedH)), versions=package_versions()), cells={}, verdicts={})
    for run in cells:
        recs, T, S = load_records(run); cache = Cache(run); X = cache.load("minilm")["X"].astype(np.float64); Xa, _ = anon_embed(run, recs, T, S, model, cache)
        deg = degenerate(recs, T, S); keep = [i for i, t in enumerate(T) if t not in deg]; Tk = [T[i] for i in keep]
        raw, anon = unit(X[keep, 1:]), unit(Xa[keep, 1:]); k1 = k_for(raw.shape[0] * raw.shape[1])
        own = {tag: atlas_pairs(M, k1, trajs=Tk) for tag, M in (("raw", raw), ("anon", anon))}
        for tag in own: (OUT / f"sw_cluster_{run}_{tag}.md").write_text(cluster_sheet(run, recs, Tk, S, own[tag], tag), encoding="utf-8")
        stats = None if a.no_judge else cell_stats(run, X[keep], Xa[keep], recs, Tk, S)
        # M2 projection onto the pooled Haiku atlas
        L = label(CH, anon); Dsh = 1.0 - np.einsum("kd,tsd->kts", CH[shH], anon); late = np.array([s >= 50 for s in S[1:]])
        in_wells = [Tk[ti] for ti in range(len(Tk)) if any(any(l >= ATLAS["min_dwell"] for l, _ in visits(L[ti] == c)) for c in shH)]
        wells_hit = sorted({int(c) for c in shH for ti in range(len(Tk)) if any(l >= ATLAS["min_dwell"] for l, _ in visits(L[ti] == c))})
        nn_shared = float(np.median(Dsh[:, :, late].min(axis=0))); inside_late = float(np.isin(L[:, late], persH).mean())
        shares = None if a.no_judge else field_shares([run]); diffs = None
        if shares: diffs = {f: max(abs(shares[f].get(k, 0) - haiku_shares[f].get(k, 0)) for k in set(shares[f]) | set(haiku_shares[f])) for f in JFIELDS}
        # M4 cross-model same-seed with Haiku A (kept trajectories only; same-seed means the same Hintze seed index)
        XA = HX[0]; idx = [i for i, t in enumerate(Tk) if t < XA.shape[0]]; m4 = same_seed_check(XA[[Tk[i] for i in idx]], anon[idx], k_for(2 * len(idx) * anon.shape[1])) if idx else None
        A_ = {tag: dict(shared=own[tag]["shared"], persistent=own[tag]["persistent"], pairs=own[tag]["n_sharing_pairs"], n_pairs=own[tag]["n_pairs"], rate=own[tag]["rate"], max_mult=own[tag]["max_mult"], W_hat=own[tag]["W_hat"]) for tag in own}
        r1 = A_["anon"]; M1 = dict(rate=r1["rate"], rate_in_band=0.003 <= r1["rate"] <= 0.012, shared_ge_8=r1["shared"] >= 8, mult_ge_3=r1["max_mult"] >= 3, raw_shared_ge_3=A_["raw"]["shared"] >= 3, W_in_band=r1["W_hat"] is not None and 80 <= r1["W_hat"] <= 330,
                  no_wells=r1["rate"] < 0.002, d_like=r1["rate"] > 0.03); M1["holds"] = all(v for k, v in M1.items() if k not in ("rate", "no_wells", "d_like"))
        M2 = dict(trajs_in_haiku_wells=len(in_wells), haiku_wells_hit=wells_hit, nn_shared_median=nn_shared, inside_late=inside_late, judge_max_diff=diffs, fields_ge_015=(sum(v >= 0.15 for v in diffs.values()) if diffs else None),
                  shared_across_families=len(in_wells) >= 10)
        M2["holds"] = len(in_wells) <= 3 and nn_shared >= 0.35 and (diffs is None or M2["fields_ge_015"] >= 2)
        M3 = dict(rate_top_or_above=0.01 <= r1["rate"] <= 0.03, W_le_100=r1["W_hat"] is not None and r1["W_hat"] <= 100, n_excluded=len(deg), half_life=stats and stats["half_life"])
        M4 = None if m4 is None else dict(same_seed_pairs=m4["same_seed_pairs_sharing"], gap=m4["gap"], holds=m4["same_seed_pairs_sharing"] <= 2 and m4["gap"] < 0.02)
        R["cells"][run] = dict(n_traj=len(T), excluded=deg, n_kept=len(Tk), atlas=A_, stats=stats, projection=dict(trajs_in_haiku_wells=in_wells, wells_hit=wells_hit, nn_shared_median=nn_shared, inside_late=inside_late), judge_shares=shares, haiku_shares=haiku_shares, same_seed_vs_haiku_A=m4)
        R["verdicts"][run] = dict(M1=M1, M2=M2, M3=M3, M4=M4); print(f"[{run}] kept {len(Tk)}; M1 {M1['holds']} rate {r1['rate']:.4f}; M2 {M2['holds']} in-wells {len(in_wells)} nn {nn_shared:.3f}; M4 {M4}", flush=True)
    if len(cells) == 2 and all(r in R["cells"] for r in cells):
        Xs = []; keeps = []
        for run in cells:
            recs, T, S = load_records(run); Xa = Cache(run).load("minilm_anon")["X"].astype(np.float64); keep = [i for i, t in enumerate(T) if t not in R["cells"][run]["excluded"]]; Xs.append(unit(Xa[keep, 1:])); keeps.append([T[i] for i in keep])
        common = sorted(set(keeps[0]) & set(keeps[1])); ia = [keeps[0].index(t) for t in common]; ib = [keeps[1].index(t) for t in common]
        R["same_seed_mistral_vs_qwen"] = same_seed_check(Xs[0][ia], Xs[1][ib], k_for(2 * len(common) * Xs[0].shape[1]))
    (OUT / "s7b.json").write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")
    f = lambda x: "holds" if x else "fails"  # noqa: E731
    L_ = ["# E3-S7B: 100-seed Mistral and Qwen cells against predictions.md \"E3-S7B\" (2026-11-03)", "", f"Pooled Haiku reference: {HAIKU}, anonymised, k {kH}, {len(sharedH)} shared wells. Atlas rules as E3-S. Exclusion rule applied before the atlas.", ""]
    for run in cells:
        c = R["cells"][run]; V = R["verdicts"][run]; A_ = c["atlas"]; st = c["stats"]
        L_ += [f"## {run}: {c['n_kept']} of {c['n_traj']} trajectories kept ({len(c['excluded'])} degenerate)", "",
               f"**M1 (same level as Haiku): {f(V['M1']['holds'])}** — anon rate {A_['anon']['rate']:.4f} ({A_['anon']['pairs']} of {A_['anon']['n_pairs']}; band 0.003–0.012), shared wells {A_['anon']['shared']}, max multiplicity {A_['anon']['max_mult']}, W-hat {A_['anon']['W_hat'] and round(A_['anon']['W_hat'])}, raw shared {A_['raw']['shared']}; no-wells clause {V['M1']['no_wells']}, D-like clause {V['M1']['d_like']}.",
               f"**M2 (different themes): {f(V['M2']['holds'])}** — {V['M2']['trajs_in_haiku_wells']} trajectories dwell in a Haiku well (wells {V['M2']['haiku_wells_hit']}), median late distance to the nearest Haiku shared well {V['M2']['nn_shared_median']:.3f} (≥ 0.35), inside any Haiku persistent cluster late {V['M2']['inside_late']:.3f}; judge max share difference vs Haiku {V['M2']['judge_max_diff']} (fields ≥ 0.15: {V['M2']['fields_ge_015']}).",
               f"**M3 (Claude's alternative)** — rate in 0.01–0.03: {V['M3']['rate_top_or_above']}; W-hat ≤ 100: {V['M3']['W_le_100']}; excluded {V['M3']['n_excluded']}; half-life {V['M3']['half_life']}.",
               f"**M4 (cross-model seed trace vs Haiku A): {f(V['M4'] and V['M4']['holds'])}** — same-seed pairs sharing a joint well {V['M4'] and V['M4']['same_seed_pairs']} of 100 (≤ 2), late-distance gap {V['M4'] and round(V['M4']['gap'], 3)} (< 0.02)." if V["M4"] else "M4: not computed", ""]
        if st:
            th = st["theme"]; L_ += [f"Cell: half-life {st['half_life']}, own seed 10 / 50 / 99 {st['ident_at'].get(10)} / {st['ident_at'].get(50)} / {st['ident_at'].get(99)}, nn-other raw / anon {st['nn_other_median']:.3f} / {st['nn_other_anon_median']:.3f}, within 0.15 {st['within_015']:.3f} / {st['within_015_anon']:.3f}, Vendi story 99 {st['vendi_story_99']:.1f}, words 99 {st['words_median_99']:.0f}, summaries ≤ 50 {st['summary_le_limit_share'] and st['summary_le_limit_share'].get(50)}, top-10 name cover {st['audit']['names_50_99']['top10_cover']:.2f} ({st['audit']['names_50_99']['top10'][0][0]}), modal tuple {' × '.join(th['modal']) if th else ''} ({th and round(th['modal_share'], 3)}), woman {th and round(th['woman_share'], 2)}, hopeful {th and round(th['hopeful_share'], 2)}.", ""]
        if c["judge_shares"]:
            L_ += ["| field | value | this cell | Haiku pooled |", "|---|---|---|---|"]
            for fld in JFIELDS:
                for k in sorted(set(c["judge_shares"][fld]) | set(c["haiku_shares"][fld]), key=lambda z: -c["judge_shares"][fld].get(z, 0)):
                    L_.append(f"| {fld} | {k} | {c['judge_shares'][fld].get(k, 0):.2f} | {c['haiku_shares'][fld].get(k, 0):.2f} |")
            L_.append("")
        if c["excluded"]: L_ += ["Excluded trajectories: " + ", ".join(f"{t} (CJK {v['cjk_late']}, median words {v['median_words_late']:.0f})" for t, v in c["excluded"].items()), ""]
    if "same_seed_mistral_vs_qwen" in R:
        m = R["same_seed_mistral_vs_qwen"]; L_ += [f"Mistral vs Qwen same-seed: {m['same_seed_pairs_sharing']} of {len(m['same_seeds']) or 'n'} pairs sharing a joint well (seeds {m['same_seeds']}), gap {m['gap']:+.3f}, joint shared wells {m['joint_shared']}, cross-model sharing pairs {m['cross_pairs']}.", ""]
    (OUT / "s7b.md").write_text("\n".join(L_) + "\n", encoding="utf-8"); print("\n".join(L_))


if __name__ == "__main__":
    main()
