"""Config loading: YAML over defaults, plus a hash of the file for the manifest."""
import copy, hashlib, pathlib, yaml

DEFAULTS = {
    "run_name": None,
    "arm": "A0",
    "mode": "two_pass",             # two_pass (8 GB: alternate SDXL and LLaVA) | single_pass (both resident)
    "steps": 100,                   # images per trajectory; image k is made from prompt k, caption of image k is prompt k+1
    "trajectories": {"first": 0, "count": 20},   # reservoir indices first .. first+count-1; count null = every seed in the file
    "temperature": 0.9,             # Ollama sampling temperature (SDXL has none)
    "seeds": {
        "file": "hintze_osf/Generation Scripts For HPCC/reservoir_100.pkl",   # .pkl = Hintze's reservoir; .json = template seed table with reps (E6, D18)
        "sdxl_base_seed": 20261017,  # sdxl_seed = base + traj*10000 + step  (D3)
    },
    "prompt_clip": {"enabled": False, "max_tokens": 77, "tokenizer": "sdxl"},   # tokenizer: sdxl (reference, D13) | generator (E2, D15)   # E1: clip every prompt to CLIP-77 before any generator (SPEC2 §4, D13); A0 relies on SDXL's own cut
    "generator": {
        "backend": "sdxl",          # sdxl | hunyuan (src/generators/hunyuan.py)
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "variant": "fp16",
        "dtype": "float16",
        "num_inference_steps": 25,
        "guidance_scale": None,     # None = diffusers default (5.0), as in the OSF code
        "height": None,             # None = model default 1024
        "width": None,
        "resize_to": 512,           # LANCZOS, as in the OSF code
        "cpu_offload": True,        # D6
        "alloc_conf": "expandable_segments:True",   # D1
        "release_mode": "offload",  # offload: keep weights in CPU RAM between passes | delete: free the pipeline
        "batch": 1,                 # prompts per SDXL call; one generator per prompt keeps the per-(traj, step) seeds (D11)
    },
    "captioner": {
        "backend": "ollama",
        "model": "llava:latest",
        "digest_prefix": "8dd30f6b0cb1",   # the run refuses to start if the Ollama tag resolves to a different digest (D2)
        "host": "http://127.0.0.1:11434",
        "instruction": ("Describe this image in vivid, artistic terms. The description must be 50 words or fewer. "
                        "Do not exceed the limit. Return only the description. Do not explain."),
        "keep_alive_during_pass": "10m",
        "unload_after_pass": True,
        "timeout_s": 600,
        "retries": 5,
        "parallel": 1,              # concurrent caption requests; pair with OLLAMA_NUM_PARALLEL on the server (D11)
    },
    # Part 2 (SPEC2 §5, D17): K captions per step, all rendered, one chosen. mode none (K = 1, Part 1) | random (arm A) | reject (B-img)
    "candidates": {"k": 1},
    "selection": {"mode": "none", "device": "cuda", "radius_archive": 0.20, "window": 5, "burn_in": 5, "radius_reject": 0.20, "resample": 2, "seed": 0},
    "gpu_log": {"interval_s": 10, "path": "logs/gpu.csv"},
    "vram_free_threshold_mb": 1500,   # consider the GPU "free" for the next pass below this nvidia-smi usage
}


def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else copy.deepcopy(v)
    return out


def load_config(path):
    path = pathlib.Path(path)
    raw = path.read_bytes()
    cfg = deep_merge(DEFAULTS, yaml.safe_load(raw) or {})
    if not cfg.get("run_name"):
        cfg["run_name"] = path.stem
    cfg["_config_path"] = str(path)
    cfg["_config_sha256"] = hashlib.sha256(raw).hexdigest()
    return cfg
