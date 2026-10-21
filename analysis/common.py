"""Shared helpers for embed.py, build_archive.py and e1_report.py.

Rules re-used verbatim from a0_report.py (keep both in sync):
  * k-means: KMeans(n_clusters=k, n_init=10, random_state=0); elbow = knee of inertia over k = 2..min(25, n-1),
    largest distance from the chord between the first and last point; only trusted with >= 30 points.
  * plateau: first step after which the 10-step rolling mean of the mean step-to-step drift stays within
    10% (+0.01) of the final-20-step level; needs >= 30 steps.
Step 0 (the image made from the seed prompt) is excluded from every analysis, as in Hintze.
"""
import json, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis")); sys.path.insert(0, str(ROOT / "src"))
from a0_report import cos_dist, style, BLUE, ORANGE, GRAY, INK, SURF  # noqa: E402  (palette + axis style)

CACHE = ROOT / "analysis" / "cache"
# dataviz reference palette, categorical slots 1..8 in fixed order (slot 1 = reference run)
SERIES = [BLUE, ORANGE, "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]

# Pinned models (HF commit shas resolved 2026-10-18). Passed as revision= to every from_pretrained.
MODELS = {
    "dinov2": {"id": "facebook/dinov2-base", "revision": "f9e44c814b77203eaa57a6bdbbd535f21ede1415", "pooling": "CLS token, L2-normalised"},
    "minilm": {"id": "sentence-transformers/all-MiniLM-L6-v2", "revision": "1110a243fdf4706b3f48f1d95db1a4f5529b4d41", "pooling": "sentence-transformers default, L2-normalised"},
    "clip": {"id": "openai/clip-vit-large-patch14", "revision": "32bd64288804d66eefd0ccbe215aa642df71cc41", "pooling": "projected image/text embeds, L2-normalised; text truncated at 77 tokens"},
    # steering-only image space for the Part 2 B-img archive (SPEC2 §5; D17). Never graded with (rule 4), like clip.
    "siglip": {"id": "google/siglip-base-patch16-224", "revision": "7fd15f0689c79d79e38b1c2e2e2370a7bf2761ed", "pooling": "pooled image embeds, L2-normalised"},
    # E6 skin-tone pipeline (analysis/skin_tone.py): CelebAMask-HQ face parser (SegFormer) on YuNet face crops
    "faceparse": {"id": "jonathandinu/face-parsing", "revision": "758b82e15a0178c9db39c1ff666a8b56e3a550c8", "pooling": "argmax labels; skin = label 1"},
    "yunet": {"id": "opencv_zoo face_detection_yunet_2023mar.onnx", "revision": "sha256 8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4", "pooling": "boxes with score >= 0.6"},
}
SPACES = ("dinov2", "minilm", "clip")   # clip (and siglip, embed.py --spaces siglip) are for steering only; never graded (CLAUDE.md rule 4)


def cpu_only():
    """Under WSL, any CUDA runtime call aborts the process (double free in libcuda) when CUDA_VISIBLE_DEVICES="".
    The GPU is reserved for the loop runs, so analysis never touches it: when the variable is set empty, make every
    torch.cuda probe that transformers / sentence-transformers call return the CPU answer without entering libcuda."""
    import os, torch
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        return torch.cuda.is_available()
    torch.cuda.is_available = lambda: False
    torch.cuda.device_count = lambda: 0
    torch.cuda.is_initialized = lambda: False
    torch.cuda.is_current_stream_capturing = lambda: False
    return False


def package_versions():
    import torch, transformers, sklearn, sentence_transformers, PIL, huggingface_hub
    return {"torch": torch.__version__, "transformers": transformers.__version__, "sentence_transformers": sentence_transformers.__version__,
            "scikit_learn": sklearn.__version__, "numpy": np.__version__, "pillow": PIL.__version__, "huggingface_hub": huggingface_hub.__version__}


# ---------------------------------------------------------------- run records
def list_steps(run_dir):
    """{traj: [steps with a complete record]} for runs/<run>/. A step counts only if step_NNN.json exists (store.py)."""
    out = {}
    for td in sorted(pathlib.Path(run_dir).glob("traj_*")):
        steps = sorted(int(p.stem.split("_")[1]) for p in td.glob("step_???.json"))
        if steps:
            out[int(td.name.split("_")[1])] = steps
    return out


def read_record(run_dir, traj, step):
    return json.loads((pathlib.Path(run_dir) / f"traj_{traj:03d}" / f"step_{step:03d}.json").read_text(encoding="utf-8"))


def caption_used(run_dir, traj, step, rec=None):
    """The caption of image `step` that made image step+1. Part 1 records: `caption`. Part 2 records (K candidates, D17):
    `caption` is None and the chosen one is step+1's `prompt_raw`; for the last step (no successor) the first candidate."""
    rec = rec or read_record(run_dir, traj, step)
    if rec.get("caption") is not None:
        return rec["caption"]
    nxt = pathlib.Path(run_dir) / f"traj_{traj:03d}" / f"step_{step + 1:03d}.gen.json"
    if nxt.exists():
        g = json.loads(nxt.read_text(encoding="utf-8")); return g.get("prompt_raw", g["prompt"])
    return (rec.get("captions") or [""])[0]


def image_path(run_dir, traj, step):
    return pathlib.Path(run_dir) / f"traj_{traj:03d}" / f"step_{step:03d}.png"


# ---------------------------------------------------------------- embedding cache
class Cache:
    """analysis/cache/<run>/<space>.npz: arrays X (or X_image, X_text for clip) of shape [n_traj, n_step, dim], NaN where
    missing; trajs [n_traj]; steps [n_step]; mask [n_traj, n_step] (True = cached). meta.json: model ids, revisions, packages."""

    def __init__(self, run):
        self.run = run
        self.dir = CACHE / run

    def path(self, space):
        return self.dir / f"{space}.npz"

    def load(self, space):
        p = self.path(space)
        if not p.exists():
            return None
        z = np.load(p)
        return {k: z[k] for k in z.files}

    def arrays(self, space):
        """{'X': ...} or {'X_image','X_text'} plus trajs, steps, mask. Raises if the space was never embedded."""
        d = self.load(space)
        if d is None:
            raise FileNotFoundError(f"{self.path(space)} missing: run  .venv/bin/python analysis/embed.py {self.run} --spaces {space}")
        return d

    def save(self, space, arrays, meta_extra=None):
        import io
        from store import atomic_write_bytes, atomic_write_json
        self.dir.mkdir(parents=True, exist_ok=True)
        buf = io.BytesIO(); np.savez(buf, **arrays); atomic_write_bytes(self.path(space), buf.getvalue())
        mp = self.dir / "meta.json"
        meta = json.loads(mp.read_text()) if mp.exists() else {"run": self.run, "spaces": {}}
        meta["spaces"][space] = dict(MODELS[space], packages=package_versions(), n_cached=int(arrays["mask"].sum()), **(meta_extra or {}))
        atomic_write_json(mp, meta)



def final_step_matrix(cache, space, run_dir, step=None, key="X"):
    """Final-step embeddings: for each trajectory the embedding at `step` if cached, else its last cached step (>= 1).
    Returns (traj ids, X [n, dim], {traj: step used})."""
    d = cache.arrays(space)
    trajs, steps, mask, X = d["trajs"], d["steps"], d["mask"], d[key]
    ids, rows, used = [], [], {}
    for i, t in enumerate(trajs):
        avail = [int(steps[j]) for j in range(len(steps)) if mask[i, j] and steps[j] >= 1]
        if not avail:
            continue
        s = step if (step is not None and step in avail) else max(avail)
        ids.append(int(t)); rows.append(X[i, list(steps).index(s)]); used[int(t)] = s
    return ids, np.stack(rows).astype(np.float64), used


def series_matrix(cache, space, key="X"):
    """{traj: embeddings for steps 1..last contiguous cached step} (step 0 dropped)."""
    d = cache.arrays(space)
    trajs, steps, mask, X = d["trajs"], d["steps"], d["mask"], d[key]
    out = {}
    for i, t in enumerate(trajs):
        rows = []
        for j, s in enumerate(steps):
            if s < 1: continue
            if not mask[i, j]: break
            rows.append(X[i, j])
        if len(rows) >= 2:
            out[int(t)] = np.stack(rows).astype(np.float64)
    return out


# ---------------------------------------------------------------- metrics
def kmeans(X, k):
    from sklearn.cluster import KMeans
    return KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)


