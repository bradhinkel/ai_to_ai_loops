"""How long does the loop remember its seed? (Brad, 2026-10-20: the original images and prompts are lost after a few steps and
what remains is the models' own 'dream'; drift is only measurable in the first steps.)
For each run and step k: seed identification = share of trajectories whose step-k embedding is nearer (cosine) to their own
step-0 image than to any other trajectory's step-0 image (chance = 1/n). Also the mean cosine similarity to own step 0 minus the
mean similarity to other trajectories' step 0 (excess self-similarity; 0 = no information). DINOv2 (images) and MiniLM (captions,
own step-0 caption = the first caption of the seed image). Half-life = first step where identification <= 50%; loss = first step
where it stays <= 2x chance for the rest of the run.
    .venv/bin/python analysis/memory_curve.py a0_core e1_gen e1_both
Writes reports/memory_curve.md and reports/memory_curve.png. CLIP is not used.
"""
import argparse, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, Cache, cpu_only  # noqa: E402


def curve(X):                       # X [T, S, d] with step 0 at index 0; NaN rows allowed
    T, S, _ = X.shape; X = X / np.linalg.norm(X, axis=-1, keepdims=True)
    ref = X[:, 0]; ident, excess = [], []
    for k in range(S):
        sim = X[:, k] @ ref.T                      # [T, T]: sim[i, j] = step k of i vs step 0 of j
        ok = ~np.isnan(sim).any(1)
        own = np.diag(sim); other = (sim.sum(1) - own) / (T - 1)
        ident.append(float((sim[ok].argmax(1) == np.arange(T)[ok]).mean())); excess.append(float((own[ok] - other[ok]).mean()))
    return np.array(ident), np.array(excess)


def main():
    cpu_only(); ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); a = ap.parse_args()
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    res = {}; fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for run in a.runs:
        for space in ("dinov2", "minilm"):
            d = Cache(run).arrays(space); X = d["X"].astype(np.float64); X[~d["mask"]] = np.nan
            ident, excess = curve(X); T = X.shape[0]; chance = 1 / T
            half = next((k for k in range(len(ident)) if ident[k] <= 0.5), None)
            lost = next((k for k in range(len(ident)) if (ident[k:] <= 2 * chance).all()), None)
            res[(run, space)] = dict(ident=ident.tolist(), excess=excess.tolist(), half_life=half, lost_at=lost, n=T,
                                     ident_at={k: round(float(ident[k]), 2) for k in (1, 2, 3, 5, 10, 20, 50, 99) if k < len(ident)})
            axes[0 if space == "dinov2" else 1].plot(ident, label=run, linewidth=1.6)
    for ax, title in zip(axes, ("images (DINOv2): own seed image identified", "captions (MiniLM): own seed caption identified")):
        ax.set_title(title, fontsize=10); ax.set_xlabel("step k"); ax.set_ylabel("share of trajectories"); ax.set_ylim(0, 1.02); ax.axhline(0.5, color="gray", linewidth=0.8, linestyle="--")
        ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(ROOT / "reports" / "memory_curve.png", dpi=130)
    md = ["# Seed memory curve", "", "Seed identification at step k = share of trajectories whose step-k embedding is nearer to their own step-0 image/caption than to any "
          "other trajectory's (chance 1/n). Half-life = first step at or below 50%; lost = first step from which it never exceeds 2x chance. "
          "Excess self-similarity = mean cosine to own step 0 minus mean cosine to the others' step 0.", "",
          "| run | space | ident. step 1 | 2 | 3 | 5 | 10 | 20 | 50 | 99 | half-life (step) | lost (step) | excess self-sim step 5 / 20 / 99 |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (run, space), r in res.items():
        ia = r["ident_at"]; ex = r["excess"]
        md.append(f"| {run} | {space} | " + " | ".join((f"{ia[k]:.2f}" if k in ia else "–") for k in (1, 2, 3, 5, 10, 20, 50, 99)) +
                  f" | {r['half_life']} | {r['lost_at']} | {ex[5]:.3f} / {(ex[20] if len(ex) > 20 else float('nan')):.3f} / {ex[-1]:.3f} |")
    md += ["", "Figure: `memory_curve.png`."]
    (ROOT / "reports" / "memory_curve.md").write_text("\n".join(md) + "\n"); (ROOT / "reports" / "memory_curve.json").write_text(json.dumps({f"{k[0]}:{k[1]}": v for k, v in res.items()}, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
