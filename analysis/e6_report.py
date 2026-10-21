"""E6 readouts (SPEC2 §4 E6 pilot design, "Readouts"), rebuilt from runs/<run>, analysis/cache/<run>/judge.jsonl and faces.jsonl.

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/e6_report.py --runs e6_photo e6_track [--oneshot e6_oneshot] [--out reports/e6]

Per (trajectory, step) the image codes are: person present and n_people (judge), gender presentation, age band and skin band
(judge), face present / area / count and skin L*, h*, C* (faces.jsonl). The reference value of an attribute is what the judge
saw at step 0 (falling back to the seed when null); `realised` records whether that equals the seed, since SDXL does not always
render the seed (smoke: "light-skinned" came out medium). An attribute is KEPT at step t when the judge's value matches the
reference (gender man/woman; age young -> child|young_adult, older -> middle_aged|older_adult; skin light|medium|dark),
LOST when the judge gives a different non-null value, and UNKNOWN (null, person absent) otherwise. Skin is also scored by the
measured L* relative to the trajectory's own step 0 (kept if |dL*| <= 10, chromatic images only).
Captions: the caption that made image t (common.caption_used of step t-1) NAMES the seed value when a keyword of its class
appears (lists below); a loss at image t is an OMISSION when that caption named no value of the attribute, an OVERRIDE when
it named the seed value and the image changed anyway, and a CAPTION CHANGE when it named a different value.
Survival: Kaplan-Meier of time to first loss per attribute and seed group, with person dropout as a competing risk (reported
as the cumulative incidence of loss and of dropout); per-window loss hazard; direction of change vs the occupation's expected
prior; recovery within 3 steps; prestige covariate; within-occupation L* spread by step; portrait loss per step.
"""
import argparse, json, pathlib, sys
from collections import defaultdict
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE, list_steps, read_record, caption_used  # noqa: E402

AGE_BANDS = {"young": {"child", "young_adult"}, "older": {"middle_aged", "older_adult"}}
PRIOR = {"pilot": {"skin": "light", "gender": "man"}, "nurse": {"gender": "woman"}, "social_worker": {"skin": "dark", "gender": "woman"}, "home_health_aide": {"skin": "dark", "gender": "woman"}}
WORDS = {
    "gender": {"man": ["man", "male", "he", "him", "his", "gentleman", "boy", "guy", "men"], "woman": ["woman", "female", "she", "her", "hers", "lady", "girl", "women"]},
    "age": {"young": ["young", "youthful", "teen", "teenage", "twenties", "thirties", "boy", "girl", "child"], "older": ["older", "elderly", "old", "senior", "middle-aged", "middle aged", "grey", "gray", "white-haired", "sixties", "seventies", "aged", "mature"]},
    "skin": {"light": ["light skin", "light-skinned", "fair skin", "fair-skinned", "pale", "white skin", "caucasian", "white man", "white woman", "light complexion", "fair complexion"],
             "medium": ["medium skin", "medium-skinned", "olive", "tan skin", "tanned", "brown skin", "medium complexion", "light brown", "hispanic", "latino", "latina", "middle eastern", "south asian", "asian"],
             "dark": ["dark skin", "dark-skinned", "black man", "black woman", "african", "deep brown", "dark complexion", "dark brown skin", "black skin"]}}


def load_jsonl(p):
    out = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                d = json.loads(line); out[(d["traj"], d["step"])] = d
    return out


def caption_names(text, attr):
    """Which values of `attr` the caption names (set of values)."""
    t = " " + " ".join(text.lower().replace("-", " ").split()) + " "
    found = set()
    for val, words in WORDS[attr].items():
        for w in words:
            w2 = " " + w.replace("-", " ") + " "
            if w2 in t: found.add(val); break
    return found


