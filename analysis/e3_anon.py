"""E3-A: anonymised re-embedding control (predictions.md "E3 follow-ups", A1). Are names and places what keep the text
trajectories apart in MiniLM space? Every name-like token (the gate's filter from e3_report: capitalised, non-initial, with a
rare lower-case form, built per cell over its stories) is replaced by the neutral token "X" in every story and every E3-1
summary; the texts are re-embedded with the pinned MiniLM and the gate's scale controls and persistent atlas are recomputed on
the original and the anonymised embeddings under one procedure, so the two columns differ only in the text.

    .venv/bin/python analysis/e3_anon.py [--runs e3_1_sonnet ...] [--k 40] [--radius 0.15] [--exit_factor 1.25] [--min_dwell 5] [--min_visits 3]

Writes analysis/cache/<run>/minilm_anon.npz and minilm_summary_anon.npz, reports/e3/anon.md and reports/e3/anon.json.
CLIP is not used (CLAUDE.md rule 4).
"""
import argparse, json, pathlib, re, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, MODELS, Cache, cpu_only, vendi, package_versions  # noqa: E402
from gravity import label_steps, visits  # noqa: E402
from e3_report import CELLS, load_records, build_name_filter, unit, is_cjk  # noqa: E402

for sp in ("minilm_anon", "minilm_summary_anon"):
    MODELS[sp] = dict(MODELS["minilm"], pooling=MODELS["minilm"]["pooling"] + "; names and places replaced by 'X' (e3_anon.py)")
for sp in ("minilm_rand", "minilm_summary_rand"):
    MODELS[sp] = dict(MODELS["minilm"], pooling=MODELS["minilm"]["pooling"] + "; null: the same number of random non-name content words replaced by 'X' (e3_anon.py)")
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]+")


def random_replace(text, n, names, rng, stop):
    """Null for anonymise(): replace n random alphabetic words that are neither names nor stopwords by 'X' (same token budget, no name removed)."""
    if n <= 0: return text
    spans = [m.span() for m in WORD.finditer(text) if m.group(0) not in names and m.group(0).lower() not in stop and len(m.group(0)) > 2]
    if not spans: return text
    pick = sorted(rng.choice(len(spans), size=min(n, len(spans)), replace=False), reverse=True)
    for i in pick:
        a, b = spans[i]; text = text[:a] + "X" + text[b:]
    return text


def anonymise(text, names):
    if not names: return text
    pat = re.compile(r"\b(" + "|".join(sorted(map(re.escape, names), key=len, reverse=True)) + r")(?:'s)?\b")
    return pat.sub("X", text)


def nn_other(X, s0=25):
    T, S, _ = X.shape; Y = X[:, s0:]; out = []
    for t in range(T):
        others = np.delete(Y, t, 0).reshape(-1, Y.shape[-1]); out.append((1 - Y[t] @ others.T).min(1))
    return np.concatenate(out)


def atlas_counts(E, k, radius, exit_factor, min_dwell, min_visits, seed=0):
    """Joint k-means over the cells in E ({run: unit [T,S,d] for steps 1..}); per cell, the clusters with >= min_visits
    persistent visits and how many of them are shared by >= 2 trajectories; plus the share of steps inside any such cluster."""
    from sklearn.cluster import KMeans
    runs = list(E); pooled = np.concatenate([E[r].reshape(-1, E[r].shape[-1]) for r in runs])
    C = unit(KMeans(n_clusters=k, n_init=3, random_state=seed).fit(pooled).cluster_centers_.astype(np.float32))
    out = {}
    for r in runs:
        X = E[r]; T, S, _ = X.shape; D = 1.0 - np.einsum("kd,tsd->kts", C, X); L = label_steps(D, np.full(k, radius), exit_factor)
        pers, shared, inside_any = 0, 0, np.zeros((T, S), bool)
        for c in range(k):
            inside = L == c; nv, trajs = 0, set()
            for ti in range(T):
                for length, _ in visits(inside[ti]):
                    if length >= min_dwell: nv += 1; trajs.add(ti)
            if nv >= min_visits:
                pers += 1; inside_any |= inside
                if len(trajs) >= 2: shared += 1
        out[r] = dict(persistent=pers, shared_by_2plus_traj=shared, share_steps_inside=float(inside_any.mean()))
    return out


