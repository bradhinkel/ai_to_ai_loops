"""Transient visits (Brad, 2026-10-19): do the attractors found in one run appear as *intermediate* states of another run,
i.e. were they visited but not stable, or less prevalent, there?

Probes are endpoint clusters of run A in DINOv2 space (k-means on step-99 embeddings, k = knee unless --k; or the A0
archive centroids with --archive). Every cached step of run B is scanned: for each probe, a trajectory "visited" if any
step 1..99 lies within the probe radius of the centroid, "stayed" if its final step does, "transient" if visited but did
not stay. Radius = the probe's own 95th-percentile member distance with a floor (--floor, default 0.20 cosine distance;
A0-core clusters range 0.11-0.79). The nearest intermediate images are also shown, so the reader is not hostage to the
threshold. CLIP is not used.

    .venv/bin/python analysis/transient_visits.py --probes e1_cap_pilot --scan a0_core
    .venv/bin/python analysis/transient_visits.py --probes a0_core --archive archive/a0_core_centroids.npz --scan e1_cap_pilot
Writes reports/visits_<probes>_in_<scan>/{visits.md,visits.json,probe_<k>.jpg}.
"""
import argparse, json, pathlib, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, cpu_only, kmeans, elbow_k, ROOT  # noqa: E402


def caption_of(run, traj, step):
    p = ROOT / "runs" / run / f"traj_{traj:03d}" / f"step_{step:03d}.json"
    if not p.exists(): return ""
    r = json.loads(p.read_text())
    return (r.get("caption") or r.get("prompt_raw") or r.get("prompt") or "")[:160]


def thumb(run, traj, step, size, label, stayed=False):
    p = ROOT / "runs" / run / f"traj_{traj:03d}" / f"step_{step:03d}.png"
    im = Image.open(p).convert("RGB").resize((size, size), Image.LANCZOS) if p.exists() else Image.new("RGB", (size, size), "gray")
    d = ImageDraw.Draw(im); d.rectangle([0, 0, size, 14], fill=(0, 0, 0)); d.text((2, 1), label, fill=(255, 255, 255))
    if stayed: d.rectangle([0, 0, size - 1, size - 1], outline=(235, 104, 52), width=3)
    return im


