"""E1 comparison: does each run converge, and how much do its attractors overlap the reference (A0) archive? (SPEC2 §4)

    .venv/bin/python analysis/e1_report.py --ref a0_core --runs e1_cap e1_gen e1_both [--out reports/e1] [--step 99]

Needs analysis/embed.py for the ref and every run (dinov2 + minilm; clip only for the ref archive). Per run, on DINOv2 (primary)
and MiniLM (secondary), using a0_report's rules (see common.py):
  elbow k on the final-step embeddings; Vendi score of the final-step embeddings; plateau step of the mean step-to-step
  DINOv2 drift; drift curves (step-to-step d(k,k-1) and cumulative d(k,1), k >= 2; step 0 excluded) overlaid for all runs.
Overlap with the ref: share of final-step images inside the ref archive's per-cluster DINOv2 radii (archive/<ref>_centroids.npz,
built with build_archive.py if missing); a joint k-means over the pooled final-step DINOv2 embeddings (k = elbow on the pool),
each joint cluster labelled "shared" (ref >= 20% of members and some run >= 20%), "ref only" or "unique to <run>".
Outputs in --out: summary.json, summary.md, drift_dinov2.png, drift_minilm.png, elbow.png, endpoints_<run>.jpg (per run,
grouped by joint cluster), joint_clusters.jpg. No CLIP-based number appears here (CLIP steers; it never grades).
"""
import argparse, datetime, json, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from common import (ROOT, Cache, MODELS, SERIES, GRAY, package_versions, final_step_matrix, series_matrix, read_record, image_path,
                    elbow_k, k_for_sheet, kmeans, plateau_step, vendi, drift_curves, cos_dist, style, thumb)

SHARE_MIN = 0.20   # a group "holds" a joint cluster when it supplies >= 20% of its members


def analyse_run(run, step):
    cache = Cache(run); run_dir = ROOT / "runs" / run; r = {"run": run}
    for space in ("dinov2", "minilm"):
        ids, X, used = final_step_matrix(cache, space, run_dir, step)
        elbow, ks, inertia = elbow_k(X) if len(X) >= 3 else (None, [], [])
        series = series_matrix(cache, space)
        step_d, cum_d, mean_step, mean_cum, L = drift_curves(series)
        r[space] = {"ids": ids, "X": X, "final_steps": used, "elbow_k": elbow, "ks": ks, "inertia": inertia, "vendi": vendi(X) if len(X) >= 2 else None,
                    "mean_step": mean_step, "mean_cum": mean_cum, "L": L, "n_series": len(series),
                    "plateau_step": plateau_step(mean_step, first_step=2), "step_drift_last20": float(mean_step[-20:].mean()) if L else None}
    assert r["dinov2"]["ids"] == r["minilm"]["ids"], f"{run}: dinov2 and minilm caches cover different trajectories; re-run embed.py"
    return r


def ensure_archive(ref):
    p = ROOT / "archive" / f"{ref}_centroids.npz"
    if not p.exists():
        print(f"archive for {ref} missing -> building it", flush=True)
        subprocess.run([sys.executable, str(ROOT / "analysis" / "build_archive.py"), ref], check=True)
    z = np.load(p, allow_pickle=True)
    return {k: z[k] for k in z.files}


def overlap(X, arch):
    """Per endpoint: nearest ref centroid (cosine), inside its per-cluster radius?, inside the pooled radius?"""
    C = arch["centroid_dinov2"].astype(np.float64); R = arch["radius"].astype(np.float64)
    D = 1.0 - (X / np.linalg.norm(X, axis=1, keepdims=True)) @ (C / np.linalg.norm(C, axis=1, keepdims=True)).T   # [n, k]
    nearest = D.argmin(axis=1); dmin = D[np.arange(len(X)), nearest]
    inside_any = (D <= R[None, :] + 1e-6).any(axis=1)          # tolerance: a singleton cluster has radius 0 and its own member sits at ~1e-7
    return {"nearest": nearest, "dmin": dmin, "inside_cluster_radii": inside_any, "inside_pooled_radius": dmin <= float(arch["radius_pooled"]) + 1e-6,
            "share_inside_cluster_radii": float(inside_any.mean()), "share_inside_pooled_radius": float((dmin <= float(arch["radius_pooled"]) + 1e-6).mean()),
            "share_per_ref_cluster": {str(c): float((inside_any & (nearest == c)).mean()) for c in range(len(C))}}


