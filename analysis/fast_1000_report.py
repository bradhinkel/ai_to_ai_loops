"""A0-ESC T3 grading: the fast pair (SDXL-Turbo + Moondream 2) at 100 trajectories x 1,000 steps (runs/fast_1000).
Predictions: predictions.md "A0-ESC" P2, P2b, P3 (T3 clause), and Brad's eye/lips speculation of 2026-11-13. DINOv2 only; CLIP is not used.

    .venv/bin/python analysis/fast_1000_report.py

States (A0-ESC T3 definitions): k-means at the elbow on steps 800-999 (DINOv2, L2-normalised), fixed radius 0.20 cosine, exit
hysteresis 1.25 (gravity.label_steps), labels over all steps 0-999. Persistent = >= 3 visits of >= 5 steps (counted over 0-999;
the 800-999-only count is reported beside it). Depth = exit hazard (exits / steps inside), radius = capture (entries / steps outside),
both over 800-999 (0-999 reported too). An entrant is *held* if after its first entry it never visits another attractor and does
not end >= 10 steps outside (fast_report.py's rule); *lost to another attractor* = visits another attractor after first entry.
Eye/lips: FAST-100's own cluster 0 (rebuilt by fast_report.own_attractors, fixed k-means seed; entrants 2, 12, 19).
Writes reports/fast_1000_metrics.json, reports/figures/fast_1000_attractors.jpg, reports/figures/fast_1000_occupancy.png.
"""
import collections, json, pathlib, re, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, kmeans, elbow_k, ROOT  # noqa: E402
from gravity import label_steps, visits  # noqa: E402
import fast_report  # noqa: E402

RUN, R0, EXIT, LO, HI, MID = "fast_1000", 0.20, 1.25, 800, 1000, 600
STOP = set("a an the of and in on with is are this image shows its it to at from by for as be that which there their his her".split())


def load_all():
    B = Cache(RUN).arrays("dinov2"); assert B["mask"].all(), "missing embeddings"
    X = B["X"].astype(np.float64); return X / np.linalg.norm(X, axis=-1, keepdims=True)


def labels(C, X):
    D = 1 - np.einsum("kd,tsd->kts", C, X); return label_steps(D, np.full(len(C), R0), EXIT)


def gravity(L, c, lo, hi):
    W = L[:, lo:hi]; inside = (W == c); prev = inside[:, :-1]; nxt = inside[:, 1:]
    exits = int((prev & ~nxt).sum()); entries = int((~prev & nxt).sum())
    s_in = int(prev.sum()); s_out = int((~prev).sum())
    return dict(hazard=exits / s_in if s_in else None, capture=entries / s_out if s_out else None, exits=exits, entries=entries)


def caption(t, s):
    return json.loads((ROOT / "runs" / RUN / f"traj_{t:03d}" / f"step_{s:03d}.json").read_text()).get("caption") or ""


def top_words(L, c, n=60):
    cnt = collections.Counter(); pts = list(zip(*np.where(L[:, LO:HI] == c)))
    rng = np.random.default_rng(0); pick = [pts[i] for i in rng.choice(len(pts), min(n, len(pts)), replace=False)] if pts else []
    for t, s in pick:
        cnt.update(w for w in set(re.findall(r"[a-z]+", caption(int(t), int(s) + LO).lower())) if w not in STOP and len(w) > 2)
    return [w for w, _ in cnt.most_common(8)]


