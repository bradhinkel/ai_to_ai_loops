"""Persistent-attractor atlas (Brad, 2026-10-20: attractors are never permanent, so an endpoint census is one time slice; look for
states that persist for at least n steps anywhere in the run). Pools EVERY intermediate step (1..99) of every cell in DINOv2,
clusters them jointly (k-means, k fixed, finer than the endpoint atlas), and labels each trajectory-step with the nearest centroid
within one fixed radius (hysteresis as gravity.py). A 'persistent visit' is a run of >= --min_dwell consecutive labelled steps.
Per cluster and cell: persistent visits, trajectories with one, steps inside, mean and longest dwell, endpoints, escape hazard
(exits / steps inside) and the share of the cell's trajectory-steps spent there. Attribution by the presence pattern over the
captioner x generator factorial, as in attractor_atlas.py, with 'present' = >= --min_visits persistent visits in the cell.
Clusters with no persistent visit anywhere are transit states and are dropped from the tables.
    .venv/bin/python analysis/persistent_atlas.py --cells a0_core:llava:sdxl e1_cap_pilot:qwen:sdxl e1_gen:llava:hunyuan e1_both:qwen:hunyuan --k 40 --min_dwell 5
Writes reports/persistent_atlas.md, .json and reports/persistent_atlas/cluster_<c>.jpg (one row per cell; thumbs are the
middle step of up to --per_row persistent visits, labelled traj:step). CLIP is not used (rule 4).
"""
import argparse, json, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache, cpu_only, series_matrix, image_path, thumb  # noqa: E402
from gravity import label_steps, visits  # noqa: E402


