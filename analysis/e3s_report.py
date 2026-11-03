"""E3-S (100-seed scale arm) and E3-W (20-word bottleneck) report against predictions.md "E3 scale and bottleneck width" (2026-11-02).

Primary measure: the pair-sharing rate = share of unordered trajectory pairs that both make a persistent visit (dwell >= 5, radius 0.15,
hysteresis 1.25) to the same persistent cluster (>= 3 persistent visits in all) of the story embeddings; raw and anonymised (E3-A's
name filter, names -> "X"). k scales with the data (k = 40 per 2,000 trajectory-steps: k 200 for the 100-trajectory cell alone);
random 20-trajectory subsamples at k 40 give the sampling distribution the 20-trajectory cells are draws from, and the sharing-pairs-vs-n
curve. Same-seed check: the base cell (e3_1_haiku) and the scale cell share seeds 0-19 with fresh step 0.

Usage: .venv/bin/python analysis/e3s_report.py [--scale e3_1_haiku_100] [--width e3_1w20_haiku] [--base e3_1_haiku] [--no-embed] [--n-sub 50]
Writes reports/e3/scale_width.md, scale_width.json, scale_width.png, sw_cluster_*.md; embeddings cached under analysis/cache/<run>/.
"""
import argparse, collections, itertools, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, MODELS, Cache, cpu_only, vendi, package_versions  # noqa: E402
from gravity import label_steps, visits  # noqa: E402
from memory_curve import curve as memory_curve  # noqa: E402
from e3_report import load_records, embed_all, content_audit, build_name_filter, unit  # noqa: E402
from e3_anon import anonymise, nn_other  # noqa: E402
from e3_theme_report import load_judge  # noqa: E402

OUT = ROOT / "reports" / "e3"
ATLAS = dict(radius=0.15, exit_factor=1.25, min_dwell=5, min_visits=3, k_per_2000=40)


def k_for(n_points):
    return max(10, int(round(ATLAS["k_per_2000"] * n_points / 2000.0)))


def atlas_pairs(X, k, seed=0, trajs=None):
    """X unit [T,S,d] (steps >= 1). k-means on these points; per persistent cluster the set of trajectories with a dwell>=5 visit.
    Returns dict(persistent, shared, pairs (set of (i,j)), rate, max_mult, inside_share, clusters=[(c, trajs, n_visits)])."""
    from sklearn.cluster import KMeans
    T, S, d = X.shape; pooled = X.reshape(-1, d)
    C = unit(KMeans(n_clusters=k, n_init=3, random_state=seed).fit(pooled).cluster_centers_.astype(np.float32))
    D = 1.0 - np.einsum("kd,tsd->kts", C, X); L = label_steps(D, np.full(k, ATLAS["radius"]), ATLAS["exit_factor"])
    ids = list(range(T)) if trajs is None else list(trajs)
    pers, shared, pairs, mult, inside_any, clusters = 0, 0, set(), 0, np.zeros((T, S), bool), []
    for c in range(k):
        inside = L == c; nv, ts = 0, set()
        for ti in range(T):
            for length, _ in visits(inside[ti]):
                if length >= ATLAS["min_dwell"]: nv += 1; ts.add(ids[ti])
        if nv >= ATLAS["min_visits"]:
            pers += 1; inside_any |= inside; clusters.append((c, sorted(ts), nv))
            if len(ts) >= 2:
                shared += 1; mult = max(mult, len(ts))
                pairs |= set(itertools.combinations(sorted(ts), 2))
    n_pairs = T * (T - 1) // 2
    return dict(persistent=pers, shared=shared, pairs=sorted(pairs), n_sharing_pairs=len(pairs), n_pairs=n_pairs, rate=len(pairs) / n_pairs,
                W_hat=(n_pairs / len(pairs)) if pairs else None, max_mult=mult, inside_share=float(inside_any.mean()), clusters=clusters, labels=L)


def anon_embed(run, recs, T, S, model, cache):
    """Anonymised story embeddings (names -> X), cached as minilm_anon (same convention as e3_anon.py)."""
    have = cache.load("minilm_anon")
    if have is not None: return have["X"].astype(np.float64), None
    if model is None: raise SystemExit(f"{run}: no minilm_anon cache; run without --no-embed")
    names = build_name_filter([recs[(t, s)]["story"] for t in T for s in S])
    texts = [anonymise(recs[(t, s)]["story"] or "", names) for t in T for s in S]
    X = model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=False).reshape(len(T), len(S), -1)
    cache.save("minilm_anon", dict(X=X.astype(np.float32), trajs=np.array(T), steps=np.array(S), mask=np.ones((len(T), len(S)), bool)), {"field": "story", "n_names": len(names)})
    print(f"[{run}] minilm_anon: {X.shape} ({len(names)} names)", flush=True); return X.astype(np.float64), len(names)


