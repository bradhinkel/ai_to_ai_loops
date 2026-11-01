"""E3-C report (SPEC2 §4 E3 follow-ups; predictions.md "E3 follow-ups" C1–C4): the absolute-length rewrite loop (E3-2b) and the two
new models (claude-haiku-5-5, mistral:7b), plus E3-2b under Qwen. Same measurements as the E3 gate (analysis/e3_report.py), on
whatever finished cells are named on the command line; the gate's six cells are the references (reports/e3.json). MiniLM only
(CLAUDE.md rule 4); the theme tuple comes from the Haiku judge cache when present and is reported, never fed back.

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/e3c_report.py e3_1_haiku e3_2b_haiku [e3_1_mistral e3_2b_mistral e3_2b_qwen] [--no-embed]

Writes reports/e3/c.md, c.json, c_curves.png, c_cluster_NN.md; archive/e3c_persistent_atlas_centroids.npz.
"""
import argparse, collections, json, math, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache, cpu_only, series_matrix, final_step_matrix, drift_curves, plateau_step, vendi, package_versions  # noqa: E402
from gravity import label_steps, visits, km_median  # noqa: E402
from memory_curve import curve as memory_curve  # noqa: E402
from e3_report import load_records, embed_all, content_audit, is_cjk, unit  # noqa: E402

REFS = ["e3_1_sonnet", "e3_2_sonnet", "e3_1_qwen", "e3_2_qwen", "e3_1_llava", "e3_2_llava"]
TUPLE = ("lead_age", "conflict_type", "ending_valence"); TUPLE_B = ("lead_gender", "conflict_type", "ending_valence")


def model_of(run):
    return run.split("_")[-1]


def loop_of(run):
    return {"1": "E3-1", "2": "E3-2", "2b": "E3-2b"}[run.split("_")[1]]


def nn_other(X, s0=25):
    T, S, _ = X.shape; Y = X[:, s0:]; out = []
    for t in range(T):
        others = np.delete(Y, t, 0).reshape(-1, Y.shape[-1]); out.append((1 - Y[t] @ others.T).min(1))
    return np.concatenate(out)


def self_share(X, s0=50, r=0.15):
    Y = X[:, s0:]; cc = Y.mean(1); cc /= np.linalg.norm(cc, axis=-1, keepdims=True); return float((1 - np.einsum("tsd,td->ts", Y, cc) <= r).mean())


def cons_med(X):
    return float(np.median(1 - np.einsum("tsd,tsd->ts", X[:, 2:], X[:, 1:-1])))


def load_judge(run):
    p = ROOT / "analysis" / "cache" / run / "theme_judge.jsonl"
    if not p.exists(): return None
    out = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            if d.get("judge"): out[(d["traj"], d["step"])] = d["judge"]
    return out or None