def elbow_k(X, kmax=25):
    """(elbow, ks, inertia) with a0_report's knee rule. elbow is None when fewer than 4 candidate k."""
    n = len(X)
    ks = list(range(2, min(kmax, n - 1) + 1)); inertia = [float(kmeans(X, k).inertia_) for k in ks]
    elbow = None
    if len(ks) >= 4:
        yn = (np.array(inertia) - inertia[-1]) / (inertia[0] - inertia[-1] + 1e-9)
        xn = (np.array(ks) - ks[0]) / (ks[-1] - ks[0]); d = np.abs(xn + yn - 1) / np.sqrt(2); elbow = int(ks[int(np.argmax(d))])
    return elbow, ks, inertia


def k_for_sheet(elbow, n, fixed=0):
    """a0_report's choice: fixed k, else the elbow when n >= 30, else min(12, max(2, n // 2))."""
    return fixed or (elbow if elbow and n >= 30 else min(12, max(2, n // 2)))


def plateau_step(mean_step, first_step=2):
    """a0_report's rule. mean_step[i] is the mean step-to-step drift at step first_step + i. Returns the step or None."""
    L = len(mean_step)
    if L < 30: return None
    final = mean_step[-20:].mean()
    roll = np.convolve(mean_step, np.ones(10) / 10, mode="valid")
    ok = np.abs(roll - final) <= 0.10 * final + 0.01
    for s in range(len(ok)):
        if ok[s:].all(): return int(first_step + s + 10 - 1)
    return None


def vendi(X):
    """Vendi score (Friedman & Dieng 2023): exp(Shannon entropy of the eigenvalues of K/n), K = cosine-similarity kernel."""
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    lam = np.linalg.eigvalsh(Xn @ Xn.T / len(Xn)); lam = lam[lam > 1e-12]
    return float(np.exp(-np.sum(lam * np.log(lam))))


def drift_curves(series):
    """From {traj: [steps 1..N]} -> per-traj step-to-step d(k,k-1) for k>=2 and cumulative d(k,1) for k>=2, plus means
    over the common length. x axis starts at step 2."""
    step_d = {t: cos_dist(e[1:], e[:-1]) for t, e in series.items()}
    cum_d = {t: cos_dist(e[1:], e[:1]) for t, e in series.items()}
    L = min(len(x) for x in step_d.values()) if step_d else 0
    mean_step = np.mean([x[:L] for x in step_d.values()], axis=0) if L else np.array([])
    mean_cum = np.mean([x[:L] for x in cum_d.values()], axis=0) if L else np.array([])
    return step_d, cum_d, mean_step, mean_cum, L


def thumb(path, T):
    from PIL import Image
    return Image.open(path).convert("RGB").resize((T, T), Image.LANCZOS)
