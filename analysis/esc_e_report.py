"""ESC-E grading: escape from the fast pair's eye attractor (predictions.md "ESC", approved 2026-11-15): ESC-1 (eye half), ESC-2 (eye half),
ESC-3. ESC-4 needs ESC-C and is graded there. DINOv2 only; CLIP is not used.

    .venv/bin/python analysis/esc_e_report.py

Definitions (predictions.md "ESC", fixed before the run):
  centroid   T3's eye centroid, reports/fast_1000_labels.npz C[1] (the file runs/esc_e/seed_states.json names, sha256 checked).
  inside     DINOv2 cosine distance to the centroid, radius 0.20 and exit hysteresis 1.25 (gravity.label_steps). Every chain's step 0
             is a T3 state that was inside under T3's hysteresis labels, so a chain starts inside if its step-0 distance is <= 1.25 x 0.20
             (the count of step-0 distances above 0.20 is reported).
  exit       step s outside with step s-1 inside. escape = an exit whose outside run lasts >= 40 consecutive steps (s .. s+39 all outside).
  at risk    inside steps 0-360 (each has >= 40 steps of run after it). rate = escapes / steps at risk; 95 % interval exact Poisson (Garwood).
  ESC-3      eye words \\beyes?\\b|\\biris(es)?\\b|\\bpupils?\\b|eyelash|\\blashes\\b|eyebrow|eyelid|\\bsclera\\b. An escape is a *focus shift* if
             >= 3 of its outside steps (s until re-entry or the end) have captions naming the eye; it *starts from a dropped word* if the
             caption of step s-1 (the prompt of the first outside image) has no eye word. Graded only with >= 4 escapes.
Context, not graded: T3's in-run figure (3.2e-4) used "left >= 100 steps and never returned"; the same count is reported here.
Writes reports/esc_e_metrics.json, reports/figures/esc_e_escapes.jpg, reports/figures/esc_e_distance.png.
"""
import hashlib, json, pathlib, re, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.stats import chi2

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, ROOT  # noqa: E402

RUN, R0, EXIT, OUT_MIN, LAST_RISK, NSTEP = "esc_e", 0.20, 1.25, 40, 360, 401
EYE = re.compile(r"\beyes?\b|\biris(es)?\b|\bpupils?\b|eyelash|\blashes\b|eyebrow|eyelid|\bsclera\b", re.I)
RD = ROOT / "runs" / RUN


def caption(t, s):
    return json.loads((RD / f"traj_{t:03d}" / f"step_{s:03d}.json").read_text()).get("caption") or ""


def label(d):
    """inside mask for one chain's distance row; starts inside if d[0] <= EXIT*R0 (the T3 state was inside)."""
    ins = np.zeros(len(d), bool); cur = d[0] <= EXIT * R0
    for s, v in enumerate(d):
        cur = v <= EXIT * R0 if cur else v <= R0; ins[s] = cur
    return ins


def garwood(k, n):
    lo = chi2.ppf(0.025, 2 * k) / 2 / n if k else 0.0; return lo, chi2.ppf(0.975, 2 * k + 2) / 2 / n


