# Deviations from Hintze et al. (OSF WGDQ4)

Reference implementation: `hintze_osf/Generation Scripts For HPCC/OSFcontinue.py` (the temperature sweep; `OSFtest.py` is the same loop without resume, `OSFmulti.py` is the 4x4 generator/captioner swap). Verified 2026-10-17. Nothing in the OSF project pins package versions; the SLURM scripts show CUDA 12.4 on a V100 with a conda env.

## What Hintze's code actually does (facts that correct SPEC §4.1 as first written)
| Parameter | SPEC §4.1 said | OSF code does | A0 will do |
|---|---|---|---|
| Resolution | 512x512 | SDXL default 1024x1024, then `resize((512,512), LANCZOS)` | Same as code (see D1 if infeasible) |
| Inference steps | 50 | `num_inference_steps=25` | 25 |
| Guidance scale | 7.5 | not set, diffusers default 5.0 | 5.0 |
| Scheduler | verify | not set, model default EulerDiscreteScheduler | EulerDiscreteScheduler |
| Captioner | llava:13b | `model="llava"` / `"llava:latest"` (7B); `llava:13b-v1.6` only appears in the 4x4 swap | `llava:latest`, digest logged (D2) |
| Caption truncation | implied 50 words | none: `response["response"].strip()` is used verbatim | none (Brad, 2026-10-17) |
| Image format | JPEG | PNG, `optimize=True` | PNG |
| Temperature | 0.9 | Ollama `options={"temperature": temp}`; SDXL has no temperature | 0.9 |
| Negative prompt | n/a | none; SDXL config `force_zeros_for_empty_prompt` gives zero negative embeds | same |
| SDXL seed | fixed per step | not set (random every step) | fixed and logged (D3) |

Prompt-encoding quirk in the code: it calls `pipe.encode_prompt(prompt)` and passes `prompt_embeds` and `pooled_prompt_embeds`, plus `prompt_embeds_2`/`pooled_prompt_embeds_2` from an empty prompt. `StableDiffusionXLPipeline.__call__` has no such parameters; they land in `**kwargs` and are ignored (checked on diffusers 0.41.0). Net effect is an ordinary SDXL call with the prompt and no negative prompt. `encode_prompt` tokenizes with CLIP's 77-token limit, so every caption longer than ~75 tokens is cut there: 85% of Hintze's T=0.9 captions are (median 107 tokens), and on average the first 69 words reach the generator. This is the only truncation in Hintze's loop.

## Deviations
- **D1 Resolution: none.** 1024x1024 at 25 steps fits on 8 GB with `enable_model_cpu_offload()` plus `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. After the WSL restart of 2026-10-17 the figures are 5.49 GB peak allocated, 5.63 GB reserved, 15 to 18 s per image warm (`logs/sysmem_policy_retest.log`, confirmed in the smoke run); the earlier 7.0 GB / 10 GB-reserved numbers in `logs/sdxl_vram_check.log` came from a session that had already spilled. Without the allocator setting the retest reserved 7.85 GB and did not spill, so the sysmem-fallback policy was never exercised; we keep the allocator setting regardless. VAE tiling and attention slicing changed nothing, so they are off. We generate at Hintze's resolution and resize to 512 as he did.
- **D2 Captioner tag.** `llava:latest` is a moving tag. We pin the digest Ollama resolved on 2026-10-17, `8dd30f6b0cb1` (LLaVA 1.6, 7B, Q4_0, 4.7 GB), and log it per step. Hintze's runs (2025) most likely used the same LLaVA 1.6 7B Q4_0 build, but the OSF project does not record the digest.
- **D3 Determinism.** SDXL seeds are fixed per (trajectory, step) and logged. Hintze's were random. Same distribution, reproducible draws.
- **D4 Two-pass lockstep.** Hintze ran one trajectory per V100 job with SDXL and Ollama both resident. We alternate SDXL and LLaVA on the GPU and run all trajectories in lockstep. No change to the per-step computation.
- **D5 Package versions.** Hintze's are unrecorded. Ours: torch 2.11.0+cu128, diffusers 0.41.0, transformers 5.20.1 (pinned in `requirements.txt` once the runner exists). Blackwell requires CUDA 12.8 builds.
- **D6 Model CPU offload.** `enable_model_cpu_offload()` and the expandable-segments allocator to fit 8 GB. Same weights and math; only placement differs.
- **D7 Atomic per-step records.** We write `step_NNN.png` + `step_NNN.json` per step; Hintze rewrote one CSV per run after every step. Content is a superset of his log.

- **D8 Prompt path.** The runner calls `pipe(prompt=...)` instead of the OSF `encode_prompt` + `prompt_embeds` route. Same CLIP encoders, same 77-token truncation, same zero negative embeds (see the quirk note above); the extra `*_2` kwargs the OSF code passes are ignored by diffusers either way. Each record logs `prompt_tokens_clip` and `prompt_truncated_by_clip`.
- **D9 Ollama context and client.** Ollama 0.40.5 loads `llava:latest` with `n_ctx = 4096` (its default, from `journalctl -u ollama`); a 512x512 image plus the instruction is 620 prompt tokens. Hintze's Ollama version and context size are unrecorded. We send exactly his request (`prompt`, `images`, `options={"temperature": T}`) through the same `ollama` Python client (0.6.3); the only addition is `keep_alive` for the two-pass unload, which does not affect generation.
- **D10 Caption of the last image.** Hintze computed but never logged the caption of image 99 (his CSV row k holds the prompt that made image k). We store both `prompt` and `caption` per step, so our records are a superset; analysis that compares with his CSVs uses the prompt series.

## Planned variants (not A0)
- **A0-trunc (was "P0a").** Hard-truncate each caption to 50 words before it is used as the next prompt. Tests whether an explicit word limit changes the attractors. Needs its own prediction before it runs.
- **A0-long.** Encode captions beyond 77 tokens by chunking (e.g. compel-style concatenation) so the full caption reaches SDXL. Tests whether a wider channel slows or changes convergence. A generator-side change, so it is a different arm, not a replication.
