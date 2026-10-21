"""Compute and cache per-step embeddings for one run (CPU by default; GPU only if CUDA_VISIBLE_DEVICES allows it).

    .venv/bin/python analysis/embed.py <run> [--spaces dinov2,minilm,clip] [--batch 16]

Spaces (pinned in common.MODELS):
  dinov2  facebook/dinov2-base CLS token of every step image, L2-normalised                      -> cache/<run>/dinov2.npz  X
  minilm  sentence-transformers/all-MiniLM-L6-v2 of every record's `caption`                     -> cache/<run>/minilm.npz  X
  clip    openai/clip-vit-large-patch14 image embeds and text embeds of `caption` (77-token cut) -> cache/<run>/clip.npz    X_image, X_text
  siglip  google/siglip-base-patch16-224 pooled image embeds (B-img steering space, D17; never graded) -> cache/<run>/siglip.npz  X
Arrays are [n_traj, n_step, dim] with NaN where not cached, plus trajs, steps, mask. Incremental: (traj, step) pairs already in
the cache are skipped, so this can be re-run as a run grows. meta.json records model ids, HF revisions and package versions.
CLIP embeddings are stored for steering (archive) only; nothing is graded with them.
"""
import argparse, os, pathlib, sys, time
import numpy as np
import torch
from common import ROOT, Cache, MODELS, SPACES, list_steps, read_record, image_path, cpu_only, caption_used

DIMS = {"dinov2": {"X": 768}, "minilm": {"X": 384}, "clip": {"X_image": 768, "X_text": 768}, "siglip": {"X": 768}}


def grow(d, trajs, steps, dims):
    """Return arrays covering trajs x steps, carrying over whatever `d` (old cache or None) already holds."""
    out = {"trajs": np.array(trajs, dtype=np.int32), "steps": np.array(steps, dtype=np.int32), "mask": np.zeros((len(trajs), len(steps)), bool)}
    for k, dim in dims.items():
        out[k] = np.full((len(trajs), len(steps), dim), np.nan, dtype=np.float32)
    if d is not None:
        ti = {int(t): i for i, t in enumerate(trajs)}; si = {int(s): j for j, s in enumerate(steps)}
        for i0, t in enumerate(d["trajs"]):
            for j0, s in enumerate(d["steps"]):
                if d["mask"][i0, j0] and int(t) in ti and int(s) in si:
                    out["mask"][ti[int(t)], si[int(s)]] = True
                    for k in dims: out[k][ti[int(t)], si[int(s)]] = d[k][i0, j0]
    return out


def pending(arr, avail):
    """(traj, step) pairs that exist on disk but are not cached, as (i, j) index pairs."""
    ti = {int(t): i for i, t in enumerate(arr["trajs"])}; si = {int(s): j for j, s in enumerate(arr["steps"])}
    return [(ti[t], si[s]) for t, ss in avail.items() for s in ss if not arr["mask"][ti[t], si[s]]]


def batches(seq, n):
    for i in range(0, len(seq), n): yield seq[i:i + n]


def embed_dinov2(run_dir, arr, todo, bs, dev):
    from transformers import AutoImageProcessor, AutoModel
    m = MODELS["dinov2"]
    proc = AutoImageProcessor.from_pretrained(m["id"], revision=m["revision"])
    model = AutoModel.from_pretrained(m["id"], revision=m["revision"]).to(dev).eval()
    for b in batches(todo, bs):
        ims = [thumb_open(image_path(run_dir, int(arr["trajs"][i]), int(arr["steps"][j]))) for i, j in b]
        with torch.no_grad():
            h = model(**proc(images=ims, return_tensors="pt").to(dev)).last_hidden_state[:, 0]
        h = torch.nn.functional.normalize(h, dim=-1).cpu().numpy()
        for (i, j), v in zip(b, h): arr["X"][i, j] = v; arr["mask"][i, j] = True
        yield len(b)


