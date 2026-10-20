"""Caption-side audit of one or more runs, from the step JSON records only (no embeddings, no GPU).

  analysis/caption_audit.py a0_core e1_gen e1_cap_pilot e1_both   -> reports/caption_audit.md + .json

Per run and step window: caption length, CLIP-77 clip rate and words before/after, caption flags, the share of captions
using style vocabulary (Hintze's "vivid, artistic" register) or photographic vocabulary, captions mentioning people,
and gendered words. The word lists are fixed here so every run is counted the same way.
"""
import argparse, json, re, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); from common import ROOT  # noqa: E402

STYLE = {"vibrant", "vivid", "ethereal", "dreamlike", "dreamy", "surreal", "whimsical", "painterly", "painted", "painting",
         "brushstrokes", "brushstroke", "watercolor", "impressionist", "impressionistic", "luminous", "glowing", "radiant",
         "enchanting", "enchanted", "magical", "mystical", "otherworldly", "fantastical", "kaleidoscopic", "iridescent",
         "shimmering", "swirling", "swirls", "artistic", "stylized", "stylised", "abstract", "majestic", "breathtaking",
         "celestial", "mesmerizing", "mesmerising", "opulent", "ornate", "gilded", "golden", "hues", "palette", "canvas"}
PHOTO = {"photograph", "photographic", "photo", "realistic", "photorealistic", "candid", "snapshot", "camera", "lens",
         "depth of field", "shallow focus", "bokeh", "natural light", "overcast", "daylight", "street", "sidewalk",
         "parking", "sign", "signage", "logo", "plastic", "concrete", "asphalt", "wearing", "jeans", "t-shirt", "sneakers"}
PEOPLE = {"person", "people", "man", "woman", "men", "women", "boy", "girl", "child", "children", "figure", "figures",
          "couple", "crowd", "family", "lady", "gentleman", "individual", "individuals", "pedestrian", "pedestrians",
          "worker", "workers", "nurse", "nurses", "doctor", "doctors", "professional", "professionals", "silhouette",
          "silhouettes", "he", "she", "his", "her", "they", "someone", "player", "players", "dancer", "dancers"}
MALE = {"man", "men", "boy", "boys", "he", "his", "him", "gentleman", "gentlemen", "male", "father", "king", "prince"}
FEMALE = {"woman", "women", "girl", "girls", "she", "her", "hers", "lady", "ladies", "female", "mother", "queen", "princess"}
WINDOWS = [(0, 0), (1, 5), (6, 10), (11, 25), (26, 50), (51, 75), (76, 99)]


def words(text):
    return re.findall(r"[a-z][a-z'\-]*", text.lower())


def audit(run):
    recs = []
    for f in sorted((ROOT / "runs" / run).glob("traj_*/step_*.json")):
        if f.name.endswith(".gen.json"): continue
        r = json.load(open(f)); recs.append(r)
    rows = []
    for r in recs:
        cap = r.get("caption") or ""; w = words(cap); ws = set(w); lw = cap.lower()
        fl = r.get("caption_flags", {})
        rows.append(dict(step=r["step"], traj=r["traj"], n_words=len(w),
                         clipped=bool(r.get("clipped", r.get("prompt_truncated_by_clip", False))),
                         wb=r.get("clip_words_before"), wa=r.get("clip_words_after"),
                         empty=bool(fl.get("empty")), refusal=bool(fl.get("refusal")), cutoff=bool(fl.get("length_cutoff")),
                         style=bool(ws & STYLE), n_style=sum(1 for x in w if x in STYLE),
                         photo=bool(ws & {p for p in PHOTO if " " not in p}) or any(p in lw for p in PHOTO if " " in p),
                         people=bool(ws & PEOPLE), male=sum(1 for x in w if x in MALE), female=sum(1 for x in w if x in FEMALE),
                         mt5_trunc=bool(r.get("prompt_truncated_by_mt5", False))))
    out = {"run": run, "n_records": len(rows), "windows": []}
    for lo, hi in WINDOWS:
        sub = [x for x in rows if lo <= x["step"] <= hi]
        if not sub: continue
        clipped = [x for x in sub if x["clipped"] and x["wb"] is not None]
        out["windows"].append(dict(
            steps=f"{lo}-{hi}" if lo != hi else str(lo), n=len(sub),
            words_median=float(np.median([x["n_words"] for x in sub])),
            clip_rate=float(np.mean([x["clipped"] for x in sub])),
            clip_words_before=float(np.median([x["wb"] for x in clipped])) if clipped else None,
            clip_words_after=float(np.median([x["wa"] for x in clipped])) if clipped else None,
            style_share=float(np.mean([x["style"] for x in sub])), style_words_per_caption=float(np.mean([x["n_style"] for x in sub])),
            photo_share=float(np.mean([x["photo"] for x in sub])), people_share=float(np.mean([x["people"] for x in sub])),
            male=int(sum(x["male"] for x in sub)), female=int(sum(x["female"] for x in sub)),
            mt5_trunc_rate=float(np.mean([x["mt5_trunc"] for x in sub]))))
    out["flags"] = dict(empty=int(sum(x["empty"] for x in rows)), refusal=int(sum(x["refusal"] for x in rows)),
                        length_cutoff=int(sum(x["cutoff"] for x in rows)), over_50_words=int(sum(x["n_words"] > 50 for x in rows)))
    # per-step people share (for the E6 dropout curve)
    out["people_by_step"] = [float(np.mean([x["people"] for x in rows if x["step"] == s])) for s in range(max(x["step"] for x in rows) + 1)]
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--out", default="reports/caption_audit")
    a = ap.parse_args(); res = [audit(r) for r in a.runs]
    md = ["# Caption audit", "", "Counted from the step records only. Word lists are fixed in `analysis/caption_audit.py` (style = Hintze's "
          "'vivid, artistic' register; photo = photographic / everyday-scene vocabulary; people = any person word incl. pronouns). "
          "Shares are the fraction of captions in the step window containing at least one list word; clip columns are median words "
          "of the clipped prompts before and after the CLIP-77 cut.", ""]
    for r in res:
        f = r["flags"]
        md += [f"## {r['run']}  ({r['n_records']} records; empty {f['empty']}, refusals {f['refusal']}, length cutoffs {f['length_cutoff']}, over 50 words {f['over_50_words']})", "",
               "| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |",
               "|---|---|---|---|---|---|---|---|---|---|---|"]
        for w in r["windows"]:
            cb = "" if w["clip_words_before"] is None else f"{w['clip_words_before']:.0f} -> {w['clip_words_after']:.0f}"
            md.append(f"| {w['steps']} | {w['n']} | {w['words_median']:.0f} | {w['clip_rate']:.1%} | {cb} | {w['style_share']:.0%} | {w['style_words_per_caption']:.2f} | "
                      f"{w['photo_share']:.0%} | {w['people_share']:.0%} | {w['male']} : {w['female']} | {w['mt5_trunc_rate']:.1%} |")
        md.append("")
    out = ROOT / a.out; out.with_suffix(".md").write_text("\n".join(md)); out.with_suffix(".json").write_text(json.dumps(res, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