def half_life(X):
    ident, _ = memory_curve(X); return next((k for k in range(len(ident)) if ident[k] <= 0.5), None), ident


def subsample_half_lives(X, n=20, reps=50, seed=0):
    rng = np.random.default_rng(seed); hs = []
    for _ in range(reps):
        idx = rng.choice(X.shape[0], n, replace=False); h, _ = half_life(X[idx]); hs.append(h if h is not None else 100)
    return hs


def theme_stats(run, T, late=range(50, 100)):
    J, bad = load_judge(run)
    if not J: return None
    tup = collections.Counter(); woman = hope = n = 0
    for t in T:
        for s in late:
            j = J.get((t, s))
            if not j: continue
            n += 1; tup[(j["lead_age"], j["conflict_type"], j["ending_valence"])] += 1
            woman += j["lead_gender"] == "woman"; hope += j["ending_valence"] == "hopeful"
    if not n: return None
    (mt, mc), = tup.most_common(1)
    return dict(n=n, bad=bad, modal=list(mt), modal_share=mc / n, woman_share=woman / n, hopeful_share=hope / n)


def cell_stats(run, X, Xa, recs, T, S):
    Xu = unit(X); h, ident = half_life(X); words99 = [recs[(t, S[-1])]["story_words"] for t in T]
    summ = [recs[(t, s)].get("summary_words") for t in T for s in S if recs[(t, s)].get("summary") is not None]
    sum_flags = collections.Counter(k for t in T for s in S for k, v in (recs[(t, s)].get("summary_meta") or {}).get("flags", {}).items() if v)
    audit, _ = content_audit(run, recs, T, S)
    S99 = Cache(run).load("minilm_summary"); vs99 = vendi(S99["X"][:, -1].astype(np.float64)) if S99 is not None else None
    nn = nn_other(Xu); nna = nn_other(unit(Xa))
    return dict(n_traj=len(T), n_steps=len(S), half_life=h, ident_at={k: round(float(ident[k]), 2) for k in (1, 5, 10, 25, 50, 99) if k < len(ident)}, memory_curve=[float(x) for x in ident],
                nn_other_median=float(np.median(nn)), nn_other_anon_median=float(np.median(nna)), within_015=float((nn <= 0.15).mean()), within_015_anon=float((nna <= 0.15).mean()),
                vendi_story_99=vendi(Xu[:, -1]), vendi_summary_99=vs99, words_median_99=float(np.median(words99)),
                summary_words_median=float(np.median(summ)) if summ else None, summary_le_limit_share={lim: float(np.mean([w <= lim for w in summ])) for lim in (20, 25, 30, 50)} if summ else None,
                summary_flags=dict(sum_flags), audit=dict(exact_copies=audit["exact_copies"], n_cjk=audit["n_cjk_stories"], names_50_99=audit["names_50_99"], flags=audit["flags"]),
                theme=theme_stats(run, T))


