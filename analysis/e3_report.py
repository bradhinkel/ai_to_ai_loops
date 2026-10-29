"""E3 text-loop gate analysis (SPEC2 §4 E3 as amended 2026-10-28; predictions.md "E3 text loops").

  .venv/bin/python analysis/e3_report.py                       # all six cells
  .venv/bin/python analysis/e3_report.py --no-embed            # reuse analysis/cache/<run>/minilm.npz

The story is the state in both loops. Steps:
  1. MiniLM (common.MODELS pin) of every story -> analysis/cache/<run>/minilm.npz in the standard Cache layout (same arrays the
     image-era scripts read), and of every E3-1 summary -> minilm_summary.npz.
  2. Per cell: drift curves + plateau (a0_report rule), seed memory curve (memory_curve.curve), Vendi at step 99, length curve.
  3. Persistent atlas over the six cells jointly (k-means k 40 on all 11,880 intermediate steps, radius 0.15, hysteresis 1.25,
     dwell >= 5, present = >= 3 visits; the same rules and the same label_steps as persistent_atlas.py / gravity.py), with text
     "contact sheets" (reports/e3/cluster_<k>.md: the middle step of the longest persistent visits, one block per cell).
  4. Within-model overlap of E3-2 and E3-1 attractors (joint clusters shared, and per-cell centroid distances), and the distance
     of every story to A0-S's named caption-space attractors (archive/persistent_atlas_minilm_s_names_centroids.npz).
  5. Content audit from the records only: names (lead character = most frequent name-like token), lead gender by pronoun
     majority, gendered-word totals (caption_audit lexicons), elderly lexicon, VADER compound, Flesch-Kincaid grade, word count,
     Jaccard of per-trajectory top-50 content words with the pooled top-50, compliance flags; CJK stories excluded from the
     English-only measures and counted.
  6. The verdict numbers for predictions 1-9 -> reports/e3.json; tables printed as markdown for reports/e3.md.
CLIP is not used; no judge is used.
"""
import argparse, collections, json, pathlib, re, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, MODELS, SERIES, Cache, cpu_only, series_matrix, final_step_matrix, drift_curves, plateau_step, vendi, package_versions  # noqa: E402
from gravity import label_steps, visits, km_median  # noqa: E402
from memory_curve import curve as memory_curve  # noqa: E402
from caption_audit import MALE, FEMALE, words as audit_words  # noqa: E402
sys.path.insert(0, str(ROOT / "src"))
from prompt_clip import CJK_RE  # noqa: E402

CELLS = [  # run, model, loop
    ("e3_1_sonnet", "sonnet", "E3-1"), ("e3_2_sonnet", "sonnet", "E3-2"),
    ("e3_1_qwen", "qwen", "E3-1"), ("e3_2_qwen", "qwen", "E3-2"),
    ("e3_1_llava", "llava", "E3-1"), ("e3_2_llava", "llava", "E3-2"),
]
WINDOWS = [(1, 10), (11, 25), (26, 50), (51, 75), (76, 89), (90, 99)]
ELDERLY = {"grandmother", "grandfather", "grandparent", "grandparents", "grandma", "grandpa", "widow", "widower", "retired",
           "retirement", "elderly", "aged", "wrinkled", "seventy", "eighty", "ninety", "octogenarian", "pensioner", "nana", "granny"}
ELDERLY_PHRASES = ("old man", "old woman", "older man", "older woman", "years old")
LLM_NAMES = {"Elara", "Elias", "Maya", "Kai", "Lena", "Theo", "Mira", "Amara", "Eli", "Clara"}
HONORIFIC = {"Mr", "Mrs", "Ms", "Miss", "Dr", "Sir", "Lady", "Lord", "Aunt", "Uncle", "Captain", "Professor", "Prime", "Minister", "Saint", "St"}
MODELS["minilm_summary"] = dict(MODELS["minilm"], pooling=MODELS["minilm"]["pooling"] + "; field = summary")   # same model, second text field
A0S_NAMED = {11: "gnarled tree over still water", 12: "gilded baroque ballroom", 16: "terracotta courtyard", 32: "blush-pink rococo salon", 34: "twilight lake in lavender haze"}


def unit(X):
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def load_records(run):
    recs = {}
    for f in sorted((ROOT / "runs" / run).glob("traj_*/step_???.json")):
        r = json.loads(f.read_text(encoding="utf-8")); recs[(r["traj"], r["step"])] = r
    T = sorted({k[0] for k in recs}); S = sorted({k[1] for k in recs})
    assert len(recs) == len(T) * len(S), f"{run}: ragged records"
    return recs, T, S


def is_cjk(text):
    return len(CJK_RE.findall(text)) > 0.05 * max(1, len(text))