def main():
    X = load_all(); T, S, _ = X.shape
    E = X[:, LO:HI].reshape(-1, X.shape[-1]); k, ks, inertia = elbow_k(E); km = kmeans(E, k)
    C = np.stack([E[km.labels_ == c].mean(0) for c in range(k)]); C /= np.linalg.norm(C, axis=1, keepdims=True)
    L = labels(C, X)

    # FAST-100 eye/lips centroid
    X100 = fast_report.load("fast_100"); k100, C100, L100, rows100 = fast_report.own_attractors(X100)
    eye = C100[0]; eye_entr = [t for t in range(len(L100)) if (L100[t] == 0).any()]
    assert eye_entr == [2, 12, 19], eye_entr
    curly = C100[2]

    rows = []
    for c in range(k):
        v_all = [n for t in range(T) for n, _ in visits(L[t] == c)]; v_late = [n for t in range(T) for n, _ in visits(L[t, LO:HI] == c)]
        entrants = [t for t in range(T) if (L[t] == c).any()]; held, lost = [], []
        for t in entrants:
            first = int(np.argmax(L[t] == c)); after = L[t, first:]
            other = bool(((after >= 0) & (after != c)).any()); tail_out = int((after[::-1] == c).argmax()) if after[-1] != c else 0
            held.append(not other and tail_out < 10); lost.append(other)
        g_late, g_all = gravity(L, c, LO, HI), gravity(L, c, 0, S)
        rows.append(dict(k=c, words=top_words(L, c), visits_ge5=sum(n >= 5 for n in v_all), visits_ge5_800_999=sum(n >= 5 for n in v_late),
                         persistent=sum(n >= 5 for n in v_all) >= 3, persistent_800_999=sum(n >= 5 for n in v_late) >= 3,
                         entrants=len(entrants), n_held=int(sum(held)), held_all=bool(entrants) and all(held), n_lost_to_other=int(sum(lost)),
                         first_entry_median=float(np.median([int(np.argmax(L[t] == c)) for t in entrants])) if entrants else None,
                         endpoints=int((L[:, S - 1] == c).sum()), occ_800_999=float((L[:, LO:HI] == c).mean()),
                         occ_600_799=float((L[:, MID:LO] == c).mean()), hazard=g_late["hazard"], capture=g_late["capture"],
                         hazard_0_999=g_all["hazard"], capture_0_999=g_all["capture"],
                         dist_eye=float(1 - C[c] @ eye), dist_curly=float(1 - C[c] @ curly)))
    # depth / radius ranks among all k attractors (top half = rank < k/2); None hazard (never inside) ranks last
    hz = [r["hazard"] if r["hazard"] is not None else np.inf for r in rows]; cp = [r["capture"] or 0 for r in rows]
    for r, rh, rc in zip(rows, np.argsort(np.argsort(hz)), np.argsort(np.argsort(-np.array(cp)))):
        r["depth_rank"] = int(rh); r["radius_rank"] = int(rc); r["top_half"] = bool(rh < k / 2 or rc < k / 2)

    pers = [r for r in rows if r["persistent"]]; pers_ids = {r["k"] for r in pers}
    W = L[:, LO:HI]; in_pers = float(np.isin(W, list(pers_ids)).mean()); in_any = float((W >= 0).mean())
    srt = sorted(pers, key=lambda r: -r["occ_800_999"]); acc, core = 0.0, []
    for r in srt:
        core.append(r["k"]); acc += r["occ_800_999"]
        if acc > in_pers / 2: break
    P2 = dict(share_in_persistent=in_pers, share_in_any=in_any, a=in_pers > 0.90,
              core_set=core, b=all(rows[c]["top_half"] for c in core),
              max_occ_shift=max(abs(r["occ_800_999"] - r["occ_600_799"]) for r in rows),
              c=all(abs(r["occ_800_999"] - r["occ_600_799"]) < 0.05 for r in rows))
    P2["pass"] = P2["a"] and P2["b"] and P2["c"]
    occs = sorted((r["occ_800_999"] for r in rows), reverse=True)
    P2b = dict(max_occ=occs[0], n_ge_10pct=sum(o >= 0.10 for o in occs), pass_=occs[0] <= 0.50 and sum(o >= 0.10 for o in occs) >= 3)
    big = [r for r in pers if r["entrants"] >= 5]
    P3 = dict(attractors_ge5_entrants=[r["k"] for r in big], absorbing=[r["k"] for r in big if r["n_lost_to_other"] == 0],
              pass_=all(r["n_lost_to_other"] >= 1 for r in big))
    near_eye = min(rows, key=lambda r: r["dist_eye"]); largest = max(rows, key=lambda r: r["occ_800_999"])
    SPEC = dict(nearest_eye_k=near_eye["k"], dist=near_eye["dist_eye"], is_largest=near_eye["k"] == largest["k"],
                held_all=near_eye["held_all"], entrants=near_eye["entrants"], n_held=near_eye["n_held"], pass_=near_eye["k"] == largest["k"] and near_eye["held_all"])

    out = dict(definitions=dict(radius=R0, exit_factor=EXIT, fit_window=[LO, HI - 1], space="dinov2", elbow_k=k, ks=ks, inertia=inertia),
               P2=P2, P2b=P2b, P3_T3=P3, eye_lips_speculation=SPEC, attractors=rows,
               occupancy_by_100=[{"window": [s, s + 99], "free": float((L[:, s:s + 100] == -1).mean()),
                                  **{str(c): float((L[:, s:s + 100] == c).mean()) for c in range(k)}} for s in range(0, S, 100)])
    (ROOT / "reports" / "fast_1000_metrics.json").write_text(json.dumps(out, indent=1, default=float))
    np.savez(ROOT / "reports" / "fast_1000_labels.npz", L=L.astype(np.int16), C=C.astype(np.float32))
    sheet(L, rows, ROOT / "reports" / "figures" / "fast_1000_attractors.jpg")
    print(json.dumps({kk: v for kk, v in out.items() if kk not in ("attractors", "occupancy_by_100")}, indent=1, default=float))
    for r in sorted(rows, key=lambda r: -r["occ_800_999"]):
        print({kk: (round(v, 4) if isinstance(v, float) else v) for kk, v in r.items()})


