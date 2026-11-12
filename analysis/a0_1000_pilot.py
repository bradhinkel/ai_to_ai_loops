"""A0-1000 pilot gate (predictions.md "A0-1000", P1-P5): trajectories 0-19 of runs/a0_1000, steps 0-999, DINOv2.
Run gravity.py first for the windows (100-step windows, 100:500, 500:1000, 100:1000; --trajs 0:20 --labels archive/a0_core_names.json);
this script reads their JSON, adds what gravity.py does not report (per-visit cathedral detail, step-999 k-means vs the A0-core
centroids, seed identification, drift, a state timeline, the step-999 contact sheet) and writes reports/a0_1000_pilot_metrics.json
plus figures in reports/figures/a0_1000_pilot_*.png.
    .venv/bin/python analysis/a0_1000_pilot.py
State labels use the same fixed radius 0.20 / exit 1.25x hysteresis as gravity.py, computed once over steps 0-999
(gravity.py --window relabels inside each window, so per-window counts can differ by a visit at a window edge).
"""
import json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache, cpu_only, kmeans, elbow_k, vendi, image_path  # noqa: E402
from gravity import label_steps, visits  # noqa: E402
from memory_curve import curve  # noqa: E402

RUN, TRAJS, RADIUS, EXIT = "a0_1000", range(20), 0.20, 1.25
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]   # dataviz default categorical, fixed order
FREE = "#d9d8d2"
REP, FIG = ROOT / "reports", ROOT / "reports" / "figures"


