"""E3-DS (predictions.md "E3-DS", 2026-11-05): grade the Sonnet theme-bottleneck cell against DS1-DS4.

    .venv/bin/python analysis/e3ds_report.py [--run e3_d_sonnet] [--haiku-d e3_d_haiku] [--handread-shared N]

Inputs (all produced before this script runs): the cell's records in runs/<run>/, its minilm and minilm_anon caches
(analysis/e3s_report.py --d1 writes them), the Haiku theme judge (analysis/cache/<run>/theme_judge.jsonl) and the
Haiku moral judge with Haiku D's five morals (analysis/cache/<run>/moral_judge.jsonl, analysis/moral_judge.py --run <run>).
--handread-shared is the number of the hand-read Sonnet menu's top-five morals that are also in Haiku's five
(reports/e3/ds_handread.md, written before the moral-judge shares were read). Nothing here feeds any loop.

DS4's "confession-and-forgiveness" moral is operationalised by a keyword rule on the late theme sentences (steps 50-99),
declared here rather than tuned: CONFESS below. Output: reports/e3/ds.{md,json}.
"""
import argparse, collections, json, pathlib, re, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, CACHE, Cache, cpu_only  # noqa: E402
from e3_report import load_records, unit  # noqa: E402
from e3s_report import atlas_pairs, k_for, half_life, ATLAS  # noqa: E402
from gravity import visits  # noqa: E402
from moral_judge import MORALS  # noqa: E402

OUT = ROOT / "reports" / "e3"; LATE = range(50, 100)
CONFESS = re.compile(r"\b(confess|confession|honest|honesty|truth|forgiv|secret|lie|lies|lied|lying|deceit|deception|wrong)\w*", re.I)
FAMILY = {"parent_or_grandparent", "sibling", "partner_or_spouse", "child"}


def load_jsonl(path, key):
    out = {}
    if not path.exists(): return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line); v = d.get(key)
            if v is not None: out[(d["traj"], d["step"])] = v
    return out


def dwell_diag(L):
    """L [T,S] labels (-1 free): clusters visited per trajectory (median), median visit length, share of free steps."""
    nclu = [len({int(c) for c in row if c >= 0}) for row in L]
    lens = [l for row in L for c in {int(c) for c in row if c >= 0} for l, _ in visits(row == c)]
    return dict(clusters_per_traj_median=float(np.median(nclu)), dwell_median=float(np.median(lens)) if lens else None, free_share=float((L < 0).mean()),
                dwell_ge5_share=float(np.mean([l >= ATLAS["min_dwell"] for l in lens])) if lens else None)


