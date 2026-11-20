"""ESC-C grading: escape from the SDXL + llava:latest cathedral (predictions.md "ESC", approved 2026-11-15): ESC-1 and ESC-2 (cathedral
halves) and ESC-4 (cathedral rate below the eye's, from reports/esc_e_metrics.json). DINOv2 only; CLIP is not used.

    .venv/bin/python analysis/esc_c_report.py

Definitions (predictions.md "ESC", the same as analysis/esc_e_report.py):
  centroid   the A0-core cathedral, archive/a0_core_centroids.npz centroid_dinov2[0] (as in analysis/esc_c_states.py).
  inside     cosine distance <= 0.20, exit hysteresis 1.25; a chain starts inside if its step-0 distance is <= 0.25 (every start state was
             inside its source run under the same hysteresis labels).
  escape     an exit followed by >= 40 consecutive outside steps; at risk = inside steps 0-260 (>= 40 steps of run after each).
  ESC-1      >= 1 escape; with none, the 95 % upper bound 3.69 / steps at risk is reported (exact Poisson; the prediction text says 3 /).
  ESC-2      rate < 1e-3 per step.
  ESC-4      cathedral rate < eye rate (ESC-E); 95 % intervals exact Poisson (Garwood); if they overlap the verdict is "not resolved".
Not graded: church words in the captions after each exit (the A0-ESC church vocabulary), the return-length distribution, and the escape
count as a function of the out-window (40 ... 200 steps) for both ESC-C and ESC-E, since ESC-E showed returns after up to 88 steps.
Writes reports/esc_c_metrics.json, reports/figures/esc_c_escapes.jpg, reports/figures/esc_c_distance.png, reports/figures/esc_window.png.
"""
import json, pathlib, re, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, ROOT  # noqa: E402
from esc_e_report import label, garwood, R0, EXIT, OUT_MIN  # noqa: E402

RUN, NSTEP, LAST_RISK, CAT = "esc_c", 301, 260, 0
CHURCH = re.compile(r"cathedral|church|\bnave\b|stained|chapel|basilica|altar|\bpews?\b|gothic|abbey|cloister|monaster|notre|spire", re.I)
RD = ROOT / "runs" / RUN


def caption(t, s):
    return json.loads((RD / f"traj_{t:03d}" / f"step_{s:03d}.json").read_text()).get("caption") or ""


def exits(INS, last_risk):
    """(chain, exit step, out length, returned) for every exit whose last inside step is at risk."""
    out = []
    for t in range(INS.shape[0]):
        ins = INS[t]; n = len(ins)
        for s in range(1, n):
            if ins[s - 1] and not ins[s] and s - 1 <= last_risk:
                e = s
                while e < n and not ins[e]: e += 1
                out.append((t, s, e - s, e < n))
    return out


def distances(run, c):
    B = Cache(run).arrays("dinov2"); assert B["mask"].all(), f"{run}: embeddings incomplete"
    X = B["X"].astype(np.float64); X /= np.linalg.norm(X, axis=-1, keepdims=True); return 1 - X @ c


