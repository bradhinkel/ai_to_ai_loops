"""SDXL base 1.0 generator, matching OSFcontinue.py: fp16, default 1024x1024, 25 steps, default guidance and scheduler,
no negative prompt (force_zeros_for_empty_prompt gives zero negative embeds), then LANCZOS resize to 512.

The OSF code goes through pipe.encode_prompt() and passes prompt_embeds; passing the prompt string yields the same
embeddings and the same CLIP 77-token truncation (DEVIATIONS.md). Seeds are fixed per (trajectory, step) (D3).
"""
import gc, os, pathlib, time
from PIL import Image


def hf_snapshot_revision(model_id):
    p = pathlib.Path.home() / ".cache/huggingface/hub" / ("models--" + model_id.replace("/", "--")) / "refs/main"
    return p.read_text().strip() if p.exists() else None


class SDXLGenerator:
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
        from diffusers import StableDiffusionXLPipeline
        diffusers.utils.logging.set_verbosity_error()      # the per-call CLIP truncation warning; we record it ourselves
        dtype = getattr(torch, self.cfg["dtype"])
        pipe = StableDiffusionXLPipeline.from_pretrained(self.cfg["model"], torch_dtype=dtype, variant=self.cfg.get("variant"))
        pipe.set_progress_bar_config(disable=True)
        if self.cfg.get("cpu_offload"):
            pipe.enable_model_cpu_offload()
        else:
            pipe.to("cuda")
        self.pipe = pipe
        self._info = {
            "model": self.cfg["model"], "revision": hf_snapshot_revision(self.cfg["model"]), "variant": self.cfg.get("variant"),
            "dtype": self.cfg["dtype"], "scheduler": type(pipe.scheduler).__name__,
            "num_inference_steps": self.cfg["num_inference_steps"],
            "guidance_scale": self.cfg["guidance_scale"] if self.cfg["guidance_scale"] is not None else 5.0,
            "height": self.cfg["height"] or pipe.default_sample_size * pipe.vae_scale_factor,
            "width": self.cfg["width"] or pipe.default_sample_size * pipe.vae_scale_factor,
            "resized_to": self.cfg["resize_to"], "negative_prompt": None, "cpu_offload": bool(self.cfg.get("cpu_offload")),
            "alloc_conf": os.environ.get("PYTORCH_CUDA_ALLOC_CONF"),
            "diffusers": diffusers.__version__, "torch": torch.__version__,
        }

    def info(self):
        self.load()
        return dict(self._info)

    def prompt_tokens(self, prompt):
        ids = self.pipe.tokenizer(prompt, truncation=False)["input_ids"]
        return len(ids), len(ids) > self.pipe.tokenizer.model_max_length

    def generate(self, prompt: str, seed: int):
        import torch
        self.load()
        kw = {"num_inference_steps": self.cfg["num_inference_steps"]}
        if self.cfg["guidance_scale"] is not None: kw["guidance_scale"] = self.cfg["guidance_scale"]
        if self.cfg["height"]: kw["height"] = self.cfg["height"]
        if self.cfg["width"]: kw["width"] = self.cfg["width"]
        torch.cuda.reset_peak_memory_stats()
        t0 = time.time()
        g = torch.Generator("cuda").manual_seed(int(seed))
        image = self.pipe(prompt=prompt, generator=g, **kw).images[0]
        r = self.cfg["resize_to"]
        if r:
            image = image.resize((r, r), Image.LANCZOS)
        n_tok, truncated = self.prompt_tokens(prompt)
        return image, {"gen_time_s": round(time.time() - t0, 2), "gen_peak_alloc_gb": round(torch.cuda.max_memory_allocated() / 1e9, 3),
                       "gen_peak_reserved_gb": round(torch.cuda.max_memory_reserved() / 1e9, 3),
                       "prompt_tokens_clip": n_tok, "prompt_truncated_by_clip": truncated}

    def release(self):
        """Give the GPU back between passes. offload: weights stay in CPU RAM; delete: drop the pipeline entirely."""
        import torch
        if self.pipe is None:
            return
        if self.cfg.get("release_mode", "offload") == "offload" and self.cfg.get("cpu_offload"):
            self.pipe.maybe_free_model_hooks()
        else:
            self.pipe = None
        gc.collect(); torch.cuda.empty_cache()
        return round(torch.cuda.memory_allocated() / 1e9, 3)