def sheet(L, rows, path):
    rs = sorted(rows, key=lambda r: -r["occ_800_999"]); W = Image.new("RGB", (6 * 160 + 220, len(rs) * 160), "white"); d = ImageDraw.Draw(W)
    for i, r in enumerate(rs):
        d.text((4, i * 160 + 30), f"#{r['k']} occ {r['occ_800_999']:.2f}\nentr {r['entrants']} held {r['n_held']}\nend {r['endpoints']}"
                                  f"{' P' if r['persistent'] else ''}\n" + "\n".join(r["words"][:4]), fill="black")
        pts = [(t, s) for s in range(LO, HI) for t in range(L.shape[0]) if L[t, s] == r["k"]]; seen, pick = set(), []
        for t, s in pts:
            if t not in seen: seen.add(t); pick.append((t, s))
        for j, (t, s) in enumerate(pick[:6]):
            W.paste(Image.open(ROOT / "runs" / RUN / f"traj_{t:03d}" / f"step_{s:03d}.png").resize((160, 160)), (220 + j * 160, i * 160))
    W.save(path, quality=85)


NAMES = {1: "eye close-up", 6: "silhouette, pink/purple sky", 3: "pink rose close-up", 4: "rustic stone living room",
         7: "crystal-and-floral pink room", 0: "cobblestone street, balloons"}  # from the k = 8 fit's caption words and contact sheet


def plot_occupancy(L, path, w=50):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    cols = ["#0072B2", "#E69F00", "#CC79A7", "#009E73", "#D55E00", "#56B4E9"]; xs = np.arange(0, 1000, w) + w / 2
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=130)
    for (k, n), c in zip(NAMES.items(), cols):
        y = [(L[:, s:s + w] == k).mean() for s in range(0, 1000, w)]
        ax.plot(xs, y, color=c, lw=2, label=n); ax.text(1005, y[-1], n, color="#333", va="center", fontsize=8)
    yf = [(L[:, s:s + w] == -1).mean() for s in range(0, 1000, w)]
    ax.set_xlim(0, 1000); ax.set_ylim(0, 0.2); ax.set_xlabel("step (50-step windows)"); ax.set_ylabel("share of trajectory-steps")
    ax.axvspan(800, 1000, color="#eee", zorder=0); ax.text(900, 0.192, "fit window", ha="center", fontsize=8, color="#555")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#ddd", lw=0.6); ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.set_title(f"fast_1000: occupancy of the six persistent attractors (outside all: {yf[0]:.2f} at start → {yf[-1]:.2f} at end)", fontsize=9)
    plt.subplots_adjust(right=0.75); plt.savefig(path)


if __name__ == "__main__":
    if sys.argv[1:] == ["--plot-only"]:
        plot_occupancy(np.load(ROOT / "reports" / "fast_1000_labels.npz")["L"], ROOT / "reports" / "figures" / "fast_1000_occupancy.png")
    else:
        main(); plot_occupancy(np.load(ROOT / "reports" / "fast_1000_labels.npz")["L"], ROOT / "reports" / "figures" / "fast_1000_occupancy.png")