def joint_clustering(results, ref):
    names = [r["run"] for r in results]
    X = np.concatenate([r["dinov2"]["X"] for r in results]); group = np.concatenate([[r["run"]] * len(r["dinov2"]["X"]) for r in results])
    elbow, ks, inertia = elbow_k(X) if len(X) >= 3 else (None, [], [])
    k = min(k_for_sheet(elbow, len(X)), len(X)); labels = kmeans(X, k).labels_
    clusters = []
    for c in range(k):
        m = labels == c; comp = {g: int((group[m] == g).sum()) for g in names}; n = int(m.sum())
        share = {g: comp[g] / n for g in names}
        holders = [g for g in names if share[g] >= SHARE_MIN]
        if share[ref] >= SHARE_MIN and any(share[g] >= SHARE_MIN for g in names if g != ref): label = "shared"
        elif share[ref] >= SHARE_MIN: label = "ref only"
        else: label = "unique to " + "+".join(g for g in holders if g != ref)
        clusters.append({"cluster": c, "size": n, "composition": comp, "share": {g: round(s, 3) for g, s in share.items()}, "label": label,
                         "members": {g: [int(t) for t, l, gg in zip(np.concatenate([r["dinov2"]["ids"] for r in results]), labels, group) if l == c and gg == g] for g in names}})
    return {"k": k, "elbow_k": elbow, "ks": ks, "inertia": inertia, "n_pooled": int(len(X)), "labels": labels, "group": group, "clusters": clusters}


def drift_figure(results, space, out, plt):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
    for i, r in enumerate(results):
        d = r[space]; col = SERIES[i % len(SERIES)]
        if not d["L"]: continue
        x = np.arange(2, 2 + d["L"])
        axes[0].plot(x, d["mean_step"], color=col, linewidth=2, label=f"{r['run']} (n={d['n_series']})")
        axes[1].plot(x, d["mean_cum"], color=col, linewidth=2, label=r["run"])
        if d["plateau_step"] and space == "dinov2": axes[0].axvline(d["plateau_step"], color=col, linewidth=1, linestyle="--", alpha=0.7)
    name = {"dinov2": "DINOv2 image", "minilm": "MiniLM caption"}[space]
    style(axes[0], f"Step-to-step drift, {name} (d(k, k-1), mean over trajectories)", "step k", "cosine distance")
    style(axes[1], f"Cumulative drift, {name} (d(k, 1))", "step k", "cosine distance")
    axes[0].legend(frameon=False, fontsize=8); axes[1].legend(frameon=False, fontsize=8)
    if space == "dinov2": axes[0].text(0.99, 0.97, "dashed: plateau step", transform=axes[0].transAxes, ha="right", va="top", fontsize=8, color="#52514e")
    fig.tight_layout(); fig.savefig(out / f"drift_{space}.png"); plt.close(fig)


def elbow_figure(results, joint, out, plt):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.0), dpi=130)
    for ax, space in zip(axes, ("dinov2", "minilm")):
        for i, r in enumerate(results):
            d = r[space]
            if not d["ks"]: continue
            inert = np.array(d["inertia"]) / d["inertia"][0]
            ax.plot(d["ks"], inert, color=SERIES[i % len(SERIES)], linewidth=2, marker="o", markersize=3, label=f"{r['run']} (elbow {d['elbow_k']})")
        if space == "dinov2" and joint["ks"]:
            ax.plot(joint["ks"], np.array(joint["inertia"]) / joint["inertia"][0], color=GRAY, linewidth=2, linestyle="--", label=f"pooled (elbow {joint['elbow_k']})")
        style(ax, f"k-means inertia, final-step {space} (÷ inertia at k=2)", "k", "relative inertia")
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(out / "elbow.png"); plt.close(fig)