def main():
    cpu_only()
    ap = argparse.ArgumentParser()
    ap.add_argument("--probes", required=True); ap.add_argument("--scan", required=True)
    ap.add_argument("--archive", default=None, help="use these archive centroids/radii as probes instead of clustering --probes")
    ap.add_argument("--k", type=int, default=0); ap.add_argument("--floor", type=float, default=0.20); ap.add_argument("--thumb", type=int, default=128)
    a = ap.parse_args()
    A = Cache(a.probes).arrays("dinov2"); B = Cache(a.scan).arrays("dinov2")
    XA = A["X"].astype(np.float64); XB = B["X"].astype(np.float64)
    stepsA, stepsB = list(A["steps"]), list(B["steps"]); iA99 = stepsA.index(99); iB99 = stepsB.index(99)
    okA = A["mask"][:, iA99]; EA = XA[okA, iA99]; trajA = A["trajs"][okA]
    # probes
    if a.archive:
        z = np.load(a.archive, allow_pickle=True); C = z["centroid_dinov2"].astype(np.float64); R = z["radius"].astype(np.float64)
        members = [list(map(int, m)) for m in z["members"]]; source = a.archive
    else:
        k = a.k or elbow_k(EA)[0] or min(10, len(EA) // 2); km = kmeans(EA, k)
        members = [[int(trajA[i]) for i in np.where(km.labels_ == c)[0]] for c in range(k)]
        C = np.stack([EA[km.labels_ == c].mean(0) for c in range(k)]); source = f"k-means k={k} on {a.probes} step-99 DINOv2"
        R = np.array([np.percentile(1 - EA[km.labels_ == c] @ (C[c] / np.linalg.norm(C[c])), 95) if (km.labels_ == c).sum() > 1 else 0 for c in range(k)])
    C = C / np.linalg.norm(C, axis=1, keepdims=True); Ruse = np.maximum(R, a.floor)
    # scan: distances [probe, traj, step]
    D = 1 - np.einsum("pd,tsd->pts", C, XB); D[:, ~B["mask"]] = np.inf
    stepidx = {s: i for i, s in enumerate(stepsB)}; mid = [stepidx[s] for s in stepsB if 1 <= s <= 99]
    out = {"probes_run": a.probes, "scan_run": a.scan, "probe_source": source, "floor": a.floor, "probes": []}
    rep = ROOT / "reports" / f"visits_{a.probes}_in_{a.scan}"; rep.mkdir(parents=True, exist_ok=True)
    lines = [f"# Transient visits: {a.probes} attractors inside {a.scan}'s trajectories", "",
             f"Probes: {source}. Scan: every cached step 1..99 of {a.scan} ({int(B['mask'].sum())} steps, {len(B['trajs'])} trajectories), DINOv2 cosine distance. "
             f"Radius = probe p95 member distance, floor {a.floor}. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.", "",
             "| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |", "|---|---|---|---|---|---|---|---|---|"]
    for p in range(len(C)):
        d = D[p][:, mid]; inside = d <= Ruse[p]
        visited = inside.any(1); stayed = D[p][:, iB99] <= Ruse[p]; transient = visited & ~stayed
        first = [int(np.argmax(inside[t])) + 1 for t in np.where(visited)[0]]
        dwell = []
        for t in np.where(transient)[0]:
            best = cur = 0
            for v in inside[t]:
                cur = cur + 1 if v else 0; best = max(best, cur)
            dwell.append(best)
        nearest_per_traj = d.min(1); order = np.argsort(nearest_per_traj)
        examples = []
        for t in order[:12]:
            s = int(np.argmin(d[t])) + 1; examples.append({"traj": int(B["trajs"][t]), "step": s, "dist": round(float(d[t, s - 1]), 3), "stayed": bool(stayed[t]),
                                                           "caption": caption_of(a.scan, int(B["trajs"][t]), s)})
        rec = {"probe": p, "members": members[p], "radius_used": round(float(Ruse[p]), 3), "radius_p95": round(float(R[p]), 3), "n_visited": int(visited.sum()),
               "n_stayed": int(stayed.sum()), "n_transient": int(transient.sum()), "median_first_visit": float(np.median(first)) if first else None,
               "max_transient_dwell": int(max(dwell)) if dwell else 0, "nearest": round(float(nearest_per_traj.min()), 3), "examples": examples}
        out["probes"].append(rec)
        lines.append(f"| {p} | {len(members[p])}: {members[p][:8]}{'…' if len(members[p]) > 8 else ''} | {rec['radius_used']} | {rec['n_visited']} | {rec['n_stayed']} | {rec['n_transient']} | "
                     f"{rec['median_first_visit']} | {rec['max_transient_dwell']} | {rec['nearest']} |")
        # sheet: row 0 probe members' endpoints, rows 1-2 nearest scan images (best step per trajectory)
        S = a.thumb; cols = 6; rows = 1 + 2; sheet = Image.new("RGB", (cols * S, rows * S), "white")
        for j, m in enumerate(members[p][:cols]): sheet.paste(thumb(a.probes, m, 99, S, f"{a.probes[:6]} t{m:03d} s99"), (j * S, 0))
        for j, e in enumerate(examples[:cols * 2]): sheet.paste(thumb(a.scan, e["traj"], e["step"], S, f"t{e['traj']:03d} s{e['step']:02d} d{e['dist']:.2f}", e["stayed"]), ((j % cols) * S, (1 + j // cols) * S))
        sheet.save(rep / f"probe_{p}.jpg", quality=88)
    lines += ["", "Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step)."]
    (rep / "visits.md").write_text("\n".join(lines) + "\n"); (rep / "visits.json").write_text(json.dumps(out, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