def tuple_stats(J, fields, lo, hi):
    c = collections.Counter(tuple(str(j[f]) for f in fields) for (t, s), j in J.items() if lo <= s <= hi)
    n = sum(c.values()); p = np.array(list(c.values()), float) / max(1, n)
    return dict(n=n, eff=float(math.exp(-(p * np.log(p)).sum())) if n else None, modal=(c.most_common(1)[0][0] if n else None), modal_share=(c.most_common(1)[0][1] / n) if n else None)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--no-embed", action="store_true"); ap.add_argument("--k", type=int, default=40)
    ap.add_argument("--radius", type=float, default=0.15); ap.add_argument("--exit_factor", type=float, default=1.25); ap.add_argument("--min_dwell", type=int, default=5)
    ap.add_argument("--min_visits", type=int, default=3); ap.add_argument("--seed", type=int, default=0); a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    runs = a.runs
    for run in runs:
        st = json.loads((ROOT / "runs" / run / "progress.json").read_text())["state"]
        assert st == "finished", f"{run} is {st}"
    if not a.no_embed: embed_all(runs, dev)
    out_dir = ROOT / "reports" / "e3"; out_dir.mkdir(parents=True, exist_ok=True)
    gate = json.loads((ROOT / "reports" / "e3.json").read_text(encoding="utf-8"))["cells"]
    theme_gate = json.loads((out_dir / "theme.json").read_text(encoding="utf-8")) if (out_dir / "theme.json").exists() else {}
    R = {"cells": {}, "params": dict(k=a.k, radius=a.radius, exit_factor=a.exit_factor, min_dwell=a.min_dwell, min_visits=a.min_visits, device=dev, packages=package_versions())}

    # ---- per-cell curves and scalars (new cells; references re-derived from the gate's caches for the figure)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8)); series_all, recs_all, audits = {}, {}, {}
    palette = ["#1b6ca8", "#d1495b", "#edae49", "#00798c", "#6a4c93", "#2e933c"]
    for i, run in enumerate(runs + REFS):
        new = run in runs; cache = Cache(run)
        if not (cache.dir / "minilm.npz").exists(): continue
        ser = series_matrix(cache, "minilm"); step_d, cum_d, mean_step, mean_cum, L = drift_curves(ser)
        X = cache.arrays("minilm")["X"].astype(np.float64); ident, excess = memory_curve(X); Tn = X.shape[0]
        half = next((k for k in range(len(ident)) if ident[k] <= 0.5), None)
        recs, T, S = load_records(run)
        lens = np.array([[recs[(t, s)]["story_words"] for s in S] for t in T], float)
        cjk = np.array([[is_cjk(recs[(t, s)]["story"]) for s in S] for t in T]); lens[cjk] = np.nan
        lab = f"{model_of(run)} {loop_of(run)}"
        if new:
            series_all[run] = ser; recs_all[run] = (recs, T, S)
            _, X99, _ = final_step_matrix(cache, "minilm", ROOT / "runs" / run, step=99); _, X1, _ = final_step_matrix(cache, "minilm", ROOT / "runs" / run, step=1)
            Xu = unit(X); audit, _ = content_audit(run, recs, T, S); audits[run] = audit
            R["cells"][run] = dict(model=model_of(run), loop=loop_of(run), n_traj=len(T), n_steps=len(S), plateau_step=plateau_step(mean_step),
                                   mean_step_drift_first5=float(mean_step[:5].mean()), mean_step_drift_last20=float(mean_step[-20:].mean()),
                                   cum_dist_step99_median=float(np.median([cum_d[t][-1] for t in cum_d])), vendi_step1=vendi(X1), vendi_step99=vendi(X99),
                                   memory=dict(half_life=half, ident_at={k: round(float(ident[k]), 2) for k in (1, 5, 10, 25, 50, 99)}),
                                   words_median_by_step=np.nanmedian(lens, 0).tolist(), words_median_step99=float(np.nanmedian(lens[:, -1])),
                                   words_step99_min_max=[float(np.nanmin(lens[:, -1])), float(np.nanmax(lens[:, -1]))],
                                   nn_other_median=float(np.median(nn_other(Xu))), self_centroid_share_50_99=self_share(Xu), consecutive_median=cons_med(Xu),
                                   audit=dict(exact_copies=audit["exact_copies"], n_cjk_stories=audit["n_cjk_stories"], names_50_99=audit["names_50_99"], compliance=audit["compliance"], flags=audit["flags"],
                                              windows={w: {k: v for k, v in d.items() if k in ("words_median", "named_share", "lead_female", "lead_male", "elderly_share", "vader_mean", "jaccard_top50_median", "top_leads", "top_content")} for w, d in audit["windows"].items()}),
                                   step_drift_curve_mean=mean_step.tolist(), cum_dist_curve_mean=mean_cum.tolist(), memory_curve=[float(x) for x in ident])
            col, lw, ls, alpha = palette[i % len(palette)], 1.8, "-" if loop_of(run) == "E3-1" else "--", 1.0
        else:
            col, lw, ls, alpha = "gray", 0.9, "-" if loop_of(run) == "E3-1" else "--", 0.6; lab += " (gate)"
        axes[0, 0].plot(range(2, 2 + L), mean_step, ls, color=col, lw=lw, alpha=alpha, label=lab); axes[0, 1].plot(range(2, 2 + L), mean_cum, ls, color=col, lw=lw, alpha=alpha, label=lab)
        axes[1, 0].plot(ident, ls, color=col, lw=lw, alpha=alpha, label=lab); axes[1, 1].plot(np.nanmedian(lens, 0), ls, color=col, lw=lw, alpha=alpha, label=lab)
    for ax, t, yl in zip(axes.flat, ("mean step-to-step drift (MiniLM cosine)", "mean distance from the step-1 story", "own seed story identified (memory curve)", "median story length (words; CJK excluded)"),
                         ("distance", "distance", "share of trajectories", "words")):
        ax.set_title(t, fontsize=10); ax.set_xlabel("step"); ax.set_ylabel(yl); ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=6, ncol=2)
    axes[1, 0].axhline(0.5, color="gray", lw=0.8, ls=":"); axes[1, 1].axhspan(450, 550, color="#edae49", alpha=0.12)
    fig.tight_layout(); fig.savefig(out_dir / "c_curves.png", dpi=130); plt.close(fig)

    # ---- joint persistent atlas over the new cells (the gate's procedure)
    E = {run: unit(np.stack([series_all[run][t] for t in sorted(series_all[run])]).astype(np.float32)) for run in runs}
    trajs = {run: sorted(series_all[run]) for run in runs}
    pooled = np.concatenate([E[r].reshape(-1, E[r].shape[-1]) for r in runs])
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=a.k, n_init=3, random_state=a.seed).fit(pooled); C = unit(km.cluster_centers_.astype(np.float32))
    np.savez(ROOT / "archive" / "e3c_persistent_atlas_centroids.npz", C=C, runs=np.array(runs))
    stats, examples = {}, {}
    for run in runs:
        X = E[run]; T, S, _ = X.shape
        D = 1.0 - np.einsum("kd,tsd->kts", C, X); Lb = label_steps(D, np.full(a.k, a.radius), a.exit_factor)
        inside_any = np.zeros((T, S), bool); shared = 0; pers = 0
        for k in range(a.k):
            inside = Lb == k; ex, alld = [], []
            for ti in range(T):
                pos = 0
                for length, censored in visits(inside[ti]):
                    while pos < S and not inside[ti, pos]: pos += 1
                    start = pos; pos += length
                    if length >= a.min_dwell: alld.append(length); ex.append((trajs[run][ti], start + 1 + length // 2, length, bool(censored)))
            stats[(run, k)] = dict(persistent_visits=len(alld), trajectories=len({e[0] for e in ex}), steps_inside=int(inside.sum()), median_dwell=float(np.median(alld)) if alld else None)
            examples[(run, k)] = sorted(ex, key=lambda e: -e[2])
            if len(alld) >= a.min_visits:
                pers += 1; inside_any |= inside; shared += stats[(run, k)]["trajectories"] >= 2
        R["cells"][run]["atlas"] = dict(n_persistent=pers, n_shared_ge2_traj=shared, share_steps_inside=float(inside_any.mean()), share_endpoints_inside=float(inside_any[:, -1].mean()))
    # contact sheets for every persistent cluster
    for k in range(a.k):
        pres = [r for r in runs if stats[(r, k)]["persistent_visits"] >= a.min_visits]
        if not pres: continue
        md = [f"# E3-C cluster {k:02d}", "", "cells: " + ", ".join(f"{r} ({stats[(r, k)]['persistent_visits']} visits, {stats[(r, k)]['trajectories']} trajectories, median dwell {stats[(r, k)]['median_dwell']})" for r in pres), ""]
        for r in pres:
            recs, T, S = recs_all[r]
            for (t, s, length, cens) in examples[(r, k)][:4]:
                rec = recs[(t, s)]; md += [f"## {r} traj {t} step {s} (dwell {length}{', censored' if cens else ''})", "", (rec.get("summary") or "").strip(), "", rec["story"][:700].replace("\n", " ") + " …", ""]
        (out_dir / f"c_cluster_{k:02d}.md").write_text("\n".join(md), encoding="utf-8")

    # ---- theme tuple from the judge cache, if present
    for run in runs:
        J = load_judge(run)
        if not J: R["cells"][run]["theme"] = None; continue
        th = {"judged": len(J)}
        for name, fields in (("tuple", TUPLE), ("tuple_b", TUPLE_B)):
            e, l = tuple_stats(J, fields, 1, 10), tuple_stats(J, fields, 50, 99)
            th[name] = dict(early=e, late=l, eff_ratio=(l["eff"] / e["eff"]) if e["eff"] and l["eff"] else None)
        th["field_modal_late"] = {f: collections.Counter(str(j[f]) for (t, s), j in J.items() if s >= 50).most_common(1)[0] for f in ("lead_age", "lead_gender", "lead_role_class", "setting_place", "setting_time", "conflict_type", "ending_valence", "secondary_character", "death_present", "reconciliation_present", "nature_central")}
        R["cells"][run]["theme"] = th

    # ---- verdicts
    c = R["cells"]; V = {}
    def g(run, *ks):
        d = gate.get(run)
        for k in ks:
            if d is None: return None
            d = d.get(k) if isinstance(d, dict) else None
        return d
    def gate_modal(run, key="tuple"):
        try: return tuple(theme_gate["cells"][run][key]["modal_late"][0])
        except Exception: return None
    for run in runs:
        m, lp = model_of(run), loop_of(run); v = {}
        w99 = c[run]["words_median_step99"]
        if lp == "E3-2b" or m in ("haiku",):
            lo, hi = (400, 600) if m == "mistral" else (450, 550); v["C1_length_450_550"] = dict(words_median_99=w99, holds=lo <= w99 <= hi, band=[lo, hi])
        if run == "e3_2b_qwen": v["C1_copies_below_half_of_E3_2"] = dict(copies=c[run]["audit"]["exact_copies"], e3_2=g("e3_2_qwen", "audit", "exact_copies"), holds=c[run]["audit"]["exact_copies"] < 0.5 * (g("e3_2_qwen", "audit", "exact_copies") or 276))
        if lp == "E3-2b":
            own = c.get(f"e3_1_{m}", {}).get("cum_dist_step99_median") or g(f"e3_1_{m}", "cum_dist_step99_median")
            v["C2_rewrite_reproduces"] = dict(half_life=c[run]["memory"]["half_life"], half_gt_99=c[run]["memory"]["half_life"] is None, cum99=c[run]["cum_dist_step99_median"], own_e3_1_cum99=own,
                                              cum99_below_e3_1=(own is not None and c[run]["cum_dist_step99_median"] < own), shared=c[run]["atlas"]["n_shared_ge2_traj"], self_share=c[run]["self_centroid_share_50_99"],
                                              holds=(c[run]["memory"]["half_life"] is None and own is not None and c[run]["cum_dist_step99_median"] < own and c[run]["atlas"]["n_shared_ge2_traj"] == 0 and c[run]["self_centroid_share_50_99"] >= 0.85))
        if run == "e3_1_mistral":
            q10 = {n for n, _ in (g("e3_1_qwen", "audit", "names_50_99", "top10") or [])}; m10 = {n for n, _ in c[run]["audit"]["names_50_99"]["top10"]}
            hq, hs = g("e3_1_qwen", "memory", "half_life"), g("e3_1_sonnet", "memory", "half_life"); h = c[run]["memory"]["half_life"]
            tq, tm = gate_modal("e3_1_qwen"), (tuple(c[run]["theme"]["tuple"]["late"]["modal"]) if c[run].get("theme") else None)
            v["C3_mistral_distinct"] = dict(shared=c[run]["atlas"]["n_shared_ge2_traj"], nn_other=c[run]["nn_other_median"], nn_in_band=0.35 <= c[run]["nn_other_median"] <= 0.60, half_life=h, qwen_half=hq, sonnet_half=hs,
                                            half_between=(h is not None and hq is not None and hs is not None and min(hq, hs) < h < max(hq, hs)), top10_cover=c[run]["audit"]["names_50_99"]["top10_cover"],
                                            cover_ge_05=c[run]["audit"]["names_50_99"]["top10_cover"] >= 0.5, shared_names_with_qwen=sorted(q10 & m10), le3_shared=len(q10 & m10) <= 3,
                                            cjk_stories=c[run]["audit"]["n_cjk_stories"], no_code_switch=c[run]["audit"]["n_cjk_stories"] == 0,
                                            modal_tuple=tm, qwen_modal=tq, differs_ge1=(tm is not None and tq is not None and tm != tq))
        if run == "e3_1_haiku":
            hs = g("e3_1_sonnet", "memory", "half_life"); h = c[run]["memory"]["half_life"]; ts, th_ = gate_modal("e3_1_sonnet"), (tuple(c[run]["theme"]["tuple"]["late"]["modal"]) if c[run].get("theme") else None)
            agree = sum(x == y for x, y in zip(ts, th_)) if (ts and th_) else None
            tsb, thb = gate_modal("e3_1_sonnet", "tuple_b"), (tuple(c[run]["theme"]["tuple_b"]["late"]["modal"]) if c[run].get("theme") else None)
            v["C4_size_axis"] = dict(half_life=h, sonnet_half=hs, half_le_30=(h is not None and h <= 30), top10_cover=c[run]["audit"]["names_50_99"]["top10_cover"], sonnet_cover=g("e3_1_sonnet", "audit", "names_50_99", "top10_cover"),
                                     cover_ge_05=c[run]["audit"]["names_50_99"]["top10_cover"] >= 0.5, words_99=w99, holds_500=450 <= w99 <= 550,
                                     modal_tuple=th_, sonnet_modal=ts, fields_agree=agree, agree_ge2=(agree is not None and agree >= 2),
                                     tuple_b_haiku=thb, tuple_b_sonnet=tsb, tuple_b_agree=(sum(x == y for x, y in zip(tsb, thb)) if (tsb and thb) else None))
        V[run] = v
    R["verdicts"] = V
    (out_dir / "c.json").write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")

    # ---- markdown
    md = ["# E3-C: absolute-length rewrite and the new models", "",
          f"Cells: {', '.join(runs)}. Same measurements as the E3 gate; gate cells in grey in `c_curves.png`. Atlas: joint k-means over these cells only (k {a.k}), radius {a.radius}, hysteresis {a.exit_factor}, dwell ≥ {a.min_dwell}, ≥ {a.min_visits} visits; shared = ≥ 2 trajectories. nn-other = median cosine distance (steps ≥ 25) to the nearest step of any other trajectory. Theme tuple = lead_age × conflict_type × ending_valence from the Haiku judge (reported, never fed back); tuple B swaps lead_age for lead_gender (post-hoc robustness, see theme.md).", "",
          "## Verdicts", "", "| cell | prediction | holds | numbers |", "|---|---|---|---|"]
    for run, v in V.items():
        for k, d in v.items():
            md.append(f"| {run} | {k} | {'yes' if d.get('holds', all(x for kk, x in d.items() if isinstance(x, bool))) else 'no'} | {json.dumps({kk: (round(x, 3) if isinstance(x, float) else x) for kk, x in d.items() if kk != 'holds'}, default=str)} |")
    md += ["", "## Cells", "", "| cell | plateau | step drift first 5 → last 20 | dist from step 1 at 99 | half-life | own seed at 10 / 50 / 99 | Vendi 1 → 99 | persistent (shared) | steps inside | nn-other | self-share 50–99 | words at 99 (min–max) | exact copies | CJK | top-10 names cover | top names 50–99 |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for run in runs:
        d = c[run]; n = d["audit"]["names_50_99"]
        md.append(f"| {run} | {d['plateau_step']} | {d['mean_step_drift_first5']:.3f} → {d['mean_step_drift_last20']:.3f} | {d['cum_dist_step99_median']:.3f} | {d['memory']['half_life']} | {d['memory']['ident_at'][10]} / {d['memory']['ident_at'][50]} / {d['memory']['ident_at'][99]} | {d['vendi_step1']:.1f} → {d['vendi_step99']:.1f} | {d['atlas']['n_persistent']} ({d['atlas']['n_shared_ge2_traj']}) | {d['atlas']['share_steps_inside']:.2f} | {d['nn_other_median']:.3f} | {d['self_centroid_share_50_99']:.2f} | {d['words_median_step99']:.0f} ({d['words_step99_min_max'][0]:.0f}–{d['words_step99_min_max'][1]:.0f}) | {d['audit']['exact_copies']} | {d['audit']['n_cjk_stories']} | {n['top10_cover']:.2f} | {', '.join(f'{a_} {b}' for a_, b in n['top10'][:6])} |")
    md += ["", "Gate references: " + "; ".join(f"{r}: half-life {gate[r]['memory']['half_life']}, dist@99 {gate[r]['cum_dist_step99_median']:.3f}, words@99 {gate[r]['words_median_by_step'][-1]:.0f}, copies {gate[r]['audit']['exact_copies']}, cover {gate[r]['audit']['names_50_99']['top10_cover']:.2f}" for r in REFS if r in gate), "",
           "## Theme tuple (Haiku judge)", "", "| cell | judged | eff. tuples 1–10 → 50–99 | modal late tuple (share) | tuple B modal late (share) | modal fields late |", "|---|---|---|---|---|---|"]
    for run in runs:
        th = c[run].get("theme")
        if not th: md.append(f"| {run} | not judged | | | | |"); continue
        md.append(f"| {run} | {th['judged']} | {th['tuple']['early']['eff']:.1f} → {th['tuple']['late']['eff']:.1f} | {'/'.join(th['tuple']['late']['modal'])} ({th['tuple']['late']['modal_share']:.2f}) | {'/'.join(th['tuple_b']['late']['modal'])} ({th['tuple_b']['late']['modal_share']:.2f}) | {', '.join(f'{f} {v[0]} {v[1] / max(1, sum(1 for (t, s) in load_judge(run) if s >= 50)):.2f}' for f, v in th['field_modal_late'].items())} |")
    md += ["", "Compliance / flags: " + "; ".join(f"{r}: {c[r]['audit']['compliance']} flags {c[r]['audit']['flags']}" for r in runs), "", "Cluster sheets: `c_cluster_NN.md`. Figure: `c_curves.png`."]
    (out_dir / "c.md").write_text("\n".join(md), encoding="utf-8"); print("\n".join(md))


if __name__ == "__main__":
    main()
