"""Build the A0 attractor archive from one run's final-step images (SPEC2 §3 "Output").

    .venv/bin/python analysis/build_archive.py <run> [--k K] [--step 99] [--thumb 128]

Needs analysis/embed.py <run> to have been run for dinov2, minilm and clip. Clusters the final-step DINOv2 embeddings with
k-means (n_init=10, random_state=0); k = --k, else the a0_report elbow rule on DINOv2 inertia (elbow when >= 30 trajectories,
otherwise min(12, n // 2)). Writes
  archive/<run>_centroids.npz   centroid_dinov2 / centroid_clip_image / centroid_clip_text / centroid_minilm [k, dim]
                                (mean of the members' L2-normalised embeddings, re-normalised), size [k], radius [k]
                                (95th-percentile cosine distance of members to the DINOv2 centroid), radius_pooled (scalar,
                                95th percentile over all members' distances to their own centroid), members (object array
                                of trajectory-id lists), labels [n], trajs [n], final_steps [n], plus a json string `meta`
  archive/<run>_labels.json     cluster -> members, size, radius, 3 captions nearest the centroid (label hint) + model pins
  reports/<run>/archive_clusters.jpg  one row per cluster, members sorted by distance to the centroid
CLIP centroids are kept for steering only (B1/B2, B-img); nothing is evaluated with them.
"""
import argparse, datetime, json, pathlib
import numpy as np
from PIL import Image, ImageDraw
from common import ROOT, Cache, MODELS, package_versions, final_step_matrix, read_record, image_path, elbow_k, k_for_sheet, kmeans, cos_dist, thumb


def build(run, k_fixed=0, step=99):
    run_dir = ROOT / "runs" / run; cache = Cache(run)
    ids, Xd, used = final_step_matrix(cache, "dinov2", run_dir, step)
    _, Xm, used_m = final_step_matrix(cache, "minilm", run_dir, step)
    _, Xci, _ = final_step_matrix(cache, "clip", run_dir, step, key="X_image")
    _, Xct, _ = final_step_matrix(cache, "clip", run_dir, step, key="X_text")
    assert used == used_m and len(Xd) == len(Xm) == len(Xci) == len(Xct), "embedding caches disagree; re-run embed.py for all spaces"
    n = len(ids)
    if n < 2: raise SystemExit(f"{run}: need >= 2 trajectories with a final step, have {n}")
    elbow, ks, inertia = elbow_k(Xd) if n >= 3 else (None, [], [])
    k = min(k_for_sheet(elbow, n, k_fixed), n)
    km = kmeans(Xd, k); labels = km.labels_

    def centroid(X, members):
        c = X[members].mean(axis=0); return c / (np.linalg.norm(c) + 1e-12)

    out = {s: [] for s in ("centroid_dinov2", "centroid_clip_image", "centroid_clip_text", "centroid_minilm")}
    size, radius, members, order_in_cluster, dists_all, label_json = [], [], [], {}, [], {}
    for c in range(k):
        m = np.where(labels == c)[0]
        cd = centroid(Xd, m); d = cos_dist(Xd[m], cd); dists_all.extend(d.tolist())
        out["centroid_dinov2"].append(cd); out["centroid_clip_image"].append(centroid(Xci, m))
        out["centroid_clip_text"].append(centroid(Xct, m)); out["centroid_minilm"].append(centroid(Xm, m))
        size.append(len(m)); radius.append(float(np.percentile(d, 95)) if len(m) > 1 else 0.0)
        o = m[np.argsort(d)]; order_in_cluster[c] = o; members.append([ids[i] for i in o])
        label_json[str(c)] = {"size": int(len(m)), "radius_p95_dinov2": radius[-1], "mean_dist_dinov2": float(d.mean()),
                              "members": [ids[i] for i in o], "member_dist": [round(float(x), 4) for x in np.sort(d)],
                              "nearest_captions": [{"traj": ids[i], "step": used[ids[i]], "dist": round(float(cos_dist(Xd[i], cd)), 4),
                                                    "caption": read_record(run_dir, ids[i], used[ids[i]])["caption"]} for i in o[:3]]}
    radius_pooled = float(np.percentile(dists_all, 95))
    meta = {"run": run, "built_at": datetime.datetime.now().isoformat(timespec="seconds"), "n_traj": n, "k": k, "k_source": "fixed" if k_fixed else ("elbow" if (elbow and n >= 30) else "fallback min(12, n//2)"),
            "elbow_k_dinov2": elbow, "inertia_dinov2": dict(zip(map(str, ks), [round(v, 4) for v in inertia])), "final_step_requested": step,
            "final_steps_used": {str(t): used[t] for t in ids}, "radius_pooled_p95_dinov2": radius_pooled,
            "kmeans": {"n_init": 10, "random_state": 0, "space": "dinov2"}, "models": MODELS, "packages": package_versions(),
            "note": "CLIP centroids are for steering only (SPEC2 §2: never grade with what steers)."}
    arch = ROOT / "archive"; arch.mkdir(exist_ok=True)
    np.savez(arch / f"{run}_centroids.npz", **{s: np.stack(v).astype(np.float32) for s, v in out.items()},
             size=np.array(size, np.int32), radius=np.array(radius, np.float32), radius_pooled=np.float32(radius_pooled),
             members=np.array(members, dtype=object), labels=labels.astype(np.int32), trajs=np.array(ids, np.int32),
             final_steps=np.array([used[t] for t in ids], np.int32), meta=json.dumps(meta))
    (arch / f"{run}_labels.json").write_text(json.dumps({"meta": meta, "clusters": label_json}, indent=1, ensure_ascii=False))
    return ids, used, labels, order_in_cluster, size, radius, radius_pooled, meta


def contact_sheet(run, ids, used, labels, order_in_cluster, size, radius, T, out_path):
    run_dir = ROOT / "runs" / run; k = len(size); cols = max(size); pad = 16
    sheet = Image.new("RGB", (cols * T, k * (T + pad)), "white"); d = ImageDraw.Draw(sheet)
    for c in range(k):
        y = c * (T + pad)
        d.text((4, y + 2), f"cluster {c}   size {size[c]}   r95 {radius[c]:.3f}   (members sorted by distance to centroid)", fill="black")
        for n, i in enumerate(order_in_cluster[c]):
            t = ids[i]; sheet.paste(thumb(image_path(run_dir, t, used[t]), T), (n * T, y + pad))
            d.rectangle((n * T, y + pad, n * T + 52, y + pad + 12), fill="black"); d.text((n * T + 2, y + pad), f"t{t:03d}", fill="white")
    out_path.parent.mkdir(parents=True, exist_ok=True); sheet.save(out_path, quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--k", type=int, default=0); ap.add_argument("--step", type=int, default=99); ap.add_argument("--thumb", type=int, default=128)
    a = ap.parse_args()
    ids, used, labels, order, size, radius, rp, meta = build(a.run, a.k, a.step)
    contact_sheet(a.run, ids, used, labels, order, size, radius, a.thumb, ROOT / "reports" / a.run / "archive_clusters.jpg")
    print(json.dumps({"run": a.run, "n_traj": len(ids), "k": meta["k"], "k_source": meta["k_source"], "elbow_k_dinov2": meta["elbow_k_dinov2"],
                      "sizes": size, "radius_p95": [round(r, 4) for r in radius], "radius_pooled_p95": round(rp, 4),
                      "final_steps": sorted(set(used.values()))}, indent=1))
    print(f"wrote archive/{a.run}_centroids.npz, archive/{a.run}_labels.json, reports/{a.run}/archive_clusters.jpg")


if __name__ == "__main__":
    main()
