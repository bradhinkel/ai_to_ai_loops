"""Attractor atlas for the E1 2x2 (Brad, 2026-10-20: "a list of top attractors associated with each model - even specific to the
caption and generator models"). Pools the final-step DINOv2 embeddings of every cell, clusters them jointly (k fixed, finer than
the elbow so distinct motifs are not merged), and attributes each joint cluster by the presence pattern over the factorial:
  present in all cells                      -> universal
  present only in the two cells of captioner C -> captioner: C
  present only in the two cells of generator G -> generator: G
  present in one cell                        -> pair: C + G
  present in three                           -> all but <cell>   (suppressed by that pair)
  present in a diagonal pair                 -> mixed
'present' = at least --min_share of the cell's endpoints (and >= 2 endpoints). Also, for every cluster and cell, the transit
numbers at ONE fixed radius (as gravity.py): endpoints inside, trajectories that ever visited, steps inside, exits, per-step
escape hazard; these are the inputs of the escape-hazard test in predictions.md (2026-10-19). Sheets: one per cluster, one row
per cell, so attractors can be named by eye; names go in --names (json {cluster: name}) and are re-applied on the next run.
    .venv/bin/python analysis/attractor_atlas.py --cells a0_core:llava:sdxl e1_cap_pilot:qwen:sdxl e1_gen:llava:hunyuan e1_both:qwen:hunyuan --k 16
Writes reports/attractor_atlas.md, .json and reports/attractor_atlas/cluster_<c>.jpg. CLIP is not used (rule 4).
"""
import argparse, json, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache, cpu_only, kmeans, final_step_matrix, series_matrix, image_path, thumb  # noqa: E402
from gravity import label_steps  # noqa: E402