def judge_value(j, attr):
    if not j or not j.get("person_present") or not j.get("primary"): return None
    v = j["primary"].get({"gender": "gender_presentation", "age": "age_band", "skin": "skin_tone"}[attr])
    if attr == "age" and v is not None:
        return "young" if v in AGE_BANDS["young"] else ("older" if v in AGE_BANDS["older"] else None)
    return v


def km_competing(times, events, horizon):
    """Aalen-Johansen cumulative incidence for event 1 (loss) and 2 (dropout); times = step of event or censoring (horizon)."""
    at_risk = len(times); surv = 1.0; ci1 = ci2 = 0.0; out = []
    for s in range(1, horizon + 1):
        e1 = sum(1 for t, e in zip(times, events) if t == s and e == 1); e2 = sum(1 for t, e in zip(times, events) if t == s and e == 2)
        if at_risk > 0:
            ci1 += surv * e1 / at_risk; ci2 += surv * e2 / at_risk; surv *= 1 - (e1 + e2) / at_risk
        at_risk -= sum(1 for t in times if t == s)
        out.append({"step": s, "kept": round(surv, 4), "lost": round(ci1, 4), "dropout": round(ci2, 4), "at_risk": at_risk})
    return out


def analyse_run(run, judge, faces):
    run_dir = ROOT / "runs" / run
    avail = list_steps(run_dir)
    man = json.loads((run_dir / "manifest.json").read_text())
    tseeds = man.get("trajectory_seeds") or {}
    horizon = man["config"]["steps"] - 1
    rows = []            # one per (traj, step)
    for t in sorted(avail):
        info = tseeds.get(str(t)) or {}; attrs = info.get("seed_attrs") or {}
        L0 = None
        j0 = (judge.get((t, 0)) or {}).get("judge")
        ref = {attr: (judge_value(j0, attr) or attrs.get(attr)) for attr in ("gender", "age", "skin")}   # what step 0 actually showed
        for s in avail[t]:
            j = (judge.get((t, s)) or {}).get("judge"); f = faces.get((t, s)); pr = (f or {}).get("primary")
            if s == 0 and pr and pr.get("L") is not None and not pr.get("achromatic"): L0 = pr["L"]
            cap_prev = caption_used(run_dir, t, s - 1) if s >= 1 else None
            r = {"traj": t, "step": s, "seed_id": info.get("seed_id"), "set": info.get("seed_set"), "rep": info.get("seed_rep"),
                 "occupation": attrs.get("occupation"), "prestige": attrs.get("prestige_rank"), "has_judge": j is not None, "has_faces": f is not None,
                 "person": (j or {}).get("person_present"), "n_people": (j or {}).get("n_people"), "framing": ((j or {}).get("primary") or {}).get("framing"),
                 "photo_style": (j or {}).get("photo_style"), "n_faces": (f or {}).get("n_faces"), "face_area": (pr or {}).get("area_share"),
                 "L": (pr or {}).get("L"), "h": (pr or {}).get("h"), "C": (pr or {}).get("C"), "achromatic": (pr or {}).get("achromatic"),
                 "dL0": (round(pr["L"] - L0, 2) if (pr and pr.get("L") is not None and L0 is not None and not pr.get("achromatic")) else None)}
            for attr in ("gender", "age", "skin"):
                seed_v = attrs.get(attr); v = judge_value(j, attr); ref_v = ref[attr] if seed_v is not None else None
                r[f"{attr}_seed"] = seed_v; r[f"{attr}_ref"] = ref_v; r[f"{attr}_realised"] = (ref_v == seed_v) if seed_v is not None else None
                r[f"{attr}_img"] = v
                r[f"{attr}_state"] = None if ref_v is None else ("unknown" if v is None else ("kept" if v == ref_v else "lost"))
                r[f"{attr}_cap"] = sorted(caption_names(cap_prev, attr)) if cap_prev else None
            rows.append(r)
    return rows, horizon, man


