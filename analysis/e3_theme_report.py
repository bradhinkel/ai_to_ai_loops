"""E3-B theme-layer analysis of the text loops (predictions.md "E3 follow-ups" B1–B7, 2026-11-01), from the judge codings
written by theme_judge.py (claude-haiku-5-5 on every story; claude-sonnet-5-5 on a stratified subsample for reliability).

Theme attractor, operational (predictions.md): (i) a persistent-atlas cluster of theme-sentence MiniLM embeddings with >= 3
persistent visits (dwell >= 5) from >= 2 trajectories, or (ii) a tuple (lead_age x conflict_type x ending_valence) held by
>= 3 of 20 trajectories for >= 5 consecutive steps. Collapse = effective number of tuples (exp Shannon entropy) at steps
50-99 below steps 1-10. Nulls: steps 1-10, and a within-trajectory step shuffle.

    .venv/bin/python analysis/e3_theme_report.py [--runs ...] [--k 40] [--radius 0.15] [--exit_factor 1.25] [--min_dwell 5] [--min_visits 3]
    [--second sonnet]  (suffix of the second judge's jsonl)  [--handcode 50]

Writes reports/e3/theme.md, theme.json, theme_curves.png, theme_cluster_NN.md, codebook.md, handcode_sample.md (and the key
under analysis/cache/e3_handcode_key.json, not in reports/). CLIP is not used (CLAUDE.md rule 4).
"""
import argparse, collections, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE, MODELS, SERIES, Cache, cpu_only, vendi, package_versions  # noqa: E402
from gravity import label_steps, visits  # noqa: E402
from e3_report import CELLS, load_records, build_name_filter, audit_story, unit  # noqa: E402
from theme_judge import FIELDS, BOOLS  # noqa: E402

MODELS["minilm_theme"] = dict(MODELS["minilm"], pooling=MODELS["minilm"]["pooling"] + "; field = judge theme sentence (theme_judge.py)")
TUPLE = ("lead_age", "conflict_type", "ending_valence")
CATS = list(FIELDS) + BOOLS                      # 11 categorical fields (secondary_character is extra; the verdict uses the 10 named in B7)
VERDICT_FIELDS = [f for f in CATS if f != "secondary_character"]
WIN_EARLY, WIN_LATE = (1, 10), (50, 99)
WINDOWS = [(1, 10), (11, 25), (26, 50), (51, 75), (76, 89), (90, 99)]


def load_judge(run, suffix=""):
    p = CACHE / run / f"theme_judge{('_' + suffix) if suffix else ''}.jsonl"
    out, bad = {}, 0
    if not p.exists(): return out, bad
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        d = json.loads(line); j = d.get("judge")
        if not j or d.get("judge_error"): bad += 1; continue
        out[(d["traj"], d["step"])] = j
    return out, bad


def eff_number(counter):
    n = sum(counter.values())
    if n == 0: return float("nan")
    p = np.array([c / n for c in counter.values()]); return float(np.exp(-(p * np.log(p)).sum()))


def entropy(counter):
    n = sum(counter.values()); p = np.array([c / n for c in counter.values()]); return float(-(p * np.log(p)).sum()) if n else float("nan")


def js(c1, c2):
    keys = set(c1) | set(c2); n1, n2 = sum(c1.values()), sum(c2.values())
    p = np.array([c1.get(k, 0) / n1 for k in keys]); q = np.array([c2.get(k, 0) / n2 for k in keys]); m = (p + q) / 2
    kl = lambda a, b: float(np.sum([x * np.log(x / y) for x, y in zip(a, b) if x > 0]))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def tup(j): return tuple(j[f] for f in TUPLE)


