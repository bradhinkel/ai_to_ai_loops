"""Is there a palette attractor independent of the subject? (Brad, 2026-10-20: "a color attractor that acts independent of a
subject attractor - i.e. it stays Black & White while escaping the subject.")
Every image gets a palette class from pixel statistics alone (no embedding): grayscale (mean HSV saturation < 0.12),
tinted-mono (saturation 0.12-0.30 with low hue dispersion), rainbow (high saturation-weighted hue dispersion), vivid
(saturation >= 0.35, not rainbow), high-contrast (luminance std > 0.25, not already classed), else neutral. Subject changes are
read from DINOv2: a "subject jump" is a step whose cosine distance to the previous step exceeds --jump (default 0.35; the median
step drift is ~0.17). Tests per run: P(palette class kept | subject jump) vs P(kept | no jump) vs the chance rate from the class
frequencies; palette dwells (>= --min_dwell consecutive steps in one class) and how many of them contain a subject jump; the
longest dwell per class. Example strips: the longest dwells that span a jump, as reports/palette_persistence/<run>_<class>.jpg.
    .venv/bin/python analysis/palette_persistence.py a0_core e1_cap e1_gen e1_both
"""
import argparse, glob, json, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache, cpu_only, thumb  # noqa: E402
from gravity import visits  # noqa: E402

CLASSES = ["grayscale", "tinted-mono", "rainbow", "vivid", "high-contrast", "neutral"]


def palette(path):
    im = np.asarray(Image.open(path).convert("RGB").resize((96, 96))).astype(np.float64)
    hsv = np.asarray(Image.fromarray(im.astype(np.uint8)).convert("HSV")).astype(np.float64)
    H = hsv[..., 0] / 255 * 2 * np.pi; S = hsv[..., 1] / 255; L = (0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]) / 255
    s = S.mean(); w = S.flatten(); R = np.hypot((w * np.cos(H.flatten())).sum(), (w * np.sin(H.flatten())).sum()) / max(w.sum(), 1e-6)
    disp = 1 - R                                     # 0 = one hue, 1 = hues spread evenly (saturation-weighted)
    if s < 0.12: c = "grayscale"
    elif s < 0.30 and disp < 0.45: c = "tinted-mono"
    elif s >= 0.25 and disp > 0.80: c = "rainbow"
    elif s >= 0.35: c = "vivid"
    elif L.std() > 0.25: c = "high-contrast"
    else: c = "neutral"
    return c, dict(sat=round(float(s), 3), hue_disp=round(float(disp), 3), contrast=round(float(L.std()), 3))


