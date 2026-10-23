"""E6: which occupations the captions assign as the loop runs, and whether the re-assignment is biased (Brad, 2026-10-23:
"did the loop convert a nurse into a doctor? ... a male nurse into a male doctor; or a white, male nurse into a white male doctor?
The loop also converted pilots into service men/women - is there a bias in this conversion as well").

Caption at step s (common.caption_used) describes image s. Occupation words are matched in the caption; the person's gender and
skin band at that step are the judge's (analysis/cache/<run>/judge.jsonl, via reports/e6/<run>_rows.json). The seed's gender,
skin and age come from the manifest. For each seed occupation and each target role: share of trajectories whose captions ever
name the role in steps 1-19, by seed gender and seed skin, with the judge's reading of the image at the first such step and the
caption's own gender words; also the role share per step (all captions).

    .venv/bin/python analysis/e6_occupations.py --runs e6_photo e6_track --out reports/e6/occupations.md
"""
import argparse, json, pathlib, re, sys
from collections import defaultdict, Counter
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, caption_used, list_steps  # noqa: E402
from e6_report import caption_names, wilson  # noqa: E402

ROLES = {
    "doctor": r"\b(doctor|doctors|physician|physicians|surgeon|surgeons)\b",
    "nurse": r"\bnurses?\b",
    "medical staff (unspecified)": r"\b(medical (staff|professional|professionals|personnel|worker|workers|team)|healthcare (worker|workers|professional|professionals))\b",
    "patient": r"\bpatients?\b",
    "pilot": r"\bpilots?\b",
    "military / soldier": r"\b(soldier|soldiers|military|army|navy|naval|air force|marines?|troops?|servicem[ae]n|service members?|infantry|combat|camouflage|fatigues)\b",
    "astronaut": r"\bastronauts?\b",
    "police": r"\b(police|policem[ae]n|law enforcement)\b",
    "scientist / lab": r"\b(scientists?|laboratory|lab coats?|researchers?)\b",
    "business / office worker": r"\b(business(man|woman|men|women|person|people)|executives?|office workers?)\b",
    "social worker": r"\bsocial workers?\b",
    "teacher / student": r"\b(teachers?|students?|professors?)\b",
}
RX = {k: re.compile(v) for k, v in ROLES.items()}


def load_rows(run):
    rows = json.loads((ROOT / "reports" / "e6" / f"{run}_rows.json").read_text())
    by = defaultdict(dict)
    for r in rows: by[r["traj"]][r["step"]] = r
    return by


