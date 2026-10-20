"""Escape-hazard hypothesis test (predictions.md note of 2026-10-19). Brad: for an attractor shared by two cells, per-step escape
hazard tracks the attractor (agrees within a factor of 2 across all cell pairs). Claude: it tracks the captioner (agrees only
within a captioner). Reads reports/persistent_atlas.json (per cluster and cell: steps inside, exits, hazard at one fixed radius)
and, for every cluster with >= --min_steps inside in both cells of a pair, reports the hazard ratio per pair type.
    .venv/bin/python analysis/hazard_test.py --min_steps 40
"""
import argparse, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); from common import ROOT  # noqa: E402


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--atlas", default="reports/persistent_atlas.json"); ap.add_argument("--min_steps", type=int, default=40); a = ap.parse_args()
    d = json.load(open(ROOT / a.atlas)); cells = d["cells"]; by = {c["run"]: c for c in cells}
    pairs = []
    for i, c1 in enumerate(cells):
        for c2 in cells[i + 1:]:
            kind = "same captioner" if c1["cap"] == c2["cap"] else ("same generator" if c1["gen"] == c2["gen"] else "nothing shared")
            pairs.append((c1["run"], c2["run"], kind))
    rows = []
    for cl in d["clusters"]:
        for r1, r2, kind in pairs:
            s1, s2 = cl["per_cell"][r1], cl["per_cell"][r2]
            if s1["steps_inside"] >= a.min_steps and s2["steps_inside"] >= a.min_steps and s1["hazard"] and s2["hazard"]:
                ratio = max(s1["hazard"], s2["hazard"]) / min(s1["hazard"], s2["hazard"])
                rows.append(dict(cluster=cl["cluster"], name=cl["name"], pair=f"{r1} / {r2}", kind=kind, h1=s1["hazard"], h2=s2["hazard"], n1=s1["steps_inside"], n2=s2["steps_inside"], ratio=ratio))
    md = ["# Escape-hazard test across the E1 2x2", "", f"Source: `{a.atlas}` (fixed radius {d['radius']}, dwell >= {d['min_dwell']}). A pair counts when both cells have >= {a.min_steps} trajectory-steps inside the cluster. "
          "Ratio = larger hazard / smaller hazard. Brad's claim: ratios <= 2 for every pair type. Claude's: <= 2 only for same-captioner pairs.", "",
          "| cluster | name | pair | pair type | hazard 1 (steps) | hazard 2 (steps) | ratio |", "|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["kind"], r["ratio"])):
        md.append(f"| {r['cluster']} | {r['name']} | {r['pair']} | {r['kind']} | {r['h1']:.3f} ({r['n1']}) | {r['h2']:.3f} ({r['n2']}) | {r['ratio']:.2f} |")
    md += ["", "| pair type | n comparisons | median ratio | share within 2x |", "|---|---|---|---|"]
    for kind in ("same captioner", "same generator", "nothing shared"):
        rs = [r["ratio"] for r in rows if r["kind"] == kind]
        md.append(f"| {kind} | {len(rs)} | {np.median(rs):.2f} | {np.mean([x <= 2 for x in rs]):.0%} |" if rs else f"| {kind} | 0 | - | - |")
    (ROOT / "reports" / "hazard_test.md").write_text("\n".join(md) + "\n"); print("\n".join(md))


if __name__ == "__main__":
    main()
