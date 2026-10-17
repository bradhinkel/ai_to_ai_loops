"""Rebuild the A0 figures and tables for one run from runs/<run>/ alone (SPEC §8, §4.3).

Outputs in reports/<run>/:
  drift_step.png        step-to-step cosine distance between consecutive captions (MiniLM), per trajectory + mean
  drift_cumulative.png  cosine distance of each caption from the trajectory's first caption
  contact_endpoints.jpg last complete image per trajectory, grouped by k-means cluster of the endpoint captions
  trajectories.jpg      sample steps for the first 8 trajectories
  elbow.png             k-means inertia vs k on endpoint caption embeddings (only meaningful with >= 30 trajectories)
  summary.json          throughput, plateau step, elbow k, flag counts, captions per cluster

Captions: record k holds `prompt` (what made image k; = caption of image k-1) and `caption` (caption of image k).
Hintze's CSV step k is our prompt at step k, so the Hintze-comparable series is prompt_1..prompt_{N-1} plus the last caption.
    .venv/bin/python analysis/a0_report.py a0_pilot [--k 12] [--hintze data/hintze_figshare/temps_0.9/logs]
"""
import argparse, csv, json, pathlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLUE, ORANGE, GRAY, INK, SURF = "#2a78d6", "#eb6834", "#b8b7b1", "#0b0b0b", "#fcfcfb"   # dataviz reference palette (light)


def load_run(run_dir):
    trajs = {}
    for td in sorted(run_dir.glob("traj_*")):
        recs = []
        for p in sorted(td.glob("step_???.json")):
            recs.append(json.loads(p.read_text()))
        if recs:
            trajs[int(td.name.split("_")[1])] = recs
    return trajs


def caption_series(recs):
    """Hintze-comparable caption sequence: caption_0 .. caption_{N-1} (caption k describes image k)."""
    return [r["caption"] for r in recs]


def embed(texts, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(model_name, device="cpu")
    return m.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=False)


def cos_dist(a, b):
    return 1.0 - np.sum(a * b, axis=-1)


def style(ax, title, xlabel, ylabel):
    ax.set_facecolor(SURF); ax.figure.set_facecolor(SURF)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(GRAY)
    ax.grid(axis="y", color=GRAY, linewidth=0.5, alpha=0.6); ax.set_axisbelow(True)
    ax.tick_params(colors="#52514e", labelsize=9); ax.set_title(title, loc="left", color=INK, fontsize=11)
    ax.set_xlabel(xlabel, color="#52514e", fontsize=9); ax.set_ylabel(ylabel, color="#52514e", fontsize=9)