def main():
    cpu_only(); ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="e3_d_sonnet"); ap.add_argument("--haiku-d", default="e3_d_haiku"); ap.add_argument("--mistral-d", default="e3_d_mistral")
    ap.add_argument("--handread-shared", type=int, default=None, help="hand-read Sonnet top-5 morals that are in Haiku's five (reports/e3/ds_handread.md)")
    a = ap.parse_args(); run = a.run
    recs, T, S = load_records(run); cache = Cache(run)
    X = cache.load("minilm")["X"].astype(np.float64); Xa = cache.load("minilm_anon")["X"].astype(np.float64)
    R = dict(run=run, params=dict(atlas=ATLAS, confess_regex=CONFESS.pattern, family=sorted(FAMILY)), cells={})

    # ---- DS2: dynamics (own atlases, raw and anonymised, k for 20 x 99 steps) and dwell diagnostics, for this cell and the two reference D cells
    for r in (run, a.haiku_d, a.mistral_d):
        if not (ROOT / "runs" / r).exists() or Cache(r).load("minilm_anon") is None: continue
        Xr = Cache(r).load("minilm")["X"].astype(np.float64); Xra = Cache(r).load("minilm_anon")["X"].astype(np.float64)
        h, ident = half_life(Xr); k = k_for(Xr.shape[0] * (Xr.shape[1] - 1)); cell = dict(half_life=h, k=k)
        for tag, Y in (("raw", unit(Xr[:, 1:])), ("anon", unit(Xra[:, 1:]))):
            at = atlas_pairs(Y, k); cell[tag] = dict(persistent=at["persistent"], shared=at["shared"], n_sharing_pairs=at["n_sharing_pairs"], n_pairs=at["n_pairs"], rate=at["rate"],
                                                     W_hat=at["W_hat"], max_mult=at["max_mult"], inside_share=at["inside_share"], clusters=[(int(c), ts, nv) for c, ts, nv in at["clusters"] if len(ts) >= 2],
                                                     dwell=dwell_diag(at["labels"]))
        R["cells"][r] = cell; print(f"[{r}] half-life {h}; anon shared {cell['anon']['shared']} rate {cell['anon']['rate']:.3f}; dwell raw {cell['raw']['dwell']}", flush=True)
    c = R["cells"][run]
    ds2 = dict(half_life=c["half_life"], dwell_median_raw=c["raw"]["dwell"]["dwell_median"], clusters_per_traj_raw=c["raw"]["dwell"]["clusters_per_traj_median"], free_share_raw=c["raw"]["dwell"]["free_share"],
               anon_shared=c["anon"]["shared"], anon_rate=c["anon"]["rate"])
    ds2["holds"] = bool(ds2["half_life"] <= 3 and ds2["dwell_median_raw"] == 1 and 7 <= ds2["clusters_per_traj_raw"] <= 12 and ds2["free_share_raw"] >= 0.6 and ds2["anon_shared"] >= 5 and 0.10 <= ds2["anon_rate"] <= 0.30)

    # ---- DS3: judge field shares, steps 50-99 (this cell and the two reference D cells)
    shares = {}
    for r in (run, a.haiku_d, a.mistral_d):
        J = load_jsonl(CACHE / r / "theme_judge.jsonl", "judge"); late = [j for (t, s), j in J.items() if s in LATE]
        if not late: continue
        n = len(late)
        shares[r] = dict(n=n, interpersonal_plus_internal=sum(j["conflict_type"] in ("interpersonal", "internal") for j in late) / n,
                         home_plus_small_town=sum(j["setting_place"] in ("home_interior", "small_town_or_village") for j in late) / n,
                         hopeful=sum(j["ending_valence"] == "hopeful" for j in late) / n, family_secondary=sum(j["secondary_character"] in FAMILY for j in late) / n,
                         social=sum(j["conflict_type"] == "social_or_community" for j in late) / n, artist_lead=sum(j["lead_role_class"] == "artist_or_craftsperson" for j in late) / n,
                         woman=sum(j["lead_gender"] == "woman" for j in late) / n, death=sum(j["death_present"] is True for j in late) / n, reconciliation=sum(j["reconciliation_present"] is True for j in late) / n,
                         conflict=dict(collections.Counter(j["conflict_type"] for j in late).most_common()), setting=dict(collections.Counter(j["setting_place"] for j in late).most_common()),
                         secondary=dict(collections.Counter(j["secondary_character"] for j in late).most_common()), lead_role=dict(collections.Counter(j["lead_role_class"] for j in late).most_common(6)),
                         modal_tuple=collections.Counter((j["lead_age"], j["conflict_type"], j["ending_valence"]) for j in late).most_common(1)[0])
    R["judge_shares"] = shares; s = shares.get(run)
    ds3 = dict(interpersonal_plus_internal=s["interpersonal_plus_internal"], home_plus_small_town=s["home_plus_small_town"], hopeful=s["hopeful"], family_secondary=s["family_secondary"]) if s else None
    if ds3: ds3["holds"] = bool(ds3["interpersonal_plus_internal"] >= 0.6 and ds3["home_plus_small_town"] >= 0.5 and ds3["hopeful"] >= 0.8 and ds3["family_secondary"] >= 0.4)

    # ---- DS1 / DS4: Haiku moral judge on this cell's late stories; confession keyword rule on the late theme sentences
    M = load_jsonl(CACHE / run / "moral_judge.jsonl", "moral"); late_m = {k: v for k, v in M.items() if k[1] in LATE}; n = len(late_m)
    cnt = collections.Counter(late_m.values()); overall = {int(k): cnt[k] / n for k in range(6)} if n else {}
    fit = 1 - overall.get(0, 1.0) if n else None; above = [k for k in range(1, 6) if overall.get(k, 0) > 0.10]
    ds1 = dict(n_judged=n, fit_share=fit, shares={MORALS[k][:40]: round(overall[k], 3) for k in range(1, 6)} if n else None, none_share=overall.get(0), morals_above_010=above,
               handread_shared=a.handread_shared)
    ds1["holds"] = bool(fit is not None and fit >= 0.5 and len(above) >= 2 and (a.handread_shared is None or a.handread_shared >= 2))
    ds1["judge_clause_holds"] = bool(fit is not None and fit >= 0.5 and len(above) >= 2)
    sents = {(t, s): recs[(t, s)].get("summary") or "" for t in T for s in S if s in LATE}
    conf = {k: bool(CONFESS.search(v)) for k, v in sents.items()}; conf_share = float(np.mean(list(conf.values())))
    conf_none = float(np.mean([conf[k] for k, m in late_m.items() if m == 0 and k in conf])) if any(m == 0 for m in late_m.values()) else None
    none_sents = [sents[k] for k, m in sorted(late_m.items()) if m == 0 and k in sents]
    ref_conf = {}
    for r in (a.haiku_d, a.mistral_d):
        if (ROOT / "runs" / r).exists():
            rr, rT, rS = load_records(r); ref_conf[r] = float(np.mean([bool(CONFESS.search(rr[(t, s)].get("summary") or "")) for t in rT for s in rS if s in LATE]))
    ds4 = dict(confession_share_late=conf_share, confession_share_among_none=conf_none, n_none=len(none_sents), reference_confession_share=ref_conf, none_sentences_sample=none_sents[:40])
    ds4["holds"] = bool(conf_share >= 0.15 and conf_none is not None and conf_none >= 0.5)
    R["verdicts"] = dict(DS1=ds1, DS2=ds2, DS3=ds3, DS4=ds4)
    (OUT / "ds.json").write_text(json.dumps(R, indent=1, default=float))

    L = [f"# E3-DS: Sonnet theme-bottleneck cell `{run}` against predictions.md \"E3-DS\" (2026-11-05)", "",
         f"**DS1 (shared menu with Haiku): {'holds' if ds1['holds'] else 'fails'}** — Haiku moral judge on {n} late stories: fit to one of Haiku's five morals {fit if fit is None else round(fit, 2)} (needs ≥ 0.5), "
         f"morals above 0.10: {len(above)} (needs ≥ 2); hand-read top-five overlap {a.handread_shared} (needs ≥ 2).",
         "", "| Haiku D moral | share of Sonnet late stories |", "|---|---|"] + [f"| {MORALS[k]} | {overall.get(k, 0):.2f} |" for k in range(1, 6)] + [f"| none of these | {overall.get(0, 0):.2f} |", "",
         f"**DS2 (D dynamics): {'holds' if ds2['holds'] else 'fails'}** — half-life {ds2['half_life']} (≤ 3), raw median dwell {ds2['dwell_median_raw']} (1), clusters per trajectory {ds2['clusters_per_traj_raw']} (7–12), "
         f"free steps {ds2['free_share_raw']:.2f} (≥ 0.6), anonymised shared wells {ds2['anon_shared']} (≥ 5), rate {ds2['anon_rate']:.3f} (0.10–0.30).", ""]
    if ds3: L += [f"**DS3 (domestic shape): {'holds' if ds3['holds'] else 'fails'}** — interpersonal + internal {ds3['interpersonal_plus_internal']:.2f} (≥ 0.6), home + small town {ds3['home_plus_small_town']:.2f} (≥ 0.5), "
                  f"hopeful {ds3['hopeful']:.2f} (≥ 0.8), family secondary {ds3['family_secondary']:.2f} (≥ 0.4).", ""]
    else: L += ["**DS3**: theme judge not run yet.", ""]
    L += [f"**DS4 (confession moral): {'holds' if ds4['holds'] else 'fails'}** — late theme sentences matching the confession/honesty rule {conf_share:.2f} (≥ 0.15); among stories the Haiku judge scored \"none\" {conf_none if conf_none is None else round(conf_none, 2)} (≥ 0.5, i.e. the top none-moral); "
          f"reference D cells: " + ", ".join(f"{r} {v:.2f}" for r, v in ref_conf.items()) + ".", "",
          "## Cells", "", "| cell | half-life | raw shared / rate | anon shared / rate / W-hat / max mult | clusters per traj / median dwell (raw) | free steps (raw) | anon dwell ≥ 5 share |", "|---|---|---|---|---|---|---|"]
    for r, cc in R["cells"].items():
        L.append(f"| {r} | {cc['half_life']} | {cc['raw']['shared']} / {cc['raw']['rate']:.3f} | {cc['anon']['shared']} / {cc['anon']['rate']:.3f} / {cc['anon']['W_hat'] if cc['anon']['W_hat'] is None else round(cc['anon']['W_hat'], 1)} / {cc['anon']['max_mult']} | "
                 f"{cc['raw']['dwell']['clusters_per_traj_median']:.0f} / {cc['raw']['dwell']['dwell_median']} | {cc['raw']['dwell']['free_share']:.2f} | {cc['anon']['dwell']['dwell_ge5_share']:.2f} |")
    if shares:
        L += ["", "## Judge field shares, steps 50–99", "", "| field | " + " | ".join(shares) + " |", "|---|" + "---|" * len(shares)]
        for f in ("interpersonal_plus_internal", "home_plus_small_town", "hopeful", "family_secondary", "social", "artist_lead", "woman", "death", "reconciliation"):
            L.append(f"| {f} | " + " | ".join(f"{shares[r][f]:.2f}" for r in shares) + " |")
        L.append("| modal tuple | " + " | ".join(f"{' × '.join(shares[r]['modal_tuple'][0])} {shares[r]['modal_tuple'][1] / shares[r]['n']:.2f}" for r in shares) + " |")
        for f in ("conflict", "setting", "secondary", "lead_role"):
            L.append(f"| {f} | " + " | ".join(", ".join(f"{k} {v / shares[r]['n']:.2f}" for k, v in list(shares[r][f].items())[:4]) for r in shares) + " |")
    L += ["", "## Theme sentences the Haiku judge scored as none of Haiku's five (first 40 of " + str(len(none_sents)) + ")", ""] + [f"- {x}" for x in none_sents[:40]]
    (OUT / "ds.md").write_text("\n".join(L) + "\n"); print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
