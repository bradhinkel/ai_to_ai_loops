"""Moondream 2 via Hugging Face transformers (FAST pair, 2026-11-12). Same interface as OllamaCaptioner.

Ollama's `moondream` tag returns junk at T 0.9 (17 of 30 test captions empty or garbage), so the model runs from
vikhyatk/moondream2 at a pinned revision with trust_remote_code (code read 2026-11-12: the only network access is
lora.py, used only when settings carry a non-None `variant`; this class sends variant None, which the code requires as a key). Hintze's rule: the verbatim
instruction, only the temperature set, every other sampling setting at the model's default (top_p 0.3, max_tokens 768).
"""
import gc, time
from PIL import Image
from .ollama_llava import REFUSAL_RE


class MoondreamCaptioner:
    def __init__(self, cfg: dict, temperature: float, logger=None):
        self.cfg = cfg; self.temperature = temperature; self.log = logger
        self.model = None; self._info = None; self._fresh_buffers = None

    def load(self):
        if self.model is not None:
            return
        import torch, transformers
        from transformers.dynamic_module_utils import get_class_from_dynamic_module
        # The 2025-06-21 remote code targets transformers 4.52; under 5.x two shims are needed (2026-11-12):
        # 1. 5.x reads all_tied_weights_keys, which the remote class never sets (it never calls post_init); Moondream ties no weights.
        # 2. 5.x builds the model on the meta device, so the non-persistent buffers computed in __init__ (attn_mask, freqs_cis) come
        #    back as uninitialised memory: NaN logits in fp16/bf16, and bursts of empty captions (15/60) once freqs_cis alone was fixed.
        #    Copy every buffer from one normally constructed CPU instance. With both shims: 0 empty in 60, median 31 words.
        cls = get_class_from_dynamic_module("hf_moondream.HfMoondream", self.cfg["model"], revision=self.cfg["revision"])
        cls.all_tied_weights_keys = {}
        m = cls.from_pretrained(self.cfg["model"], revision=self.cfg["revision"], dtype=getattr(torch, self.cfg.get("dtype", "bfloat16")))
        if self._fresh_buffers is None:
            with torch.device("cpu"):
                fresh = cls(m.config)
            self._fresh_buffers = {k: v.clone() for k, v in fresh.named_buffers()}
            del fresh; gc.collect()
        for name, _ in list(m.named_buffers()):
            mod_name, buf = name.rsplit(".", 1)
            m.get_submodule(mod_name)._buffers[buf] = self._fresh_buffers[name].clone()
        self.model = m.to("cuda")
        self._tf = transformers.__version__

    def info(self):
        if self._info is None:
            from huggingface_hub import HfApi
            sha = HfApi().model_info(self.cfg["model"], revision=self.cfg["revision"]).sha
            self._info = {"backend": "hf_moondream", "model": self.cfg["model"], "revision": self.cfg["revision"], "commit": sha,
                          "dtype": self.cfg.get("dtype", "bfloat16"), "temperature": self.temperature, "instruction": self.cfg["instruction"],
                          "settings_sent": {"temperature": self.temperature, "variant": None},
                          "shims": "transformers-5 compat: all_tied_weights_keys={}, non-persistent buffers rebuilt"}
        return dict(self._info)

    def caption(self, image_path, keep_alive=None):
        import torch
        self.load()
        t0 = time.time()
        with torch.inference_mode():
            text = self.model.query(Image.open(image_path).convert("RGB"), self.cfg["instruction"],
                                    settings={"temperature": self.temperature, "variant": None})["answer"].strip()
        words = len(text.split())
        meta = {"caption_time_s": round(time.time() - t0, 2), "caption_words": words, "caption_chars": len("".join(text.split())),
                "caption_flags": {"empty": words == 0, "over_50_words": words > 50, "refusal": bool(REFUSAL_RE.search(text)), "length_cutoff": None},
                "caption_attempts": 1, "transformers": self._tf}
        if words == 0 and self.log:
            self.log.warning("empty caption for %s", image_path)
        return text, meta

    def unload(self):
        import torch
        self.model = None
        gc.collect(); torch.cuda.empty_cache()

    def loaded_models(self):
        return [self.cfg["model"]] if self.model is not None else []
