"""E3-E essay-loop pilot report against predictions.md "E3-E essay-loop pilot" (2026-11-03), E1-E4 (E5 is for the record).
Measures as the story cells (e3s_report: raw and anonymised atlases at k 40 per 2,000 trajectory-steps, persistent-visit and pair-sharing
rules, seed memory, nn-other, Vendi) plus the essay judge (analysis/essay_judge.py): domain, subject kind, stance, tone per (traj, step).

Usage: .venv/bin/python analysis/e3e_report.py [--run e3_e_haiku] [--no-embed]
Writes reports/e3/essay.md, essay.json, essay.png and sw_cluster_<run>_{raw,anon}.md.
"""
import argparse, collections, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, MODELS, CACHE, Cache, cpu_only, package_versions  # noqa: E402
from e3_report import load_records, embed_all, unit  # noqa: E402
from e3s_report import ATLAS, k_for, atlas_pairs, anon_embed, cell_stats, cluster_sheet  # noqa: E402
from essay_judge import FIELDS  # noqa: E402

OUT = ROOT / "reports" / "e3"
LATE = range(50, 100)


def load_essay_judge(run):
    p = CACHE / run / "essay_judge.jsonl"; out, bad = {}, 0
    if not p.exists(): return out, bad
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        d = json.loads(line); j = d.get("judge")
        if not j or d.get("judge_error"): bad += 1; continue
        out[(d["traj"], d["step"])] = j
    return out, bad


def shares(J, T, steps, field):
    c = collections.Counter(J[(t, s)][field] for t in T for s in steps if (t, s) in J); n = sum(c.values())
    return {k: v / n for k, v in c.most_common()} if n else {}


