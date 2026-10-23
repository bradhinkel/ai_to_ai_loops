"""Culture judge for the E2 language question (SPEC2 §4 E2; Brad's observation during E2-QZ, 2026-10-22: faces turning East
Asian within five steps). An independent judge (Claude Sonnet 5.5, never a loop captioner) codes, from the image alone,
whether the primary person's apparent appearance reads as East Asian, which East Asian cultural motifs are visible, the
apparent region of the setting and any visible script. Run on the same steps of the Chinese cell and its English control.

    .venv/bin/python analysis/culture_judge.py e2_qz e1_both --steps 0,5,20,99      # judge -> analysis/cache/<run>/culture_judge.jsonl
    .venv/bin/python analysis/culture_judge.py e2_qz e1_both --report               # -> reports/culture_judge_e2_qz.md + .json

Reuses attribute_judge.Judge (retries, usage logging, no temperature control, D16) with this prompt. CLIP is not used.
"""
import argparse, json, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE, list_steps, image_path  # noqa: E402
import attribute_judge as aj  # noqa: E402

MOTIFS = ["pagoda", "temple_or_shrine", "lantern", "east_asian_dress", "cjk_text_or_calligraphy", "ink_wash_style", "cherry_blossom",
          "bamboo", "dragon_or_koi", "fuji_like_mountain", "curved_tiled_roof", "other_east_asian"]
SCHEMA = {"person_present": "bool", "n_people": "int", "face_visible": "bool",
          "primary_apparent_east_asian": "yes|no|ambiguous|null",
          "east_asian_motifs": f"list drawn from {MOTIFS} or []",
          "setting_region": "east_asia|south_asia|western|middle_east|africa|latin_america|other|none_or_abstract",
          "visible_text_script": "chinese|japanese|korean|latin|other|none", "notes": "short string"}
PROMPT = ("You are coding images for a research study of the cultural priors of image-generation loops. Describe only what is visible. "
          "Return one JSON object and nothing else (no prose, no code fence), with exactly these keys: " + json.dumps(SCHEMA) +
          ". `primary_apparent_east_asian` concerns the most prominent person: 'yes' if their visible facial features and appearance would commonly be "
          "read as East Asian (Chinese, Japanese or Korean), 'no' if they would commonly be read otherwise, 'ambiguous' if a face is visible but too "
          "small, stylised or indeterminate, null if no person or no face is visible. `east_asian_motifs` lists visible cultural elements only. "
          "`setting_region` is the apparent cultural region of the scene's architecture, landscape style or objects; use none_or_abstract for "
          "scenes with no regional cue.")


def judge_runs(runs, steps, parallel, model, limit):
    aj.PROMPT = PROMPT
    judge = aj.Judge(model)
    for run in runs:
        run_dir = ROOT / "runs" / run; out = CACHE / run / "culture_judge.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
        done = set()
        if out.exists():
            for line in out.read_text(encoding="utf-8").splitlines():
                if line.strip(): d = json.loads(line); done.add((d["traj"], d["step"]))
        avail = list_steps(run_dir)
        todo = [(t, s) for t in sorted(avail) for s in steps if s in avail[t] and (t, s) not in done]
        if limit: todo = todo[:limit]
        print(f"{run}: {len(done)} judged, {len(todo)} to do -> {out}", flush=True)
        t0 = time.time(); usage = [0, 0]
        with open(out, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=parallel) as ex:
            for i0 in range(0, len(todo), parallel):
                wave = todo[i0:i0 + parallel]
                for (t, s), rec in zip(wave, ex.map(lambda ts: judge.judge(image_path(run_dir, *ts)), wave)):
                    f.write(json.dumps({"run": run, "traj": t, "step": s, "prompt_version": "culture_v1", **rec}, ensure_ascii=False) + "\n")
                    usage[0] += rec["judge_api"]["usage"]["input"]; usage[1] += rec["judge_api"]["usage"]["output"]
                f.flush()
        if todo: print(f"  done {len(todo)} in {(time.time() - t0) / 60:.1f} min; tokens in {usage[0]} out {usage[1]}", flush=True)