def analyse(run, horizon=19):
    rd = ROOT / "runs" / run; avail = list_steps(rd); by = load_rows(run)
    caps = {(t, s): caption_used(rd, t, s).lower() for t in avail for s in avail[t] if s <= horizon}
    out = {"run": run, "per_step": {}, "transitions": {}}
    # role share per step by seed occupation
    for occ in ("pilot", "nurse", "social_worker", "portrait"):
        trajs = [t for t in by if (by[t][0]["occupation"] or "portrait") == occ]
        for role, rx in RX.items():
            out["per_step"][f"{occ}|{role}"] = {str(s): round(sum(1 for t in trajs if rx.search(caps[(t, s)])) / len(trajs), 3) for s in (0, 1, 2, 3, 5, 10, 15, 19)}
    # transitions: for each seed occupation x target role, trajectories whose captions ever name the role in steps 1..H
    for occ in ("pilot", "nurse", "social_worker", "portrait"):
        trajs = [t for t in by if (by[t][0]["occupation"] or "portrait") == occ]
        for role, rx in RX.items():
            ever = {}
            for t in trajs:
                first = next((s for s in range(1, horizon + 1) if rx.search(caps[(t, s)])), None)
                ever[t] = first
            n_ever = sum(1 for v in ever.values() if v is not None)
            if n_ever < 4: continue
            rec = {"n_traj": len(trajs), "n_ever": n_ever, "share": round(n_ever / len(trajs), 3), "first_step_median": None, "by_seed": {}, "at_first": {}}
            firsts = sorted(v for v in ever.values() if v is not None); rec["first_step_median"] = firsts[len(firsts) // 2]
            for key in ("gender_seed", "skin_seed", "age_seed"):
                for val in sorted({by[t][0][key] for t in trajs if by[t][0][key]}):
                    tt = [t for t in trajs if by[t][0][key] == val]; k = sum(1 for t in tt if ever[t] is not None)
                    rec["by_seed"][f"{key}={val}"] = {"n": len(tt), "ever": k, "share": round(k / len(tt), 3), "ci": wilson(k, len(tt))}
            # what the image showed (judge) and what the caption said at the first step naming the role
            jg = Counter(); js = Counter(); cg = Counter(); kept_g = []; kept_s = []
            for t, s in ever.items():
                if s is None: continue
                r = by[t][s]
                jg[r["gender_img"] or "none"] += 1; js[r["skin_img"] or "none"] += 1
                cw = caption_names(caps[(t, s)], "gender"); cg["+".join(sorted(cw)) or "none"] += 1
                if r["gender_state"] in ("kept", "lost"): kept_g.append(r["gender_state"] == "kept")
                if r["skin_state"] in ("kept", "lost"): kept_s.append(r["skin_state"] == "kept")
            rec["at_first"] = {"judge_gender": dict(jg), "judge_skin": dict(js), "caption_gender_words": dict(cg),
                               "seed_gender_still_shown": {"n": len(kept_g), "share": round(sum(kept_g) / len(kept_g), 3) if kept_g else None},
                               "seed_skin_still_shown": {"n": len(kept_s), "share": round(sum(kept_s) / len(kept_s), 3) if kept_s else None}}
            out["transitions"][f"{occ}|{role}"] = rec
    # per image (steps 1..H, single person in the image): role word in the caption x what the judge saw x the caption's pronoun
    out["per_image"] = {}
    for occ, roles in (("nurse", ("doctor", "nurse", "patient", "scientist / lab")), ("pilot", ("pilot", "military / soldier", "astronaut"))):
        trajs = [t for t in by if by[t][0]["occupation"] == occ]
        base = {"n": 0, "judge_gender": Counter(), "judge_skin": Counter(), "caption_gender_words": Counter(), "seed_gender": Counter()}
        tabs = {role: {"n": 0, "judge_gender": Counter(), "judge_skin": Counter(), "caption_gender_words": Counter(), "seed_gender": Counter()} for role in roles}
        for t in trajs:
            for s_ in range(1, horizon + 1):
                r = by[t][s_]
                if r["n_people"] != 1: continue
                c = caps[(t, s_)]; cw = "+".join(sorted(caption_names(c, "gender"))) or "none"
                for tab, hit in [(base, True)] + [(tabs[role], bool(RX[role].search(c))) for role in roles]:
                    if not hit: continue
                    tab["n"] += 1; tab["judge_gender"][r["gender_img"] or "none"] += 1; tab["judge_skin"][r["skin_img"] or "none"] += 1
                    tab["caption_gender_words"][cw] += 1; tab["seed_gender"][r["gender_seed"]] += 1
        out["per_image"][occ] = {"all single-person images": base, **tabs}
    return out


def write_md(results, out):
    md = ["# E6: occupations named by the captions, and who gets re-assigned", "",
          "Caption at step s describes image s. Role words: " + "; ".join(f"**{k}**: `{v}`" for k, v in ROLES.items()), ""]
    for res in results:
        md += [f"## {res['run']}", "", "### Share of captions naming each role, by seed occupation and step", "",
               "| seed occupation | role | 0 | 1 | 2 | 3 | 5 | 10 | 15 | 19 |", "|---|---|---|---|---|---|---|---|---|---|"]
        for k, v in res["per_step"].items():
            occ, role = k.split("|")
            if max(v.values()) < 0.03: continue
            md.append(f"| {occ} | {role} | " + " | ".join(f"{v[s]:.2f}" for s in ("0", "1", "2", "3", "5", "10", "15", "19")) + " |")
        md += ["", "### Re-assignment by seed group (trajectories whose captions ever name the role in steps 1–19; Wilson 95% CI)", "",
               "| seed occupation → role | n ever / n | median first step | by seed gender | by seed skin | by seed age |", "|---|---|---|---|---|---|"]
        for k, v in res["transitions"].items():
            occ, role = k.split("|")
            def grp(prefix):
                return "; ".join(f"{g.split('=')[1]} {d['share']:.2f} ({d['ever']}/{d['n']})" for g, d in v["by_seed"].items() if g.startswith(prefix))
            md.append(f"| {occ} → {role} | {v['n_ever']} / {v['n_traj']} ({v['share']:.2f}) | {v['first_step_median']} | {grp('gender_seed')} | {grp('skin_seed')} | {grp('age_seed')} |")
        md += ["", "### At the first caption naming the role: what the image showed (judge) and what the caption said", "",
               "| seed occupation → role | judge gender | judge skin | caption gender words | seed gender still shown | seed skin still shown |", "|---|---|---|---|---|---|"]
        for k, v in res["transitions"].items():
            occ, role = k.split("|"); a = v["at_first"]
            fmt = lambda c: ", ".join(f"{kk} {vv}" for kk, vv in sorted(c.items(), key=lambda x: -x[1]))
            md.append(f"| {occ} → {role} | {fmt(a['judge_gender'])} | {fmt(a['judge_skin'])} | {fmt(a['caption_gender_words'])} | {a['seed_gender_still_shown']['share']} (n {a['seed_gender_still_shown']['n']}) | {a['seed_skin_still_shown']['share']} (n {a['seed_skin_still_shown']['n']}) |")
        md += ["### Per image, steps 1–19, single person in frame: role word in the caption vs what the judge saw and the caption's gender words", "",
               "| seed occupation | caption names | n images | judge: man / woman / ambiguous / none | judge: light / medium / dark | caption words: man / woman / both / none | seed: man / woman |", "|---|---|---|---|---|---|---|"]
        for occ, tabs in res["per_image"].items():
            for role, tab in tabs.items():
                g = tab["judge_gender"]; sk = tab["judge_skin"]; cw = tab["caption_gender_words"]; sg = tab["seed_gender"]
                md.append(f"| {occ} | {role} | {tab['n']} | {g.get('man', 0)} / {g.get('woman', 0)} / {g.get('ambiguous', 0)} / {g.get('none', 0)} | {sk.get('light', 0)} / {sk.get('medium', 0)} / {sk.get('dark', 0)} | {cw.get('man', 0)} / {cw.get('woman', 0)} / {cw.get('man+woman', 0)} / {cw.get('none', 0)} | {sg.get('man', 0)} / {sg.get('woman', 0)} |")
        md.append("")
    pathlib.Path(out).write_text("\n".join(md) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", nargs="+", default=["e6_photo", "e6_track"]); ap.add_argument("--out", default="reports/e6/occupations.md")
    a = ap.parse_args(argv)
    results = [analyse(r) for r in a.runs]
    (ROOT / a.out).with_suffix(".json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    write_md(results, ROOT / a.out); print((ROOT / a.out).read_text())


if __name__ == "__main__":
    main()