def unit(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def carry_names(C, names_path, cent_path, max_dist=0.10):
    """Names are hand-written against one clustering; when the cells change, clusters re-index. Carry each saved name to the
    nearest new centroid (cosine distance <= max_dist) from the centroids saved with the previous run; others start blank."""
    names = json.loads((ROOT / names_path).read_text()) if (ROOT / names_path).exists() else {}
    cp = ROOT / cent_path
    if cp.exists():
        z = np.load(cp, allow_pickle=True); Cp = z["C"]; np_names = list(z["names"])
        Cp = Cp / np.linalg.norm(Cp, axis=1, keepdims=True)
        if Cp.shape[1] == C.shape[1] and len(np_names) == len(Cp):
            D = 1.0 - C @ Cp.T; carried = {}
            for k in range(len(C)):
                j = int(D[k].argmin())
                if D[k, j] <= max_dist and np_names[j]: carried[str(k)] = np_names[j]
            # hand edits in the names file (keyed by the CURRENT indices) win only if the file is newer than the centroid file
            if (ROOT / names_path).exists() and (ROOT / names_path).stat().st_mtime > cp.stat().st_mtime:
                carried.update({k: v for k, v in names.items() if v})
            names = carried
    return names


def save_centroids(C, names, cent_path, k):
    np.savez(ROOT / cent_path, C=C, names=np.array([names.get(str(i), "") for i in range(k)], dtype=object))


def main():
    cpu_only()
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", nargs="+", required=True, help="run:captioner:generator")
    ap.add_argument("--k", type=int, default=16); ap.add_argument("--radius", type=float, default=0.20); ap.add_argument("--exit_factor", type=float, default=1.25)
    ap.add_argument("--min_share", type=float, default=0.05); ap.add_argument("--names", default="archive/atlas_names.json")
    ap.add_argument("--out", default="reports/attractor_atlas"); ap.add_argument("--thumb", type=int, default=112); ap.add_argument("--per_row", type=int, default=10)
    a = ap.parse_args()
    cells = [dict(zip(("run", "cap", "gen"), c.split(":"))) for c in a.cells]
    caps = sorted({c["cap"] for c in cells}); gens = sorted({c["gen"] for c in cells})

    # final-step embeddings per cell
    ids, X, grp = {}, [], []
    for c in cells:
        i, x, _ = final_step_matrix(Cache(c["run"]), "dinov2", ROOT / "runs" / c["run"]); ids[c["run"]] = i; X.append(x); grp += [c["run"]] * len(x)
    X = unit(np.concatenate(X)); grp = np.array(grp)
    km = kmeans(X, a.k); lab = km.labels_; C = unit(km.cluster_centers_.astype(np.float64))
    n_cell = {c["run"]: int((grp == c["run"]).sum()) for c in cells}
    cent_path = a.names.replace(".json", "_centroids.npz"); names = carry_names(C, a.names, cent_path); save_centroids(C, names, cent_path, a.k)
    (ROOT / a.names).write_text(json.dumps({str(i): names.get(str(i), "") for i in range(a.k)}, indent=1, ensure_ascii=False))

    # transit numbers per cell at the fixed radius
    transit = {}
    for c in cells:
        ser = series_matrix(Cache(c["run"]), "dinov2"); trajs = sorted(ser); S = min(len(ser[t]) for t in trajs)
        E = np.stack([unit(ser[t][:S]) for t in trajs])                      # [T,S,d]
        D = 1.0 - np.einsum("kd,tsd->kts", C, E)                              # [K,T,S]
        L = label_steps(D, np.full(a.k, a.radius), a.exit_factor)
        for k in range(a.k):
            inside = L == k; steps_in = int(inside.sum()); exits = int((inside[:, :-1] & ~inside[:, 1:]).sum())
            transit[(c["run"], k)] = dict(visited=int(inside.any(1).sum()), stayed=int(inside[:, -1].sum()), steps_inside=steps_in, exits=exits,
                                          hazard=(exits / steps_in) if steps_in else None)

    clusters = []
    for k in range(a.k):
        m = lab == k; comp = {c["run"]: int((grp[m] == c["run"]).sum()) for c in cells}
        share = {r: comp[r] / n_cell[r] for r in comp}
        present = {r: (share[r] >= a.min_share and comp[r] >= 2) for r in comp}
        pc = [c for c in cells if present[c["run"]]]
        pcaps = {c["cap"] for c in pc}; pgens = {c["gen"] for c in pc}
        if len(pc) == len(cells): attr = "universal"
        elif len(pc) == 0: attr = "none (below threshold everywhere)"
        elif len(pc) == 1: attr = f"pair: {pc[0]['cap']} + {pc[0]['gen']}"
        elif len(pc) == 2 and len(pcaps) == 1 and len(gens) == 2: attr = f"captioner: {pcaps.pop()}"
        elif len(pc) == 2 and len(pgens) == 1 and len(caps) == 2: attr = f"generator: {pgens.pop()}"
        elif len(pc) == len(cells) - 1: attr = "all but " + [c["run"] for c in cells if not present[c["run"]]][0]
        else: attr = "mixed"
        # graded attribution: how much of the between-cell variation in share is along the captioner axis vs the generator axis
        d_cap = abs(np.mean([share[c["run"]] for c in cells if c["cap"] == caps[0]]) - np.mean([share[c["run"]] for c in cells if c["cap"] == caps[-1]])) if len(caps) == 2 else 0
        d_gen = abs(np.mean([share[c["run"]] for c in cells if c["gen"] == gens[0]]) - np.mean([share[c["run"]] for c in cells if c["gen"] == gens[-1]])) if len(gens) == 2 else 0
        cap_frac = d_cap / (d_cap + d_gen) if (d_cap + d_gen) > 0 else None
        members = {c["run"]: [int(t) for t, l, g in zip(sum((ids[c2["run"]] for c2 in cells), []), lab, grp) if l == k and g == c["run"]] for c in cells}
        dm = 1.0 - X[m] @ C[k]; r95 = float(np.percentile(dm, 95)) if m.sum() > 1 else 0.0
        clusters.append(dict(cluster=k, name=names.get(str(k), ""), size=int(m.sum()), composition=comp, share={r: round(s, 3) for r, s in share.items()},
                             present=present, attribution=attr, captioner_fraction=None if cap_frac is None else round(float(cap_frac), 2), r95=round(r95, 3),
                             loose=bool(r95 > 0.6), members=members, transit={r: transit[(r, k)] for r in comp}))
    clusters.sort(key=lambda c: -c["size"])

    # sheets: one per cluster, one row per cell
    out = ROOT / a.out; out.mkdir(parents=True, exist_ok=True); T = a.thumb
    for cl in clusters:
        rows = len(cells); sheet = Image.new("RGB", (a.per_row * T + 120, rows * T), "white"); d = ImageDraw.Draw(sheet)
        for ri, c in enumerate(cells):
            d.text((4, ri * T + 4), f"{c['run']}\n{cl['composition'][c['run']]} / {n_cell[c['run']]}", fill="black")
            for j, t in enumerate(cl["members"][c["run"]][:a.per_row]):
                p = image_path(ROOT / "runs" / c["run"], t, 99)
                if not pathlib.Path(p).exists():
                    cands = sorted((ROOT / "runs" / c["run"] / f"traj_{t:03d}").glob("step_*.png")); p = cands[-1] if cands else None
                if p: sheet.paste(thumb(p, T), (120 + j * T, ri * T))
        sheet.save(out / f"cluster_{cl['cluster']:02d}.jpg", quality=80)

    # markdown
    md = [f"# Attractor atlas: joint k = {a.k} over {len(X)} final-step DINOv2 endpoints of {', '.join(c['run'] for c in cells)}", "",
          f"Cells (captioner x generator): " + "; ".join(f"{c['run']} = {c['cap']} + {c['gen']} (n {n_cell[c['run']]})" for c in cells) + ".",
          f"'present' = >= {a.min_share:.0%} of a cell's endpoints and >= 2. Transit at one fixed radius {a.radius} (hysteresis {a.exit_factor}x): "
          "visited = trajectories ever inside, steps = trajectory-steps inside, hazard = exits / steps inside. r95 = cluster's 95th-percentile member distance; "
          "loose (r95 > 0.6) clusters are catch-alls, not attractors. Names from `archive/atlas_names.json` (hand-labelled from the sheets); blank = not yet named. "
          "Sheets: `cluster_<c>.jpg`, one row per cell. CLIP is not used.", "",
          "## All clusters", "", "| cluster | name | size | " + " | ".join(c["run"] for c in cells) + " | attribution | captioner fraction of the difference | r95 |",
          "|---|---|---|" + "---|" * len(cells) + "---|---|---|"]
    for cl in clusters:
        md.append(f"| {cl['cluster']} | {cl['name']} | {cl['size']}{' (loose)' if cl['loose'] else ''} | " +
                  " | ".join(f"{cl['composition'][c['run']]} ({cl['share'][c['run']]:.0%})" for c in cells) +
                  f" | {cl['attribution']} | {'' if cl['captioner_fraction'] is None else cl['captioner_fraction']} | {cl['r95']} |")
    md += ["", "## Top attractors by component (endpoints in the component's cells; loose clusters excluded)", ""]
    groups = [(f"captioner {cp}", [c for c in cells if c["cap"] == cp]) for cp in caps] + [(f"generator {g}", [c for c in cells if c["gen"] == g]) for g in gens] + \
             [(f"pair {c['cap']} + {c['gen']} ({c['run']})", [c]) for c in cells]
    for title, gc in groups:
        md += [f"### {title}", "", "| cluster | name | endpoints in these cells | attribution |", "|---|---|---|---|"]
        rk = sorted([cl for cl in clusters if not cl["loose"]], key=lambda cl: -sum(cl["composition"][c["run"]] for c in gc))
        for cl in rk[:8]:
            n = sum(cl["composition"][c["run"]] for c in gc)
            if n == 0: break
            md.append(f"| {cl['cluster']} | {cl['name']} | {n} ({', '.join(str(cl['composition'][c['run']]) for c in gc)}) | {cl['attribution']} |")
        md.append("")
    md += ["## Transit and escape hazard per cell (fixed radius)", "", "| cluster | name | " + " | ".join(f"{c['run']}: stayed / visited / steps / hazard" for c in cells) + " |",
           "|---|---|" + "---|" * len(cells)]
    for cl in clusters:
        if cl["loose"]: continue
        cellstr = []
        for c in cells:
            t = cl["transit"][c["run"]]; hz = "-" if t["hazard"] is None else f"{t['hazard']:.3f}"
            cellstr.append(f"{t['stayed']} / {t['visited']} / {t['steps_inside']} / {hz}")
        md.append(f"| {cl['cluster']} | {cl['name']} | " + " | ".join(cellstr) + " |")
    (ROOT / a.out).with_suffix(".md").write_text("\n".join(md) + "\n")
    (ROOT / a.out).with_suffix(".json").write_text(json.dumps(dict(cells=cells, k=a.k, radius=a.radius, min_share=a.min_share, clusters=clusters), indent=1, default=str))
    print("\n".join(md))


if __name__ == "__main__":
    main()
