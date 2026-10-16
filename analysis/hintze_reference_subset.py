"""Build the Hintze T=0.9 reference subset used for documentation and A0 comparison.

Input: the extracted figshare archive (file 59352803, temps_0.9.zip) at data/hintze_figshare/temps_0.9/.
  mosaics/run_RRR_rep_0_temp_0.9_grid_10x10.jpg  5120x5120, 100 tiles of 512x512, row-major, tile i = image at step i
  logs/run_RRR_rep_0_temp_0.9.csv                 run_id,rep_id,step,prompt; step 0 = seed prompt, step k = caption of image k-1
  images/*.png                                    partial leftovers (mostly step 99); not used here

Output (reports/hintze_reference/):
  run_RRR/step_NNN.jpg       cropped tiles at the sample steps for the sample runs
  trajectories.jpg           contact sheet: one row per sample run, one column per sample step
  endpoints_step099.jpg      10x10 sheet of every run's step-99 image (the attractors)
  captions.md                seed prompt and captions at the sample steps for each sample run
"""
import argparse, csv, pathlib, sys
from PIL import Image, ImageDraw

STEPS = [0, 1, 5, 10, 25, 50, 75, 99]
TILE = 512


def tile(mosaic, step, src=None, run=None):
    """Tile for `step` from the mosaic; falls back to the loose PNG when the tile is blank (run 019's last tiles)."""
    r, c = divmod(step, 10)
    im = mosaic.crop((c * TILE, r * TILE, (c + 1) * TILE, (r + 1) * TILE))
    if src is not None and im.resize((8, 8)).convert("L").getextrema()[0] > 250:
        loose = src / "images" / f"run_{run:03d}_rep_0_step_{step:03d}_temp_0.9.png"
        if loose.exists():
            return Image.open(loose).convert("RGB")
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/hintze_figshare/temps_0.9")
    ap.add_argument("--out", default="reports/hintze_reference")
    ap.add_argument("--runs", default="0,10,20,30,40,50,60,70", help="comma-separated run ids for the trajectory sheet")
    ap.add_argument("--thumb", type=int, default=256)
    a = ap.parse_args()
    src, out = pathlib.Path(a.src), pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    runs = [int(x) for x in a.runs.split(",")]
    T = a.thumb

    md = ["# Hintze et al. T=0.9 reference subset\n",
          "Source: figshare 30553604, file temps_0.9.zip. Captions are Hintze's LLaVA outputs; the caption at step k describes the image at step k-1.\n"]
    sheet = Image.new("RGB", (T * len(STEPS), T * len(runs)), "white")
    for ri, run in enumerate(runs):
        mosaic = Image.open(src / "mosaics" / f"run_{run:03d}_rep_0_temp_0.9_grid_10x10.jpg").convert("RGB")
        rows = list(csv.DictReader(open(src / "logs" / f"run_{run:03d}_rep_0_temp_0.9.csv", newline="")))
        rdir = out / f"run_{run:03d}"; rdir.mkdir(exist_ok=True)
        md.append(f"\n## run_{run:03d} ({len(rows)} caption rows)\n")
        md.append(f"- **seed prompt (step 0):** {rows[0]['prompt'].strip()}\n")
        for si, s in enumerate(STEPS):
            im = tile(mosaic, s, src, run)
            im.save(rdir / f"step_{s:03d}.jpg", quality=90)
            sheet.paste(im.resize((T, T), Image.LANCZOS), (si * T, ri * T))
            cap = rows[s + 1]["prompt"].strip() if s + 1 < len(rows) else "(no caption row)"
            md.append(f"- **caption of step {s} image (csv step {s+1}):** {cap}\n")
    d = ImageDraw.Draw(sheet)
    for si, s in enumerate(STEPS):
        d.rectangle((si * T, 0, si * T + 52, 14), fill="black"); d.text((si * T + 2, 1), f"step {s}", fill="white")
    for ri, run in enumerate(runs):
        d.rectangle((0, ri * T + 16, 52, ri * T + 30), fill="black"); d.text((2, ri * T + 17), f"run {run:03d}", fill="white")
    sheet.save(out / "trajectories.jpg", quality=85)

    end = Image.new("RGB", (T * 10, T * 10), "white")
    for run in range(100):
        p = src / "mosaics" / f"run_{run:03d}_rep_0_temp_0.9_grid_10x10.jpg"
        if not p.exists():
            continue
        r, c = divmod(run, 10)
        end.paste(tile(Image.open(p).convert("RGB"), 99, src, run).resize((T, T), Image.LANCZOS), (c * T, r * T))
    end.save(out / "endpoints_step099.jpg", quality=85)
    (out / "captions.md").write_text("".join(md))
    print("wrote", out)


if __name__ == "__main__":
    main()
