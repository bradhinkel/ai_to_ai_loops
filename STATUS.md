# Project status — 2026-10-16 (session 2)

## Decisions made by Brad (2026-10-16)
1. **OSF down (503, maintenance).** Wait. First step once it is back: clone Hintze's OSF code (WGDQ4) into `hintze_osf/` untouched, then build `src/` around it. Do not reimplement from the paper.
2. **Layout.** SPEC.md, CLAUDE.md, DEVIATIONS.md, predictions.md, PANEL.md now live at the project root. Papers and the experiment docx stay in `Resources/` (git-ignored).
3. **Git.** Local repo on `main`, private remote: https://github.com/bradhinkel/ai_to_ai_loops. `runs/`, `logs/`, `data/`, `.env`, `.venv/` are ignored.
4. **A0 prediction** recorded in `predictions.md` (Brad's wording plus a quantified version tied to the §4.3 gate).
5. **Comparison baseline.** DONE. Hintze's T=0.9 data is downloaded and extracted in `data/hintze_figshare/`; the documentation subset and contact sheets are in `reports/hintze_reference/` (see `reports/hintze_reference.md` for the data structure and caveats). Delete the zip after A0.
6. **Web UI.** Localhost FastAPI over `runs/` and `logs/`, with run controls: start, pause, resume, stop, restart. See design below.

## Environment (checked 2026-10-16)
- WSL2 now sees 24 GB RAM (`.wslconfig` memory=24GB applied). 24 cores. RTX 5070 Laptop, 8151 MiB VRAM, driver 577.05.
- Ollama installed and serving (`systemctl` active). `llava:13b` pulled: digest 0d0eb4d7f485, 8.0 GB, Q4_0, context 4096 (verify tag/quantization against the OSF code; log in DEVIATIONS.md if different).
- LLaVA smoke test (2026-10-16, synthetic 256x256 image, verbatim instruction, T=0.9, keep_alive 0): 21.8 s total, 5.7 s load, 92 tokens in 14.2 s (~6.5 tok/s); unloaded cleanly, VRAM back to ~1 GB. The caption was 68 words despite the 50-word instruction, so the truncation path matters from step 1.
- Python 3.11.15 via `uv`; `.venv` with PyTorch cu128 + diffusers stack installing (see `logs/venv_setup.log`). Versions will be pinned into `requirements.txt` after reconciling with Hintze's `requirements` from OSF; any upgrade forced by Blackwell goes in `DEVIATIONS.md`.
- SDXL base 1.0 fp16 downloaded to the HF cache (`~/.cache/huggingface`, ~7 GB). Default diffusers scheduler for it is EulerDiscreteScheduler (verify against OSF code).
- SDXL VRAM test, 512x512, 50 steps, CFG 7.5 (2026-10-16, `logs/sdxl_vram_check.log`):
  - everything on GPU: peak 8.24 GB allocated / 9.47 GB reserved, i.e. it spilled into system RAM (first image 16 s, second 45 s). This also shows the NVIDIA "Prefer No Sysmem Fallback" policy is NOT yet set, otherwise it would have OOM'd.
  - `enable_model_cpu_offload()`: peak 5.35 GB, 14 / 12.6 / 10.1 s per image (warming up). Use this mode.
  - text encoders on CPU, UNet+VAE on GPU: peak 6.60 GB / 7.71 GB reserved, 9.6 / 8.3 / 6.9 s. Too close to the limit once LLaVA's leftovers or a bigger batch appear; keep as an option.
- Throughput implication: ~10 s per image (SDXL) + ~20 s per caption (LLaVA, ~90-word captions at 6.5 tok/s) is ~30 s per trajectory-step. A0-pilot (2,000 steps) ~17 h and A0-core (10,000 steps) ~80 h, about twice SPEC §4.2's estimate. Pilot measurements decide; Ollama `OLLAMA_NUM_PARALLEL` and SDXL batching are the levers.
- Disk: 862 GB free (before the ~20 GB of models and data added today).
- Still to confirm by Brad: NVIDIA Control Panel "CUDA Sysmem Fallback Policy = Prefer No Sysmem Fallback" (cannot be checked from WSL).

## Web UI control design (to build with the runner)
The runner works in lockstep steps, so controls act at step boundaries:
- A control file `runs/<arm>/<run_id>/control.json` holds `{"state": "running"|"paused"|"stopped"}`. The runner reads it at the start of every step (and between the SDXL pass and the LLaVA pass).
- **start**: launch the runner as a background process (nohup) for a config; write the PID to `logs/<run_id>.pid`.
- **pause**: set state=paused; the runner finishes the current pass, frees VRAM (unloads SDXL, Ollama keep_alive 0) and sleeps polling the file. GPU is free for other work.
- **resume**: set state=running.
- **stop**: set state=stopped; runner exits cleanly after the current pass. Fallback: SIGTERM, which the atomic-write + resume design already survives.
- **restart**: stop, then start the same config; the idempotent resume picks up from the last complete step. (Never clears `runs/`: data is append-only.)
- Status page: per-trajectory latest step, s/step, GPU csv tail, last 20 log lines, latest image thumbnails.

## Next steps (in order)
1. Wait for OSF; clone code into `hintze_osf/`; diff Hintze's parameters (scheduler, llava tag, requirements) against SPEC §4.1; fill `DEVIATIONS.md`.
2. DONE: `.venv` CUDA works; SDXL fits with `enable_model_cpu_offload()` (5.35 GB peak).
3. Check in the OSF code whether captions are truncated to 50 words (Hintze's logged captions average 89 words, so probably not) and whether llava:13b is the Q4_0 tag.
4. Build `src/` runner (two-pass lockstep, atomic writes, resume, gpu.csv) + `configs/a0_pilot.yaml` + web UI.
5. 1 trajectory x 5 steps throughput test; kill/resume test; then the 20-trajectory pilot.