def window_counts(J, T, lo, hi, key=tup):
    return collections.Counter(key(J[(t, s)]) for t in T for s in range(lo, hi + 1) if (t, s) in J)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", nargs="*"); ap.add_argument("--k", type=int, default=40); ap.add_argument("--radius", type=float, default=0.15)
    ap.add_argument("--exit_factor", type=float, default=1.25); ap.add_argument("--min_dwell", type=int, default=5); ap.add_argument("--min_visits", type=int, default=3)
    ap.add_argument("--second", default="sonnet"); ap.add_argument("--handcode", type=int, default=50); ap.add_argument("--shuffles", type=int, default=20); ap.add_argument("--no-embed", action="store_true")
    a = ap.parse_args()
    import torch; dev = "cuda" if cpu_only() else "cpu"; torch.set_num_threads(8)
    cells = [c for c in CELLS if not a.runs or c[0] in a.runs]; runs = [c[0] for c in cells]
    out_dir = ROOT / "reports" / "e3"; out_dir.mkdir(parents=True, exist_ok=True)
    R = {"params": dict(k=a.k, radius=a.radius, exit_factor=a.exit_factor, min_dwell=a.min_dwell, min_visits=a.min_visits, tuple=TUPLE, packages=package_versions()), "cells": {}}
    J, recs_all, bad = {}, {}, {}
    for run in runs:
        J[run], bad[run] = load_judge(run); recs_all[run] = load_records(run)
    rng = np.random.default_rng(0)

    # ---- 1. tuples: collapse, modal share, shuffled null, per-field entropy, memory  (B1, B4, B5, B6)
    for run, model, loop in cells:
        recs, T, S = recs_all[run]; Jr = J[run]
        c = R["cells"][run] = dict(model=model, loop=loop, n_judged=len(Jr), n_malformed=bad[run], n_steps=len(S))
        early, late = window_counts(Jr, T, *WIN_EARLY), window_counts(Jr, T, *WIN_LATE)
        c["tuple"] = dict(eff_early=eff_number(early), eff_late=eff_number(late), ratio=eff_number(late) / eff_number(early) if early else None,
                          modal_early=(early.most_common(1)[0][0], early.most_common(1)[0][1] / sum(early.values())) if early else None,
                          modal_late=(late.most_common(1)[0][0], late.most_common(1)[0][1] / sum(late.values())) if late else None,
                          top5_late=[(k, round(v / sum(late.values()), 3)) for k, v in late.most_common(5)] if late else [], js_early_late=js(early, late) if early and late else None)
        # shuffled null: permute steps within each trajectory, same windows
        ratios = []
        for _ in range(a.shuffles):
            perm = {t: rng.permutation([s for s in S if (t, s) in Jr and s >= 1]) for t in T}
            Jp = {(t, s_new): Jr[(t, s_old)] for t in T for s_new, s_old in zip(sorted(s for s in S if (t, s) in Jr and s >= 1), perm[t])}
            e, l = window_counts(Jp, T, *WIN_EARLY), window_counts(Jp, T, *WIN_LATE)
            if e and l: ratios.append(eff_number(l) / eff_number(e))
        c["tuple"]["null_ratio_mean"] = float(np.mean(ratios)) if ratios else None
        # POST-HOC (added after the B verdicts were read, 2026-11-01): the same statistics for tuple B = lead_gender x conflict_type x
        # ending_valence, because lead_age turned out to be the judge's weakest field (Haiku codes 'unclear' far more often than Sonnet).
        # Not a prediction; reported beside the predicted tuple, never instead of it.
        tupB = lambda j: (j["lead_gender"], j["conflict_type"], j["ending_valence"])  # noqa: E731
        eB, lB = window_counts(Jr, T, *WIN_EARLY, key=tupB), window_counts(Jr, T, *WIN_LATE, key=tupB); ratiosB = []
        for _ in range(a.shuffles):
            perm = {t: rng.permutation([s for s in S if (t, s) in Jr and s >= 1]) for t in T}
            Jp = {(t, s_new): Jr[(t, s_old)] for t in T for s_new, s_old in zip(sorted(s for s in S if (t, s) in Jr and s >= 1), perm[t])}
            e_, l_ = window_counts(Jp, T, *WIN_EARLY, key=tupB), window_counts(Jp, T, *WIN_LATE, key=tupB)
            if e_ and l_: ratiosB.append(eff_number(l_) / eff_number(e_))
        holdB = [tupB(Jr[(t, 1)]) == tupB(Jr[(t, S[-1])]) for t in T if (t, 1) in Jr and (t, S[-1]) in Jr]
        memB = [float(np.mean([tupB(Jr[(t, s)]) == tupB(Jr[(t, 0)]) for t in T if (t, 0) in Jr and (t, s) in Jr])) for s in S]
        c["tuple_b"] = dict(fields=["lead_gender", "conflict_type", "ending_valence"], eff_early=eff_number(eB), eff_late=eff_number(lB), ratio=eff_number(lB) / eff_number(eB) if eB else None,
                            null_ratio_mean=float(np.mean(ratiosB)) if ratiosB else None, modal_late=(lB.most_common(1)[0][0], lB.most_common(1)[0][1] / sum(lB.values())) if lB else None,
                            top3_late=[(k, round(v / sum(lB.values()), 3)) for k, v in lB.most_common(3)] if lB else [], js_early_late=js(eB, lB) if eB and lB else None,
                            share_hold_step1_at_last=float(np.mean(holdB)) if holdB else None, memory_half_step=next((s for s in S if s >= 1 and memB[s] <= 0.5), None), memory_at_last=memB[-1])
        # per window, per field
        c["fields"] = {}
        for f in CATS:
            per = {}
            for lo, hi in WINDOWS:
                cnt = window_counts(Jr, T, lo, hi, key=lambda j, f=f: j[f])
                if cnt: per[f"{lo}-{hi}"] = dict(entropy=entropy(cnt), modal=cnt.most_common(1)[0][0], modal_share=cnt.most_common(1)[0][1] / sum(cnt.values()), dist={str(k): v for k, v in cnt.most_common()})
            ce, cl = window_counts(Jr, T, *WIN_EARLY, key=lambda j, f=f: j[f]), window_counts(Jr, T, *WIN_LATE, key=lambda j, f=f: j[f])
            c["fields"][f] = dict(windows=per, entropy_early=entropy(ce) if ce else None, entropy_late=entropy(cl) if cl else None,
                                  entropy_change=((entropy(cl) - entropy(ce)) / entropy(ce)) if ce and cl and entropy(ce) > 0 else None)
        # tuple persistence (ii): tuples held by >= min_visits trajectories for >= min_dwell consecutive steps
        held = collections.defaultdict(set); runs_len = collections.Counter()
        for t in T:
            seq = [(s, tup(Jr[(t, s)])) for s in S if s >= 1 and (t, s) in Jr]; i = 0
            while i < len(seq):
                j = i
                while j + 1 < len(seq) and seq[j + 1][1] == seq[i][1] and seq[j + 1][0] == seq[j][0] + 1: j += 1
                if j - i + 1 >= a.min_dwell: held[seq[i][1]].add(t); runs_len[seq[i][1]] += 1
                i = j + 1
        c["tuple"]["attractors_ii"] = sorted([dict(tuple=k, trajectories=len(v), runs=runs_len[k]) for k, v in held.items() if len(v) >= a.min_visits], key=lambda d: -d["trajectories"])
        # B5 / B6: hold step-1 tuple at 99; equals own step-0 tuple by step
        hold = [tup(Jr[(t, 1)]) == tup(Jr[(t, S[-1])]) for t in T if (t, 1) in Jr and (t, S[-1]) in Jr]
        c["tuple"]["share_hold_step1_at_last"] = float(np.mean(hold)) if hold else None
        mem = []
        for s in S:
            v = [tup(Jr[(t, s)]) == tup(Jr[(t, 0)]) for t in T if (t, 0) in Jr and (t, s) in Jr]; mem.append(float(np.mean(v)) if v else float("nan"))
        c["tuple"]["memory_curve"] = mem; c["tuple"]["memory_half_step"] = next((s for s in S if s >= 1 and not np.isnan(mem[s]) and mem[s] <= 0.5), None); c["tuple"]["memory_at_last"] = mem[-1]

    # ---- 2. between-cell divergences (B3)
    late = {run: window_counts(J[run], recs_all[run][1], *WIN_LATE) for run in runs}
    R["js_late"] = {f"{r1}|{r2}": js(late[r1], late[r2]) for i, r1 in enumerate(runs) for r2 in runs[i + 1:] if late[r1] and late[r2]}
    models = sorted({m for _, m, _ in cells}); by = {(m, l): r for r, m, l in cells}
    R["b3"] = {}
    for m in models:
        within = R["js_late"].get(f"{by[(m, 'E3-1')]}|{by[(m, 'E3-2')]}") if (m, "E3-1") in by and (m, "E3-2") in by else None
        across = {m2: R["js_late"].get(f"{by[(m, 'E3-1')]}|{by[(m2, 'E3-1')]}", R["js_late"].get(f"{by[(m2, 'E3-1')]}|{by[(m, 'E3-1')]}")) for m2 in models if m2 != m and (m2, "E3-1") in by}
        R["b3"][m] = dict(within_model_loops=within, across_models_e3_1=across, holds=all(v is not None and within is not None and v > within for v in across.values()) if across else None)

    # ---- 3. theme-sentence embeddings: persistent atlas (B2), scale
    if not a.no_embed:
        from sentence_transformers import SentenceTransformer
        mm = MODELS["minilm"]; enc = SentenceTransformer(mm["id"], revision=mm["revision"], device=dev)
        for run in runs:
            recs, T, S = recs_all[run]; Jr = J[run]
            texts = [(Jr[(t, s)]["theme"] if (t, s) in Jr else "") for t in T for s in S]; mask = np.array([bool(x) for x in texts]).reshape(len(T), len(S))
            X = enc.encode(texts, normalize_embeddings=True, batch_size=128, show_progress_bar=False).reshape(len(T), len(S), -1).astype(np.float32); X[~mask] = np.nan
            Cache(run).save("minilm_theme", dict(X=X, trajs=np.array(T), steps=np.array(S), mask=mask), {"device": dev, "field": "theme"})
    E, trajs = {}, {}
    for run in runs:
        d = Cache(run).arrays("minilm_theme"); X = d["X"].astype(np.float64); m = d["mask"]
        keep = [i for i in range(len(d["trajs"])) if m[i, 1:].all()]          # trajectories judged at every step >= 1
        if not keep: continue
        E[run] = unit(X[keep, 1:]).astype(np.float32); trajs[run] = [int(d["trajs"][i]) for i in keep]
    from sklearn.cluster import KMeans
    pooled = np.concatenate([E[r].reshape(-1, E[r].shape[-1]) for r in E])
    km = KMeans(n_clusters=a.k, n_init=3, random_state=0).fit(pooled); C = unit(km.cluster_centers_.astype(np.float32))
    np.savez(ROOT / "archive" / "e3_theme_atlas_centroids.npz", C=C)
    sheets = {}
    for run in E:
        X = E[run]; T, S, _ = X.shape; D = 1.0 - np.einsum("kd,tsd->kts", C, X); L = label_steps(D, np.full(a.k, a.radius), a.exit_factor)
        Jr = J[run]; pers = []
        inside_any = np.zeros((T, S), bool)
        for k in range(a.k):
            inside = L == k; ex = []
            for ti in range(T):
                pos = 0
                for length, cens in visits(inside[ti]):
                    while pos < S and not inside[ti, pos]: pos += 1
                    start = pos; pos += length
                    if length >= a.min_dwell: ex.append((trajs[run][ti], start + 1, length, bool(cens)))
            if len(ex) >= a.min_visits:
                inside_any |= inside; tr = {e[0] for e in ex}
                # field agreement inside the attractor's steps
                steps_in = [(trajs[run][ti], s + 1) for ti in range(T) for s in range(S) if inside[ti, s]]
                agree = {}
                for f in CATS:
                    cnt = collections.Counter(str(Jr[(t, s)][f]) for t, s in steps_in if (t, s) in Jr)
                    if cnt: agree[f] = (cnt.most_common(1)[0][0], round(cnt.most_common(1)[0][1] / sum(cnt.values()), 2))
                n_agree = sum(1 for f, (v, sh) in agree.items() if sh >= 0.7 and f != "setting_time")
                pers.append(dict(cluster=k, visits=len(ex), trajectories=len(tr), steps_inside=int(inside.sum()), exits=int((inside[:, :-1] & ~inside[:, 1:]).sum()),
                                 hazard=float((inside[:, :-1] & ~inside[:, 1:]).sum() / inside.sum()) if inside.sum() else None, fields_agree_070=n_agree, agreement=agree,
                                 examples=sorted(ex, key=lambda e: -e[2])[:5]))
        R["cells"][run]["theme_atlas"] = dict(n_persistent=len(pers), n_shared_by_2plus=sum(1 for p in pers if p["trajectories"] >= 2), share_steps_inside=float(inside_any.mean()),
                                              multidim_shared=sum(1 for p in pers if p["trajectories"] >= 2 and p["fields_agree_070"] >= 3), clusters=pers)
        # scale on theme embeddings
        Y = X[:, 24:]; nn = []
        for t in range(T):
            others = np.delete(Y, t, 0).reshape(-1, Y.shape[-1]); nn.append((1 - Y[t] @ others.T).min(1))
        nn = np.concatenate(nn); R["cells"][run]["theme_scale"] = dict(nn_other_median=float(np.median(nn)), nn_other_within_015=float((nn <= 0.15).mean()),
                                                                     consecutive_median=float(np.median(1 - np.einsum("tsd,tsd->ts", X[:, 1:], X[:, :-1]))), vendi_last=vendi(X[:, -1]), vendi_first=vendi(X[:, 0]))
        # POST-HOC: seed identification in theme-sentence space (own step-0 theme is the nearest of the 20 step-0 themes), the memory curve of the gate
        from memory_curve import curve as _mcurve
        ident, _ = _mcurve(X); R["cells"][run]["theme_memory"] = dict(half_life=next((k for k in range(len(ident)) if ident[k] <= 0.5), None), ident_at={**{k: round(float(ident[k]), 2) for k in (1, 5, 10, 25, 50) if k < len(ident)}, 99: round(float(ident[-1]), 2)}, curve=[float(v) for v in ident])
        for p in pers:
            if p["trajectories"] < 2: continue
            md = [f"# Theme attractor {p['cluster']} in {run}: {p['visits']} persistent visits from {p['trajectories']} trajectories, {p['steps_inside']} steps inside, hazard {p['hazard']:.3f}", "",
                  "Field agreement inside (modal value, share): " + "; ".join(f"{f} = {v} ({sh})" for f, (v, sh) in p["agreement"].items()), ""]
            for t, s0, length, cens in p["examples"]:
                s = s0 + length // 2
                md.append(f"- traj {t} steps {s0}–{s0 + length - 1}{' (still there at the end)' if cens else ''}: **{Jr[(t, s)]['theme']}** — story: {recs_all[run][0][(t, s)]['story'][:300].replace(chr(10), ' ')} …")
            sheets.setdefault(p["cluster"], []).append("\n".join(md))
    for k, parts in sheets.items():
        (out_dir / f"theme_cluster_{k:02d}.md").write_text("\n\n".join(parts) + "\n", encoding="utf-8")

    # ---- 4. reliability (B7): second judge on the subsample; lead gender vs pronoun heuristic
    from sklearn.metrics import cohen_kappa_score
    pairs = collections.defaultdict(lambda: ([], []))
    for run in runs:
        J2, _ = load_judge(run, a.second)
        for key, j2 in J2.items():
            if key in J[run]:
                for f in CATS: pairs[f][0].append(str(J[run][key][f])); pairs[f][1].append(str(j2[f]))
    kappa = {f: (float(cohen_kappa_score(x, y)) if len(set(x) | set(y)) > 1 else 1.0, len(x)) for f, (x, y) in pairs.items()}
    R["reliability"] = dict(second_judge=a.second, n_pairs=len(pairs[CATS[0]][0]) if pairs else 0, kappa={f: k for f, (k, n) in kappa.items()},
                            n_fields_ge_060=sum(1 for f in VERDICT_FIELDS if f in kappa and kappa[f][0] >= 0.6))
    agree, n = 0, 0
    for run in runs:
        recs, T, S = recs_all[run]; names_ok = build_name_filter([recs[(t, s)]["story"] for t in T for s in S])
        for (t, s), j in J[run].items():
            g = audit_story(recs[(t, s)]["story"], names_ok)["lead_gender"]
            if g in ("female", "male"): n += 1; agree += (g == "female") == (j["lead_gender"] == "woman") if j["lead_gender"] != "other_or_unclear" else 0
    R["reliability"]["lead_gender_vs_pronoun_heuristic"] = dict(agree=agree / n if n else None, n=n)
    # POST-HOC: Haiku test-retest on the same stratified subsample (theme_judge.py --suffix haiku2), to separate loop change from judge noise.
    pairs2 = collections.defaultdict(lambda: ([], []))
    for run in runs:
        J3, _ = load_judge(run, "haiku2")
        for key, j3 in J3.items():
            if key in J[run]:
                for f in CATS: pairs2[f][0].append(str(J[run][key][f])); pairs2[f][1].append(str(j3[f]))
    if pairs2:
        R["reliability"]["test_retest_haiku"] = dict(n_pairs=len(pairs2[CATS[0]][0]), kappa={f: (float(cohen_kappa_score(x, y)) if len(set(x) | set(y)) > 1 else 1.0) for f, (x, y) in pairs2.items()},
                                                     agreement={f: float(np.mean([u == v for u, v in zip(x, y)])) for f, (x, y) in pairs2.items()})
        R["reliability"]["sonnet_agreement"] = {f: float(np.mean([u == v for u, v in zip(x, y)])) for f, (x, y) in pairs.items()}
        R["reliability"]["unclear_lead_age_share"] = {"haiku": float(np.mean([u == "unclear" for u in pairs["lead_age"][0]])), a.second: float(np.mean([v == "unclear" for v in pairs["lead_age"][1]]))}

    # ---- 5. codebook draft: k-means over a stratified sample of theme sentences (Claude labels the clusters by reading them; Brad reviews)
    samp = []
    for run in runs:
        d = Cache(run).arrays("minilm_theme"); Jr = J[run]
        keys = [k for k in Jr if k[1] >= 1]; idx = rng.choice(len(keys), size=min(40, len(keys)), replace=False)
        for i in idx: samp.append((run, keys[i], Jr[keys[i]]["theme"]))
    Xs = np.stack([Cache(r).arrays("minilm_theme")["X"][list(Cache(r).arrays("minilm_theme")["trajs"]).index(k[0]), k[1]] for r, k, _ in samp])
    kc = KMeans(n_clusters=20, n_init=5, random_state=0).fit(unit(Xs.astype(np.float64)))
    md = ["# Codebook draft from 240 theme sentences (40 per cell), k-means k 20 on MiniLM", "", "Each cluster lists its members; labels are to be written by hand (Claude proposes, Brad reviews) before the closed pass.", ""]
    for c in range(20):
        mem = [(r, k, th) for (r, k, th), lab in zip(samp, kc.labels_) if lab == c]
        md.append(f"## cluster {c} ({len(mem)} sentences; cells: {dict(collections.Counter(r for r, _, _ in mem))})")
        md += [f"- [{r} t{k[0]} s{k[1]}] {th}" for r, k, th in mem[:12]] + [""]
    (out_dir / "codebook.md").write_text("\n".join(md), encoding="utf-8")

    # ---- 6. hand-coding sample for Brad (stories only; key kept out of reports/)
    hc = []; per = max(1, a.handcode // len(runs))
    for run in runs:
        Jr = J[run]; keys = sorted(k for k in Jr if k[1] >= 1); idx = sorted(rng.choice(len(keys), size=min(per, len(keys)), replace=False))
        hc += [(run, keys[i]) for i in idx]
    hc = hc[:a.handcode]
    md = ["# Hand-coding sample (Brad): fill the schema for each story; the judge's answers are held separately", "",
          "Fields and allowed values: " + "; ".join(f"{f}: {' | '.join(v)}" for f, v in FIELDS.items()) + "; " + "; ".join(f"{b}: true | false" for b in BOOLS) + "; theme: one sentence, no names.", ""]
    key = {}
    for i, (run, (t, s)) in enumerate(hc, 1):
        md += [f"## story {i}", "", recs_all[run][0][(t, s)]["story"], "", "```", *(f"{f}: " for f in CATS), "theme: ", "```", ""]
        key[str(i)] = dict(run=run, traj=t, step=s, judge=J[run][(t, s)])
    (out_dir / "handcode_sample.md").write_text("\n".join(md), encoding="utf-8"); (CACHE / "e3_handcode_key.json").write_text(json.dumps(key, indent=1))

    # ---- 7. figure
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    for i, (run, model, loop) in enumerate(cells):
        c = R["cells"][run]; col = SERIES[i % len(SERIES)]; ls = "-" if loop == "E3-1" else "--"; lab = f"{model} {loop}"
        xs = [np.mean(w) for w in WINDOWS]
        eff = [eff_number(window_counts(J[run], recs_all[run][1], *w)) for w in WINDOWS]; axes[0].plot(xs, eff, ls, marker="o", color=col, label=lab, lw=1.5)
        ms = [max(window_counts(J[run], recs_all[run][1], *w).values()) / max(1, sum(window_counts(J[run], recs_all[run][1], *w).values())) if window_counts(J[run], recs_all[run][1], *w) else np.nan for w in WINDOWS]
        axes[1].plot(xs, ms, ls, marker="o", color=col, label=lab, lw=1.5); axes[2].plot(c["tuple"]["memory_curve"], ls, color=col, label=lab, lw=1.5)
    for ax, t, yl in zip(axes, ("effective number of (age × conflict × ending) tuples", "modal tuple share", "own step-0 tuple held (theme memory)"), ("exp(entropy)", "share of trajectory-steps", "share of trajectories")):
        ax.set_title(t, fontsize=10); ax.set_xlabel("step"); ax.set_ylabel(yl); ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=7, ncol=2)
    axes[2].axhline(0.5, color="gray", lw=0.8, ls=":"); fig.tight_layout(); fig.savefig(out_dir / "theme_curves.png", dpi=130); plt.close(fig)

    # ---- 8. verdicts
    V = {}; cl = R["cells"]
    e31 = [r for r, m, l in cells if l == "E3-1"]; e32 = [r for r, m, l in cells if l == "E3-2"]
    V["B1"] = {r: dict(ratio=cl[r]["tuple"]["ratio"], modal_late=cl[r]["tuple"]["modal_late"][1] if cl[r]["tuple"]["modal_late"] else None, modal_early=cl[r]["tuple"]["modal_early"][1] if cl[r]["tuple"]["modal_early"] else None, null=cl[r]["tuple"]["null_ratio_mean"],
                       holds=bool(cl[r]["tuple"]["ratio"] is not None and cl[r]["tuple"]["ratio"] <= 0.5 and cl[r]["tuple"]["modal_late"][1] >= 0.25 and cl[r]["tuple"]["modal_early"][1] <= 0.15)) for r in e31}
    V["B2"] = {r: dict(shared=cl[r].get("theme_atlas", {}).get("n_shared_by_2plus"), multidim=cl[r].get("theme_atlas", {}).get("multidim_shared")) for r in e31}
    V["B2"]["holds"] = bool(V["B2"].get("e3_1_sonnet", {}).get("shared", 0) >= 2 and V["B2"].get("e3_1_qwen", {}).get("shared", 0) >= 1 and all((v.get("multidim") or 0) == (v.get("shared") or 0) for k, v in V["B2"].items() if k != "holds" and v.get("shared")))
    V["B3"] = dict(modal_late={r: cl[r]["tuple"]["modal_late"] for r in runs}, js=R["b3"], holds=all(v["holds"] for v in R["b3"].values() if v["holds"] is not None) and len({cl[r]["tuple"]["modal_late"][0] for r in e31 if cl[r]["tuple"]["modal_late"]}) == len(e31))
    V["B4"] = dict(sonnet_place_change=cl.get("e3_1_sonnet", {}).get("fields", {}).get("setting_place", {}).get("entropy_change"),
                   present_share_early={r: cl[r]["fields"]["setting_time"]["windows"].get("1-10", {}).get("modal_share") for r in runs})
    V["B4"]["holds"] = bool(V["B4"]["sonnet_place_change"] is not None and abs(V["B4"]["sonnet_place_change"]) <= 0.2 and all((v or 0) >= 0.8 for v in V["B4"]["present_share_early"].values()))
    V["B5"] = {r: dict(js=cl[r]["tuple"]["js_early_late"], hold=cl[r]["tuple"]["share_hold_step1_at_last"]) for r in e32}
    V["B5"]["holds"] = all(v["js"] is not None and v["js"] <= 0.05 and v["hold"] >= 0.9 for k, v in V["B5"].items() if k != "holds")
    V["B6"] = {r: dict(half=cl[r]["tuple"]["memory_half_step"], at_last=cl[r]["tuple"]["memory_at_last"]) for r in e31}
    V["B6"]["holds"] = all(v["half"] is not None and v["half"] <= 25 for k, v in V["B6"].items() if k != "holds") and (V["B6"].get("e3_1_sonnet", {}).get("at_last") or 0) > 0.2
    rel = R["reliability"]; kp = rel["kappa"]
    V["B7"] = dict(n_fields_ge_060=rel["n_fields_ge_060"], gender=kp.get("lead_gender"), death=kp.get("death_present"), heuristic=rel["lead_gender_vs_pronoun_heuristic"]["agree"],
                   holds=bool(rel["n_pairs"] and rel["n_fields_ge_060"] >= 6 and (kp.get("lead_gender") or 0) >= 0.8 and (kp.get("death_present") or 0) >= 0.8 and (rel["lead_gender_vs_pronoun_heuristic"]["agree"] or 0) >= 0.85))
    R["verdicts"] = V
    (out_dir / "theme.json").write_text(json.dumps(R, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))

    # ---- 9. markdown
    md = ["# E3-B: theme-layer coding of the six text cells", "", f"Judge claude-haiku-5-5 (effort low, default sampling, D16) on every story; second judge claude-{a.second}-5-5 on a stratified subsample. Tuple = {' × '.join(TUPLE)}. Windows early {WIN_EARLY}, late {WIN_LATE}. Atlas on theme-sentence MiniLM embeddings: joint k-means k {a.k}, radius {a.radius}, hysteresis {a.exit_factor}, dwell ≥ {a.min_dwell}, ≥ {a.min_visits} visits.", "",
          "## Verdicts", "", "| prediction | result | numbers |", "|---|---|---|"]
    md.append(f"| B1 collapse in E3-1 (eff. tuples late/early ≤ 0.5; modal late ≥ 0.25, early ≤ 0.15) | " + ", ".join(f"{r.split('_')[-1]} {'holds' if V['B1'][r]['holds'] else 'fails'}" for r in e31) + " | " + "; ".join(f"{r.split('_')[-1]}: ratio {V['B1'][r]['ratio']:.2f} (null {V['B1'][r]['null']:.2f}), modal {V['B1'][r]['modal_early']:.2f} → {V['B1'][r]['modal_late']:.2f}" for r in e31) + " |")
    md.append(f"| B2 shared theme attractors (Sonnet ≥ 2, Qwen ≥ 1), multidimensional (≥ 3 fields ≥ 0.7) | {'holds' if V['B2']['holds'] else 'fails'} | " + "; ".join(f"{r.split('_')[-1]}: shared {V['B2'][r]['shared']}, of which multidimensional {V['B2'][r]['multidim']}" for r in e31) + " |")
    md.append(f"| B3 attractors belong to the model (modal tuples differ; JS across models > within model) | {'holds' if V['B3']['holds'] else 'fails'} | " + "; ".join(f"{r}: {cl[r]['tuple']['modal_late'][0]} {cl[r]['tuple']['modal_late'][1]:.2f}" for r in runs if cl[r]['tuple']['modal_late']) + "; JS " + json.dumps({m: {k: (round(v, 3) if isinstance(v, float) else {kk: round(vv, 3) for kk, vv in v.items() if vv is not None}) for k, v in d.items() if k != 'holds'} for m, d in R['b3'].items()}) + " |")
    md.append(f"| B4 setting place under Sonnet within ±20% entropy; setting time ≥ 80% present at 1–10 everywhere | {'holds' if V['B4']['holds'] else 'fails'} | Sonnet place entropy change {V['B4']['sonnet_place_change']}; present share 1–10 " + ", ".join(f"{r.split('_', 2)[-1]} {v:.2f}" for r, v in V['B4']['present_share_early'].items() if v is not None) + " |")
    md.append(f"| B5 rewrite cells do not move (JS early–late ≤ 0.05; ≥ 90% hold step-1 tuple at 99) | {'holds' if V['B5']['holds'] else 'fails'} | " + "; ".join(f"{r.split('_')[-1]}: JS {v['js']:.3f}, hold {v['hold']:.2f}" for r, v in V['B5'].items() if r != 'holds') + " |")
    md.append(f"| B6 theme memory: own step-0 tuple ≤ 0.5 by step 25; Sonnet > 0.2 at 99 | {'holds' if V['B6']['holds'] else 'fails'} | " + "; ".join(f"{r.split('_')[-1]}: half {v['half']}, at 99 {v['at_last']:.2f}" for r, v in V['B6'].items() if r != 'holds') + " |")
    md.append(f"| B7 reliability (≥ 6 of 10 fields κ ≥ 0.6; gender and death ≥ 0.8; heuristic agreement ≥ 0.85) | {'holds' if V['B7']['holds'] else 'fails'} | n {rel['n_pairs']}; fields ≥ 0.6: {rel['n_fields_ge_060']}; κ " + ", ".join(f"{f} {k:.2f}" for f, k in kp.items()) + f"; gender vs pronouns {V['B7']['heuristic']:.2f} |" if rel['n_pairs'] else "| B7 reliability | not yet (second judge not run) | |")
    md += ["", "## Tuple distribution per cell", "", "| cell | judged (malformed) | eff. tuples 1–10 → 50–99 (null ratio) | modal tuple 50–99 (share) | top-5 late | tuple attractors (ii): tuple, trajectories, runs | hold step-1 at 99 | theme memory half / at 99 |", "|---|---|---|---|---|---|---|---|"]
    for r in runs:
        c = cl[r]; t = c["tuple"]
        md.append(f"| {r} | {c['n_judged']} ({c['n_malformed']}) | {t['eff_early']:.1f} → {t['eff_late']:.1f} ({t['null_ratio_mean']:.2f}) | {t['modal_late'][0]} ({t['modal_late'][1]:.2f}) | " + "; ".join(f"{'/'.join(k)} {v}" for k, v in t["top5_late"]) + " | " +
                  "; ".join(f"{'/'.join(d['tuple'])} {d['trajectories']}t {d['runs']}r" for d in t["attractors_ii"][:4]) + f" | {t['share_hold_step1_at_last']:.2f} | {t['memory_half_step']} / {t['memory_at_last']:.2f} |")
    md += ["", "## Per-field modal value and share, steps 1–10 → 50–99", "", "| cell | " + " | ".join(CATS) + " |", "|---|" + "---|" * len(CATS)]
    for r in runs:
        row = []
        for f in CATS:
            w = cl[r]["fields"][f]["windows"]; e, l = w.get("1-10"), w.get("90-99") or w.get("76-89")
            row.append(f"{e['modal']} {e['modal_share']:.2f} → {l['modal']} {l['modal_share']:.2f}" if e and l else "–")
        md.append(f"| {r} | " + " | ".join(row) + " |")
    md += ["", "## Theme-sentence atlas and scale", "", "| cell | persistent | shared by ≥ 2 traj | multidimensional | steps inside | nn-other median | within 0.15 | consecutive | Vendi first → last |", "|---|---|---|---|---|---|---|---|---|"]
    for r in runs:
        ta, ts = cl[r].get("theme_atlas"), cl[r].get("theme_scale")
        if ta: md.append(f"| {r} | {ta['n_persistent']} | {ta['n_shared_by_2plus']} | {ta['multidim_shared']} | {ta['share_steps_inside']:.2f} | {ts['nn_other_median']:.3f} | {ts['nn_other_within_015']:.2f} | {ts['consecutive_median']:.3f} | {ts['vendi_first']:.1f} → {ts['vendi_last']:.1f} |")
    md += ["", "Shared theme attractors: `theme_cluster_NN.md` (theme sentences, field agreement, story openings). Codebook draft: `codebook.md`. Hand-coding sample for Brad: `handcode_sample.md`. Figure: `theme_curves.png`.", ""]
    # POST-HOC section
    md += ["## Post-hoc checks (added after the verdicts above were read; not predictions)", "",
           "**Tuple B = lead_gender × conflict_type × ending_valence.** lead_age is the judge's weakest field: on the reliability subsample Haiku codes it 'unclear' far more often than Sonnet does (shares below), so the predicted tuple is dominated by 'unclear' in the 7B cells. Tuple B uses three fields with κ ≥ 0.63.", "",
           "| cell | eff. tuples 1–10 → 50–99 (null ratio) | modal late (share) | top-3 late | JS early–late | hold step-1 at 99 | memory half / at 99 |", "|---|---|---|---|---|---|---|"]
    for r in runs:
        t = cl[r].get("tuple_b")
        if t: md.append(f"| {r} | {t['eff_early']:.1f} → {t['eff_late']:.1f} ({t['null_ratio_mean']:.2f}) | {'/'.join(t['modal_late'][0])} ({t['modal_late'][1]:.2f}) | " + "; ".join(f"{'/'.join(k)} {v}" for k, v in t["top3_late"]) + f" | {t['js_early_late']:.3f} | {t['share_hold_step1_at_last']:.2f} | {t['memory_half_step']} / {t['memory_at_last']:.2f} |")
    md += ["", "**Seed memory in theme-sentence space** (own step-0 theme nearest among the 20 step-0 themes; the gate's memory curve on the judge's sentences): " + "; ".join(f"{r} half-life {cl[r]['theme_memory']['half_life']}, at 10 / 50 / 99 {cl[r]['theme_memory']['ident_at'].get(10)} / {cl[r]['theme_memory']['ident_at'].get(50)} / {cl[r]['theme_memory']['ident_at'].get(99)}" for r in runs if cl[r].get("theme_memory")) + "."]
    tr = rel.get("test_retest_haiku")
    if tr:
        md += ["", f"**Judge noise.** Haiku test-retest on the same {tr['n_pairs']} stories (κ / raw agreement): " + ", ".join(f"{f} {tr['kappa'][f]:.2f}/{tr['agreement'][f]:.2f}" for f in CATS) + ".",
               "Haiku–Sonnet raw agreement: " + ", ".join(f"{f} {rel['sonnet_agreement'][f]:.2f}" for f in CATS) + f". Share of lead_age coded 'unclear' on the subsample: Haiku {rel['unclear_lead_age_share']['haiku']:.2f}, {a.second} {rel['unclear_lead_age_share'][a.second]:.2f}.", ""]
    (out_dir / "theme.md").write_text("\n".join(md), encoding="utf-8"); print("\n".join(md[:14]))


if __name__ == "__main__":
    main()