# ------------------------------------------------------------------ 1. embeddings
def embed_all(runs, dev):
    from sentence_transformers import SentenceTransformer
    m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    for run in runs:
        recs, T, S = load_records(run); cache = Cache(run)
        for space, field in (("minilm", "story"), ("minilm_summary", "summary")):
            if recs[(T[0], S[0])].get(field) is None: continue
            texts = [recs[(t, s)][field] or "" for t in T for s in S]
            X = model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=False).reshape(len(T), len(S), -1)
            arrays = dict(X=X.astype(np.float32), trajs=np.array(T), steps=np.array(S), mask=np.ones((len(T), len(S)), bool))
            cache.save(space, arrays, {"device": dev, "field": field})
            print(f"[{run}] {space}: {X.shape} -> {cache.path(space)}", flush=True)


# ------------------------------------------------------------------ 5. content audit helpers
STOP = None
def stopwords():
    global STOP
    if STOP is None:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        STOP = set(ENGLISH_STOP_WORDS) | {"said", "like", "just", "didn", "don", "ll", "ve", "did", "does", "went", "came", "knew", "felt", "looked", "thought", "wasn", "couldn", "wouldn"}
    return STOP


def name_tokens(text):
    """Capitalised tokens that are not sentence-initial, not honorifics; returned with their counts."""
    out = collections.Counter()
    for m in re.finditer(r"(?<![.!?\"“”]\s)(?<![.!?\"“”])(?<!^)(?<!\n)\b([A-Z][a-z]{2,})\b", text):
        w = m.group(1)
        if w in HONORIFIC: continue
        out[w] += 1
    return out


def build_name_filter(all_texts):
    """A capitalised token is a name if its lower-case form is rare in the corpus relative to its capitalised, non-initial form."""
    cap = collections.Counter(); low = collections.Counter()
    for t in all_texts:
        cap.update(name_tokens(t)); low.update(re.findall(r"\b[a-z][a-z]{2,}\b", t))
    return {w for w, c in cap.items() if c >= 3 and low.get(w.lower(), 0) < 0.2 * c}


def audit_story(text, names_ok):
    w = audit_words(text); ws = collections.Counter(w); lw = text.lower()
    nt = {k: v for k, v in name_tokens(text).items() if k in names_ok}
    lead = max(nt, key=nt.get) if nt else None
    he = ws["he"] + ws["him"] + ws["his"]; she = ws["she"] + ws["her"] + ws["hers"]
    return dict(n_words=len(w), named=bool(nt), n_names=len(nt), lead=lead,
                lead_gender=("female" if she > he else "male" if he > she else "tie") if (he or she) else "none",
                male=sum(ws[x] for x in MALE), female=sum(ws[x] for x in FEMALE),
                elderly=bool(set(w) & ELDERLY) or any(p in lw for p in ELDERLY_PHRASES),
                content=[x for x in w if x not in stopwords() and len(x) > 2])


