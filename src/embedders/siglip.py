"""SigLIP image embedder for the Part 2 image archive (SPEC2 §5 B-img; D17). Steering only: the archive and the rejection
distance live in this space; evaluation stays in DINOv2 and MiniLM (CLAUDE.md rule 4), and CLIP is not used for either.

google/siglip-base-patch16-224 at a pinned revision; pooled image embeds, L2-normalised; distance = 1 - cosine."""
import numpy as np

SIGLIP_ID = "google/siglip-base-patch16-224"
SIGLIP_REV = "7fd15f0689c79d79e38b1c2e2e2370a7bf2761ed"


class SiglipEmbedder:
    def __init__(self, device="cuda", model_id=SIGLIP_ID, revision=SIGLIP_REV):
        self.device, self.model_id, self.revision = device, model_id, revision
        self.model = self.proc = None

    def load(self):
        if self.model is not None: return
        import torch
        from transformers import AutoModel, AutoProcessor
        self.proc = AutoProcessor.from_pretrained(self.model_id, revision=self.revision)
        self.model = AutoModel.from_pretrained(self.model_id, revision=self.revision).eval().to(self.device)
        self.torch = torch

    def info(self):
        return {"model": self.model_id, "revision": self.revision, "pooling": "pooled image embeds, L2-normalised", "distance": "1 - cosine", "device": self.device}

    def embed(self, images):
        """PIL images -> float32 array [n, 768], unit norm."""
        self.load()
        with self.torch.no_grad():
            o = self.model.get_image_features(**self.proc(images=list(images), return_tensors="pt").to(self.device))
        e = getattr(o, "pooler_output", o)
        return self.torch.nn.functional.normalize(e, dim=-1).float().cpu().numpy()

    def release(self):
        if self.model is None: return
        self.model = self.proc = None
        import gc, torch
        gc.collect(); torch.cuda.empty_cache()


def cos_dist(A, B):
    """Pairwise 1 - cosine for unit-norm rows: [n, m]."""
    return 1.0 - np.asarray(A, dtype=np.float32) @ np.asarray(B, dtype=np.float32).T