def endpoint_sheets(results, joint, out, T=128, cols=10):
    """Per run: final-step images grouped by joint cluster, labelled with the joint cluster id and its label."""
    lab = {c["cluster"]: c["label"] for c in joint["clusters"]}
    for r in results:
        run = r["run"]; ids = r["dinov2"]["ids"]; used = r["dinov2"]["final_steps"]
        mine = [(int(c), t) for c in range(joint["k"]) for t in joint["clusters"][c]["members"][run]]
        rows = (len(mine) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * T, max(1, rows) * T), "white"); d = ImageDraw.Draw(sheet)
        for n, (c, t) in enumerate(mine):
            rr, cc = divmod(n, cols); sheet.paste(thumb(image_path(ROOT / "runs" / run, t, used[t]), T), (cc * T, rr * T))
            tag = f"j{c} {lab[c][:14]} t{t:03d}"; d.rectangle((cc * T, rr * T, cc * T + 6 * len(tag) + 4, rr * T + 12), fill="black"); d.text((cc * T + 2, rr * T), tag, fill="white")
        sheet.save(out / f"endpoints_{run}.jpg", quality=88)
    # joint sheet: one row per joint cluster, members from all runs, tagged with run
    k = joint["k"]; pad = 16; width = max(c["size"] for c in joint["clusters"])
    sheet = Image.new("RGB", (min(width, 24) * T, k * (T + pad)), "white"); d = ImageDraw.Draw(sheet)
    for c in joint["clusters"]:
        y = c["cluster"] * (T + pad); d.text((4, y + 2), f"joint cluster {c['cluster']}  size {c['size']}  {c['label']}  composition {c['composition']}", fill="black"); n = 0
        for r in results:
            run = r["run"]; used = r["dinov2"]["final_steps"]
            for t in c["members"][run]:
                if n >= 24: break
                sheet.paste(thumb(image_path(ROOT / "runs" / run, t, used[t]), T), (n * T, y + pad))
                tag = f"{run[:10]} t{t:03d}"; d.rectangle((n * T, y + pad, n * T + 6 * len(tag) + 4, y + pad + 12), fill="black"); d.text((n * T + 2, y + pad), tag, fill="white"); n += 1
    sheet.save(out / "joint_clusters.jpg", quality=88)