def unit(X):
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def main():
    cpu_only()
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", nargs="+", required=True, help="run:captioner:generator")
    ap.add_argument("--k", type=int, default=40); ap.add_argument("--radius", type=float, default=0.20); ap.add_argument("--exit_factor", type=float, default=1.25)
    ap.add_argument("--min_dwell", type=int, default=5); ap.add_argument("--min_visits", type=int, default=3)
    ap.add_argument("--names", default="archive/persistent_atlas_names.json"); ap.add_argument("--out", default="reports/persistent_atlas")
    ap.add_argument("--thumb", type=int, default=112); ap.add_argument("--per_row", type=int, default=10); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    cells = [dict(zip(("run", "cap", "gen"), c.split(":"))) for c in a.cells]
    caps = sorted({c["cap"] for c in cells}); gens = sorted({c["gen"] for c in cells})
    names = json.loads((ROOT / a.names).read_text()) if (ROOT / a.names).exists() else {}

    # all steps per cell: E[run] = [T, S, d] unit vectors (steps 1..S)
    E, trajs = {}, {}
    for c in cells:
        ser = series_matrix(Cache(c["run"]), "dinov2"); ts = sorted(ser); S = min(len(ser[t]) for t in ts)
        E[c["run"]] = unit(np.stack([ser[t][:S] for t in ts]).astype(np.float32)); trajs[c["run"]] = ts
    pooled = np.concatenate([E[c["run"]].reshape(-1, E[c["run"]].shape[-1]) for c in cells])
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=a.k, n_init=3, random_state=a.seed).fit(pooled); C = unit(km.cluster_centers_.astype(np.float32))
    print(f"k-means k={a.k} on {len(pooled)} steps done", flush=True)

    stats = {}   # (run, k) -> dict
    examples = {}
    for c in cells:
        r = c["run"]; X = E[r]; T, S, _ = X.shape
        D = 1.0 - np.einsum("kd,tsd->kts", C, X)
        L = label_steps(D, np.full(a.k, a.radius), a.exit_factor)
        for k in range(a.k):
            inside = L == k; steps_in = int(inside.sum()); exits = int((inside[:, :-1] & ~inside[:, 1:]).sum())
            dwells, ex = [], []
            for ti in range(T):
                pos = 0
                for length, censored in visits(inside[ti]):
                    # find the start index of this run
                    while pos < S and not inside[ti, pos]: pos += 1
                    start = pos; pos += length
                    if length >= a.min_dwell:
                        dwells.append(length); ex.append((trajs[r][ti], start + 1 + length // 2, length, bool(censored)))   # +1: series start at step 1
            stats[(r, k)] = dict(persistent_visits=len(dwells), trajectories=len({e[0] for e in ex}), steps_inside=steps_in, exits=exits,
                                 hazard=(exits / steps_in) if steps_in else None, mean_dwell=float(np.mean(dwells)) if dwells else None,
                                 longest_dwell=int(max(dwells)) if dwells else 0, endpoints=int(inside[:, -1].sum()),
                                 share_of_steps=steps_in / (T * S), still_there=int(sum(1 for e in ex if e[3])))
            examples[(r, k)] = sorted(ex, key=lambda e: -e[2])
    n_traj = {c["run"]: len(trajs[c["run"]]) for c in cells}

    clusters = []
    for k in range(a.k):
        tot = sum(stats[(c["run"], k)]["persistent_visits"] for c in cells)
        if tot == 0: continue
        present = {c["run"]: stats[(c["run"], k)]["persistent_visits"] >= a.min_visits for c in cells}
        pc = [c for c in cells if present[c["run"]]]; pcaps = {c["cap"] for c in pc}; pgens = {c["gen"] for c in pc}
        if len(pc) == len(cells): attr = "universal"
        elif len(pc) == 0: attr = "none (below threshold everywhere)"
        elif len(pc) == 1: attr = f"pair: {pc[0]['cap']} + {pc[0]['gen']}"
        elif len(pc) == 2 and len(pcaps) == 1 and len(gens) == 2: attr = f"captioner: {pcaps.pop()}"
        elif len(pc) == 2 and len(pgens) == 1 and len(caps) == 2: attr = f"generator: {pgens.pop()}"
        elif len(pc) == len(cells) - 1: attr = "all but " + [c["run"] for c in cells if not present[c["run"]]][0]
        else: attr = "mixed"
        rate = {c["run"]: stats[(c["run"], k)]["persistent_visits"] / n_traj[c["run"]] for c in cells}   # visits per trajectory, comparable across n
        d_cap = abs(np.mean([rate[c["run"]] for c in cells if c["cap"] == caps[0]]) - np.mean([rate[c["run"]] for c in cells if c["cap"] == caps[-1]])) if len(caps) == 2 else 0
        d_gen = abs(np.mean([rate[c["run"]] for c in cells if c["gen"] == gens[0]]) - np.mean([rate[c["run"]] for c in cells if c["gen"] == gens[-1]])) if len(gens) == 2 else 0
        clusters.append(dict(cluster=k, name=names.get(str(k), ""), total_persistent_visits=tot, attribution=attr,
                             captioner_fraction=None if d_cap + d_gen == 0 else round(float(d_cap / (d_cap + d_gen)), 2),
                             per_cell={c["run"]: stats[(c["run"], k)] for c in cells}, present=present,
                             examples={c["run"]: [list(e) for e in examples[(c["run"], k)][:a.per_row]] for c in cells}))
    clusters.sort(key=lambda c: -c["total_persistent_visits"])

    out = ROOT / a.out; out.mkdir(parents=True, exist_ok=True); T_ = a.thumb
    for cl in clusters:
        sheet = Image.new("RGB", (a.per_row * T_ + 130, len(cells) * T_), "white"); d = ImageDraw.Draw(sheet)
        for ri, c in enumerate(cells):
            st = cl["per_cell"][c["run"]]
            d.text((4, ri * T_ + 4), f"{c['run']}\nvisits {st['persistent_visits']}\ntraj {st['trajectories']}\nend {st['endpoints']}", fill="black")
            for j, (t, s, length, cens) in enumerate(cl["examples"][c["run"]]):
                p = image_path(ROOT / "runs" / c["run"], int(t), int(s))
                if pathlib.Path(p).exists():
                    sheet.paste(thumb(p, T_), (130 + j * T_, ri * T_)); d.text((132 + j * T_, ri * T_ + 2), f"{t}:{s} ({length})", fill="yellow")
        sheet.save(out / f"cluster_{cl['cluster']:02d}.jpg", quality=80)

    md = [f"# Persistent-attractor atlas: joint k = {a.k} over all {len(pooled)} intermediate steps of {', '.join(c['run'] for c in cells)}", "",
          "Cells (captioner x generator): " + "; ".join(f"{c['run']} = {c['cap']} + {c['gen']} (n {n_traj[c['run']]} trajectories)" for c in cells) + ".",
          f"Membership: nearest centroid within radius {a.radius} (DINOv2 cosine), hysteresis {a.exit_factor}x. Persistent visit = >= {a.min_dwell} consecutive steps inside. "
          f"'present' in a cell = >= {a.min_visits} persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / "
          "mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. "
          f"Clusters with no persistent visit anywhere ({a.k - len(clusters)} of {a.k}) are transit states and omitted. Names from `{a.names}` (blank = unnamed). "
          "Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.", "",
          "## Persistent attractors", "", "| cluster | name | " + " | ".join(c["run"] for c in cells) + " | attribution | captioner fraction |",
          "|---|---|" + "---|" * len(cells) + "---|---|"]
    for cl in clusters:
        cols = []
        for c in cells:
            st = cl["per_cell"][c["run"]]; hz = "-" if st["hazard"] is None else f"{st['hazard']:.2f}"; md_ = "-" if st["mean_dwell"] is None else f"{st['mean_dwell']:.0f}"
            cols.append(f"{st['persistent_visits']} / {st['trajectories']} / {st['endpoints']} / {md_} / {hz}")
        md.append(f"| {cl['cluster']} | {cl['name']} | " + " | ".join(cols) + f" | {cl['attribution']} | {'' if cl['captioner_fraction'] is None else cl['captioner_fraction']} |")
    md += ["", "## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)", ""]
    groups = [(f"captioner {cp}", [c for c in cells if c["cap"] == cp]) for cp in caps] + [(f"generator {g}", [c for c in cells if c["gen"] == g]) for g in gens] + \
             [(f"pair {c['cap']} + {c['gen']} ({c['run']})", [c]) for c in cells]
    for title, gc in groups:
        md += [f"### {title}", "", "| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |", "|---|---|---|---|---|"]
        rk = sorted(clusters, key=lambda cl: -sum(cl["per_cell"][c["run"]]["persistent_visits"] / n_traj[c["run"]] for c in gc))
        for cl in rk[:10]:
            v = [cl["per_cell"][c["run"]]["persistent_visits"] / n_traj[c["run"]] * 100 for c in gc]
            if sum(v) == 0: break
            md.append(f"| {cl['cluster']} | {cl['name']} | {sum(v):.0f} ({', '.join(f'{x:.0f}' for x in v)}) | {sum(cl['per_cell'][c['run']]['endpoints'] for c in gc)} | {cl['attribution']} |")
        md.append("")
    md += ["## Time spent in persistent attractors, per cell", "", "| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |", "|---|---|---|---|---|"]
    for c in cells:
        r = c["run"]; ks = [cl["cluster"] for cl in clusters]
        steps_share = sum(stats[(r, k)]["steps_inside"] for k in ks) / (n_traj[r] * E[r].shape[1]); end_share = sum(stats[(r, k)]["endpoints"] for k in ks) / n_traj[r]
        vis = sum(stats[(r, k)]["persistent_visits"] for k in ks); dw = [e[2] for k in ks for e in examples[(r, k)]]
        md.append(f"| {r} | {steps_share:.0%} | {end_share:.0%} | {vis / n_traj[r]:.2f} | {int(np.median(dw)) if dw else '-'} |")
    (ROOT / a.out).with_suffix(".md").write_text("\n".join(md) + "\n")
    (ROOT / a.out).with_suffix(".json").write_text(json.dumps(dict(cells=cells, k=a.k, radius=a.radius, min_dwell=a.min_dwell, min_visits=a.min_visits, clusters=clusters), indent=1, default=str))
    print("\n".join(md))


if __name__ == "__main__":
    main()