def main():
    cpu_only(); ap = argparse.ArgumentParser(); ap.add_argument("--run", default="e3_e_haiku"); ap.add_argument("--no-embed", action="store_true"); a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8); run = a.run; model = None
    if not a.no_embed:
        if Cache(run).load("minilm") is None: embed_all([run], dev)
        from sentence_transformers import SentenceTransformer
        m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    recs, T, S = load_records(run); cache = Cache(run); X = cache.load("minilm")["X"].astype(np.float64); Xa, _ = anon_embed(run, recs, T, S, model, cache)
    raw, anon = unit(X[:, 1:]), unit(Xa[:, 1:]); k1 = k_for(raw.shape[0] * raw.shape[1])
    stats = cell_stats(run, X, Xa, recs, T, S); own = {tag: atlas_pairs(M, k1) for tag, M in (("raw", raw), ("anon", anon))}
    for tag in own: (OUT / f"sw_cluster_{run}_{tag}.md").write_text(cluster_sheet(run, recs, T, S, own[tag], tag), encoding="utf-8")
    J, bad = load_essay_judge(run); late = [s for s in LATE if s in S]
    dom0, domL = shares(J, T, [0], "domain"), shares(J, T, late, "domain"); kind0, kindL = shares(J, T, [0], "subject_kind"), shares(J, T, late, "subject_kind")
    per_step = {f: [shares(J, T, [s], f) for s in S] for f in ("domain", "subject_kind", "stance", "tone", "mentions_ai_or_computing", "mentions_environment_or_climate")}
    modal_dom = next(iter(domL), None); modal_share = domL.get(modal_dom, 0.0)
    refusals = sum(1 for t in T for s in S for k in ("story_meta", "summary_meta") if ((recs[(t, s)].get(k) or {}).get("flags") or {}).get("refusal"))
    flagged = [(t, s) for t in T for s in S if ((recs[(t, s)].get("story_meta") or {}).get("flags") or {}).get("refusal")][:10]
    A = {tag: dict(shared=own[tag]["shared"], persistent=own[tag]["persistent"], pairs=own[tag]["n_sharing_pairs"], rate=own[tag]["rate"], max_mult=own[tag]["max_mult"], W_hat=own[tag]["W_hat"], inside=own[tag]["inside_share"]) for tag in own}
    V = {}
    V["E1_rate_similar"] = dict(raw_shared=A["raw"]["shared"], anon_shared=A["anon"]["shared"], anon_rate=A["anon"]["rate"], nn_other=stats["nn_other_median"], within_015=stats["within_015"],
                                holds=A["raw"]["shared"] <= 2 and A["anon"]["shared"] <= 3 and A["anon"]["rate"] <= 0.02 and 0.30 <= stats["nn_other_median"] <= 0.45 and stats["within_015"] <= 0.01,
                                fails_upward=A["anon"]["rate"] >= 0.05 or A["raw"]["shared"] >= 4)
    hl = stats["half_life"]; V["E2_longer_memory"] = dict(half_life=hl, own_seed_50=stats["ident_at"].get(50), holds=hl is not None and 15 <= hl <= 40 and stats["ident_at"].get(50, 0) >= 0.5, under_8=hl is not None and hl < 8)
    top0 = max(dom0.values()) if dom0 else None
    V["E3_abstract_drift"] = dict(step0_top_domain=top0, late_modal_domain=modal_dom, late_modal_share=modal_share, abstract_step0=kind0.get("abstract", 0.0), abstract_late=kindL.get("abstract", 0.0),
                                  holds=bool(J) and top0 <= 0.20 and modal_share >= 0.35 and kindL.get("abstract", 0.0) >= 0.6 and kind0.get("abstract", 0.0) <= 0.3,
                                  named_direction_holds=modal_dom in ("society_and_politics", "philosophy_and_religion"), no_menu=bool(J) and modal_share < 0.25)
    V["E4_format"] = dict(words_99=stats["words_median_99"], summary_le_50=stats["summary_le_limit_share"][50] if stats["summary_le_limit_share"] else None, refusal_flags=refusals,
                          holds=400 <= stats["words_median_99"] <= 600 and (stats["summary_le_limit_share"] or {}).get(50, 0) >= 0.5 and refusals == 0)
    R = dict(params=dict(atlas=ATLAS, k=k1, versions=package_versions()), cell=stats, atlas=A, judge=dict(n=len(J), bad=bad, domain_step0=dom0, domain_late=domL, kind_step0=kind0, kind_late=kindL,
             stance_late=shares(J, T, late, "stance"), tone_late=shares(J, T, late, "tone"), ai_late=shares(J, T, late, "mentions_ai_or_computing"), env_late=shares(J, T, late, "mentions_environment_or_climate"),
             per_step=per_step), verdicts=V, refusal_flagged_examples=flagged)
    (OUT / "essay.json").write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")
    # figure: seed memory, domain shares over steps, abstract share
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4)); ax[0].plot(stats["memory_curve"], lw=1.6); ax[0].axhline(0.5, ls=":", c="grey"); ax[0].set(title=f"own-seed identification ({run})", xlabel="step", ylabel="share", ylim=(0, 1.02))
    doms = [d for d, _ in collections.Counter({**{d: 0 for d in FIELDS["domain"]}, **{d: int(round(v * 1000)) for d, v in domL.items()}}).most_common(6)]
    for d in doms: ax[1].plot([ps.get(d, 0.0) for ps in per_step["domain"]], lw=1.4, label=d)
    ax[1].set(title="domain share by step (top 6 late)", xlabel="step", ylim=(0, 1.02)); ax[1].legend(fontsize=7)
    ax[2].plot([ps.get("abstract", 0.0) for ps in per_step["subject_kind"]], lw=1.6, label="abstract"); ax[2].plot([ps.get("argues_a_position", 0.0) for ps in per_step["stance"]], lw=1.4, label="argues a position")
    ax[2].plot([ps.get("yes", 0.0) for ps in per_step["mentions_ai_or_computing"]], lw=1.4, label="mentions AI/computing"); ax[2].set(title="subject kind, stance, AI mentions", xlabel="step", ylim=(0, 1.02)); ax[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / "essay.png", dpi=110); plt.close(fig)
    f = lambda x: "holds" if x else "fails"  # noqa: E731
    L = [f"# E3-E essay-loop pilot: {run}", "", f"Predictions: predictions.md \"E3-E essay-loop pilot\" (2026-11-03), E1–E4. Atlas rules as E3-S (k {k1}); raw unless stated.", "",
         f"**E1 (rate similar to story cells): {f(V['E1_rate_similar']['holds'])}** — raw shared wells {A['raw']['shared']} (persistent {A['raw']['persistent']}), anonymised shared {A['anon']['shared']} (persistent {A['anon']['persistent']}), anonymised rate {A['anon']['rate']:.4f} ({A['anon']['pairs']} of {own['anon']['n_pairs']}), raw rate {A['raw']['rate']:.4f}, nn-other {stats['nn_other_median']:.3f} (anon {stats['nn_other_anon_median']:.3f}), within 0.15 {stats['within_015']:.3f} (anon {stats['within_015_anon']:.3f}); fails upward: {V['E1_rate_similar']['fails_upward']}.",
         f"**E2 (longer memory): {f(V['E2_longer_memory']['holds'])}** — half-life {hl}, own-seed identification at 10 / 25 / 50 / 99: {stats['ident_at'].get(10)} / {stats['ident_at'].get(25)} / {stats['ident_at'].get(50)} / {stats['ident_at'].get(99)}.",
         f"**E3 (drift to a few abstract domains): {f(V['E3_abstract_drift']['holds'])}** — step-0 top domain share {top0 and round(top0, 2)}; late (steps 50–99) modal domain {modal_dom} {modal_share:.2f}; abstract share step 0 {kind0.get('abstract', 0.0):.2f} → late {kindL.get('abstract', 0.0):.2f}; named direction (society/politics or philosophy/religion): {f(V['E3_abstract_drift']['named_direction_holds'])}; no-menu clause (<0.25): {V['E3_abstract_drift']['no_menu']}. Judge: {len(J)} essays coded, {bad} malformed.",
         f"**E4 (format): {f(V['E4_format']['holds'])}** — median words at step 99 {stats['words_median_99']:.0f}, summaries within 50 words {V['E4_format']['summary_le_50'] and round(V['E4_format']['summary_le_50'], 2)}, refusal flags {refusals} (the flag is the D19 heuristic; flagged examples: {flagged}), Vendi story 99 {stats['vendi_story_99']:.1f}, summary 99 {stats['vendi_summary_99'] and round(stats['vendi_summary_99'], 1)}.", "",
         "![essay](e3/essay.png)", "", "## Domain and subject kind", "", "| domain | step 0 | steps 50–99 |", "|---|---|---|"]
    for d in FIELDS["domain"]:
        if dom0.get(d, 0) or domL.get(d, 0): L.append(f"| {d} | {dom0.get(d, 0.0):.2f} | {domL.get(d, 0.0):.2f} |")
    L += ["", "| field (steps 50–99) | shares |", "|---|---|"]
    for name, sh in (("subject kind", kindL), ("stance", R["judge"]["stance_late"]), ("tone", R["judge"]["tone_late"]), ("mentions AI/computing", R["judge"]["ai_late"]), ("mentions environment/climate", R["judge"]["env_late"])):
        L.append(f"| {name} | " + ", ".join(f"{k} {v:.2f}" for k, v in sh.items()) + " |")
    L += ["", "## Each trajectory: seed topic → step 50 → step 99 (judge topic sentences)", "", "| traj | seed (first words) | step 0 domain | step 50 topic | step 99 domain / kind | step 99 topic |", "|---|---|---|---|---|---|"]
    for t in T:
        j0, j50, j99 = J.get((t, 0), {}), J.get((t, 50), {}), J.get((t, S[-1]), {}); seed = (recs[(t, 0)].get("seed_prompt") or "")[:60].replace("|", "/")
        L.append(f"| {t} | {seed} | {j0.get('domain', '')} | {j50.get('topic', '')} | {j99.get('domain', '')} / {j99.get('subject_kind', '')} | {j99.get('topic', '')} |")
    L += ["", "## Step-99 summaries", ""] + [f"- traj {t}: {(recs[(t, S[-1])].get('summary') or '').strip()}" for t in T]
    (OUT / "essay.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L[:9]))


if __name__ == "__main__":
    main()
