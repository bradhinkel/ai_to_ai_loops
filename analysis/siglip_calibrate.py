"""Choose the SigLIP radii for the B-img archive (SPEC2 §5 B-img pilot design; D17) so they mean what the DINOv2 gravity radius
0.20 means on A0-core. Both caches must exist (analysis/embed.py a0_core --spaces dinov2,siglip).

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/siglip_calibrate.py [--run a0_core] [--dino 0.20] [--window 5]

Two matchings, both reported:
  pairs    the SigLIP distance whose quantile among consecutive-step pairs (steps >= 1) equals that of DINOv2 0.20;
  windows  the SigLIP radius at which the same share of 5-step windows (max distance to the normalised window mean) counts as
           persistent as under DINOv2 0.20 -- this is the archive condition itself, so it is the one used for radius_archive.
Also: Spearman rank correlation of the two distances over the same pairs, and the agreement of the persistence decisions.
Writes reports/siglip_calibration.md and .json.
"""
import argparse, json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache  # noqa: E402


def series(cache, space):
    d = cache.arrays(space)
    out = {}
    for i, t in enumerate(d["trajs"]):
        rows = [d["X"][i, j] for j, s in enumerate(d["steps"]) if d["mask"][i, j]]
        if len(rows) >= 2: out[int(t)] = np.stack(rows).astype(np.float64)
    return out


def window_max(X, w):
    """For each end step t >= w-1: max cosine distance of X[t-w+1..t] to their normalised mean."""
    out = []
    for t in range(w - 1, len(X)):
        W = X[t - w + 1:t + 1]; m = W.mean(0); m /= np.linalg.norm(m) + 1e-9
        out.append(float((1 - W @ m).max()))
    return np.array(out)


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--run", default="a0_core"); ap.add_argument("--dino", type=float, default=0.20)
    ap.add_argument("--window", type=int, default=5); ap.add_argument("--burn_in", type=int, default=5)
    a = ap.parse_args(argv)
    cache = Cache(a.run); D, S = series(cache, "dinov2"), series(cache, "siglip")
    trajs = sorted(set(D) & set(S))
    dp, sp, dw, sw = [], [], [], []
    for t in trajs:
        n = min(len(D[t]), len(S[t])); X, Y = D[t][:n], S[t][:n]
        dp.append(1 - (X[1:] * X[:-1]).sum(1)); sp.append(1 - (Y[1:] * Y[:-1]).sum(1))
        wx, wy = window_max(X, a.window), window_max(Y, a.window)
        k = max(0, a.burn_in - (a.window - 1)); dw.append(wx[k:]); sw.append(wy[k:])
    dp, sp, dw, sw = map(np.concatenate, (dp, sp, dw, sw))
    from scipy.stats import spearmanr
    q_pairs = float((dp <= a.dino).mean()); r_pairs = float(np.quantile(sp, q_pairs))
    q_win = float((dw <= a.dino).mean()); r_win = float(np.quantile(sw, q_win))
    rho = float(spearmanr(dp, sp).correlation); rho_w = float(spearmanr(dw, sw).correlation)
    agree = float(((dw <= a.dino) == (sw <= r_win)).mean())
    both = int(((dw <= a.dino) & (sw <= r_win)).sum()); dino_only = int(((dw <= a.dino) & (sw > r_win)).sum()); sig_only = int(((dw > a.dino) & (sw <= r_win)).sum())
    res = {"run": a.run, "dino_radius": a.dino, "window": a.window, "burn_in": a.burn_in, "n_pairs": int(len(dp)), "n_windows": int(len(dw)),
           "pairs": {"share_within_dino": q_pairs, "siglip_radius": r_pairs, "spearman": rho},
           "windows": {"share_persistent_dino": q_win, "siglip_radius": r_win, "spearman": rho_w, "decision_agreement": agree, "both": both, "dino_only": dino_only, "siglip_only": sig_only},
           "siglip_pair_quantiles": {str(q): float(np.quantile(sp, q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)},
           "dino_pair_quantiles": {str(q): float(np.quantile(dp, q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)}}
    md = [f"# SigLIP radius calibration on {a.run} (D17)", "",
          f"DINOv2 gravity radius {a.dino}; {len(trajs)} trajectories, {len(dp)} consecutive-step pairs, {len(dw)} {a.window}-step windows ending at step >= {a.burn_in}.", "",
          "| matching | share under DINOv2 0.20 | SigLIP radius with the same share | Spearman (DINOv2 vs SigLIP distance) |", "|---|---|---|---|",
          f"| consecutive pairs | {q_pairs:.3f} | {r_pairs:.4f} | {rho:.3f} |", f"| {a.window}-step windows (archive condition) | {q_win:.3f} | {r_win:.4f} | {rho_w:.3f} |", "",
          f"Persistence decisions (window max distance <= radius) agree in {agree:.1%} of windows: both {both}, DINOv2 only {dino_only}, SigLIP only {sig_only}.", "",
          "SigLIP consecutive-pair distance quantiles: " + ", ".join(f"q{int(float(q)*100)} {v:.3f}" for q, v in res["siglip_pair_quantiles"].items()),
          "DINOv2 consecutive-pair distance quantiles: " + ", ".join(f"q{int(float(q)*100)} {v:.3f}" for q, v in res["dino_pair_quantiles"].items()), "",
          f"Decision: radius_archive = radius_reject = {r_win:.3f} (window matching), rounded in the config and recorded in DEVIATIONS D17."]
    (ROOT / "reports" / "siglip_calibration.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (ROOT / "reports" / "siglip_calibration.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