def gravity_json(sfx):
    p = REP / f"gravity_{RUN}{sfx}.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    cpu_only()
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    FIG.mkdir(parents=True, exist_ok=True)
    B = Cache(RUN).arrays("dinov2"); trajs = list(B["trajs"]); steps = list(B["steps"])
    ti = [trajs.index(t) for t in TRAJS]; X = B["X"][ti].astype(np.float64); mask = B["mask"][ti]
    assert mask[:, :1000].all(), "pilot trajectories not fully embedded"
    X = X[:, :1000]; X /= np.linalg.norm(X, axis=-1, keepdims=True)
    z = np.load(ROOT / "archive/a0_core_centroids.npz", allow_pickle=True); C = z["centroid_dinov2"].astype(np.float64); C /= np.linalg.norm(C, axis=1, keepdims=True)
    names = json.loads((ROOT / "archive/a0_core_names.json").read_text()); K = len(C)
    D = 1 - np.einsum("pd,tsd->pts", C, X); L = label_steps(D, np.full(K, RADIUS), EXIT); T, S = L.shape
    out = {"n_traj": T, "n_steps": S, "radius": RADIUS, "exit_factor": EXIT}

    # occupancy per step (share of trajectories in each state)
    occ = np.stack([(L == k).mean(0) for k in range(K)] + [(L == -1).mean(0)])
    out["free_share_by_window"] = {f"{lo}-{lo + 99}": float((L[:, lo:lo + 100] == -1).mean()) for lo in range(0, 1000, 100)}

    # P3: cathedral (k=0) visits after step 100
    cat = []
    for t in range(T):
        s = 0
        while s < S:
            if L[t, s] == 0:
                e = s
                while e < S and L[t, e] == 0: e += 1
                cat.append(dict(traj=t, start=s, length=e - s, censored=e == S)); s = e
            else: s += 1
    out["cathedral_visits"] = cat
    absorbed = [t for t in range(T) if (L[t, 100:] == 0).any() and (L[t, int(np.argmax(L[t, 100:] == 0)) + 100:] == 0).all()]
    done = [v["length"] for v in cat if not v["censored"] and v["start"] >= 100]
    out["cathedral_late"] = dict(entries_from_100=sum(1 for v in cat if v["start"] >= 100), completed_from_100=len(done),
                                 mean_completed=float(np.mean(done)) if done else None, longest_completed=max(done) if done else 0,
                                 censored_at_999=[v for v in cat if v["censored"]], absorbed_trajs=absorbed,
                                 trajs_ever_in_cathedral=sorted({v["traj"] for v in cat}))

    # P2: k-means at the knee on the 20 step-999 endpoints vs A0-core step-99 centroids
    E = X[:, 999]; kk = elbow_k(E, kmax=min(10, T - 1))[0] or 4; km = kmeans(E, kk); p2 = []
    for c in range(kk):
        m = km.labels_ == c; cen = E[m].mean(0); cen /= np.linalg.norm(cen); d = 1 - C @ cen
        p2.append(dict(cluster=c, size=int(m.sum()), members=[int(t) for t in np.where(m)[0]], nearest=names[int(d.argmin())], nearest_k=int(d.argmin()), dist=float(d.min()),
                       states_at_999=[int(L[t, 999]) for t in np.where(m)[0]]))
    out["p2_kmeans_999"] = dict(k=kk, clusters=p2)
    out["endpoint_states_99"] = [int(v) for v in L[:, 99]]; out["endpoint_states_999"] = [int(v) for v in L[:, 999]]
    out["endpoint_nearest_999"] = [dict(traj=t, nearest=names[int(D[:, t, 999].argmin())], dist=float(D[:, t, 999].min())) for t in range(T)]

    # P5: seed identification (DINOv2; step 0 = the seed image)
    ident, excess = curve(X)
    out["seed_ident"] = {str(s): float(ident[s]) for s in (0, 1, 5, 10, 20, 50, 99, 199, 499, 999)}
    out["seed_ident_mean_100_999"] = float(ident[100:].mean()); out["seed_excess_mean_100_999"] = float(excess[100:].mean())

    # drift: step-to-step DINOv2 cosine distance; distance from own step 99; endpoint Vendi at every 100th step
    step_d = 1 - np.einsum("tsd,tsd->ts", X[:, 1:], X[:, :-1])
    out["step_change_by_window"] = {f"{lo}-{lo + 99}": float(step_d[:, max(lo, 1) - 1:lo + 99].mean()) for lo in range(0, 1000, 100)}
    out["vendi_by_step"] = {str(s): float(vendi(X[:, s])) for s in range(99, 1000, 100)}
    d99 = 1 - np.einsum("tsd,td->ts", X, X[:, 99])

    # windows from gravity.py
    win = {}
    for lo in range(0, 1000, 100):
        g = gravity_json(f"_w{lo}_{lo + 99}_t0_20")
        if g: win[f"{lo}-{lo + 99}"] = g
    for lo, hi in ((100, 499), (500, 999), (100, 999)):
        g = gravity_json(f"_w{lo}_{hi}_t0_20")
        if g: win[f"{lo}-{hi}"] = g
    out["windows"] = {w: dict(free_steps=float(out["free_share_by_window"].get(w, np.nan)) if w in out["free_share_by_window"] else None,
                              attractors={r["name"]: {k: r[k] for k in ("steps_inside", "entries", "exits", "hazard", "mean_residence", "capture", "max_completed_dwell", "endpoints")} for r in g["attractors"]},
                              by_step=g["hazard_by_step"]) for w, g in win.items()}
    (REP / "a0_1000_pilot_metrics.json").write_text(json.dumps(out, indent=1))

    # ---- figures
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#888", "axes.grid": True, "grid.color": "#e6e6e6"})
    # 1 timeline
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap([FREE] + SLOTS[:K]); fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.imshow(L + 1, aspect="auto", cmap=cmap, vmin=0, vmax=K, interpolation="nearest"); ax.grid(False)
    ax.axvline(99.5, color="#222", lw=1, ls="--"); ax.text(104, T - 0.3, "A0-core ends | continuation", fontsize=7, va="bottom", color="#222")
    ax.set_yticks(range(T)); ax.set_yticklabels([f"{t}" for t in range(T)], fontsize=7); ax.set_xlabel("step"); ax.set_ylabel("trajectory")
    used = [k for k in range(K) if (L == k).any()]
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=SLOTS[k], label=names[k]) for k in used] + [Patch(color=FREE, label="free (no attractor)")], ncol=4, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    ax.set_title("A0-1000 pilot: attractor state of every step (DINOv2, A0-core centroids, r 0.20)", loc="left"); fig.tight_layout(); fig.savefig(FIG / "a0_1000_pilot_timeline.png", dpi=150); plt.close(fig)
    # 2 occupancy (100-step means) as small lines, one axis
    fig, ax = plt.subplots(figsize=(8, 3.6)); xs = np.arange(50, 1000, 100)
    for k in used:
        ax.plot(xs, [occ[k, lo:lo + 100].mean() for lo in range(0, 1000, 100)], color=SLOTS[k], lw=2, marker="o", ms=4, label=names[k])
    ax.plot(xs, [occ[K, lo:lo + 100].mean() for lo in range(0, 1000, 100)], color="#777", lw=2, marker="o", ms=4, ls="--", label="free")
    ax.axvline(100, color="#222", lw=1, ls=":"); ax.set_xlabel("step (100-step window centre)"); ax.set_ylabel("share of trajectory-steps"); ax.set_ylim(0, 1)
    ax.legend(fontsize=7, frameon=False, ncol=2); ax.set_title("Occupancy by window (20 trajectories)", loc="left"); fig.tight_layout(); fig.savefig(FIG / "a0_1000_pilot_occupancy.png", dpi=150); plt.close(fig)
    # 3 drift: step-to-step change and seed identification
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    sm = np.convolve(step_d.mean(0), np.ones(10) / 10, mode="valid"); axs[0].plot(np.arange(len(sm)) + 6, sm, color=SLOTS[0], lw=2)
    axs[0].axvline(100, color="#222", lw=1, ls=":"); axs[0].set_xlabel("step"); axs[0].set_ylabel("cosine distance to previous step"); axs[0].set_title("Step-to-step change (mean of 20, 10-step smoothing)", loc="left")
    axs[1].plot(np.arange(S), ident, color=SLOTS[1], lw=2); axs[1].axhline(1 / T, color="#777", lw=1, ls="--"); axs[1].text(700, 1 / T + 0.02, "chance 1/20", fontsize=8, color="#555")
    axs[1].set_xscale("symlog", linthresh=10); axs[1].set_xlim(0, 1000);axs[1].set_xlabel("step (log after 10)"); axs[1].set_ylabel("seed identification"); axs[1].set_title("Nearest-seed identification (DINOv2)", loc="left")
    fig.tight_layout(); fig.savefig(FIG / "a0_1000_pilot_drift.png", dpi=150); plt.close(fig)
    # 4 contact sheets step 99 vs step 999 (5 x 4)
    from PIL import Image, ImageDraw
    for s in (99, 999):
        cell, gap, top = 256, 8, 4; W = 5 * cell + 4 * gap; H = 4 * (cell + 22) + 3 * gap
        page = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(page)
        for t in range(T):
            r, c = divmod(t, 5); x, y = c * (cell + gap), r * (cell + 22 + gap)
            page.paste(Image.open(image_path(ROOT / "runs" / RUN, t, s)).convert("RGB").resize((cell, cell)), (x, y))
            st = int(L[t, s]); lab = names[st] if st >= 0 else "free"
            dr.rectangle([x, y + cell + 4, x + 12, y + cell + 16], fill=SLOTS[st] if st >= 0 else FREE); dr.text((x + 16, y + cell + top), f"{t}: {lab[:34]}", fill="#222")
        page.save(FIG / f"a0_1000_pilot_sheet_{s}.jpg", quality=88)
    print(json.dumps({k: v for k, v in out.items() if k not in ("cathedral_visits", "windows", "endpoint_nearest_999")}, indent=1))


if __name__ == "__main__":
    main()
