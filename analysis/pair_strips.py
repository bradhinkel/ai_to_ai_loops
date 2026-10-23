"""Side-by-side trajectory strips for two runs that share seeds (E2-QZ vs E1-both): for each trajectory, one row per run,
one thumb per listed step, labelled run:traj:step. Rebuilds from runs/ only.

    .venv/bin/python analysis/pair_strips.py e2_qz e1_both --trajs 3,7,12 --steps 0,1,2,5,10,20,50,99 --out reports/e2_qz/strips_faces.jpg
"""
import argparse, pathlib, sys
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, image_path  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs=2); ap.add_argument("--trajs", required=True); ap.add_argument("--steps", default="0,1,2,5,10,20,50,99")
    ap.add_argument("--thumb", type=int, default=160); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv); trajs = [int(x) for x in a.trajs.split(",")]; steps = [int(x) for x in a.steps.split(",")]; T = a.thumb
    rows = len(trajs) * 2; sheet = Image.new("RGB", (len(steps) * T, rows * (T + 14) + 4 * len(trajs)), "white"); d = ImageDraw.Draw(sheet)
    y = 0
    for t in trajs:
        for run in a.runs:
            for i, s in enumerate(steps):
                p = image_path(ROOT / "runs" / run, t, s)
                if p.exists(): sheet.paste(Image.open(p).convert("RGB").resize((T, T)), (i * T, y))
                d.text((i * T + 3, y + T + 1), f"{run}:{t}:{s}", fill="black")
            y += T + 14
        y += 4
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True); sheet.save(a.out, quality=85); print(a.out, sheet.size)


if __name__ == "__main__":
    main()