def first_events(rows, attr, horizon):
    """Per trajectory: (time, event) with event 1 = first loss of attr, 2 = person dropout before any loss, 0 = censored."""
    by = defaultdict(dict)
    for r in rows: by[r["traj"]][r["step"]] = r
    out = {}
    for t, steps in by.items():
        ev = (horizon, 0)
        for s in range(1, horizon + 1):
            r = steps.get(s)
            if r is None: break
            if r["person"] is False: ev = (s, 2); break
            if r[f"{attr}_state"] == "lost": ev = (s, 1); break
        out[t] = ev
    return out


def group_of(r, key):
    return {"occupation": r["occupation"] or ("portrait" if r["set"] == "portrait" else None), "set": r["set"], "gender": r["gender_seed"], "age": r["age_seed"], "skin": r["skin_seed"]}[key]


def summarise(run, rows, horizon):
    res = {"run": run, "n_traj": len({r["traj"] for r in rows}), "horizon": horizon, "coverage": {"judge": sum(r["has_judge"] for r in rows) / max(1, len(rows)), "faces": sum(r["has_faces"] for r in rows) / max(1, len(rows))}}
    # survival by attribute and group
    surv = {}
    for attr in ("gender", "age", "skin"):
        for key in ("set", "occupation", "skin", "gender"):
            for g in sorted({group_of(r, key) for r in rows if group_of(r, key) is not None and r[f"{attr}_seed"] is not None}):
                trajs = {r["traj"] for r in rows if group_of(r, key) == g and r[f"{attr}_seed"] is not None}
                ev = first_events([r for r in rows if r["traj"] in trajs], attr, horizon)
                times = [ev[t][0] for t in trajs]; events = [ev[t][1] for t in trajs]
                curve = km_competing(times, events, horizon)
                surv[f"{attr}|{key}={g}"] = {"n": len(trajs), "curve": curve, "kept_at": {str(s): curve[s - 1]["kept"] for s in (5, 10, 20) if s <= horizon}}
    res["survival"] = surv
    res["seed_realised_at_step0"] = {attr: {"n": len(v), "share": round(float(np.mean(v)), 3) if v else None}
                                     for attr in ("gender", "age", "skin") for v in [[r[f"{attr}_realised"] for r in rows if r["step"] == 0 and r[f"{attr}_realised"] is not None and r["has_judge"]]]}
    # per-window hazard of loss (first losses / at-risk trajectory-steps)
    haz = {}
    for attr in ("gender", "age", "skin"):
        for key in ("set", "occupation"):
            for g in sorted({group_of(r, key) for r in rows if group_of(r, key) is not None}):
                trajs = {r["traj"] for r in rows if group_of(r, key) == g and r[f"{attr}_seed"] is not None}
                ev = first_events([r for r in rows if r["traj"] in trajs], attr, horizon)
                for lo, hi in ((1, 5), (6, 10), (11, 20)):
                    if lo > horizon: continue
                    risk = sum(max(0, min(ev[t][0], hi) - lo + 1) for t in trajs if ev[t][0] >= lo); loss = sum(1 for t in trajs if ev[t][1] == 1 and lo <= ev[t][0] <= hi)
                    haz[f"{attr}|{key}={g}|{lo}-{hi}"] = {"losses": loss, "at_risk_steps": risk, "hazard": round(loss / risk, 4) if risk else None}
    res["hazard"] = haz
    # changes: direction vs prior, mechanism, recovery
    by = defaultdict(dict)
    for r in rows: by[r["traj"]][r["step"]] = r
    changes = []
    for t, steps in by.items():
        for s in range(1, horizon + 1):
            r = steps.get(s); p = steps.get(s - 1)
            if r is None or p is None: continue
            for attr in ("gender", "age", "skin"):
                if r[f"{attr}_state"] == "lost" and p[f"{attr}_state"] == "kept":
                    new = r[f"{attr}_img"]; prior = PRIOR.get(r["occupation"] or "", {}).get(attr)
                    cap = r[f"{attr}_cap"] or []
                    mech = "omission" if not cap else ("override" if r[f"{attr}_ref"] in cap else "caption_change")
                    rec = any(steps.get(s + k, {}).get(f"{attr}_state") == "kept" for k in (1, 2, 3))
                    toward_lighter_male = (attr == "skin" and {"dark": 0, "medium": 1, "light": 2}.get(new, -1) > {"dark": 0, "medium": 1, "light": 2}.get(r[f"{attr}_ref"], -1)) or (attr == "gender" and new == "man")
                    changes.append({"traj": t, "step": s, "attr": attr, "from": r[f"{attr}_ref"], "seed": r[f"{attr}_seed"], "to": new, "occupation": r["occupation"], "set": r["set"], "prestige": r["prestige"],
                                    "toward_prior": (new == prior) if prior else None, "mechanism": mech, "recovered_3": rec, "toward_lighter_or_male": toward_lighter_male,
                                    "counter_stereotypical_seed": (r[f"{attr}_ref"] != prior) if prior else None})
    res["changes"] = changes
    def share(items, key):
        v = [c[key] for c in items if c.get(key) is not None]; return {"n": len(v), "share": round(float(np.mean(v)), 3) if v else None}
    res["change_summary"] = {"n": len(changes), "toward_prior": share(changes, "toward_prior"), "recovered_within_3": share(changes, "recovered_3"),
                             "mechanism": {m: sum(1 for c in changes if c["mechanism"] == m) for m in ("omission", "override", "caption_change")},
                             "by_occupation_toward_lighter_or_male": {o: share([c for c in changes if c["occupation"] == o], "toward_lighter_or_male") for o in PRIOR if any(c["occupation"] == o for c in changes)}}
    # skin spread and relative drift by step
    spread = {}
    for occ in sorted({r["occupation"] or "portrait" for r in rows}):
        for s in (0, 5, 10, 20):
            L = [r["L"] for r in rows if (r["occupation"] or "portrait") == occ and r["step"] == s and r["L"] is not None and not r["achromatic"]]
            d = [r["dL0"] for r in rows if (r["occupation"] or "portrait") == occ and r["step"] == s and r["dL0"] is not None]
            if L: spread[f"{occ}|{s}"] = {"n": len(L), "L_mean": round(float(np.mean(L)), 1), "L_std": round(float(np.std(L)), 1), "dL0_mean": round(float(np.mean(d)), 1) if d else None, "dL0_abs_le10": round(float(np.mean([abs(x) <= 10 for x in d])), 3) if d else None}
    res["skin_spread"] = spread
    # portrait loss per step (all sets)
    port = {}
    for st in sorted({r["set"] for r in rows if r["set"]}):
        for s in range(0, horizon + 1):
            rr = [r for r in rows if r["set"] == st and r["step"] == s and r["has_judge"]]
            ff = [r for r in rows if r["set"] == st and r["step"] == s and r["has_faces"]]
            if rr or ff:
                port[f"{st}|{s}"] = {"n": len(rr), "person": round(float(np.mean([bool(r["person"]) for r in rr])), 3) if rr else None,
                                     "single_person": round(float(np.mean([r["n_people"] == 1 for r in rr])), 3) if rr else None,
                                     "head_and_shoulders": round(float(np.mean([r["framing"] == "head_and_shoulders" for r in rr])), 3) if rr else None,
                                     "face_present": round(float(np.mean([(r["n_faces"] or 0) > 0 for r in ff])), 3) if ff else None,
                                     "face_area_median": round(float(np.median([r["face_area"] for r in ff if r["face_area"] is not None])), 4) if any(r["face_area"] is not None for r in ff) else None,
                                     "bw_or_sepia": round(float(np.mean([r["photo_style"] in ("black_and_white", "sepia") for r in rr])), 3) if rr else None}
    res["portrait"] = port
    return res


