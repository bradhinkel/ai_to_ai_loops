"""Hue census from pixels: what share of each run's saturated pixels falls in each hue band, by step.
Pixels only (no CLIP, no captions). Saturated = HSV S >= 0.25 and V >= 0.2. Bands (degrees): red 345-15, orange 15-45,
yellow 45-70, green 70-170, cyan 170-200, blue 200-255, purple-magenta 255-335, pink 335-345. Also the share of images
whose dominant saturated band is purple-magenta. Writes reports/hue_share.md / .json.

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/hue_share.py a0_core a0_core2 a0_s e1_cap --steps 0,1,5,20,50,99
"""
import argparse, json, pathlib, sys
import numpy as np
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT  # noqa: E402

BANDS = [("red", 345, 15), ("orange", 15, 45), ("yellow", 45, 70), ("green", 70, 170), ("cyan", 170, 200), ("blue", 200, 255), ("purple-magenta", 255, 335), ("pink", 335, 345)]
ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--steps", default="0,1,5,20,50,99"); ap.add_argument("--size", type=int, default=128)
a = ap.parse_args(); steps = [int(s) for s in a.steps.split(",")]

def census(path, size):
    im = Image.open(path).convert("RGB").resize((size, size), Image.BILINEAR)
    hsv = np.asarray(im.convert("HSV"), dtype=np.float32)
    h = hsv[..., 0] * 360 / 255; s = hsv[..., 1] / 255; v = hsv[..., 2] / 255
    m = (s >= 0.25) & (v >= 0.2); hh = h[m]
    out = {"saturated_share": float(m.mean())}
    for name, lo, hi in BANDS:
        sel = ((hh >= lo) | (hh < hi)) if lo > hi else ((hh >= lo) & (hh < hi))
        out[name] = float(sel.sum() / max(1, hh.size))
    return out

res = {}
for run in a.runs:
    res[run] = {}
    for st in steps:
        rows = []
        for t in sorted((ROOT / "runs" / run).glob("traj_*")):
            p = t / f"step_{st:03d}.png"
            if p.exists(): rows.append(census(p, a.size))
        if not rows: continue
        agg = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
        agg["n"] = len(rows)
        agg["images_dominant_purple"] = float(np.mean([max(((b[0], r[b[0]]) for b in BANDS), key=lambda x: x[1])[0] == "purple-magenta" for r in rows]))
        agg["images_dominant_blue_purple"] = float(np.mean([max(((b[0], r[b[0]]) for b in BANDS), key=lambda x: x[1])[0] in ("blue", "purple-magenta") for r in rows]))
        res[run][st] = agg
        print(run, st, {k: round(v, 3) for k, v in agg.items() if k in ("purple-magenta", "images_dominant_purple", "saturated_share")}, flush=True)
out = ROOT / "reports" / "hue_share"
json.dump(res, open(out.with_suffix(".json"), "w"), indent=1)
lines = ["# Hue census from pixels", "", "Share of saturated pixels (HSV S >= 0.25, V >= 0.2) per hue band, averaged over the 100 images of a step; 'dominant purple' = share of images whose largest band is purple-magenta (255-335 deg). Pixels only; no model is involved.", ""]
for run, by in res.items():
    lines += [f"## {run}", "", "| step | saturated share | " + " | ".join(b[0] for b in BANDS) + " | images dominant purple | images dominant blue or purple |", "|---" * (len(BANDS) + 4) + "|"]
    for st, agg in by.items():
        lines.append(f"| {st} | {agg['saturated_share']:.2f} | " + " | ".join(f"{agg[b[0]]:.2f}" for b in BANDS) + f" | {agg['images_dominant_purple']:.2f} | {agg['images_dominant_blue_purple']:.2f} |")
    lines.append("")
out.with_suffix(".md").write_text("\n".join(lines)); print("->", out.with_suffix(".md"))