def shared_sheet(E, recs, field, a, label):
    """Markdown: for the joint atlas on anonymised embeddings, every cluster with >= min_visits persistent visits from >= 2 trajectories in any cell, with the original texts of its longest dwells."""
    from sklearn.cluster import KMeans
    runs = list(E); pooled = np.concatenate([E[r].reshape(-1, E[r].shape[-1]) for r in runs])
    C = unit(KMeans(n_clusters=a.k, n_init=3, random_state=0).fit(pooled).cluster_centers_.astype(np.float32))
    md = [f"## {label}: clusters shared by >= 2 trajectories after anonymising", ""]
    for r in runs:
        X = E[r]; T, S, _ = X.shape; D = 1.0 - np.einsum("kd,tsd->kts", C, X); L = label_steps(D, np.full(a.k, a.radius), a.exit_factor)
        trajs = sorted({k[0] for k in recs[r]})
        for c in range(a.k):
            inside = L == c; ex = []
            for ti in range(T):
                pos = 0
                for length, cens in visits(inside[ti]):
                    while pos < S and not inside[ti, pos]: pos += 1
                    start = pos; pos += length
                    if length >= a.min_dwell: ex.append((trajs[ti], start + 1 + length // 2, length))
            if len(ex) >= a.min_visits and len({e[0] for e in ex}) >= 2:
                md.append(f"### {r} cluster {c}: {len(ex)} persistent visits from {len({e[0] for e in ex})} trajectories")
                for t, s_, length in sorted(ex, key=lambda e: -e[2])[:5]:
                    md.append(f"- traj {t} step {s_} (dwell {length}): {recs[r][(t, s_)][field][:300].replace(chr(10), ' ')} …")
                md.append("")
    return "\n".join(md)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", nargs="*"); ap.add_argument("--k", type=int, default=40); ap.add_argument("--radius", type=float, default=0.15)
    ap.add_argument("--exit_factor", type=float, default=1.25); ap.add_argument("--min_dwell", type=int, default=5); ap.add_argument("--min_visits", type=int, default=3)
    ap.add_argument("--no-embed", action="store_true"); a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    runs = a.runs or [c[0] for c in CELLS]
    from sentence_transformers import SentenceTransformer
    m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev) if not a.no_embed else None
    stats = {}
    for run in runs:
        recs, T, S = load_records(run); cache = Cache(run)
        names = build_name_filter([recs[(t, s)]["story"] for t in T for s in S])
        n_tok = {"story": 0, "summary": 0}; n_words = {"story": 0, "summary": 0}
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as STOP
        rng = np.random.default_rng(0)
        for space, field in (("minilm_anon", "story"), ("minilm_summary_anon", "summary")):
            if recs[(T[0], S[0])].get(field) is None: continue
            texts = [recs[(t, s)][field] or "" for t in T for s in S]
            anon = [anonymise(x, names) for x in texts]
            per = [x.count("X") - y.count("X") for x, y in zip(anon, texts)]
            rand = [random_replace(y, n, names, rng, STOP) for y, n in zip(texts, per)]
            n_tok[field] = sum(per); n_words[field] = sum(len(x.split()) for x in texts)
            if not a.no_embed:
                for sp, txts, note in ((space, anon, "names replaced"), (space.replace("_anon", "_rand"), rand, "random words replaced (null)")):
                    X = model.encode(txts, normalize_embeddings=True, batch_size=64, show_progress_bar=False).reshape(len(T), len(S), -1)
                    cache.save(sp, dict(X=X.astype(np.float32), trajs=np.array(T), steps=np.array(S), mask=np.ones((len(T), len(S)), bool)),
                               {"device": dev, "field": field, "n_names": len(names), "replaced_tokens": n_tok[field]})
                    print(f"[{run}] {sp}: {X.shape}, {n_tok[field]} tokens {note} ({len(names)} distinct names)", flush=True)
        stats[run] = dict(n_names=len(names), replaced=n_tok, words=n_words)
        # CJK trajectories (Qwen code-switching) are left in: the control is about names, and the same steps are in both columns.

    # ---- metrics under one procedure, original vs anonymised
    R = {"params": dict(k=a.k, radius=a.radius, exit_factor=a.exit_factor, min_dwell=a.min_dwell, min_visits=a.min_visits, packages=package_versions()), "cells": {}, "names": stats}
    def U(run, space):
        d = Cache(run).arrays(space); return unit(d["X"].astype(np.float64))
    COLS = ("original", "anon", "rand")
    sheets = []
    for label, base in (("stories", "minilm"), ("summaries", "minilm_summary")):
        spaces = {"original": base, "anon": base + "_anon", "rand": base + "_rand"}
        avail = [r for r in runs if all((Cache(r).dir / f"{sp}.npz").exists() for sp in spaces.values())]
        if not avail: continue
        E = {c: {r: U(r, spaces[c])[:, 1:].astype(np.float32) for r in avail} for c in COLS}
        at = {c: atlas_counts(E[c], a.k, a.radius, a.exit_factor, a.min_dwell, a.min_visits) for c in COLS}
        for r in avail:
            X = {c: U(r, spaces[c]) for c in COLS}; nn = {c: nn_other(X[c]) for c in COLS}
            R["cells"].setdefault(r, {})[label] = dict(
                nn_other_median={c: float(np.median(nn[c])) for c in COLS}, nn_other_within_015={c: float((nn[c] <= 0.15).mean()) for c in COLS},
                vendi_step99={c: vendi(X[c][:, -1]) for c in COLS}, consecutive_median={c: float(np.median(1 - np.einsum("tsd,tsd->ts", X[c][:, 2:], X[c][:, 1:-1]))) for c in COLS},
                atlas={c: at[c][r] for c in COLS}, median_shift_from_anonymising=float(np.median(1 - np.einsum("tsd,tsd->ts", X["original"], X["anon"]))),
                median_shift_from_random=float(np.median(1 - np.einsum("tsd,tsd->ts", X["original"], X["rand"]))))
        # contact sheet of the clusters shared by >= 2 trajectories after anonymising (E3-1 cells)
        sheets.append(shared_sheet(E["anon"], {r: load_records(r)[0] for r in avail}, "summary" if label == "summaries" else "story", a, label))
    (ROOT / "reports" / "e3" / "anon_clusters.md").write_text("\n".join(sheets), encoding="utf-8")
    # ---- verdict A1
    drops, shared = [], []
    for r, d in R["cells"].items():
        for label, v in d.items():
            n = v["nn_other_median"]; drops.append((r, label, n["original"] - n["anon"], n["original"] - n["rand"]))
            if r.startswith("e3_1_"): shared.append((r, label, v["atlas"]["anon"]["shared_by_2plus_traj"], v["atlas"]["rand"]["shared_by_2plus_traj"]))
    max_drop = max(x[2] for x in drops); any_shared = any(x[2] > 0 for x in shared)
    R["verdict"] = dict(A1_holds=bool(max_drop < 0.05 and not any_shared), max_drop=max_drop, max_drop_where=[x for x in drops if x[2] == max_drop][0][:2],
                        max_drop_names_beyond_null=max(x[2] - x[3] for x in drops), shared_attractors_e3_1_anon_vs_rand=shared,
                        rule="A1 as written: fall >= 0.10 or any shared attractor in an E3-1 cell -> names were the barrier. The rand column is the null added after the first pass (same token budget, random content words): the names-specific effect is anon minus rand.")
    out = ROOT / "reports" / "e3"; out.mkdir(parents=True, exist_ok=True)
    (out / "anon.json").write_text(json.dumps(R, indent=1, default=float))
    md = ["# E3-A: anonymised re-embedding control", "",
          f"Names and places (the gate's filter, per cell) replaced by \"X\"; MiniLM re-embedding; the same procedure on both columns (joint k-means k {a.k} per text kind, radius {a.radius}, hysteresis {a.exit_factor}, dwell ≥ {a.min_dwell}, ≥ {a.min_visits} visits). "
          "nn-other = median cosine distance from each trajectory-step (steps ≥ 25) to the nearest step of any other trajectory in the cell; within = share of those ≤ 0.15; shared = persistent clusters visited by ≥ 2 trajectories. shift = median distance between a text's original and anonymised embedding.", "",
          "| cell | text | names | tokens replaced | shift anon / rand | nn-other orig → anon / rand | within 0.15 orig → anon / rand | Vendi@99 orig → anon / rand | persistent (shared) orig → anon / rand | steps inside orig → anon / rand |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r, d in R["cells"].items():
        for label, v in d.items():
            at = v["atlas"]; f3 = lambda key, fmt: " / ".join(fmt.format(v[key][c]) for c in ("anon", "rand"))
            md.append(f"| {r} | {label} | {stats[r]['n_names']} | {stats[r]['replaced']['story' if label == 'stories' else 'summary']} | {v['median_shift_from_anonymising']:.3f} / {v['median_shift_from_random']:.3f} | "
                      f"{v['nn_other_median']['original']:.3f} → {f3('nn_other_median', '{:.3f}')} | {v['nn_other_within_015']['original']:.2f} → {f3('nn_other_within_015', '{:.2f}')} | {v['vendi_step99']['original']:.1f} → {f3('vendi_step99', '{:.1f}')} | "
                      f"{at['original']['persistent']} ({at['original']['shared_by_2plus_traj']}) → {at['anon']['persistent']} ({at['anon']['shared_by_2plus_traj']}) / {at['rand']['persistent']} ({at['rand']['shared_by_2plus_traj']}) | "
                      f"{at['original']['share_steps_inside']:.2f} → {at['anon']['share_steps_inside']:.2f} / {at['rand']['share_steps_inside']:.2f} |")
    v = R["verdict"]
    md += ["", f"**A1 ({'holds' if v['A1_holds'] else 'fails'} as written)**: largest fall in nn-other {v['max_drop']:.3f} ({v['max_drop_where'][0]}, {v['max_drop_where'][1]}); largest names-specific fall beyond the random-replacement null {v['max_drop_names_beyond_null']:.3f}. "
           "Shared persistent attractors in E3-1 cells, anonymised / null: " + ", ".join(f"{r} {label} {n} / {m}" for r, label, n, m in v["shared_attractors_e3_1_anon_vs_rand"]) + f". {v['rule']}", "",
           "Shared-cluster texts: `anon_clusters.md`."]
    (out / "anon.md").write_text("\n".join(md) + "\n", encoding="utf-8"); print("\n".join(md))


if __name__ == "__main__":
    main()