def embed_minilm(run_dir, arr, todo, bs, dev):
    from sentence_transformers import SentenceTransformer
    m = MODELS["minilm"]
    model = SentenceTransformer(m["id"], revision=m["revision"], device=dev)
    for b in batches(todo, max(bs, 64)):
        caps = [caption_used(run_dir, int(arr["trajs"][i]), int(arr["steps"][j])) for i, j in b]
        E = model.encode(caps, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
        for (i, j), v in zip(b, E): arr["X"][i, j] = v; arr["mask"][i, j] = True
        yield len(b)


def embed_clip(run_dir, arr, todo, bs, dev):
    from transformers import CLIPModel, CLIPProcessor
    m = MODELS["clip"]
    proc = CLIPProcessor.from_pretrained(m["id"], revision=m["revision"])
    model = CLIPModel.from_pretrained(m["id"], revision=m["revision"]).to(dev).eval()
    for b in batches(todo, bs):
        ims, caps = [], []
        for i, j in b:
            t, s = int(arr["trajs"][i]), int(arr["steps"][j])
            ims.append(thumb_open(image_path(run_dir, t, s))); caps.append(caption_used(run_dir, t, s))
        with torch.no_grad():
            vi = model.get_image_features(**proc(images=ims, return_tensors="pt").to(dev))
            vt = model.get_text_features(**proc(text=caps, return_tensors="pt", padding=True, truncation=True, max_length=77).to(dev))
            vi = getattr(vi, "pooler_output", vi); vt = getattr(vt, "pooler_output", vt)   # transformers >= 5 returns a ModelOutput
        vi = torch.nn.functional.normalize(vi, dim=-1).cpu().numpy(); vt = torch.nn.functional.normalize(vt, dim=-1).cpu().numpy()
        for (i, j), a, c in zip(b, vi, vt): arr["X_image"][i, j] = a; arr["X_text"][i, j] = c; arr["mask"][i, j] = True
        yield len(b)


def embed_siglip(run_dir, arr, todo, bs, dev):
    """Steering-only space (B-img archive, D17): cached here for the radius calibration and archive diagnostics, never graded."""
    sys.path.insert(0, str(ROOT / "src"))
    from embedders.siglip import SiglipEmbedder
    emb = SiglipEmbedder(dev)
    for b in batches(todo, bs):
        ims = [thumb_open(image_path(run_dir, int(arr["trajs"][i]), int(arr["steps"][j]))) for i, j in b]
        for (i, j), v in zip(b, emb.embed(ims)): arr["X"][i, j] = v; arr["mask"][i, j] = True
        yield len(b)


def thumb_open(p):
    from PIL import Image
    return Image.open(p).convert("RGB")


EMBEDDERS = {"dinov2": embed_dinov2, "minilm": embed_minilm, "clip": embed_clip, "siglip": embed_siglip}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--spaces", default=",".join(SPACES)); ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--save-every", type=int, default=256, help="checkpoint the cache after this many new items")
    a = ap.parse_args()
    run_dir = ROOT / "runs" / a.run
    avail = list_steps(run_dir)
    if not avail: raise SystemExit(f"no complete records under {run_dir}")
    trajs = sorted(avail); steps = sorted({s for ss in avail.values() for s in ss})
    dev = "cuda" if cpu_only() else "cpu"      # see common.cpu_only: CUDA_VISIBLE_DEVICES="" must never enter libcuda under WSL
    torch.set_num_threads(max(1, (os.cpu_count() or 2) - 2))
    cache = Cache(a.run)
    print(f"{a.run}: {len(trajs)} traj, {sum(len(s) for s in avail.values())} records, device={dev}")
    for space in [s.strip() for s in a.spaces.split(",") if s.strip()]:
        if space not in EMBEDDERS: raise SystemExit(f"unknown space {space}; choose from {SPACES}")
        arr = grow(cache.load(space), trajs, steps, DIMS[space])
        todo = pending(arr, avail)
        print(f"[{space}] cached={int(arr['mask'].sum())} todo={len(todo)}", flush=True)
        if not todo:
            cache.save(space, arr); continue
        t0 = time.time(); done = 0; since = 0
        for n in EMBEDDERS[space](run_dir, arr, todo, a.batch, dev):
            done += n; since += n
            if since >= a.save_every:
                cache.save(space, arr, {"device": dev}); since = 0
                print(f"[{space}] {done}/{len(todo)}  {(time.time() - t0) / done:.3f} s/item", flush=True)
        cache.save(space, arr, {"device": dev, "seconds_last_pass": round(time.time() - t0, 1), "items_last_pass": done})
        print(f"[{space}] done {done} in {time.time() - t0:.0f} s ({(time.time() - t0) / done:.3f} s/item) -> {cache.path(space)}", flush=True)


if __name__ == "__main__":
    main()