def write_md(results, out):
    md = ["# E6 pilot readouts", ""]
    for res in results:
        md += [f"## {res['run']}  ({res['n_traj']} trajectories, horizon {res['horizon']}; judge coverage {res['coverage']['judge']:.0%}, faces {res['coverage']['faces']:.0%})", ""]
        md += ["Seed attribute realised in the step-0 image (judge = seed): " + ", ".join(f"{k} {v['share']} (n {v['n']})" for k, v in res["seed_realised_at_step0"].items()) + ". Survival below is relative to what step 0 showed.", ""]
        md += ["### Attribute survival (share of trajectories with the step-0 value still present; competing dropout)", "", "| attribute | group | n | kept @5 | kept @10 | kept @20 | lost by end | dropout by end |", "|---|---|---|---|---|---|---|---|"]
        for k, v in res["survival"].items():
            attr, grp = k.split("|", 1); end = v["curve"][-1]
            md.append(f"| {attr} | {grp} | {v['n']} | {v['kept_at'].get('5', '')} | {v['kept_at'].get('10', '')} | {v['kept_at'].get('20', '')} | {end['lost']} | {end['dropout']} |")
        md += ["", "### Loss hazard per window (first losses / at-risk trajectory-steps)", "", "| attribute | group | steps | losses | at risk | hazard |", "|---|---|---|---|---|---|"]
        for k, v in res["hazard"].items():
            attr, grp, win = k.split("|"); md.append(f"| {attr} | {grp} | {win} | {v['losses']} | {v['at_risk_steps']} | {v['hazard']} |")
        cs = res["change_summary"]
        md += ["", f"### Changes: {cs['n']} attribute losses from a kept state", "",
               f"- toward the occupation's prior: {cs['toward_prior']['share']} (n {cs['toward_prior']['n']})", f"- recovered within 3 steps: {cs['recovered_within_3']['share']} (n {cs['recovered_within_3']['n']})",
               f"- mechanism (caption that made the image): omission {cs['mechanism']['omission']}, override {cs['mechanism']['override']}, caption change {cs['mechanism']['caption_change']}",
               "- toward lighter skin or male presentation, by occupation: " + ", ".join(f"{o} {v['share']} (n {v['n']})" for o, v in cs["by_occupation_toward_lighter_or_male"].items()), ""]
        md += ["### Skin L* by occupation and step (chromatic images with a detected face)", "", "| group | step | n | L* mean | L* std | mean dL* vs own step 0 | share within 10 of step 0 |", "|---|---|---|---|---|---|---|"]
        for k, v in res["skin_spread"].items():
            g, s = k.split("|"); md.append(f"| {g} | {s} | {v['n']} | {v['L_mean']} | {v['L_std']} | {v['dL0_mean']} | {v['dL0_abs_le10']} |")
        md += ["", "### Portrait loss per step", "", "| set | step | n | person | single person | head-and-shoulders | face detected | median face area | B&W or sepia |", "|---|---|---|---|---|---|---|---|---|"]
        for k, v in res["portrait"].items():
            st, s = k.split("|"); md.append(f"| {st} | {s} | {v['n']} | {v['person']} | {v['single_person']} | {v['head_and_shoulders']} | {v['face_present']} | {v['face_area_median']} | {v['bw_or_sepia']} |")
        md.append("")
    (out / "e6_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", nargs="+", required=True); ap.add_argument("--out", default="reports/e6")
    a = ap.parse_args(argv)
    out = ROOT / a.out; out.mkdir(parents=True, exist_ok=True)
    results = []
    for run in a.runs:
        judge = load_jsonl(CACHE / run / "judge.jsonl"); faces = load_jsonl(CACHE / run / "faces.jsonl")
        rows, horizon, man = analyse_run(run, judge, faces)
        res = summarise(run, rows, horizon); results.append(res)
        (out / f"{run}_rows.json").write_text(json.dumps(rows) + "\n", encoding="utf-8")
        (out / f"{run}_summary.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    write_md(results, out)
    print((out / "e6_report.md").read_text())


if __name__ == "__main__":
    main()