def main():
    meta = json.loads((RD / "seed_states.json").read_text()); lab = ROOT / meta["labels"]
    assert hashlib.sha256(lab.read_bytes()).hexdigest() == meta["labels_sha256"], "labels file changed"
    c = np.load(lab)["C"][meta["attractor"]].astype(np.float64); c /= np.linalg.norm(c)
    B = Cache(RUN).arrays("dinov2"); assert B["mask"].all() and B["X"].shape[:2] == (100, NSTEP), "embeddings incomplete"
    X = B["X"].astype(np.float64); X /= np.linalg.norm(X, axis=-1, keepdims=True); D = 1 - X @ c   # [100, 401]
    src = {s["chain"]: s for s in meta["states"]}
    INS = np.stack([label(D[t]) for t in range(100)])
    at_risk = int(INS[:, : LAST_RISK + 1].sum()); escapes, exits, returns = [], 0, []
    for t in range(100):
        ins = INS[t]
        for s in range(1, NSTEP):
            if ins[s - 1] and not ins[s]:
                exits += 1; e = s
                while e < NSTEP and not ins[e]: e += 1
                length, censored = e - s, e == NSTEP
                if not censored: returns.append(length)
                if s - 1 <= LAST_RISK and length >= OUT_MIN:
                    caps = [caption(t, j) for j in range(s, e)]; eye_out = sum(bool(EYE.search(x)) for x in caps)
                    prev = caption(t, s - 1)
                    escapes.append(dict(chain=t, source_traj=src[t]["source_traj"], source_step=src[t]["source_step"], exit_step=s,
                                        out_steps=length, returned=not censored, eye_captions_outside=eye_out, focus_shift=eye_out >= 3,
                                        dropped_word_start=not EYE.search(prev), d_start=round(float(D[t, 0]), 4),
                                        d_end=round(float(D[t, -1]), 4), prev_caption=prev, first_out_caption=caps[0],
                                        caption_at_plus10=caps[min(10, len(caps) - 1)], last_caption=caption(t, e - 1)))
    k = len(escapes); rate = k / at_risk; lo, hi = garwood(k, at_risk)
    never = sum(1 for t in range(100) if INS[t].any() and np.where(INS[t])[0].max() <= NSTEP - 1 - 100)   # last inside step >= 100 before the end
    t3_band = (3.2e-4 / 3, 3.2e-4 * 3)
    ESC1 = dict(escapes=k, pass_=k >= 1)
    ESC2 = dict(rate=rate, ci95=[lo, hi], below_1e3=rate < 1e-3, in_claude_band_1e4_1e3=1e-4 <= rate <= 1e-3,
                within_3x_of_T3=t3_band[0] <= rate <= t3_band[1], pass_brad=rate < 1e-3,
                pass_claude=1e-4 <= rate <= 1e-3 and t3_band[0] <= rate <= t3_band[1])
    fs = sum(e["focus_shift"] for e in escapes); dw = sum(e["dropped_word_start"] for e in escapes)
    ESC3 = dict(graded=k >= 4, focus_shift=fs, dropped_word_start=dw, n=k,
                pass_=(k >= 4 and fs >= 0.75 * k and dw <= 0.25 * k) if k >= 4 else None)
    chains_left = int((~INS).any(1).sum()); end_inside = int(INS[:, -1].sum())
    out = dict(run=RUN, centroid=f"{meta['labels']} C[{meta['attractor']}]", radius=R0, exit_factor=EXIT, out_min=OUT_MIN,
               step0_above_r=int((D[:, 0] > R0).sum()), step0_above_exit=int((D[:, 0] > EXIT * R0).sum()),
               steps_at_risk=at_risk, exits=exits, returning_exits=len(returns), longest_return=max(returns) if returns else None,
               returns_ge_29=sum(r > 28 for r in returns), chains_ever_outside=chains_left, chains_inside_at_400=end_inside,
               inside_share_all=float(INS.mean()), t3_style_never_returned_100=never,
               ESC1_eye=ESC1, ESC2_eye=ESC2, ESC3=ESC3, escapes=escapes,
               escapes_by_entrant={str(s): sum(e["source_traj"] == s for e in escapes) for s in meta["entrants"]})
    (ROOT / "reports" / "esc_e_metrics.json").write_text(json.dumps(out, indent=1, default=float, ensure_ascii=False))
    strips(escapes, D, ROOT / "reports" / "figures" / "esc_e_escapes.jpg"); plot(D, INS, escapes, ROOT / "reports" / "figures" / "esc_e_distance.png")
    print(json.dumps({kk: v for kk, v in out.items() if kk != "escapes"}, indent=1, default=float))
    for e in escapes: print({kk: v for kk, v in e.items() if "caption" not in kk})


def strips(escapes, D, path, T=128):
    offs = [-5, -1, 0, 3, 10, 20, 39]; W = Image.new("RGB", (230 + len(offs) * T, max(1, len(escapes)) * (T + 14)), "white"); d = ImageDraw.Draw(W)
    for i, e in enumerate(escapes):
        y = i * (T + 14); d.text((4, y + 20), f"chain {e['chain']} (T3 traj {e['source_traj']})\nexit step {e['exit_step']}\n"
                                              f"out {e['out_steps']}{'' if e['returned'] else '+ (to end)'}\neye words outside {e['eye_captions_outside']}", fill="black")
        for j, o in enumerate(offs):
            s = min(max(e["exit_step"] + o, 0), NSTEP - 1)
            W.paste(Image.open(RD / f"traj_{e['chain']:03d}" / f"step_{s:03d}.png").convert("RGB").resize((T, T)), (230 + j * T, y))
            d.text((232 + j * T, y + T), f"{s} d={D[e['chain'], s]:.2f}", fill="black")
    W.save(path, quality=85)


def plot(D, INS, escapes, path):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 4)); esc = sorted({e["chain"] for e in escapes})
    for t in range(100):
        if t not in esc: ax.plot(D[t], color="#BBBBBB", lw=0.5, alpha=0.5)
    cols = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]
    for i, t in enumerate(esc): ax.plot(D[t], color=cols[i % len(cols)], lw=1.5, label=f"chain {t}")
    ax.axhline(R0, color="#444444", lw=1, ls="--"); ax.axhline(EXIT * R0, color="#444444", lw=1, ls=":")
    ax.set_xlabel("step"); ax.set_ylabel("DINOv2 distance to T3 eye centroid"); ax.set_xlim(0, NSTEP - 1)
    ax.set_title("ESC-E: 100 chains started inside the eye (grey); chains with an escape in colour")
    if esc: ax.legend(fontsize=7, ncol=2, frameon=False)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(path, dpi=130)


if __name__ == "__main__":
    main()