def fmt(v, nd=2):
    return "–" if v is None else (f"{v:.{nd}f}" if isinstance(v, float) else str(v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True); ap.add_argument("--runs", nargs="+", required=True); ap.add_argument("--out", default="reports/e1")
    ap.add_argument("--step", type=int, default=99, help="final step (falls back to each trajectory's last complete step)"); ap.add_argument("--thumb", type=int, default=128)
    a = ap.parse_args()
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    out = (ROOT / a.out) if not pathlib.Path(a.out).is_absolute() else pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    arch = ensure_archive(a.ref); arch_meta = json.loads(str(arch["meta"]))
    results = [analyse_run(r, a.step) for r in [a.ref] + a.runs]
    for r in results: r["overlap"] = overlap(r["dinov2"]["X"], arch)
    joint = joint_clustering(results, a.ref)
    drift_figure(results, "dinov2", out, plt); drift_figure(results, "minilm", out, plt); elbow_figure(results, joint, out, plt)
    endpoint_sheets(results, joint, out, a.thumb)

    rows = []
    for r in results:
        n_shared = sum(1 for c in joint["clusters"] if c["label"] == "shared" and c["share"][r["run"]] >= SHARE_MIN)
        n_unique = sum(1 for c in joint["clusters"] if c["label"].startswith("unique to") and c["share"][r["run"]] >= SHARE_MIN) if r["run"] != a.ref \
            else sum(1 for c in joint["clusters"] if c["label"] == "ref only")
        rows.append({"run": r["run"], "is_ref": r["run"] == a.ref, "n_traj": len(r["dinov2"]["ids"]), "final_steps": sorted(set(r["dinov2"]["final_steps"].values())),
                     "n_steps_in_drift": r["dinov2"]["L"] + 1 if r["dinov2"]["L"] else 0,
                     "elbow_k_dinov2": r["dinov2"]["elbow_k"], "elbow_k_minilm": r["minilm"]["elbow_k"], "vendi_dinov2": r["dinov2"]["vendi"], "vendi_minilm": r["minilm"]["vendi"],
                     "plateau_step_dinov2": r["dinov2"]["plateau_step"], "plateau_step_minilm": r["minilm"]["plateau_step"],
                     "step_drift_last20_dinov2": r["dinov2"]["step_drift_last20"], "step_drift_last20_minilm": r["minilm"]["step_drift_last20"],
                     "share_inside_ref_cluster_radii": r["overlap"]["share_inside_cluster_radii"], "share_inside_ref_pooled_radius": r["overlap"]["share_inside_pooled_radius"],
                     "share_per_ref_cluster": r["overlap"]["share_per_ref_cluster"], "nearest_ref_cluster": [int(x) for x in r["overlap"]["nearest"]],
                     "dist_to_nearest_ref_centroid": [round(float(x), 4) for x in r["overlap"]["dmin"]],
                     "n_shared_joint_clusters": n_shared, "n_unique_joint_clusters": n_unique,
                     "inertia_dinov2": dict(zip(map(str, r["dinov2"]["ks"]), [round(v, 4) for v in r["dinov2"]["inertia"]])),
                     "inertia_minilm": dict(zip(map(str, r["minilm"]["ks"]), [round(v, 4) for v in r["minilm"]["inertia"]])),
                     "mean_step_drift_dinov2": [round(float(v), 4) for v in r["dinov2"]["mean_step"]], "mean_cum_drift_dinov2": [round(float(v), 4) for v in r["dinov2"]["mean_cum"]],
                     "mean_step_drift_minilm": [round(float(v), 4) for v in r["minilm"]["mean_step"]], "mean_cum_drift_minilm": [round(float(v), 4) for v in r["minilm"]["mean_cum"]]})
    warnings = [f"{r['run']}: only {r['n_traj']} trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful" for r in rows if r["n_traj"] < 30]
    warnings += [f"{r['run']}: only {r['n_steps_in_drift']} steps in the drift series; plateau needs >= 30" for r in rows if r["n_steps_in_drift"] < 31]
    if joint["n_pooled"] < 30: warnings.append(f"joint clustering pools only {joint['n_pooled']} endpoints; its k and labels are not meaningful")
    summary = {"ref": a.ref, "runs": a.runs, "built_at": datetime.datetime.now().isoformat(timespec="seconds"), "final_step_requested": a.step,
               "rules": {"elbow": "knee of k-means inertia, k=2..min(25,n-1), n_init=10, random_state=0 (a0_report)", "plateau": "first step after which the 10-step rolling mean of the mean step-to-step drift stays within 10% (+0.01) of the final-20 level (a0_report)",
                         "vendi": "exp(entropy of eigenvalues of K/n), K = cosine-similarity kernel of L2-normalised final-step embeddings", "overlap": "endpoint inside the ref archive when its cosine distance to some ref centroid <= that cluster's 95th-percentile radius (DINOv2)",
                         "joint_label": f"shared if ref >= {SHARE_MIN:.0%} of a joint cluster's members and some run >= {SHARE_MIN:.0%}; ref only; else unique to the run(s) >= {SHARE_MIN:.0%}", "step0": "excluded"},
               "ref_archive": {"path": f"archive/{a.ref}_centroids.npz", "k": int(len(arch["radius"])), "radius_pooled_p95": float(arch["radius_pooled"]), "built_at": arch_meta.get("built_at"), "n_traj": arch_meta.get("n_traj")},
               "spaces": {s: MODELS[s] for s in ("dinov2", "minilm")}, "packages": package_versions(), "per_run": rows,
               "joint": {k: v for k, v in joint.items() if k not in ("labels", "group")}, "warnings": warnings}
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))

    md = [f"# E1 comparison: ref `{a.ref}` vs {', '.join(f'`{r}`' for r in a.runs)}", "", f"Built {summary['built_at']}. Final step {a.step} (or each trajectory's last complete step). Step 0 excluded. "
          f"Spaces: DINOv2 `{MODELS['dinov2']['id']}` @ {MODELS['dinov2']['revision'][:8]} (primary), MiniLM `{MODELS['minilm']['id']}` @ {MODELS['minilm']['revision'][:8]} (secondary). "
          f"Ref archive: {summary['ref_archive']['k']} clusters, pooled r95 = {summary['ref_archive']['radius_pooled_p95']:.3f}.", "",
          "| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['run']}{' (ref)' if r['is_ref'] else ''} | {r['n_traj']} | {fmt(r['elbow_k_dinov2'])} | {fmt(r['elbow_k_minilm'])} | {fmt(r['vendi_dinov2'])} | {fmt(r['plateau_step_dinov2'])} | "
                  f"{fmt(r['share_inside_ref_cluster_radii'])} | {r['n_shared_joint_clusters']} | {r['n_unique_joint_clusters']} |")
    md += ["", f"Joint k-means over {joint['n_pooled']} pooled final-step DINOv2 embeddings: k = {joint['k']} (elbow {joint['elbow_k']}).", "", "| joint cluster | size | label | " + " | ".join(r["run"] for r in results) + " |", "|---|---|---|" + "---|" * len(results)]
    for c in joint["clusters"]:
        md.append(f"| {c['cluster']} | {c['size']} | {c['label']} | " + " | ".join(f"{c['composition'][r['run']]} ({c['share'][r['run']]:.0%})" for r in results) + " |")
    md += ["", "Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, " + ", ".join(f"`endpoints_{r['run']}.jpg`" for r in results) + ".", ""]
    if warnings: md += ["Warnings:"] + [f"- {w}" for w in warnings] + [""]
    md += ["CLIP is used for steering only and does not appear in any number above."]
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