def main():
    c = np.load(ROOT / "archive/a0_core_centroids.npz", allow_pickle=True)["centroid_dinov2"][CAT].astype(np.float64); c /= np.linalg.norm(c)
    D = distances(RUN, c); assert D.shape == (100, NSTEP), D.shape
    INS = np.stack([label(D[t]) for t in range(100)]); at_risk = int(INS[:, : LAST_RISK + 1].sum())
    ex = exits(INS, LAST_RISK); esc = [x for x in ex if x[2] >= OUT_MIN]
    src = {s["chain"]: s for s in json.loads((RD / "seed_states.json").read_text())["states"]}
    escapes = []
    for t, s, length, returned in esc:
        caps = [caption(t, j) for j in range(s, s + length)]; prev = caption(t, s - 1)
        escapes.append(dict(chain=t, source=f"{src[t]['source_run']}/{src[t]['source_traj']}/{src[t]['source_step']}", exit_step=s, out_steps=length,
                            returned=returned, church_captions_outside=sum(bool(CHURCH.search(x)) for x in caps), dropped_word_start=not CHURCH.search(prev),
                            d_end=round(float(D[t, -1]), 4), prev_caption=prev, first_out_caption=caps[0], last_caption=caption(t, s + length - 1)))
    k = len(escapes); rate = k / at_risk; lo, hi = garwood(k, at_risk)
    E = json.loads((ROOT / "reports" / "esc_e_metrics.json").read_text()); er, (elo, ehi) = E["ESC2_eye"]["rate"], E["ESC2_eye"]["ci95"]
    overlap = not (hi < elo or ehi < lo)
    ESC4 = dict(cathedral_rate=rate, cathedral_ci95=[lo, hi], eye_rate=er, eye_ci95=[elo, ehi], point_lower=rate < er, intervals_overlap=overlap,
                verdict="PASS" if (rate < er and not overlap) else ("FAIL" if (rate >= er and not overlap) else "not resolved"))
    returns = [x[2] for x in exits(INS, NSTEP) if x[3]]
    # out-window sensitivity, both attractors (ESC-E recomputed from its own cache and centroid)
    Ee = json.loads((ROOT / "runs" / "esc_e" / "seed_states.json").read_text())
    ce = np.load(ROOT / Ee["labels"])["C"][Ee["attractor"]].astype(np.float64); ce /= np.linalg.norm(ce)
    De = distances("esc_e", ce); INSe = np.stack([label(De[t]) for t in range(100)])
    windows = [40, 60, 80, 100, 120, 160, 200]; curve = {}
    for name, I, n in (("esc_c", INS, NSTEP), ("esc_e", INSe, 401)):
        rows = []
        for w in windows:
            lr = n - 1 - w; N = int(I[:, : lr + 1].sum()); kk = sum(1 for x in exits(I, lr) if x[2] >= w); a, b = garwood(kk, N)
            rows.append(dict(window=w, escapes=kk, at_risk=N, rate=kk / N, ci95=[a, b]))
        curve[name] = rows
    out = dict(run=RUN, centroid="archive/a0_core_centroids.npz centroid_dinov2[0]", radius=R0, exit_factor=EXIT, out_min=OUT_MIN,
               step0_above_r=int((D[:, 0] > R0).sum()), step0_above_exit=int((D[:, 0] > EXIT * R0).sum()), steps_at_risk=at_risk,
               exits_at_risk=len(ex), all_exits=len(exits(INS, NSTEP)), returning_exits=len(returns), longest_return=max(returns) if returns else None,
               chains_ever_outside=int((~INS).any(1).sum()), chains_inside_at_300=int(INS[:, -1].sum()), inside_share_all=float(INS.mean()),
               max_distance=float(D.max()), steps_beyond_035=int((D > 0.35).sum()), steps_beyond_06=int((D > 0.6).sum()),
               churchless_captions=sum(not CHURCH.search(caption(t, s)) for t in range(100) for s in range(NSTEP)),
               ESC1_cathedral=dict(escapes=k, pass_=k >= 1, upper95_if_none=hi if k == 0 else None),
               ESC2_cathedral=dict(rate=rate, ci95=[lo, hi], pass_=rate < 1e-3), ESC4=ESC4, window_curve=curve, escapes=escapes)
    (ROOT / "reports" / "esc_c_metrics.json").write_text(json.dumps(out, indent=1, default=float, ensure_ascii=False))
    plot(D, INS, escapes, ROOT / "reports" / "figures" / "esc_c_distance.png"); plot_window(curve, ROOT / "reports" / "figures" / "esc_window.png")
    strips(escapes, D, ROOT / "reports" / "figures" / "esc_c_escapes.jpg")
    print(json.dumps({kk: v for kk, v in out.items() if kk not in ("escapes", "window_curve")}, indent=1, default=float))
    for nm, rows in curve.items(): print(nm, [(r["window"], r["escapes"], f"{r['rate']:.2e}") for r in rows])
    for e in escapes: print({kk: v for kk, v in e.items() if "caption" not in kk})


def strips(escapes, D, path, T=128):
    if not escapes: return
    offs = [-5, -1, 0, 3, 10, 20, 39]; W = Image.new("RGB", (230 + len(offs) * T, len(escapes) * (T + 14)), "white"); d = ImageDraw.Draw(W)
    for i, e in enumerate(escapes):
        y = i * (T + 14); d.text((4, y + 20), f"chain {e['chain']}\n{e['source']}\nexit step {e['exit_step']}\nout {e['out_steps']}"
                                              f"{'' if e['returned'] else '+ (to end)'}\nchurch words outside {e['church_captions_outside']}", fill="black")
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
    cols = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#000000"]
    for i, t in enumerate(esc): ax.plot(D[t], color=cols[i % len(cols)], lw=1.5, label=f"chain {t}")
    ax.axhline(R0, color="#444444", lw=1, ls="--"); ax.axhline(EXIT * R0, color="#444444", lw=1, ls=":")
    ax.set_xlabel("step"); ax.set_ylabel("DINOv2 distance to A0-core cathedral centroid"); ax.set_xlim(0, NSTEP - 1)
    ax.set_title("ESC-C: 100 chains started inside the cathedral" + ("; chains with an escape in colour" if esc else " (no escape)"))
    if esc: ax.legend(fontsize=7, frameon=False)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(path, dpi=130)


def plot_window(curve, path):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    for (name, lab, col) in (("esc_e", "eye (ESC-E)", "#0072B2"), ("esc_c", "cathedral (ESC-C)", "#D55E00")):
        rows = curve[name]; x = [r["window"] for r in rows]; y = [r["rate"] for r in rows]
        ax.plot(x, y, marker="o", color=col, lw=2, label=lab)
        ax.fill_between(x, [r["ci95"][0] for r in rows], [r["ci95"][1] for r in rows], color=col, alpha=0.15, lw=0)
    ax.axvline(OUT_MIN, color="#444444", lw=1, ls="--"); ax.text(OUT_MIN + 2, ax.get_ylim()[1] * 0.92, "graded (40)", fontsize=8)
    ax.set_xlabel("out-window: consecutive steps outside to count as an escape"); ax.set_ylabel("escapes per step at risk")
    ax.legend(frameon=False); [ax.spines[s].set_visible(False) for s in ("top", "right")]
    fig.tight_layout(); fig.savefig(path, dpi=130)


if __name__ == "__main__":
    main()
