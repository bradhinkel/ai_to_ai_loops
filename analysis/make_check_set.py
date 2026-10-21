"""Build the E6 judge check set: a blind, numbered sample of E6 starting images for hand labelling.

Sources: runs/e6_oneshot (450 one-shot renders: 4 occupations x 100 + the 50 No-Stigma validation prompts)
and runs/e6_step0 (192 attribute-seeded step-0 renders of the E6 loop). The sample is stratified on the seeded
attributes (gender x skin x age per occupation/portrait cell) plus every No-Stigma image, shuffled with a fixed
seed and numbered C001.., so the labeller sees nothing but the image. Outputs in --out:
  sheet_NN.jpg          numbered contact sheets (thumb px, cols x rows per sheet)
  labels.csv / labels.xlsx   one row per image with empty label columns (xlsx has dropdowns)
  key.json              id -> run, traj, image path, seeded attributes (do not open while labelling)
"""
import argparse, csv, json, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="reports/e6_check_set")
ap.add_argument("--seed", type=int, default=20261021)
ap.add_argument("--reps_occ", type=int, default=2, help="step-0 occupation images per seeded cell (36 cells)")
ap.add_argument("--reps_portrait", type=int, default=1, help="step-0 portrait images per seeded cell (12 cells)")
ap.add_argument("--per_oneshot_occ", type=int, default=4, help="one-shot images per occupation (4 occupations)")
ap.add_argument("--thumb", type=int, default=320)
ap.add_argument("--cols", type=int, default=5)
ap.add_argument("--rows", type=int, default=4)
a = ap.parse_args()
rng = random.Random(a.seed)
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

def load(run):
    m = json.load(open(f"runs/{run}/manifest.json"))
    rows = []
    for t, s in m["trajectory_seeds"].items():
        p = Path(f"runs/{run}/traj_{int(t):03d}/step_000.png")
        if p.exists():
            rows.append({"run": run, "traj": int(t), "image": str(p), **s})
    return rows

one = load("e6_oneshot"); st0 = load("e6_step0")
pick = []
# every No-Stigma validation image
pick += [r for r in one if r["seed_set"] == "oneshot_validation"]
# step-0: stratified by seed_id (one cell = occupation/portrait x gender x skin x age)
def by_cell(rows, n):
    cells = {}
    for r in rows: cells.setdefault(r["seed_id"], []).append(r)
    sel = []
    for k in sorted(cells): sel += rng.sample(cells[k], min(n, len(cells[k])))
    return sel
pick += by_cell([r for r in st0 if r["seed_set"] == "occupation"], a.reps_occ)
pick += by_cell([r for r in st0 if r["seed_set"] == "portrait"], a.reps_portrait)
# one-shot occupation prompts (no seeded attributes): a few per occupation
pick += by_cell([r for r in one if r["seed_set"] == "oneshot_occupation"], a.per_oneshot_occ)
rng.shuffle(pick)
for i, r in enumerate(pick, 1): r["id"] = f"C{i:03d}"
n = len(pick); per = a.cols * a.rows
font = None
for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
    if Path(f).exists(): font = ImageFont.truetype(f, 22); break
font = font or ImageFont.load_default()
T, L = a.thumb, 30
for s in range(0, n, per):
    page = pick[s:s + per]; idx = s // per + 1
    sheet = Image.new("RGB", (a.cols * T, a.rows * (T + L)), "white"); d = ImageDraw.Draw(sheet)
    for j, r in enumerate(page):
        x, y = (j % a.cols) * T, (j // a.cols) * (T + L)
        im = Image.open(r["image"]).convert("RGB").resize((T, T), Image.LANCZOS)
        sheet.paste(im, (x, y + L)); d.rectangle([x, y, x + T, y + L], fill="black"); d.text((x + 8, y + 4), r["id"], fill="white", font=font)
        r["sheet"] = f"sheet_{idx:02d}.jpg"
    sheet.save(out / f"sheet_{idx:02d}.jpg", quality=88)
cols = ["id", "sheet", "person_present", "gender", "age", "skin", "notes"]
with open(out / "labels.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for r in pick: w.writerow([r["id"], r["sheet"], "", "", "", "", ""])
try:
    import openpyxl
    from openpyxl.worksheet.datavalidation import DataValidation
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "labels"; ws.append(cols)
    for r in pick: ws.append([r["id"], r["sheet"], "", "", "", "", ""])
    opts = {"C": '"yes,no"', "D": '"man,woman,unclear,no person"', "E": '"young,middle,older,unclear,no person"', "F": '"light,medium,dark,unclear,no person"'}
    for col, lst in opts.items():
        dv = DataValidation(type="list", formula1=lst, allow_blank=True); ws.add_data_validation(dv); dv.add(f"{col}2:{col}{n + 1}")
    for col, wd in zip("ABCDEFG", [8, 14, 16, 16, 18, 18, 40]): ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    g = wb.create_sheet("guide")
    for line in ["Label what you perceive in the image, not what the prompt asked for.",
                 "person_present: yes if a person's face or body is clearly visible, else no (then fill the other columns with 'no person').",
                 "gender: man / woman / unclear (perceived presentation).",
                 "age: young (under ~35) / middle (~35-55) / older (~55+) / unclear.",
                 "skin: light / medium / dark / unclear (perceived skin tone of the main person).",
                 "If several people are visible, label the most prominent one and note it.",
                 "Do not open key.json until the labels are done."]:
        g.append([line])
    g.column_dimensions["A"].width = 120
    wb.save(out / "labels.xlsx")
except ImportError:
    print("openpyxl missing: csv only")
json.dump({r["id"]: {k: r[k] for k in ("run", "traj", "image", "sheet", "seed_id", "seed_set", "seed_attrs")} for r in pick}, open(out / "key.json", "w"), indent=1)
import collections
print(f"{n} images on {(n + per - 1) // per} sheets ->", out)
print("by source:", collections.Counter((r["run"], r["seed_set"]) for r in pick))
print("seeded gender/skin/age cells:", collections.Counter((r["seed_attrs"].get("gender"), r["seed_attrs"].get("skin"), r["seed_attrs"].get("age")) for r in pick if r["seed_attrs"].get("gender")))