def hintze_step_drift(logs_dir, max_runs=100):
    """Mean step-to-step MiniLM distance for Hintze's T=0.9 captions (csv step k = caption of image k-1)."""
    seqs = []
    for p in sorted(pathlib.Path(logs_dir).glob("*.csv"))[:max_runs]:
        rows = list(csv.DictReader(open(p, newline="")))
        caps = [r["prompt"].strip() for r in rows[1:]]      # drop the seed prompt
        if len(caps) >= 50: seqs.append(caps)
    if not seqs: return None
    flat = [c for s in seqs for c in s]; E = embed(flat); out = []; i = 0
    for s in seqs:
        e = E[i:i + len(s)]; i += len(s); out.append(cos_dist(e[1:], e[:-1]))
    L = min(len(x) for x in out)
    return np.mean([x[:L] for x in out], axis=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--k", type=int, default=0, help="fixed k for the contact sheet (0 = elbow or 12)")
    ap.add_argument("--hintze", default="data/hintze_figshare/temps_0.9/logs"); ap.add_argument("--thumb", type=int, default=192)
    a = ap.parse_args()
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    run_dir = ROOT / "runs" / a.run; out = ROOT / "reports" / a.run; out.mkdir(parents=True, exist_ok=True)
    trajs = load_run(run_dir)
    if not trajs: raise SystemExit("no complete records")
    summary = {"run": a.run, "n_traj": len(trajs), "steps_complete": {t: len(r) for t, r in trajs.items()}}

    # --- embeddings and drift ---
    series = {t: caption_series(r) for t, r in trajs.items()}
    flat = [c for s in series.values() for c in s]; E = embed(flat)
    emb = {}; i = 0
    for t, s in series.items(): emb[t] = E[i:i + len(s)]; i += len(s)
    step_d = {t: cos_dist(e[1:], e[:-1]) for t, e in emb.items() if len(e) > 1}
    cum_d = {t: cos_dist(e[1:], e[:1]) for t, e in emb.items() if len(e) > 1}
    L = min(len(x) for x in step_d.values()) if step_d else 0
    mean_step = np.mean([x[:L] for x in step_d.values()], axis=0) if L else np.array([])
    mean_cum = np.mean([x[:L] for x in cum_d.values()], axis=0) if L else np.array([])
    plateau = None
    if L >= 30:      # first step after which the 10-step rolling mean stays within 10% of the final-20-step level
        final = mean_step[-20:].mean()
        roll = np.convolve(mean_step, np.ones(10) / 10, mode="valid")
        ok = np.abs(roll - final) <= 0.10 * final + 0.01
        for s in range(len(ok)):
            if ok[s:].all(): plateau = s + 10; break
    summary.update({"mean_step_drift_first5": mean_step[:5].round(3).tolist(), "mean_step_drift_last20": float(mean_step[-20:].mean()) if L else None, "plateau_step": plateau})

    hz = hintze_step_drift(ROOT / a.hintze) if (ROOT / a.hintze).exists() else None
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=130)
    for t, x in step_d.items(): ax.plot(np.arange(1, len(x) + 1), x, color=GRAY, linewidth=0.8, alpha=0.6)
    if L: ax.plot(np.arange(1, L + 1), mean_step, color=BLUE, linewidth=2, label=f"{a.run} mean (n={len(step_d)})")
    if hz is not None: ax.plot(np.arange(1, len(hz) + 1), hz, color=ORANGE, linewidth=2, label="Hintze T=0.9 mean (figshare)")
    style(ax, "Step-to-step caption drift (MiniLM cosine distance, caption k vs k-1)", "step k", "cosine distance")
    ax.legend(frameon=False, fontsize=9); fig.tight_layout(); fig.savefig(out / "drift_step.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=130)
    for t, x in cum_d.items(): ax.plot(np.arange(1, len(x) + 1), x, color=GRAY, linewidth=0.8, alpha=0.6)
    if L: ax.plot(np.arange(1, L + 1), mean_cum, color=BLUE, linewidth=2, label=f"{a.run} mean")
    style(ax, "Cumulative drift (distance of caption k from caption 0)", "step k", "cosine distance")
    ax.legend(frameon=False, fontsize=9); fig.tight_layout(); fig.savefig(out / "drift_cumulative.png"); plt.close(fig)

    # --- endpoint clustering (k-means n_init=10, random_state=0, elbow on inertia as in figures.ipynb) ---
    from sklearn.cluster import KMeans
    ends = {t: e[-1] for t, e in emb.items()}; ids = sorted(ends); X = np.stack([ends[t] for t in ids])
    ks = list(range(2, min(25, len(ids) - 1) + 1)); inertia = []
    for k in ks: inertia.append(KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_)
    elbow = None
    if len(ks) >= 4:   # knee: max distance from the chord between the first and last point
        p1, p2 = np.array([ks[0], inertia[0]]), np.array([ks[-1], inertia[-1]]); yn = (np.array(inertia) - inertia[-1]) / (inertia[0] - inertia[-1] + 1e-9)
        xn = (np.array(ks) - ks[0]) / (ks[-1] - ks[0]); d = np.abs(xn + yn - 1) / np.sqrt(2); elbow = int(ks[int(np.argmax(d))])
    k = a.k or (elbow if elbow and len(ids) >= 30 else min(12, max(2, len(ids) // 2)))
    labels = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    summary.update({"elbow_k": elbow, "k_used_for_sheet": k, "inertia": dict(zip(map(str, ks), [round(float(v), 3) for v in inertia])),
                    "clusters": {str(c): [ids[i] for i in range(len(ids)) if labels[i] == c] for c in range(k)},
                    "cluster_example_captions": {str(c): series[ids[int(np.where(labels == c)[0][0])]][-1][:200] for c in range(k)}})
    fig, ax = plt.subplots(figsize=(6, 3.6), dpi=130); ax.plot(ks, inertia, color=BLUE, linewidth=2, marker="o", markersize=4)
    if elbow: ax.axvline(elbow, color=ORANGE, linewidth=1.2, linestyle="--", label=f"elbow k={elbow}"); ax.legend(frameon=False, fontsize=9)
    style(ax, "k-means inertia on endpoint caption embeddings", "k", "inertia"); fig.tight_layout(); fig.savefig(out / "elbow.png"); plt.close(fig)

    # --- contact sheets ---
    T = a.thumb
    order = sorted(range(len(ids)), key=lambda i: (labels[i], ids[i])); cols = 10; rows = (len(order) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * T, rows * T), "white"); d = ImageDraw.Draw(sheet)
    for n, i in enumerate(order):
        t = ids[i]; last = trajs[t][-1]; im = Image.open(run_dir / f"traj_{t:03d}" / last["image"]).convert("RGB").resize((T, T), Image.LANCZOS)
        r, c = divmod(n, cols); sheet.paste(im, (c * T, r * T))
        d.rectangle((c * T, r * T, c * T + 78, r * T + 13), fill="black"); d.text((c * T + 2, r * T + 1), f"c{labels[i]} t{t:03d} s{last['step']}", fill="white")
    sheet.save(out / "contact_endpoints.jpg", quality=88)

    steps = [0, 1, 5, 10, 25, 50, 75, 99]; sample = ids[:8]
    sheet = Image.new("RGB", (len(steps) * T, len(sample) * T), "white"); d = ImageDraw.Draw(sheet)
    for ri, t in enumerate(sample):
        for ci, s in enumerate(steps):
            p = run_dir / f"traj_{t:03d}" / f"step_{s:03d}.png"
            if p.exists(): sheet.paste(Image.open(p).convert("RGB").resize((T, T), Image.LANCZOS), (ci * T, ri * T))
            d.rectangle((ci * T, ri * T, ci * T + 70, ri * T + 13), fill="black"); d.text((ci * T + 2, ri * T + 1), f"t{t:03d} s{s}", fill="white")
    sheet.save(out / "trajectories.jpg", quality=88)

    # --- throughput and flags ---
    ev = run_dir / "events.jsonl"; steps_done = [json.loads(l) for l in ev.read_text().splitlines() if '"step_done"' in l] if ev.exists() else []
    if steps_done:
        summary["throughput"] = {"n_step_events": len(steps_done), "median_s_per_traj_step": float(np.median([e["s_per_traj_step"] for e in steps_done])),
                                 "median_sdxl_s_per_traj": float(np.median([e["gen_s"] / e["n_traj"] for e in steps_done])),
                                 "median_llava_s_per_traj": float(np.median([e["cap_s"] / e["n_traj"] for e in steps_done]))}
    flags = {}; words = []; toks = 0; ntot = 0
    for recs in trajs.values():
        for r in recs:
            ntot += 1; words.append(r["caption_words"]); toks += int(r.get("prompt_truncated_by_clip", False))
            for f, v in r["caption_flags"].items(): flags[f] = flags.get(f, 0) + int(v)
    summary.update({"n_records": ntot, "caption_words_mean": float(np.mean(words)), "caption_words_median": float(np.median(words)),
                    "share_prompts_clip_truncated": toks / max(ntot, 1), "flag_counts": flags})
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("inertia", "clusters", "cluster_example_captions", "steps_complete")}, indent=1))


if __name__ == "__main__":
    main()
