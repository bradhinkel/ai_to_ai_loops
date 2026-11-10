"""Endpoint contact sheets: an N x N grid of step-99 images from one run on a
single labelled page, written as PDF (plus PNG/JPEG for web use).

The images are placed at native resolution (512 px) and the PDF page is scaled
to US letter width, so nothing is resampled.

    python analysis/endpoint_sheets.py --run a0_core --grid 10 \
        --title "..." --subtitle "..." --out papers/figures/a0_core_endpoints_10x10
"""
import argparse, datetime, json, os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def build(run, grid, step, trajs, title, subtitle, footer, cell=512, gap=14, margin=110, number=True):
    n = grid * grid
    assert len(trajs) == n, (len(trajs), n)
    gw = grid * cell + (grid - 1) * gap
    page_w = gw + 2 * margin
    f_title = ImageFont.truetype(BOLD, int(cell * 0.17))
    f_sub = ImageFont.truetype(REG, int(cell * 0.105))
    f_foot = ImageFont.truetype(REG, int(cell * 0.085))
    f_num = ImageFont.truetype(BOLD, int(cell * 0.075))
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    title_lines = wrap(tmp, title, f_title, gw)
    sub_lines = wrap(tmp, subtitle, f_sub, gw)
    foot_lines = wrap(tmp, footer, f_foot, gw)
    lh_t, lh_s, lh_f = int(f_title.size * 1.3), int(f_sub.size * 1.35), int(f_foot.size * 1.35)
    head_h = len(title_lines) * lh_t + len(sub_lines) * lh_s + int(cell * 0.12)
    foot_h = len(foot_lines) * lh_f + int(cell * 0.08)
    page_h = margin + head_h + gw + foot_h + margin
    page = Image.new("RGB", (page_w, page_h), "white")
    d = ImageDraw.Draw(page)
    y = margin
    for ln in title_lines:
        d.text((margin, y), ln, font=f_title, fill="black"); y += lh_t
    for ln in sub_lines:
        d.text((margin, y), ln, font=f_sub, fill=(60, 60, 60)); y += lh_s
    y0 = margin + head_h
    for i, t in enumerate(trajs):
        p = f"runs/{run}/traj_{t:03d}/step_{step:03d}.png"
        im = Image.open(p).convert("RGB")
        if im.size != (cell, cell):
            im = im.resize((cell, cell), Image.LANCZOS)
        r, c = divmod(i, grid)
        x, yy = margin + c * (cell + gap), y0 + r * (cell + gap)
        page.paste(im, (x, yy))
        if number:
            lab = f"{t:02d}"
            tw = d.textlength(lab, font=f_num)
            pad = 6
            d.rectangle([x, yy, x + tw + 2 * pad, yy + f_num.size + 2 * pad], fill=(0, 0, 0))
            d.text((x + pad, yy + pad - 1), lab, font=f_num, fill="white")
    y = y0 + gw + int(cell * 0.08)
    for ln in foot_lines:
        d.text((margin, y), ln, font=f_foot, fill=(90, 90, 90)); y += lh_f
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--grid", type=int, default=10)
    ap.add_argument("--step", type=int, default=99)
    ap.add_argument("--first", type=int, default=0, help="first trajectory index (grid^2 consecutive)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--footer", default="")
    ap.add_argument("--out", required=True, help="output path without extension")
    ap.add_argument("--jpeg", action="store_true", help="also write a JPEG (q 90) for web upload")
    ap.add_argument("--png", action="store_true", help="also write a lossless PNG")
    ap.add_argument("--no-numbers", action="store_true")
    a = ap.parse_args()
    man = json.load(open(f"runs/{a.run}/manifest.json"))
    trajs = man["trajectories"][a.first:a.first + a.grid * a.grid]
    page = build(a.run, a.grid, a.step, trajs, a.title, a.subtitle, a.footer, number=not a.no_numbers)
    dpi = page.width / 8.5  # scale the page to US-letter width
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    page.save(a.out + ".pdf", "PDF", resolution=dpi, title=a.title,
              author="Brad Hinkel", creationDate=datetime.datetime.now().strftime("D:%Y%m%d%H%M%S"))
    if a.png:
        page.save(a.out + ".png", "PNG", optimize=True)
    if a.jpeg:
        page.save(a.out + ".jpg", "JPEG", quality=90, optimize=True)
    print(a.out, page.size, f"{page.width/dpi:.2f}x{page.height/dpi:.2f} in", "trajs", trajs[0], "..", trajs[-1])


if __name__ == "__main__":
    main()