def report(runs, out):
    res = {}
    for run in runs:
        rows = [json.loads(l) for l in (CACHE / run / "culture_judge.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        by_step = {}
        for r in rows:
            j = r.get("judge") or {}; by_step.setdefault(r["step"], []).append(j)
        per = {}
        for s, js in sorted(by_step.items()):
            n = len(js); parsed = [j for j in js if j]
            person = [j for j in parsed if j.get("person_present")]
            face = [j for j in person if j.get("face_visible")]
            ea = [j for j in face if j.get("primary_apparent_east_asian") == "yes"]
            amb = [j for j in face if j.get("primary_apparent_east_asian") == "ambiguous"]
            no = [j for j in face if j.get("primary_apparent_east_asian") == "no"]
            motif = [j for j in parsed if j.get("east_asian_motifs")]
            mcount = {}
            for j in parsed:
                for m in j.get("east_asian_motifs") or []: mcount[m] = mcount.get(m, 0) + 1
            region = {}
            for j in parsed: region[j.get("setting_region")] = region.get(j.get("setting_region"), 0) + 1
            script = {}
            for j in parsed: script[j.get("visible_text_script")] = script.get(j.get("visible_text_script"), 0) + 1
            per[s] = dict(n=n, parsed=len(parsed), person=len(person), face=len(face), ea_yes=len(ea), ea_no=len(no), ea_amb=len(amb),
                          motif_any=len(motif), motifs=dict(sorted(mcount.items(), key=lambda kv: -kv[1])), region=dict(sorted(region.items(), key=lambda kv: -kv[1])),
                          script=dict(sorted(script.items(), key=lambda kv: -kv[1])))
        res[run] = per
    md = ["# Culture judge: " + " vs ".join(runs) + "\n",
          "Judge: Claude Sonnet 5.5, image only, prompt `culture_v1` (`analysis/culture_judge.py`). Columns: images judged / with a person / with a visible face / "
          "faces read as East Asian: yes / no / ambiguous / images with any East Asian motif / setting judged east_asia / visible CJK script.\n"]
    md.append("| run | step | judged | person | face | EA yes | EA no | EA ambiguous | EA yes share of faces | any EA motif | setting east_asia | CJK script |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for run, per in res.items():
        for s, p in per.items():
            cjk = sum(v for k, v in p["script"].items() if k in ("chinese", "japanese", "korean"))
            md.append(f"| {run} | {s} | {p['parsed']} | {p['person']} | {p['face']} | {p['ea_yes']} | {p['ea_no']} | {p['ea_amb']} | "
                      f"{(p['ea_yes'] / p['face'] if p['face'] else float('nan')):.2f} | {p['motif_any']} | {p['region'].get('east_asia', 0)} | {cjk} |")
    md.append("")
    for run, per in res.items():
        for s, p in per.items():
            md.append(f"- {run} step {s}: motifs {p['motifs']}; regions {p['region']}")
    pathlib.Path(out + ".md").write_text("\n".join(md) + "\n", encoding="utf-8"); json.dump(res, open(out + ".json", "w"), indent=1)
    print("\n".join(md))


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--steps", default="0,5,20,99")
    ap.add_argument("--parallel", type=int, default=8); ap.add_argument("--model", default=aj.JUDGE_MODEL); ap.add_argument("--limit", type=int)
    ap.add_argument("--report", action="store_true"); ap.add_argument("--out", default="reports/culture_judge_e2_qz")
    a = ap.parse_args(argv)
    if a.report: report(a.runs, a.out)
    else: judge_runs(a.runs, [int(x) for x in a.steps.split(",")], a.parallel, a.model, a.limit)


if __name__ == "__main__":
    main()