def content_audit(run, recs, T, S):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import textstat
    sia = SentimentIntensityAnalyzer()
    names_ok = build_name_filter([recs[(t, s)]["story"] for t in T for s in S])
    rows = {}
    for (t, s), r in recs.items():
        st = r["story"]; cj = is_cjk(st)
        a = audit_story(st, names_ok); a["cjk"] = cj
        a["vader"] = None if cj else sia.polarity_scores(st)["compound"]
        a["fk"] = None if cj else textstat.flesch_kincaid_grade(st)
        a["summary_words"] = r.get("summary_words"); a["summary_cjk"] = is_cjk(r["summary"]) if r.get("summary") else None
        rows[(t, s)] = a
    out = {"windows": {}, "n_cjk_stories": int(sum(a["cjk"] for a in rows.values()))}
    for lo, hi in WINDOWS:
        sub = [rows[(t, s)] for t in T for s in S if lo <= s <= hi]; eng = [a for a in sub if not a["cjk"]]
        pooled = collections.Counter(x for a in eng for x in a["content"]); top = {w for w, _ in pooled.most_common(50)}
        jac = []
        for t in T:
            c = collections.Counter(x for s in S if lo <= s <= hi and not rows[(t, s)]["cjk"] for x in rows[(t, s)]["content"])
            if c:
                mine = {w for w, _ in c.most_common(50)}; jac.append(len(mine & top) / len(mine | top))
        leads = collections.Counter(a["lead"] for a in eng if a["lead"]); genders = collections.Counter(a["lead_gender"] for a in eng)
        out["windows"][f"{lo}-{hi}"] = dict(
            n=len(sub), n_english=len(eng), words_median=float(np.median([a["n_words"] for a in eng])) if eng else None,
            named_share=float(np.mean([a["named"] for a in eng])) if eng else None,
            lead_female=genders["female"], lead_male=genders["male"], male_words=int(sum(a["male"] for a in eng)), female_words=int(sum(a["female"] for a in eng)),
            elderly_share=float(np.mean([a["elderly"] for a in eng])) if eng else None,
            vader_mean=float(np.mean([a["vader"] for a in eng])) if eng else None, fk_median=float(np.median([a["fk"] for a in eng])) if eng else None,
            jaccard_top50_median=float(np.median(jac)) if jac else None, top_content=[w for w, _ in pooled.most_common(15)],
            top_leads=leads.most_common(10))
    # name census, steps 50-99
    leads = collections.Counter(rows[(t, s)]["lead"] for t in T for s in S if s >= 50 and rows[(t, s)]["lead"])
    top10 = leads.most_common(10)
    out["names_50_99"] = dict(n_leads=sum(leads.values()), distinct=len(leads), top10=top10,
                              top10_cover=sum(c for _, c in top10) / max(1, sum(leads.values())), llm_set_hits=sorted({n for n, _ in top10} & LLM_NAMES))
    # seed names: name-like tokens in the seed prompt still present at step 10
    seed_names = {t: {k for k in name_tokens(recs[(t, 0)]["seed_prompt"]) if k in names_ok} for t in T}
    with_names = [t for t in T if seed_names[t]]
    out["seed_names"] = dict(trajectories_with_seed_names=len(with_names), gone_by_10=sum(1 for t in with_names if not (seed_names[t] & set(name_tokens(recs[(t, 10)]["story"])))))
    # compliance
    summ = [rows[(t, s)]["summary_words"] for t in T for s in S if rows[(t, s)]["summary_words"] is not None]
    out["compliance"] = dict(summaries=len(summ), summary_le50_share=float(np.mean([x <= 50 for x in summ])) if summ else None,
                             story_lt400_share=float(np.mean([rows[(t, s)]["n_words"] < 400 for t in T for s in S if s >= 1 and not rows[(t, s)]["cjk"]])),
                             length_ratio_step99_median=float(np.median([recs[(t, 99)]["length_ratio"] for t in T if not rows[(t, 99)]["cjk"]])) if 99 in S else None)
    fl = collections.Counter()
    for r in recs.values():
        for k, v in (r["story_meta"].get("flags") or {}).items():
            if v: fl["story_" + k] += 1
        for k, v in ((r.get("summary_meta") or {}).get("flags") or {}).items():
            if v: fl["summary_" + k] += 1
    out["flags"] = dict(fl)
    out["exact_copies"] = int(sum(1 for t in T for s in S[1:] if recs[(t, s)]["story"] == recs[(t, s - 1)]["story"]))
    return out, rows


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-embed", action="store_true"); ap.add_argument("--k", type=int, default=40)
    ap.add_argument("--radius", type=float, default=0.15); ap.add_argument("--exit_factor", type=float, default=1.25); ap.add_argument("--min_dwell", type=int, default=5)
    ap.add_argument("--min_visits", type=int, default=3); ap.add_argument("--seed", type=int, default=0); a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    runs = [c[0] for c in CELLS]
    if not a.no_embed: embed_all(runs, dev)
    out_dir = ROOT / "reports" / "e3"; out_dir.mkdir(parents=True, exist_ok=True)
    R = {"cells": {}, "params": dict(k=a.k, radius=a.radius, exit_factor=a.exit_factor, min_dwell=a.min_dwell, min_visits=a.min_visits, device=dev, packages=package_versions())}
    recs_all = {run: load_records(run) for run in runs}

    # ---- 2. per-cell curves
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8)); series_all = {}
    for i, (run, model, loop) in enumerate(CELLS):
        cache = Cache(run); ser = series_matrix(cache, "minilm"); series_all[run] = ser
        step_d, cum_d, mean_step, mean_cum, L = drift_curves(ser)
        d = cache.arrays("minilm"); X = d["X"].astype(np.float64)
        ident, excess = memory_curve(X); Tn = X.shape[0]
        half = next((k for k in range(len(ident)) if ident[k] <= 0.5), None)
        lost = next((k for k in range(len(ident)) if (ident[k:] <= 2 / Tn).all()), None)
        _, X99, _ = final_step_matrix(cache, "minilm", ROOT / "runs" / run, step=99)
        _, X1, _ = final_step_matrix(cache, "minilm", ROOT / "runs" / run, step=1)
        recs, T, S = recs_all[run]
        lens = np.array([[recs[(t, s)]["story_words"] for s in S] for t in T], float)
        cjk = np.array([[is_cjk(recs[(t, s)]["story"]) for s in S] for t in T]); lens[cjk] = np.nan
        c = R["cells"][run] = dict(model=model, loop=loop, n_traj=len(T), n_steps=len(S),
                                   plateau_step=plateau_step(mean_step), mean_step_drift_last20=float(mean_step[-20:].mean()), mean_step_drift_first5=float(mean_step[:5].mean()),
                                   cum_dist_step99_median=float(np.median([cum_d[t][-1] for t in cum_d])), cum_dist_curve_mean=mean_cum.tolist(),
                                   step_drift_curve_mean=mean_step.tolist(), vendi_step99=vendi(X99), vendi_step1=vendi(X1),
                                   memory=dict(half_life=half, lost_at=lost, ident_at={k: round(float(ident[k]), 2) for k in (1, 2, 3, 5, 10, 20, 50, 99)}, excess_at={k: round(float(excess[k]), 3) for k in (5, 20, 99)}),
                                   words_median_by_step=np.nanmedian(lens, 0).tolist())
        col = SERIES[i % len(SERIES)]; ls = "-" if loop == "E3-1" else "--"; lab = f"{model} {loop}"
        axes[0, 0].plot(range(2, 2 + L), mean_step, ls, color=col, label=lab, lw=1.5); axes[0, 1].plot(range(2, 2 + L), mean_cum, ls, color=col, label=lab, lw=1.5)
        axes[1, 0].plot(ident, ls, color=col, label=lab, lw=1.5); axes[1, 1].plot(np.nanmedian(lens, 0), ls, color=col, label=lab, lw=1.5)
    for ax, t, yl in zip(axes.flat, ("mean step-to-step drift (MiniLM cosine)", "mean distance from the step-1 story", "own seed story identified (memory curve)", "median story length (words; CJK stories excluded)"),
                         ("distance", "distance", "share of trajectories", "words")):
        ax.set_title(t, fontsize=10); ax.set_xlabel("step"); ax.set_ylabel(yl); ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=7, ncol=2)
    axes[1, 0].axhline(0.5, color="gray", lw=0.8, ls=":"); fig.tight_layout(); fig.savefig(out_dir / "curves.png", dpi=130); plt.close(fig)

    # ---- 3. joint persistent atlas
    E = {run: unit(np.stack([series_all[run][t] for t in sorted(series_all[run])]).astype(np.float32)) for run in runs}
    trajs = {run: sorted(series_all[run]) for run in runs}
    pooled = np.concatenate([E[r].reshape(-1, E[r].shape[-1]) for r in runs])
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=a.k, n_init=3, random_state=a.seed).fit(pooled); C = unit(km.cluster_centers_.astype(np.float32))
    np.savez(ROOT / "archive" / "e3_persistent_atlas_centroids.npz", C=C)
    stats, examples, labels = {}, {}, {}
    for run in runs:
        X = E[run]; T, S, _ = X.shape
        D = 1.0 - np.einsum("kd,tsd->kts", C, X); L = label_steps(D, np.full(a.k, a.radius), a.exit_factor); labels[run] = L
        for k in range(a.k):
            inside = L == k; steps_in = int(inside.sum()); exits = int((inside[:, :-1] & ~inside[:, 1:]).sum()); dwells, ex, cens = [], [], []
            for ti in range(T):
                pos = 0
                for length, censored in visits(inside[ti]):
                    while pos < S and not inside[ti, pos]: pos += 1
                    start = pos; pos += length
                    if length >= a.min_dwell:
                        (cens if censored else dwells).append(length); ex.append((trajs[run][ti], start + 1 + length // 2, length, bool(censored)))
            alld = dwells + cens
            stats[(run, k)] = dict(persistent_visits=len(alld), trajectories=len({e[0] for e in ex}), steps_inside=steps_in, exits=exits,
                                   hazard=(exits / steps_in) if steps_in else None, mean_dwell=float(np.mean(alld)) if alld else None, median_dwell=float(np.median(alld)) if alld else None,
                                   km_median_residence=km_median(dwells, cens) if alld else None, longest_dwell=int(max(alld)) if alld else 0, endpoints=int(inside[:, -1].sum()), share_of_steps=steps_in / (T * S))
            examples[(run, k)] = sorted(ex, key=lambda e: -e[2])
    clusters = []
    for k in range(a.k):
        tot = sum(stats[(r, k)]["persistent_visits"] for r in runs)
        if tot == 0: continue
        present = {r: stats[(r, k)]["persistent_visits"] >= a.min_visits for r in runs}
        pm = {m for (r, m, l) in CELLS if present[r]}; pl = {l for (r, m, l) in CELLS if present[r]}; n = sum(present.values())
        attr = ("none" if n == 0 else "universal" if n == len(runs) else f"model: {pm.pop()}" if len(pm) == 1 and n == 2 else f"cell: {[r for r in runs if present[r]][0]}" if n == 1 else f"loop: {pl.pop()}" if len(pl) == 1 and n >= 2 else "mixed")
        clusters.append(dict(cluster=k, total_persistent_visits=tot, attribution=attr, present=present, per_cell={r: stats[(r, k)] for r in runs}))
    clusters.sort(key=lambda c: -c["total_persistent_visits"])
    for run in runs:
        pres = [cl for cl in clusters if cl["present"][run]]; T, S, _ = E[run].shape
        hz = [cl["per_cell"][run]["hazard"] for cl in pres if cl["per_cell"][run]["hazard"] is not None]
        dw = [d for cl in pres for d in [cl["per_cell"][run]["median_dwell"]] if d]
        inside_any = np.zeros((T, S), bool)
        for cl in pres: inside_any |= labels[run] == cl["cluster"]
        R["cells"][run]["atlas"] = dict(n_persistent_attractors=len(pres), share_steps_inside=float(inside_any.mean()), share_endpoints_inside=float(inside_any[:, -1].mean()),
                                        median_hazard=float(np.median(hz)) if hz else None, median_dwell=float(np.median(dw)) if dw else None,
                                        visits_per_trajectory=sum(cl["per_cell"][run]["persistent_visits"] for cl in pres) / T, clusters=[cl["cluster"] for cl in pres])
    # text contact sheets
    for cl in clusters:
        md = [f"# E3 persistent attractor {cl['cluster']} ({cl['attribution']}; {cl['total_persistent_visits']} persistent visits)", ""]
        for run in runs:
            st = cl["per_cell"][run]; md.append(f"## {run}: visits {st['persistent_visits']}, trajectories {st['trajectories']}, steps inside {st['steps_inside']}, hazard {st['hazard'] if st['hazard'] is None else round(st['hazard'], 3)}, endpoints {st['endpoints']}")
            recs = recs_all[run][0]
            for (t, s, length, cens) in examples[(run, cl["cluster"])][:4]:
                md.append(f"- traj {t} step {s} (dwell {length}{', still there at 99' if cens else ''}): {recs[(t, s)]['story'][:420].replace(chr(10), ' ')} …")
            md.append("")
        (out_dir / f"cluster_{cl['cluster']:02d}.md").write_text("\n".join(md), encoding="utf-8")
    R["atlas"] = dict(clusters=clusters, n_clusters_with_visits=len(clusters))

    # ---- 4. overlap E3-2 vs E3-1 within a model; across models; A0-S caption attractors
    ov = {}
    for model in ("sonnet", "qwen", "llava"):
        r1, r2 = f"e3_1_{model}", f"e3_2_{model}"
        p1 = set(R["cells"][r1]["atlas"]["clusters"]); p2 = set(R["cells"][r2]["atlas"]["clusters"])
        others = set().union(*[set(R["cells"][f"e3_1_{m}"]["atlas"]["clusters"]) | set(R["cells"][f"e3_2_{m}"]["atlas"]["clusters"]) for m in ("sonnet", "qwen", "llava") if m != model])
        ov[model] = dict(e3_1=sorted(p1), e3_2=sorted(p2), shared=sorted(p1 & p2), share_of_e3_2_in_e3_1=(len(p1 & p2) / len(p2)) if p2 else None,
                         share_of_model_clusters_in_other_models=(len((p1 | p2) & others) / len(p1 | p2)) if (p1 | p2) else None)
        # literal reading: per-cell k-means (k 12) centroids of clusters with >= min_visits persistent visits, nearest-centroid distance
        cents = {}
        for r in (r1, r2):
            X = E[r]; T, S, _ = X.shape; kmc = KMeans(n_clusters=12, n_init=3, random_state=a.seed).fit(X.reshape(-1, X.shape[-1])); Cc = unit(kmc.cluster_centers_.astype(np.float32))
            D = 1.0 - np.einsum("kd,tsd->kts", Cc, X); L = label_steps(D, np.full(12, a.radius), a.exit_factor); keep = []
            for k in range(12):
                nv = sum(1 for ti in range(T) for length, _ in visits(L[ti] == k) if length >= a.min_dwell)
                if nv >= a.min_visits: keep.append(Cc[k])
            cents[r] = np.stack(keep) if keep else np.zeros((0, X.shape[-1]), np.float32)
        if len(cents[r1]) and len(cents[r2]):
            dmin = (1 - cents[r2] @ cents[r1].T).min(1); ov[model]["own_centroids"] = dict(n_e3_1=len(cents[r1]), n_e3_2=len(cents[r2]), share_e3_2_within_radius_of_e3_1=float((dmin <= a.radius).mean()), min_dists=[round(float(x), 3) for x in dmin])
        else: ov[model]["own_centroids"] = dict(n_e3_1=len(cents[r1]), n_e3_2=len(cents[r2]))
    R["overlap"] = ov
    z = np.load(ROOT / "archive" / "persistent_atlas_minilm_s_names_centroids.npz", allow_pickle=True); CA = unit(z["C"].astype(np.float32)); names_a = list(z["names"])
    a0s = {}
    for run in runs:
        X = E[run]; T, S, _ = X.shape; D = 1.0 - np.einsum("kd,tsd->kts", CA, X); L = label_steps(D, np.full(len(CA), a.radius), a.exit_factor)
        per = {}
        for k, nm in A0S_NAMED.items():
            inside = L == k; nv = sum(1 for ti in range(T) for length, _ in visits(inside[ti]) if length >= a.min_dwell)
            per[nm] = dict(steps_inside=int(inside.sum()), persistent_visits=nv, min_distance=float(D[k].min()))
        a0s[run] = dict(named=per, steps_inside_any_a0s_named=int(np.isin(L, list(A0S_NAMED)).sum()), steps_inside_any_a0s_cluster=int((L >= 0).sum()))
    R["a0s_caption_attractors"] = a0s

    # ---- 5. content audit
    for run in runs:
        recs, T, S = recs_all[run]; aud, _ = content_audit(run, recs, T, S); R["cells"][run]["audit"] = aud
        R["cells"][run]["summary_vendi_step99"] = None
        if (Cache(run).dir / "minilm_summary.npz").exists():
            _, Xs, _ = final_step_matrix(Cache(run), "minilm_summary", ROOT / "runs" / run, step=99); R["cells"][run]["summary_vendi_step99"] = vendi(Xs)

    c = R["cells"]

    # ---- 5b. scale controls (the atlas found no shared attractor; is that the space, the n, or the loop?)
    def unitX(run, space="minilm"):
        d = Cache(run).arrays(space); X = d["X"].astype(np.float64); return X / np.linalg.norm(X, axis=-1, keepdims=True)
    def nn_other(X, s0=25):
        T, S, _ = X.shape; Y = X[:, s0:]; out = []
        for t in range(T):
            others = np.delete(Y, t, 0).reshape(-1, Y.shape[-1]); out.append((1 - Y[t] @ others.T).min(1))
        return np.concatenate(out)
    def self_share(X, s0=50, r=0.15):
        Y = X[:, s0:]; cc = Y.mean(1); cc /= np.linalg.norm(cc, axis=-1, keepdims=True); return float((1 - np.einsum("tsd,td->ts", Y, cc) <= r).mean())
    def cons_med(X):
        return float(np.median(1 - np.einsum("tsd,tsd->ts", X[:, 2:], X[:, 1:-1])))
    rng = np.random.default_rng(a.seed); ctrl = {"note": "nearest other-trajectory distance = for every trajectory-step (steps >= 25) the cosine distance to the nearest step of any other trajectory in the same cell; caption cells subsampled to 20 trajectories 20 times to match n", "cells": {}}
    for run in runs + ["a0_s", "e1_cap", "a0_core"]:
        if not (Cache(run).dir / "minilm.npz").exists(): continue
        X = unitX(run); T = X.shape[0]; e = dict(n_traj=T, consecutive_median=cons_med(X), self_centroid_share_50_99=self_share(X))
        if T > 20:
            meds, shares, halves = [], [], []
            for _ in range(20):
                idx = rng.choice(T, 20, replace=False); v = nn_other(X[idx]); meds.append(np.median(v)); shares.append((v <= a.radius).mean())
                ident, _ = memory_curve(X[idx]); halves.append(next((k for k in range(len(ident)) if ident[k] <= 0.5), 99))
            e.update(nn_other_median_sub20=float(np.mean(meds)), nn_other_share_le_radius_sub20=float(np.mean(shares)), half_life_sub20_median=float(np.median(halves)), half_life_sub20_range=[int(min(halves)), int(max(halves))],
                     nn_other_median_full=float(np.median(nn_other(X))), nn_other_share_le_radius_full=float((nn_other(X) <= a.radius).mean()))
        else:
            v = nn_other(X); e.update(nn_other_median=float(np.median(v)), nn_other_p5=float(np.percentile(v, 5)), nn_other_min=float(v.min()), nn_other_share_le_radius=float((v <= a.radius).mean()))
        if (Cache(run).dir / "minilm_summary.npz").exists():
            Xs = unitX(run, "minilm_summary"); v = nn_other(Xs); ident, _ = memory_curve(Xs)
            e["summary_space"] = dict(nn_other_median=float(np.median(v)), nn_other_min=float(v.min()), nn_other_share_le_radius=float((v <= a.radius).mean()), self_centroid_share_50_99=self_share(Xs),
                                      consecutive_median=cons_med(Xs), half_life=next((k for k in range(len(ident)) if ident[k] <= 0.5), None), vendi_step99=c[run]["summary_vendi_step99"] if run in c else None)
        ctrl["cells"][run] = e
    R["scale_controls"] = ctrl

    # ---- 6. verdict numbers
    V = {}
    refs = dict(caption_median_hazard=dict(a0_s=0.187, e1_cap=0.193), caption_share_inside=dict(a0_core=0.46, a0_s=0.29, e1_cap=0.25))
    c = R["cells"]
    V["p1"] = {run: dict(plateau_le_25=(c[run]["plateau_step"] is not None and c[run]["plateau_step"] <= 25), plateau=c[run]["plateau_step"], half_life=c[run]["memory"]["half_life"],
                         half_life_3_5=c[run]["memory"]["half_life"] is not None and 3 <= c[run]["memory"]["half_life"] <= 5,
                         share_inside=c[run]["atlas"]["share_steps_inside"], share_30_50=0.30 <= c[run]["atlas"]["share_steps_inside"] <= 0.50,
                         n_attractors=c[run]["atlas"]["n_persistent_attractors"], ge_3=c[run]["atlas"]["n_persistent_attractors"] >= 3, median_hazard=c[run]["atlas"]["median_hazard"])
               for run in runs if c[run]["loop"] == "E3-1"}
    V["p1"]["sonnet_hazard_below_a0s"] = (c["e3_1_sonnet"]["atlas"]["median_hazard"] or 9) < refs["caption_median_hazard"]["a0_s"]
    V["p1"]["qwen_hazard_below_e1cap"] = (c["e3_1_qwen"]["atlas"]["median_hazard"] or 9) < refs["caption_median_hazard"]["e1_cap"]
    V["p2"] = {}
    for m in ("sonnet", "qwen", "llava"):
        h1, h2 = c[f"e3_1_{m}"]["memory"]["half_life"], c[f"e3_2_{m}"]["memory"]["half_life"]
        ratio = (h2 or 100) / (h1 or 1) if h1 else None
        V["p2"][m] = dict(half_life_e3_1=h1, half_life_e3_2=h2, ratio=ratio, ratio_ge_2=(ratio is not None and ratio >= 2), e3_2_half_ge_8=(h2 is None or h2 >= 8),
                          share_inside_e3_1=c[f"e3_1_{m}"]["atlas"]["share_steps_inside"], share_inside_e3_2=c[f"e3_2_{m}"]["atlas"]["share_steps_inside"],
                          share_at_most_half=c[f"e3_2_{m}"]["atlas"]["share_steps_inside"] <= 0.5 * c[f"e3_1_{m}"]["atlas"]["share_steps_inside"],
                          cum99_e3_1=c[f"e3_1_{m}"]["cum_dist_step99_median"], cum99_e3_2=c[f"e3_2_{m}"]["cum_dist_step99_median"], cum99_lower=c[f"e3_2_{m}"]["cum_dist_step99_median"] < c[f"e3_1_{m}"]["cum_dist_step99_median"],
                          branch=(None if ratio is None else "bottleneck (>= 1.5)" if ratio >= 1.5 else "two-attractor alternate (<= 0.67)" if ratio <= 0.67 else "model defaults alone (0.67-1.5)"))
    V["p3"] = {}
    for m in ("sonnet", "qwen", "llava"):
        w = c[f"e3_2_{m}"]["audit"]["windows"]; j1, j9 = w["1-10"]["jaccard_top50_median"], w["90-99"]["jaccard_top50_median"]
        V["p3"][m] = dict(jaccard_1_10=j1, jaccard_90_99=j9, doubled=(j1 is not None and j9 is not None and j9 >= 2 * j1), length_ratio_99=c[f"e3_2_{m}"]["audit"]["compliance"]["length_ratio_step99_median"],
                          words_median_1_10=w["1-10"]["words_median"], words_median_90_99=w["90-99"]["words_median"])
    V["p4"] = {m: dict(joint_share=ov[m]["share_of_e3_2_in_e3_1"], own_centroid_share=ov[m]["own_centroids"].get("share_e3_2_within_radius_of_e3_1"), cross_model_share=ov[m]["share_of_model_clusters_in_other_models"]) for m in ov}
    V["p5"] = {run: dict(a0s_named_with_persistent_visit=sum(1 for v in a0s[run]["named"].values() if v["persistent_visits"] >= a.min_visits), steps_inside_named=a0s[run]["steps_inside_any_a0s_named"]) for run in runs}
    V["p6"] = {}
    for run in runs:
        w = c[run]["audit"]["windows"]
        V["p6"][run] = dict(named_90_99=w["90-99"]["named_share"], lead_female_90_99=w["90-99"]["lead_female"], lead_male_90_99=w["90-99"]["lead_male"],
                            vader_1_10=w["1-10"]["vader_mean"], vader_90_99=w["90-99"]["vader_mean"], vader_up=(w["90-99"]["vader_mean"] or 0) > (w["1-10"]["vader_mean"] or 0),
                            fk_by_window={k: v["fk_median"] for k, v in w.items()}, elderly_1_10=w["1-10"]["elderly_share"], elderly_90_99=w["90-99"]["elderly_share"],
                            elderly_doubled=(w["90-99"]["elderly_share"] or 0) >= 2 * (w["1-10"]["elderly_share"] or 0) and (w["90-99"]["elderly_share"] or 0) > 0)
    V["p7"] = {run: dict(summary_le50=c[run]["audit"]["compliance"]["summary_le50_share"], story_lt400=c[run]["audit"]["compliance"]["story_lt400_share"]) for run in runs if c[run]["loop"] == "E3-1"}
    V["p8"] = dict(sonnet_half=c["e3_1_sonnet"]["memory"]["half_life"], qwen_half=c["e3_1_qwen"]["memory"]["half_life"],
                   flag=(c["e3_1_sonnet"]["memory"]["half_life"] or 0) < 0.5 * (c["e3_1_qwen"]["memory"]["half_life"] or 0))
    V["p9"] = {run: dict(**c[run]["audit"]["names_50_99"], seed_names=c[run]["audit"]["seed_names"]) for run in runs}
    s10 = {n for n, _ in c["e3_1_sonnet"]["audit"]["names_50_99"]["top10"]}; q10 = {n for n, _ in c["e3_1_qwen"]["audit"]["names_50_99"]["top10"]}
    V["p9"]["qwen_vs_sonnet_top10_differ"] = len(q10 - s10)
    R["verdict_numbers"] = V
    (ROOT / "reports" / "e3.json").write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")

    # ---- markdown tables
    md = ["## Per-cell metrics (MiniLM on the stories)", "", "| cell | plateau step | step drift first 5 / last 20 | dist. from step 1 at 99 (median) | half-life | ident. 1/2/3/5/10/20/50/99 | Vendi step 1 → 99 | attractors | steps inside | endpoints inside | median hazard | median dwell | visits / traj |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for run in runs:
        x = c[run]; at = x["atlas"]; ia = x["memory"]["ident_at"]
        md.append(f"| {run} | {x['plateau_step']} | {x['mean_step_drift_first5']:.3f} / {x['mean_step_drift_last20']:.3f} | {x['cum_dist_step99_median']:.2f} | {x['memory']['half_life']} | " + "/".join(f"{ia[k]:.2f}" for k in (1, 2, 3, 5, 10, 20, 50, 99)) +
                  f" | {x['vendi_step1']:.1f} → {x['vendi_step99']:.1f} | {at['n_persistent_attractors']} | {at['share_steps_inside']:.2f} | {at['share_endpoints_inside']:.2f} | {at['median_hazard'] if at['median_hazard'] is None else round(at['median_hazard'], 3)} | {at['median_dwell']} | {at['visits_per_trajectory']:.2f} |")
    md += ["", "## Persistent attractors (joint k 40, radius 0.15, dwell >= 5; per cell: visits / trajectories / endpoints / median dwell / hazard)", "", "| cluster | " + " | ".join(runs) + " | attribution |", "|---|" + "---|" * (len(runs) + 1)]
    for cl in clusters[:30]:
        cells_s = []
        for r in runs:
            s = cl["per_cell"][r]; cells_s.append("–" if s["persistent_visits"] == 0 else f"{s['persistent_visits']} / {s['trajectories']} / {s['endpoints']} / {s['median_dwell']:.0f} / {s['hazard']:.2f}")
        md.append(f"| {cl['cluster']} | " + " | ".join(cells_s) + f" | {cl['attribution']} |")
    md += ["", "## Content audit by step window (English stories only; CJK stories counted separately)", ""]
    for run in runs:
        w = c[run]["audit"]["windows"]; md += [f"### {run} (CJK stories {c[run]['audit']['n_cjk_stories']}, exact copies {c[run]['audit']['exact_copies']}, flags {c[run]['audit']['flags']})", "",
                                           "| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for k, v in w.items():
            md.append(f"| {k} | {v['n']} ({v['n_english']}) | {v['words_median']} | {v['named_share'] if v['named_share'] is None else round(v['named_share'], 2)} | {v['lead_female']} : {v['lead_male']} | {v['female_words']} : {v['male_words']} | {v['elderly_share'] if v['elderly_share'] is None else round(v['elderly_share'], 2)} | {v['vader_mean'] if v['vader_mean'] is None else round(v['vader_mean'], 2)} | {v['fk_median'] if v['fk_median'] is None else round(v['fk_median'], 1)} | {v['jaccard_top50_median'] if v['jaccard_top50_median'] is None else round(v['jaccard_top50_median'], 2)} | {', '.join(v['top_content'][:10])} | {', '.join(f'{n} {c_}' for n, c_ in v['top_leads'][:5])} |")
        n = c[run]["audit"]["names_50_99"]; md += ["", f"Names 50–99: {n['n_leads']} leads, {n['distinct']} distinct; top 10 cover {n['top10_cover']:.2f}: {', '.join(f'{a_} {b}' for a_, b in n['top10'])}; LLM-set hits {n['llm_set_hits']}; seed names {c[run]['audit']['seed_names']}; compliance {c[run]['audit']['compliance']}", ""]
    md += ["", "## Scale controls (MiniLM; radius 0.15)", "", "| cell | n | consecutive median | self-centroid share 50-99 | nearest other-trajectory: median / share <= 0.15 | summary space: nn-other median / share / self-centroid / half-life |", "|---|---|---|---|---|---|"]
    for run, e in ctrl["cells"].items():
        nn = f"{e['nn_other_median']:.3f} / {e['nn_other_share_le_radius']:.3f} (min {e['nn_other_min']:.2f})" if "nn_other_median" in e else f"{e['nn_other_median_sub20']:.3f} / {e['nn_other_share_le_radius_sub20']:.3f} (20-traj subsamples; full n: {e['nn_other_median_full']:.3f} / {e['nn_other_share_le_radius_full']:.3f}; half-life sub20 median {e['half_life_sub20_median']:.0f}, range {e['half_life_sub20_range']})"
        ss = e.get("summary_space"); ss_s = "–" if not ss else f"{ss['nn_other_median']:.3f} / {ss['nn_other_share_le_radius']:.3f} / {ss['self_centroid_share_50_99']:.2f} / {ss['half_life']}"
        md.append(f"| {run} | {e['n_traj']} | {e['consecutive_median']:.3f} | {e['self_centroid_share_50_99']:.2f} | {nn} | {ss_s} |")
    md += ["", "## Verdict numbers", "", "```", json.dumps(V, indent=1, default=float), "```"]
    (out_dir / "tables.md").write_text("\n".join(md), encoding="utf-8"); print("\n".join(md))


if __name__ == "__main__":
    main()
