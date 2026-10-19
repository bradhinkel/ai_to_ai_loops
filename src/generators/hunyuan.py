"""Hunyuan-DiT v1.2 generator (Tencent; bilingual CLIP + mT5 text encoders, 1.5B DiT), the NEW generator of SPEC2 E1/E2.

Same interface as SDXLGenerator. The model is run at the pipeline's defaults (1024x1024, guidance 5.0, DDPM scheduler,
no negative prompt) except num_inference_steps, which E1 sets to 25 = A0's SDXL budget (D12 amendment 2026-10-19) and the image is LANCZOS-resized to 512 like Hintze's.
Prompt clipping to CLIP-77 happens in the runner (src/prompt_clip.py), not here; this class only reports how many
tokens each of its two encoders would have read (DEVIATIONS D12).
"""
import gc, os, time
from PIL import Image

from .sdxl import hf_snapshot_revision

MODEL_ID = "Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers"


class HunyuanGenerator:
    MT5_MAX = 256       # HunyuanDiTPipeline.encode_prompt uses max_sequence_length=256 for the mT5 encoder (the tokenizer itself has no limit set)

    def __init__(self, cfg: dict):
        self.cfg = cfg
        if cfg.get("alloc_conf"):
            os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", cfg["alloc_conf"])
        self.pipe = None
        self._info = None

    def load(self):
        if self.pipe is not None:
            return
        import torch, diffusers
        from diffusers import HunyuanDiTPipeline
        diffusers.utils.logging.set_verbosity_error()
        dtype = getattr(torch, self.cfg["dtype"])
        kw = {"torch_dtype": dtype}
        if self.cfg.get("revision"): kw["revision"] = self.cfg["revision"]
        pipe = HunyuanDiTPipeline.from_pretrained(self.cfg["model"], **kw)
        pipe.set_progress_bar_config(disable=True)
        if self.cfg.get("cpu_offload"):
            pipe.enable_model_cpu_offload()
        else:
            pipe.to("cuda")
        if int(self.cfg.get("batch", 1)) > 1:
            pipe.vae.enable_slicing()
        if self.cfg.get("compile"):   # D12 amendment: torch.compile on the DiT only; numerics unchanged, one recompile for the final partial batch
            pipe.transformer = torch.compile(pipe.transformer, mode=self.cfg.get("compile_mode") or "default")
        self.pipe = pipe
        steps = self.cfg["num_inference_steps"] if self.cfg.get("num_inference_steps") is not None else 50
        self._info = {
            "backend": "hunyuan", "model": self.cfg["model"], "revision": self.cfg.get("revision") or hf_snapshot_revision(self.cfg["model"]),
            "dtype": self.cfg["dtype"], "scheduler": type(pipe.scheduler).__name__,
            "num_inference_steps": steps,
            "guidance_scale": self.cfg["guidance_scale"] if self.cfg.get("guidance_scale") is not None else 5.0,
            "height": self.cfg.get("height") or 1024, "width": self.cfg.get("width") or 1024,
            "resized_to": self.cfg["resize_to"], "negative_prompt": None, "cpu_offload": bool(self.cfg.get("cpu_offload")),
            "batch": int(self.cfg.get("batch", 1)), "vae_slicing": int(self.cfg.get("batch", 1)) > 1,
            "compile": bool(self.cfg.get("compile")), "compile_mode": (self.cfg.get("compile_mode") or "default") if self.cfg.get("compile") else None,
            "text_encoders": {"clip": pipe.tokenizer.model_max_length, "mt5": self.MT5_MAX},
            "alloc_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
            "diffusers": diffusers.__version__, "torch": torch.__version__,
        }

    def info(self):
        self.load()
        return dict(self._info)

    def prompt_tokens(self, prompt):
        """Tokens the bilingual CLIP (77) and mT5 (256) encoders would see, and whether CLIP would have cut the prompt."""
        n1 = len(self.pipe.tokenizer(prompt, truncation=False)["input_ids"])
        n2 = len(self.pipe.tokenizer_2(prompt, truncation=False)["input_ids"])
        return n1, n1 > self.pipe.tokenizer.model_max_length, n2, n2 > self.MT5_MAX

    def generate(self, prompt: str, seed: int):
        return self.generate_batch([prompt], [seed])[0]

    def generate_batch(self, prompts, seeds):
        import torch
        self.load()
        kw = {"num_inference_steps": self._info["num_inference_steps"]}
        if self.cfg.get("guidance_scale") is not None: kw["guidance_scale"] = self.cfg["guidance_scale"]
        if self.cfg.get("height"): kw["height"] = self.cfg["height"]
        if self.cfg.get("width"): kw["width"] = self.cfg["width"]
        torch.cuda.reset_peak_memory_stats()
        t0 = time.time()
        gens = [torch.Generator("cuda").manual_seed(int(s)) for s in seeds]
        images = self.pipe(prompt=list(prompts), generator=gens, **kw).images
        dt = time.time() - t0
        r = self.cfg["resize_to"]
        out = []
        for prompt, image in zip(prompts, images):
            if r:
                image = image.resize((r, r), Image.LANCZOS)
            n1, tr1, n2, tr2 = self.prompt_tokens(prompt)
            out.append((image, {"gen_time_s": round(dt / len(prompts), 2), "gen_batch_size": len(prompts), "gen_batch_time_s": round(dt, 2),
                                "gen_peak_alloc_gb": round(torch.cuda.max_memory_allocated() / 1e9, 3),
                                "gen_peak_reserved_gb": round(torch.cuda.max_memory_reserved() / 1e9, 3),
                                "prompt_tokens_clip": n1, "prompt_truncated_by_clip": tr1,
                                "prompt_tokens_mt5": n2, "prompt_truncated_by_mt5": tr2}))
        return out

    def release(self):
        import torch
        if self.pipe is None:
            return
        if self.cfg.get("release_mode", "offload") == "offload" and self.cfg.get("cpu_offload"):
            self.pipe.maybe_free_model_hooks()
        else:
            self.pipe = None
        gc.collect(); torch.cuda.empty_cache()
        return round(torch.cuda.memory_allocated() / 1e9, 3)


def make_generator(cfg: dict):
    """Generator factory keyed on cfg['backend'] (default sdxl)."""
    backend = cfg.get("backend", "sdxl")
    if backend == "sdxl":
        from .sdxl import SDXLGenerator
        return SDXLGenerator(cfg)
    if backend == "hunyuan":
        return HunyuanGenerator(cfg)
    raise ValueError(f"unknown generator backend {backend!r}")
