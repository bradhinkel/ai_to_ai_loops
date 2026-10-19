"""Robustness of the A0-core elbow k (SPEC §4.3 criterion "k in about 10 to 16").

Runs the same knee rule (max distance to the chord of the normalised inertia curve, k = 2..kmax) and the silhouette
maximum on three endpoint sets: our MiniLM caption endpoints, our DINOv2 image endpoints, and Hintze's own T=0.9
endpoint captions (last row of each figshare CSV, run 096 excluded as unpaired) embedded with the same MiniLM.
Also shows how the knee moves with kmax, because the chord rule depends on it.

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/elbow_check.py a0_core
"""
import argparse, csv, json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, cpu_only, final_step_matrix, kmeans, ROOT, elbow_k  # noqa: E402
from a0_report import embed, style, BLUE, ORANGE, GRAY  # noqa: E402


def knee(ks, inertia):
    yn = (np.array(inertia) - inertia[-1]) / (inertia[0] - inertia[-1] + 1e-9)
    xn = (np.array(ks) - ks[0]) / (ks[-1] - ks[0]); d = np.abs(xn + yn - 1) / np.sqrt(2)
    return int(ks[int(np.argmax(d))])


def curves(X, kmax):
    from sklearn.metrics import silhouette_score
    ks = list(range(2, kmax + 1)); inertia, sil = [], []
    for k in ks:
        km = kmeans(X, k); inertia.append(float(km.inertia_)); sil.append(float(silhouette_score(X, km.labels_, metric="cosine")))
    return ks, inertia, sil


def hintze_endpoints(logs_dir):
    caps = []
    for p in sorted(pathlib.Path(logs_dir).glob("*.csv")):
        if "run_096" in p.name: continue
        rows = list(csv.DictReader(open(p, newline="")))
        if len(rows) >= 90: caps.append(rows[-1]["prompt"].strip())
    return caps


def main():
    cpu_only()
    ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--hintze", default="data/hintze_figshare/temps_0.9/logs")
    ap.add_argument("--kmax", type=int, default=40)
    a = ap.parse_args()
    cache = Cache(a.run); run_dir = ROOT / "runs" / a.run
    sets = {}
    _, Xm, _ = final_step_matrix(cache, "minilm", run_dir, step=99); sets[f"{a.run} MiniLM captions"] = Xm
    _, Xd, _ = final_step_matrix(cache, "dinov2", run_dir, step=99); sets[f"{a.run} DINOv2 images"] = Xd
    hz = hintze_endpoints(ROOT / a.hintze)
    if hz: sets["Hintze T=0.9 MiniLM captions"] = embed(hz).astype(np.float64)
    out = {"kmax_curve": a.kmax, "sets": {}}
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    colors = [BLUE, ORANGE, "#1b9e77"]
    for (name, X), col in zip(sets.items(), colors):
        ks, inertia, sil = curves(X, a.kmax)
        by_kmax = {km: knee(ks[:km - 1], inertia[:km - 1]) for km in (15, 20, 25, 30, 40) if km <= a.kmax}
        out["sets"][name] = {"n": int(len(X)), "knee_by_kmax": by_kmax, "silhouette_argmax": int(ks[int(np.argmax(sil))]),
                             "silhouette_top3": [int(ks[i]) for i in np.argsort(sil)[::-1][:3]], "inertia": dict(zip(ks, np.round(inertia, 3).tolist())),
                             "silhouette": dict(zip(ks, np.round(sil, 4).tolist()))}
        yn = (np.array(inertia) - inertia[-1]) / (inertia[0] - inertia[-1])
        axes[0].plot(ks, yn, color=col, lw=2, label=f"{name} (n={len(X)})"); axes[1].plot(ks, sil, color=col, lw=2, label=name)
    style(axes[0], "Normalised inertia, k = 2..%d" % a.kmax, "k", "inertia (0..1)"); style(axes[1], "Silhouette (cosine)", "k", "silhouette")
    axes[0].legend(frameon=False, fontsize=8); axes[0].axvspan(10, 16, color=GRAY, alpha=0.15, lw=0)
    rep = ROOT / "reports" / a.run; rep.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(); fig.savefig(rep / "elbow_check.png", dpi=130); (rep / "elbow_check.json").write_text(json.dumps(out, indent=1))
    for name, s in out["sets"].items():
        print(f"{name}: n={s['n']} knee by kmax {s['knee_by_kmax']} silhouette argmax {s['silhouette_argmax']} top3 {s['silhouette_top3']}")


if __name__ == "__main__":
    main()
