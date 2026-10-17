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
- **D1 Resolution: none.** 1024x1024 at 25 steps fits on 8 GB with `enable_model_cpu_offload()` plus `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`: 7.03 GB peak allocated, 7.18 GB reserved, 20 to 23 s per image once warm (measured 2026-10-17, `logs/sdxl_vram_check.log`). Without the allocator setting the same run reserved 10 GB and spilled into system RAM. VAE tiling and attention slicing changed nothing, so they are off. We generate at Hintze's resolution and resize to 512 as he did.
- **D2 Captioner tag.** `llava:latest` is a moving tag. We pin the digest Ollama resolved on 2026-10-17, `8dd30f6b0cb1` (LLaVA 1.6, 7B, Q4_0, 4.7 GB), and log it per step. Hintze's runs (2025) most likely used the same LLaVA 1.6 7B Q4_0 build, but the OSF project does not record the digest.
- **D3 Determinism.** SDXL seeds are fixed per (trajectory, step) and logged. Hintze's were random. Same distribution, reproducible draws.
- **D4 Two-pass lockstep.** Hintze ran one trajectory per V100 job with SDXL and Ollama both resident. We alternate SDXL and LLaVA on the GPU and run all trajectories in lockstep. No change to the per-step computation.
- **D5 Package versions.** Hintze's are unrecorded. Ours: torch 2.11.0+cu128, diffusers 0.41.0, transformers 5.20.1 (pinned in `requirements.txt` once the runner exists). Blackwell requires CUDA 12.8 builds.
- **D6 Model CPU offload.** `enable_model_cpu_offload()` and the expandable-segments allocator to fit 8 GB. Same weights and math; only placement differs.
- **D7 Atomic per-step records.** We write `step_NNN.png` + `step_NNN.json` per step; Hintze rewrote one CSV per run after every step. Content is a superset of his log.

## Planned variants (not A0)
- **A0-trunc (was "P0a").** Hard-truncate each caption to 50 words before it is used as the next prompt. Tests whether an explicit word limit changes the attractors. Needs its own prediction before it runs.
- **A0-long.** Encode captions beyond 77 tokens by chunking (e.g. compel-style concatenation) so the full caption reaches SDXL. Tests whether a wider channel slows or changes convergence. A generator-side change, so it is a different arm, not a replication.