def main():
    cpu_only(); ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--jump", type=float, default=0.35)
    ap.add_argument("--min_dwell", type=int, default=5); ap.add_argument("--thumb", type=int, default=96); a = ap.parse_args()
    out = ROOT / "reports" / "palette_persistence"; out.mkdir(parents=True, exist_ok=True)
    md = ["# Palette persistence vs subject change", "", f"Palette class from pixels only; subject jump = DINOv2 step distance > {a.jump}. "
          f"Dwell = >= {a.min_dwell} consecutive steps in one palette class. 'kept' = same class as the previous step. Strips: `reports/palette_persistence/<run>_<class>.jpg` "
          "(longest dwells that contain a subject jump; yellow = step, red bar under a step = subject jump).", ""]
    allres = {}
    for run in a.runs:
        d = Cache(run).arrays("dinov2"); X = d["X"].astype(np.float64); X /= np.linalg.norm(X, axis=-1, keepdims=True); trajs = list(d["trajs"]); S = X.shape[1]
        cls = np.full((len(trajs), S), "", dtype=object)
        for i, t in enumerate(trajs):
            for s in range(S):
                p = ROOT / "runs" / run / f"traj_{int(t):03d}" / f"step_{s:03d}.png"
                if p.exists(): cls[i, s] = palette(p)[0]
        jump = np.zeros((len(trajs), S), bool); jump[:, 1:] = (1 - (X[:, 1:] * X[:, :-1]).sum(-1)) > a.jump
        valid = (cls[:, 1:] != "") & (cls[:, :-1] != "")
        kept = cls[:, 1:] == cls[:, :-1]; j = jump[:, 1:]
        freq = {c: float((cls == c).mean()) for c in CLASSES}; chance = sum(f * f for f in freq.values())
        p_kept_jump = float(kept[valid & j].mean()); p_kept_nojump = float(kept[valid & ~j].mean())
        # per-class: kept across a jump
        per = {}
        for c in CLASSES:
            m = valid & j & (cls[:, :-1] == c); per[c] = dict(freq=freq[c], n_jumps=int(m.sum()), kept_across_jump=float(kept[m].mean()) if m.sum() else None)
        # dwells
        dw = {c: [] for c in CLASSES}
        for i in range(len(trajs)):
            for c in CLASSES:
                inside = cls[i] == c; pos = 0
                for length, cens in visits(inside):
                    while pos < S and not inside[pos]: pos += 1
                    start = pos; pos += length
                    if length >= a.min_dwell:
                        nj = int(jump[i, start + 1:start + length].sum()); dw[c].append((int(trajs[i]), start, length, nj))
        allres[run] = dict(freq=freq, chance=chance, p_kept_jump=p_kept_jump, p_kept_nojump=p_kept_nojump, per_class=per,
                           dwells={c: len(v) for c, v in dw.items()}, dwells_with_jump={c: sum(1 for x in v if x[3] > 0) for c, v in dw.items()},
                           longest_dwell={c: max([x[2] for x in v], default=0) for c, v in dw.items()},
                           steps_in_dwells=float(sum(x[2] for v in dw.values() for x in v) / (len(trajs) * S)))
        md += [f"## {run}", "", f"P(palette kept | subject jump) = **{p_kept_jump:.2f}**, P(kept | no jump) = {p_kept_nojump:.2f}, chance = {chance:.2f}. "
               f"Share of steps inside a palette dwell of >= {a.min_dwell}: {allres[run]['steps_in_dwells']:.0%}.", "",
               "| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |", "|---|---|---|---|---|---|---|"]
        for c in CLASSES:
            pc = per[c]; k = "-" if pc["kept_across_jump"] is None else f"{pc['kept_across_jump']:.2f}"
            md.append(f"| {c} | {pc['freq']:.0%} | {pc['n_jumps']} | {k} | {len(dw[c])} | {sum(1 for x in dw[c] if x[3] > 0)} | {allres[run]['longest_dwell'][c]} |")
        md.append("")
        # strips
        for c in CLASSES:
            ex = sorted([x for x in dw[c] if x[3] > 0], key=lambda x: -x[2])[:3]
            if not ex: continue
            T = a.thumb; L = min(max(x[2] for x in ex), 20); sheet = Image.new("RGB", (L * T, len(ex) * (T + 14)), "white"); dr = ImageDraw.Draw(sheet)
            for r, (t, start, length, nj) in enumerate(ex):
                for k2 in range(min(length, L)):
                    s = start + k2; p = ROOT / "runs" / run / f"traj_{t:03d}" / f"step_{s:03d}.png"
                    if p.exists(): sheet.paste(thumb(p, T), (k2 * T, r * (T + 14)))
                    dr.text((k2 * T + 2, r * (T + 14) + 2), f"{t}:{s}", fill="yellow")
                    if jump[trajs.index(t), s]: dr.rectangle([k2 * T, r * (T + 14) + T, k2 * T + T - 1, r * (T + 14) + T + 12], fill="red")
            sheet.save(out / f"{run}_{c}.jpg", quality=80)
    (ROOT / "reports" / "palette_persistence.md").write_text("\n".join(md) + "\n"); (ROOT / "reports" / "palette_persistence.json").write_text(json.dumps(allres, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