def cluster_sheet(run, recs, T, S, a, tag, n_max=12):
    md = [f"# {run}: shared persistent clusters ({tag})", ""]
    for c, ts, nv in sorted(a["clusters"], key=lambda z: -len(z[1])):
        if len(ts) < 2: continue
        md += [f"## cluster {c}: {len(ts)} trajectories {ts}, {nv} persistent visits", ""]
        L = a["labels"]
        for ti in ts[:n_max]:
            row = L[T.index(ti)]; steps = [S[1:][i] for i in np.where(row == c)[0]]
            if not steps: continue
            s = steps[len(steps) // 2]; r = recs[(ti, s)]
            md += [f"- traj {ti}, steps {steps[0]}–{steps[-1]} ({len(steps)} inside); step {s} summary: {(r.get('summary') or r['story'][:300]).strip()}"]
        md.append("")
    return "\n".join(md)


def main():
    cpu_only(); ap = argparse.ArgumentParser()
    ap.add_argument("--scale", default="e3_1_haiku_100"); ap.add_argument("--width", default="e3_1w20_haiku"); ap.add_argument("--base", default="e3_1_haiku")
    ap.add_argument("--no-embed", action="store_true"); ap.add_argument("--n-sub", type=int, default=50); ap.add_argument("--skip", nargs="*", default=[])
    ap.add_argument("--out", default="scale_width", help="output stem under reports/e3/")
    ap.add_argument("--d1", action="store_true", help="the --width cell is an E3-D theme-bottleneck cell: grade D1 (predictions.md E3 follow-ups) instead of W1-W4")
    a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    runs = [r for r in (a.base, a.scale, a.width) if r and r not in a.skip and (ROOT / "runs" / r).exists()]
    model = None
    if not a.no_embed:
        need = [r for r in runs if Cache(r).load("minilm") is None]
        if need: embed_all(need, dev)
        from sentence_transformers import SentenceTransformer
        m = MODELS["minilm"]; model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    R = dict(params=dict(atlas=ATLAS, n_sub=a.n_sub, versions=package_versions()), cells={}, scale={}, width={}, verdicts={})
    data = {}
    for run in runs:
        recs, T, S = load_records(run); cache = Cache(run); X = cache.load("minilm")["X"].astype(np.float64)
        Xa, _ = anon_embed(run, recs, T, S, model, cache)
        data[run] = (recs, T, S, X, Xa); R["cells"][run] = cell_stats(run, X, Xa, recs, T, S); print(f"[{run}] cell stats done", flush=True)
    sheets = []

    # ---- E3-S: scale arm
    if a.scale in data:
        recs, T, S, X, Xa = data[a.scale]; Xu, Xau = unit(X[:, 1:]), unit(Xa[:, 1:]); n = len(T); kfull = k_for(n * (len(S) - 1))
        full = {tag: atlas_pairs(Y, kfull) for tag, Y in (("raw", Xu), ("anon", Xau))}
        for tag in full: sheets.append((f"sw_cluster_{a.scale}_{tag}.md", cluster_sheet(a.scale, recs, T, S, full[tag], tag)))
        rng = np.random.default_rng(0); sub = {tag: [] for tag in full}; curve = {tag: {} for tag in full}
        for _ in range(a.n_sub):
            idx = np.sort(rng.choice(n, 20, replace=False))
            for tag, Y in (("raw", Xu), ("anon", Xau)):
                r = atlas_pairs(Y[idx], k_for(20 * (len(S) - 1)), trajs=[T[i] for i in idx]); sub[tag].append(dict(persistent=r["persistent"], shared=r["shared"], pairs=r["n_sharing_pairs"], max_mult=r["max_mult"]))
        for nn_ in (10, 20, 40, 60, 80, 100):
            if nn_ > n: continue
            for tag, Y in (("raw", Xu), ("anon", Xau)):
                vals = []
                for rep in range(10 if nn_ < n else 1):
                    idx = np.sort(rng.choice(n, nn_, replace=False)); r = atlas_pairs(Y[idx], k_for(nn_ * (len(S) - 1)), seed=rep); vals.append(r["n_sharing_pairs"])
                curve[tag][nn_] = dict(mean_pairs=float(np.mean(vals)), n_pairs=nn_ * (nn_ - 1) // 2, vals=vals)
        first20 = [i for i, t in enumerate(T) if t < 20]; h20, _ = half_life(X[first20])
        hs = subsample_half_lives(X)
        R["scale"] = dict(k_full=kfull, full={tag: {k: v for k, v in full[tag].items() if k not in ("labels", "clusters")} | dict(clusters=[(c, ts, nv) for c, ts, nv in full[tag]["clusters"] if len(ts) >= 2]) for tag in full},
                          subsamples={tag: dict(shared_median=float(np.median([s["shared"] for s in sub[tag]])), shared_iqr=[float(np.percentile([s["shared"] for s in sub[tag]], q)) for q in (25, 75)],
                                                pairs_median=float(np.median([s["pairs"] for s in sub[tag]])), pairs_mean=float(np.mean([s["pairs"] for s in sub[tag]])), max_mult_max=max(s["max_mult"] for s in sub[tag]), raw=sub[tag]) for tag in sub},
                          pairs_vs_n=curve, half_life_first20=h20, half_life_sub_median=float(np.median(hs)), half_life_sub_iqr=[float(np.percentile(hs, q)) for q in (25, 75)],
                          first20=dict(nn_other_median=float(np.median(nn_other(unit(X[first20])))), words_median_99=float(np.median([recs[(t, S[-1])]["story_words"] for t in T if t < 20]))))
        # replication content audit on the fresh 0-19
        sub_recs = {k: v for k, v in recs.items() if k[0] < 20}; aud20, _ = content_audit(a.scale, sub_recs, [t for t in T if t < 20], S)
        R["scale"]["first20"]["names_50_99"] = aud20["names_50_99"]; R["scale"]["first20"]["theme"] = theme_stats(a.scale, [t for t in T if t < 20])
        # same-seed check against the base cell
        if a.base in data:
            brecs, bT, bS, bX, bXa = data[a.base]; same, diff, same_a, diff_a = [], [], [], []
            for tag, (B, Sc) in (("raw", (unit(bX[:, 50:]), unit(X[:, 50:]))), ("anon", (unit(bXa[:, 50:]), unit(Xa[:, 50:])))):
                M = np.zeros((len(bT), 20))
                for i in range(len(bT)):
                    for j in range(20):
                        M[i, j] = np.median((1 - B[i] @ Sc[j].T).min(1))
                d_same = np.diag(M); d_diff = M[~np.eye(len(bT), dtype=bool)]
                (same if tag == "raw" else same_a).append(d_same); (diff if tag == "raw" else diff_a).append(d_diff)
            # joint atlas base + scale, same-seed pairs sharing a cluster
            J = np.concatenate([unit(bX[:, 1:]), Xu]); kj = k_for(J.shape[0] * J.shape[1]); ja = atlas_pairs(J, kj, trajs=[("b", t) for t in bT] + [("s", t) for t in T])
            ss_pairs = sum(1 for p in ja["pairs"] if {p[0][0], p[1][0]} == {"b", "s"} and p[0][1] == p[1][1] and p[0][1] < 20)
            R["scale"]["same_seed"] = dict(raw=dict(same_median=float(np.median(same[0])), diff_median=float(np.median(diff[0])), gap=float(np.median(diff[0]) - np.median(same[0])), same_lt_diff_share=float(np.mean(same[0] < np.median(diff[0])))),
                                           anon=dict(same_median=float(np.median(same_a[0])), diff_median=float(np.median(diff_a[0])), gap=float(np.median(diff_a[0]) - np.median(same_a[0]))),
                                           joint_k=kj, same_seed_pairs_sharing_cluster=ss_pairs, joint_shared_clusters=ja["shared"], joint_sharing_pairs=ja["n_sharing_pairs"])
        print("[scale] done", flush=True)

    # ---- E3-W: width arm (joint atlas with the base cell at k 40, as the gate did)
    if a.width in data and a.base in data:
        wrecs, wT, wS, wX, wXa = data[a.width]; brecs, bT, bS, bX, bXa = data[a.base]; W = {}
        for tag, (Bw, Bb) in (("raw", (unit(wX[:, 1:]), unit(bX[:, 1:]))), ("anon", (unit(wXa[:, 1:]), unit(bXa[:, 1:])))):
            J = np.concatenate([Bw, Bb]); ja = atlas_pairs(J, 40, trajs=[("w", t) for t in wT] + [("b", t) for t in bT])
            per = {}
            for cell in ("w", "b"):
                cl = [(c, [t for t in ts if t[0] == cell], nv) for c, ts, nv in ja["clusters"]]
                per[cell] = dict(persistent=sum(1 for c, ts, nv in cl if ts), shared=sum(1 for c, ts, nv in cl if len(ts) >= 2), pairs=sum(len(ts) * (len(ts) - 1) // 2 for c, ts, nv in cl if len(ts) >= 2))
            W[tag] = dict(width=per["w"], base=per["b"], cross_cell_shared=sum(1 for c, ts, nv in ja["clusters"] if len({t[0] for t in ts}) == 2))
            ja_w = dict(ja, clusters=[(c, [t[1] for t in ts if t[0] == "w"], nv) for c, ts, nv in ja["clusters"]], labels=ja["labels"][:len(wT)])
            sheets.append((f"sw_cluster_{a.width}_{tag}.md", cluster_sheet(a.width, wrecs, wT, wS, ja_w, tag + ", joint atlas with " + a.base)))
        R["width"] = dict(atlas=W)
        print("[width] done", flush=True)

    # ---- verdicts
    V = {}; c = R["cells"]
    if R["scale"]:
        sc = R["scale"]; an, rw = sc["full"]["anon"], sc["full"]["raw"]
        V["S1_wells_numerous"] = dict(anon_sharing_pairs=an["n_sharing_pairs"], anon_rate=an["rate"], anon_shared_clusters=an["shared"], anon_max_mult=an["max_mult"], raw_shared_clusters=rw["shared"], raw_sharing_pairs=rw["n_sharing_pairs"], W_hat_anon=an["W_hat"],
                                       sub_raw_shared_median=sc["subsamples"]["raw"]["shared_median"], sub_anon_shared_median=sc["subsamples"]["anon"]["shared_median"],
                                       holds=(25 <= an["n_sharing_pairs"] <= 150 and an["shared"] >= 10 and an["max_mult"] >= 4 and rw["shared"] >= 5),
                                       fails=(rw["shared"] < 5 and an["shared"] < 10 and an["max_mult"] < 4))
        f20 = sc["first20"]; base_t = c.get(a.base, {}).get("theme"); sc_t = f20.get("theme")
        V["S2_replication_first20"] = dict(half_life=sc["half_life_first20"], half_in_8_15=(sc["half_life_first20"] is not None and 8 <= sc["half_life_first20"] <= 15), cover=f20["names_50_99"]["top10_cover"], cover_in_band=0.45 <= f20["names_50_99"]["top10_cover"] <= 0.65,
                                           top_name=f20["names_50_99"]["top10"][0][0] if f20["names_50_99"]["top10"] else None, maya_top=(f20["names_50_99"]["top10"][0][0] == "Maya") if f20["names_50_99"]["top10"] else False,
                                           words=f20["words_median_99"], words_in_band=480 <= f20["words_median_99"] <= 520, modal=sc_t["modal"] if sc_t else None, base_modal=base_t["modal"] if base_t else None, modal_same=(sc_t and base_t and sc_t["modal"] == base_t["modal"]) or False,
                                           all100=dict(half_life_sub_median=sc["half_life_sub_median"], cover=c[a.scale]["audit"]["names_50_99"]["top10_cover"], words=c[a.scale]["words_median_99"]))
        V["S2_replication_first20"]["holds"] = all([V["S2_replication_first20"][k] for k in ("half_in_8_15", "cover_in_band", "maya_top", "words_in_band")]) and (V["S2_replication_first20"]["modal_same"] if sc_t else True)
        nn = c[a.scale]["nn_other_median"]; w15 = c[a.scale]["within_015"]
        V["S3_density"] = dict(nn_other=nn, base_nn=c.get(a.base, {}).get("nn_other_median"), nn_in_band=0.26 <= nn <= 0.32, within_015=w15, within_in_band=0.01 <= w15 <= 0.05, holds=(0.26 <= nn <= 0.32 and 0.01 <= w15 <= 0.05), continuum=(nn >= 0.33 and rw["shared"] < 5))
        if "same_seed" in sc:
            ss = sc["same_seed"]; V["S4_seed_trace"] = dict(gap_raw=ss["raw"]["gap"], gap_anon=ss["anon"]["gap"], gap_in_band=0.02 <= ss["raw"]["gap"] <= 0.10, same_seed_pairs_sharing=ss["same_seed_pairs_sharing_cluster"], le_1=ss["same_seed_pairs_sharing_cluster"] <= 1,
                                                          holds=(0.02 <= ss["raw"]["gap"] <= 0.10 and ss["same_seed_pairs_sharing_cluster"] <= 1))
        V["speculation_1"] = "holds" if V["S1_wells_numerous"]["holds"] else ("fails" if V["S1_wells_numerous"]["fails"] else "in between: sharing pairs present but no well reused by >= 4 (W > 500 at this n)")
    if R["width"] and a.width in c and a.base in c and a.d1:
        w, b = c[a.width], c[a.base]; wa = R["width"]["atlas"]; need = 3 if "haiku" in a.width else 2
        V["D1_abstraction_converges"] = dict(shared_raw=wa["raw"]["width"]["shared"], shared_anon=wa["anon"]["width"]["shared"], need_shared=need, shared_ok=wa["raw"]["width"]["shared"] >= need,
                                             base_shared_raw=wa["raw"]["base"]["shared"], half_life=w["half_life"], base_half=b["half_life"], half_le_10=(w["half_life"] is not None and w["half_life"] <= 10),
                                             nn_other=w["nn_other_median"], base_nn=b["nn_other_median"], nn_le_030=w["nn_other_median"] <= 0.30, within_015=w["within_015"],
                                             vendi_theme_99=w["vendi_summary_99"], base_vendi_summary_99=b["vendi_summary_99"], vendi_half=(w["vendi_summary_99"] is not None and b["vendi_summary_99"] is not None and w["vendi_summary_99"] <= 0.5 * b["vendi_summary_99"]),
                                             cover=w["audit"]["names_50_99"]["top10_cover"], base_cover=b["audit"]["names_50_99"]["top10_cover"], words=w["words_median_99"], theme_words_median=w["summary_words_median"], theme_le25=(w["summary_le_limit_share"] or {}).get(25))
        v = V["D1_abstraction_converges"]; v["n_clauses_hold"] = sum([v["shared_ok"], v["half_le_10"], v["nn_le_030"], v["vendi_half"]]); v["holds"] = v["n_clauses_hold"] == 4
        if w["theme"] and b["theme"]:
            V["D_theme_layer_posthoc"] = dict(modal=w["theme"]["modal"], base_modal=b["theme"]["modal"], modal_share=w["theme"]["modal_share"], base_modal_share=b["theme"]["modal_share"], woman=w["theme"]["woman_share"], base_woman=b["theme"]["woman_share"], hopeful=w["theme"]["hopeful_share"], base_hopeful=b["theme"]["hopeful_share"])
    elif R["width"] and a.width in c and a.base in c:
        w, b = c[a.width], c[a.base]; wa = R["width"]["atlas"]
        V["W1_width_is_a_lever"] = dict(half_life=w["half_life"], base_half=b["half_life"], half_le_7=(w["half_life"] is not None and w["half_life"] <= 7), nn_other=w["nn_other_median"], base_nn=b["nn_other_median"], nn_le_030=w["nn_other_median"] <= 0.30,
                                        within_015=w["within_015"], within_ge_002=w["within_015"] >= 0.02, shared_raw=wa["raw"]["width"]["shared"], shared_anon=wa["anon"]["width"]["shared"], base_shared_raw=wa["raw"]["base"]["shared"],
                                        cover=w["audit"]["names_50_99"]["top10_cover"], cover_ge_060=w["audit"]["names_50_99"]["top10_cover"] >= 0.60, vendi_summary_99=w["vendi_summary_99"], base_vendi_summary_99=b["vendi_summary_99"],
                                        words=w["words_median_99"], words_in_band=480 <= w["words_median_99"] <= 520)
        v = V["W1_width_is_a_lever"]; v["n_clauses_hold"] = sum([v["half_le_7"], v["nn_le_030"], v["within_ge_002"], v["shared_raw"] >= 1, v["shared_anon"] >= 2, v["cover_ge_060"], (v["vendi_summary_99"] or 9e9) < (v["base_vendi_summary_99"] or 0), v["words_in_band"]]); v["holds"] = v["n_clauses_hold"] == 8
        V["W1_width_is_a_lever"]["direction_if_wrong"] = (w["half_life"] is None or w["half_life"] >= 9) and w["nn_other_median"] >= 0.33 and wa["raw"]["width"]["shared"] == 0
        V["W2_compliance"] = dict(summary_median=w["summary_words_median"], median_in_20_28=(w["summary_words_median"] is not None and 20 <= w["summary_words_median"] <= 28), le20_share=w["summary_le_limit_share"][20] if w["summary_le_limit_share"] else None,
                                  le20_in_band=(w["summary_le_limit_share"] is not None and 0.30 <= w["summary_le_limit_share"][20] <= 0.60), base_le50=b["summary_le_limit_share"][50] if b["summary_le_limit_share"] else None,
                                  empty_or_refusal=sum(v_ for k_, v_ in w["summary_flags"].items() if k_ in ("empty", "refusal")))
        V["W2_compliance"]["holds"] = V["W2_compliance"]["median_in_20_28"] and V["W2_compliance"]["le20_in_band"] and V["W2_compliance"]["empty_or_refusal"] == 0
        V["W3_trend"] = dict(half_20=w["half_life"], half_50=b["half_life"], nn_20=w["nn_other_median"], nn_50=b["nn_other_median"], monotone_so_far=((w["half_life"] or 100) < (b["half_life"] or 100) and w["nn_other_median"] < b["nn_other_median"]),
                             shared_raw=wa["raw"]["width"]["shared"], below_D1=wa["raw"]["width"]["shared"] < 3, note="30-word cell held; D not run")
        if w["theme"] and b["theme"]:
            V["W4_same_destination"] = dict(modal=w["theme"]["modal"], base_modal=b["theme"]["modal"], modal_same=w["theme"]["modal"] == b["theme"]["modal"], modal_share=w["theme"]["modal_share"], base_modal_share=b["theme"]["modal_share"],
                                            share_up_005=w["theme"]["modal_share"] - b["theme"]["modal_share"] >= 0.05, woman=w["theme"]["woman_share"], base_woman=b["theme"]["woman_share"], hopeful=w["theme"]["hopeful_share"], base_hopeful=b["theme"]["hopeful_share"],
                                            within_005=abs(w["theme"]["woman_share"] - b["theme"]["woman_share"]) <= 0.05 and abs(w["theme"]["hopeful_share"] - b["theme"]["hopeful_share"]) <= 0.05)
            V["W4_same_destination"]["holds"] = V["W4_same_destination"]["modal_same"] and V["W4_same_destination"]["share_up_005"] and V["W4_same_destination"]["within_005"]
    R["verdicts"] = V

    # ---- figure
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    for run in runs: ax[0].plot(c[run]["memory_curve"], label=f"{run} (n={c[run]['n_traj']})")
    ax[0].axhline(0.5, ls=":", c="k"); ax[0].set_title("own seed identified (MiniLM)"); ax[0].set_xlabel("step"); ax[0].legend(fontsize=7)
    if R["scale"]:
        for tag in ("raw", "anon"):
            cv = R["scale"]["pairs_vs_n"][tag]; xs = sorted(cv); ax[1].plot([cv[x]["n_pairs"] for x in xs], [cv[x]["mean_pairs"] for x in xs], "o-", label=tag)
        ax[1].set_xscale("log"); ax[1].set_title("sharing pairs vs trajectory pairs (k scaled)"); ax[1].set_xlabel("n(n-1)/2"); ax[1].legend()
    for run in runs:
        recs, T, S, X, Xa = data[run]; ax[2].hist(nn_other(unit(X)), bins=40, histtype="step", density=True, label=run)
    ax[2].axvline(0.15, ls=":", c="k"); ax[2].set_title("nearest other-trajectory distance (steps ≥ 25)"); ax[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / f"{a.out}.png", dpi=120)

    # ---- markdown
    md = ["# E3-S (100 seeds) and E3-W (20-word summary): Haiku compress–expand", "", "Predictions: predictions.md \"E3 scale and bottleneck width\" (2026-11-02). Pair-sharing rule and k scaling as stated there; anonymised = names → X (E3-A filter).", ""]
    if V.get("speculation_1"): md += [f"**Speculation 1 (numerous wells): {V['speculation_1']}.** " + "; ".join(f"{k} {('holds' if v.get('holds') else 'fails') if isinstance(v, dict) and 'holds' in v else ''}" for k, v in V.items() if k.startswith("S")), ""]
    if "D1_abstraction_converges" in V: md += [f"**D1 (abstraction converges): {'holds' if V['D1_abstraction_converges']['holds'] else 'fails'}, {V['D1_abstraction_converges']['n_clauses_hold']} of 4 clauses** (shared raw {V['D1_abstraction_converges']['shared_raw']} vs ≥ {V['D1_abstraction_converges']['need_shared']}; half-life {V['D1_abstraction_converges']['half_life']} vs ≤ 10; nn-other {V['D1_abstraction_converges']['nn_other']:.3f} vs ≤ 0.30; theme Vendi {V['D1_abstraction_converges']['vendi_theme_99']:.1f} vs ≤ half of {V['D1_abstraction_converges']['base_vendi_summary_99']:.1f}).", ""]
    if "W1_width_is_a_lever" in V: md += [f"**Speculation 2 (width): W1 {V['W1_width_is_a_lever']['n_clauses_hold']} of 8 clauses; " + "; ".join(f"{k} {'holds' if v.get('holds') else 'fails'}" for k, v in V.items() if k.startswith("W") and "holds" in v) + (" ; direction-if-wrong condition met" if V["W1_width_is_a_lever"]["direction_if_wrong"] else "") + ".**", ""]
    md += ["## Cells", "", "| cell | n | half-life | own seed 10 / 50 / 99 | nn-other raw / anon | within 0.15 raw / anon | Vendi story / summary at 99 | words at 99 | summary words (≤20 / ≤50) | top-10 cover | top names 50–99 | modal tuple (share) | woman / hopeful |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for run in runs:
        d = c[run]; nm = d["audit"]["names_50_99"]; th = d["theme"]; sl = d["summary_le_limit_share"] or {}
        modal_s = (" × ".join(th["modal"]) + " (%.2f)" % th["modal_share"]) if th else "not judged"; wh_s = ("%.2f / %.2f" % (th["woman_share"], th["hopeful_share"])) if th else ""
        names_s = ", ".join("%s %d" % (x, y) for x, y in nm["top10"][:5]); vs = d["vendi_summary_99"]; vs_s = "%.1f" % vs if vs is not None else "-"
        md.append(f"| {run} | {d['n_traj']} | {d['half_life']} | {d['ident_at'].get(10)} / {d['ident_at'].get(50)} / {d['ident_at'].get(99)} | {d['nn_other_median']:.3f} / {d['nn_other_anon_median']:.3f} | {d['within_015']:.3f} / {d['within_015_anon']:.3f} | {d['vendi_story_99']:.1f} / {vs_s} | {d['words_median_99']:.0f} | {d['summary_words_median']} ({sl.get(20, float('nan')):.2f} / {sl.get(50, float('nan')):.2f}) | {nm['top10_cover']:.2f} | {names_s} | {modal_s} | {wh_s} |")
    if R["scale"]:
        sc = R["scale"]; md += ["", f"## E3-S: pair sharing at n = {c[a.scale]['n_traj']} (k {sc['k_full']})", "", "| atlas | persistent | shared (≥ 2 traj) | sharing pairs / pairs | rate | max trajectories in one cluster | W-hat | steps inside |", "|---|---|---|---|---|---|---|---|"]
        for tag in ("raw", "anon"):
            f = sc["full"][tag]; md.append(f"| {tag} | {f['persistent']} | {f['shared']} | {f['n_sharing_pairs']} / {f['n_pairs']} | {f['rate']:.4f} | {f['max_mult']} | {f['W_hat'] if f['W_hat'] is None else round(f['W_hat'])} | {f['inside_share']:.2f} |")
        md += ["", f"Random 20-trajectory subsamples ({a.n_sub}, k 40): shared clusters median raw {sc['subsamples']['raw']['shared_median']:.0f} (IQR {sc['subsamples']['raw']['shared_iqr']}), anon {sc['subsamples']['anon']['shared_median']:.0f} (IQR {sc['subsamples']['anon']['shared_iqr']}); mean sharing pairs raw {sc['subsamples']['raw']['pairs_mean']:.2f}, anon {sc['subsamples']['anon']['pairs_mean']:.2f}; largest multiplicity raw {sc['subsamples']['raw']['max_mult_max']}, anon {sc['subsamples']['anon']['max_mult_max']}. The 20-trajectory cell e3_1_haiku had 0 shared (raw).",
               "", "Sharing pairs vs n (mean over 10 draws, k scaled): " + "; ".join(f"n {n_}: raw {sc['pairs_vs_n']['raw'][n_]['mean_pairs']:.1f}, anon {sc['pairs_vs_n']['anon'][n_]['mean_pairs']:.1f} of {sc['pairs_vs_n']['raw'][n_]['n_pairs']}" for n_ in sorted(sc["pairs_vs_n"]["raw"])) + ". A fixed well count gives pairs ∝ n(n−1)/2.",
               "", f"Fresh sample of seeds 0–19: half-life {sc['half_life_first20']} (20-trajectory subsample median over all 100: {sc['half_life_sub_median']:.0f}, IQR {sc['half_life_sub_iqr']}); nn-other {sc['first20']['nn_other_median']:.3f}; words {sc['first20']['words_median_99']:.0f}; top-10 cover {sc['first20']['names_50_99']['top10_cover']:.2f}, top names {', '.join('%s %d' % (x, y) for x, y in sc['first20']['names_50_99']['top10'][:5])}"
               + (f"; modal tuple {' × '.join(sc['first20']['theme']['modal'])} ({sc['first20']['theme']['modal_share']:.2f})" if sc["first20"].get("theme") else "") + "."]
        if "same_seed" in sc:
            ss = sc["same_seed"]; md += ["", f"Same-seed check (base vs scale, seeds 0–19, steps 50–99, median nearest-step distance): same-seed {ss['raw']['same_median']:.3f} vs different-seed {ss['raw']['diff_median']:.3f} (gap {ss['raw']['gap']:.3f}; anonymised gap {ss['anon']['gap']:.3f}); {ss['same_seed_pairs_sharing_cluster']} of 20 same-seed pairs share a persistent cluster in the joint atlas (k {ss['joint_k']}, {ss['joint_shared_clusters']} shared clusters, {ss['joint_sharing_pairs']} sharing pairs)."]
        md += ["", f"Shared-cluster sheets: `sw_cluster_{a.scale}_raw.md`, `sw_cluster_{a.scale}_anon.md`."]
    if R["width"]:
        wa = R["width"]["atlas"]; md += ["", f"## E3-W: joint atlas with {a.base} (k 40)", "", "| atlas | width persistent (shared, pairs) | base persistent (shared, pairs) | clusters visited by both cells |", "|---|---|---|---|"]
        for tag in ("raw", "anon"): md.append(f"| {tag} | {wa[tag]['width']['persistent']} ({wa[tag]['width']['shared']}, {wa[tag]['width']['pairs']}) | {wa[tag]['base']['persistent']} ({wa[tag]['base']['shared']}, {wa[tag]['base']['pairs']}) | {wa[tag]['cross_cell_shared']} |")
        md += ["", f"Shared-cluster sheets: `sw_cluster_{a.width}_raw.md`, `sw_cluster_{a.width}_anon.md`."]
    md += ["", "## Verdicts", ""]
    for k, v in V.items(): md.append(f"- **{k}**: " + (json.dumps(v, default=float) if isinstance(v, dict) else str(v)))
    md += ["", f"![curves]({a.out}.png)", ""]
    for name, text in sheets: (OUT / name).write_text(text, encoding="utf-8")
    (OUT / f"{a.out}.json").write_text(json.dumps(R, indent=1, default=float)); (OUT / f"{a.out}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:12]))


if __name__ == "__main__": main()
