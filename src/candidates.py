"""Part 2 candidate selection (SPEC2 §5.1 mechanics, B-img pilot design; D17).

Each step the captioner writes K captions of the current image; the generator renders all K; the selector picks one.
  mode none    K = 1, Hintze's loop (every Part 1 cell).
  mode random  arm A: one of the K candidates at random (RNG seeded per trajectory and step), no archive.
  mode reject  B-img: candidates within `radius_reject` (cosine, SigLIP) of any archive entry are discarded; one survivor is
               picked at random; if none survive the runner resamples K new captions up to `resample` times, then advances
               the most distant candidate and marks the step trapped.
Archive (reject mode, shared by all trajectories, image space): after the image at step t is chosen, if t >= burn_in and the
trajectory's images at steps t-window+1 .. t all lie within `radius_archive` of their normalised mean, image t's embedding
enters the archive. Entries only act on later steps (step < s when selecting at step s), so the result does not depend on the
order trajectories are processed within a step. The archive is rebuilt from the gen records on resume (each record carries
its SigLIP embedding and `archived`), so a crash between the record and any log loses nothing.
SigLIP is steering only (CLAUDE.md rule 4): evaluation stays in DINOv2 / MiniLM.
"""
import random
import numpy as np

from .embedders.siglip import SiglipEmbedder, cos_dist

DEFAULTS = {"k": 1, "mode": "none", "embedder": "siglip", "device": "cuda", "radius_archive": 0.20, "window": 5, "burn_in": 5,
            "radius_reject": 0.20, "resample": 2, "seed": 0}
CANDIDATE_SEED_STRIDE = 10 ** 8     # sdxl_seed = base + traj*10000 + step + (round*K + k) * stride  (D17)


class Archive:
    def __init__(self):
        self.entries = []        # (traj, step)
        self.X = np.zeros((0, 768), np.float32)

    def add(self, traj, step, emb):
        self.entries.append((int(traj), int(step)))
        self.X = np.vstack([self.X, np.asarray(emb, np.float32)[None]])

    def min_dist(self, embs, before_step):
        """Per candidate: distance to the nearest entry with step < before_step (inf when none)."""
        keep = np.array([s < before_step for _, s in self.entries], bool)
        if not keep.any():
            return np.full(len(embs), np.inf, np.float32), 0
        return cos_dist(embs, self.X[keep]).min(1), int(keep.sum())

    def __len__(self):
        return len(self.entries)


class Selector:
    def __init__(self, cfg, logger=None):
        self.cfg = {**DEFAULTS, **(cfg or {})}
        self.k = int(self.cfg["k"]); self.mode = self.cfg["mode"]; self.log = logger
        if self.mode not in ("none", "random", "reject"):
            raise ValueError(f"selection.mode {self.mode!r}")
        if self.mode == "none" and self.k != 1:
            raise ValueError("candidates.k > 1 needs selection.mode random or reject")
        self.embedder = SiglipEmbedder(self.cfg["device"]) if self.mode == "reject" else None
        self.archive = Archive()
        self.history = {}          # traj -> {step: emb} of chosen images (reject mode)

    def info(self):
        return {**self.cfg, "embedder": self.embedder.info() if self.embedder else None, "candidate_seed_stride": CANDIDATE_SEED_STRIDE}

    def rng(self, traj, step, round_=0):
        return random.Random(f"{self.cfg['seed']}:{traj}:{step}:{round_}")

    def candidate_seed(self, base, traj, step, round_, k):
        return base + traj * 10000 + step + (round_ * self.k + k) * CANDIDATE_SEED_STRIDE

    # ---- resume -----------------------------------------------------------------------------------------------
    def restore(self, traj, step, rec):
        """Re-register a chosen image from its gen record (called for every existing record on start-up, in step order)."""
        if self.mode != "reject" or "siglip" not in rec:
            return
        emb = np.asarray(rec["siglip"], np.float32)
        self.history.setdefault(traj, {})[step] = emb
        if rec.get("archived"):
            self.archive.add(traj, step, emb)

    # ---- selection ----------------------------------------------------------------------------------------------
    def select(self, traj, step, images, round_=0):
        """images: K PIL candidates for this round. Returns (chosen index or None, per-candidate info list, extra record fields)."""
        if self.mode == "random":
            i = self.rng(traj, step, round_).randrange(len(images))
            return i, [{"k": k} for k in range(len(images))], {"selection_mode": "random"}
        embs = self.embedder.embed(images)
        d, n_arch = self.archive.min_dist(embs, step)
        r = float(self.cfg["radius_reject"])
        survivors = [k for k in range(len(images)) if d[k] > r]
        info = [{"k": k, "dist_archive": (None if np.isinf(d[k]) else round(float(d[k]), 4)), "rejected": k not in survivors} for k in range(len(images))]
        extra = {"selection_mode": "reject", "archive_size": n_arch, "archive_total": len(self.archive), "radius_reject": r}
        if survivors:
            i = survivors[self.rng(traj, step, round_).randrange(len(survivors))]
            return i, info, {**extra, "n_rejected": len(images) - len(survivors)}
        return None, info, {**extra, "n_rejected": len(images)}

    def most_distant(self, rounds):
        """rounds: list of per-round candidate info lists; returns (round, k) with the largest dist_archive (trapped step)."""
        best, where = -1.0, (0, 0)
        for r, infos in enumerate(rounds):
            for c in infos:
                v = c.get("dist_archive"); v = np.inf if v is None else v
                if v > best: best, where = v, (r, c["k"])
        return where

    def embed_one(self, image):
        return self.embedder.embed([image])[0]

    # ---- archive update -----------------------------------------------------------------------------------------
    def register(self, traj, step, emb):
        """Chosen image at `step`: record its embedding; archive it if the last `window` images are persistent. Returns archived flag."""
        if self.mode != "reject":
            return False
        h = self.history.setdefault(traj, {}); h[step] = np.asarray(emb, np.float32)
        w, b, R = int(self.cfg["window"]), int(self.cfg["burn_in"]), float(self.cfg["radius_archive"])
        if step < b or any(step - i not in h for i in range(w)):
            return False
        W = np.stack([h[step - i] for i in range(w)])
        m = W.mean(0); m /= (np.linalg.norm(m) + 1e-9)
        if (1.0 - W @ m).max() <= R:
            self.archive.add(traj, step, h[step])
            if self.log: self.log.info("archive +1: traj %d step %d (size %d)", traj, step, len(self.archive))
            return True
        return False
