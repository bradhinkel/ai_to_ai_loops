# Project status — 2026-10-17 (session 3)

## Decisions made by Brad (2026-10-16)
1. **OSF.** Back up 2026-10-17. The whole project (14 files, 1.5 MB) is in `hintze_osf/` with `MANIFEST.tsv` (sha256 per file), fetched by `scripts/fetch_hintze_osf.py`. Parameters verified against `OSFcontinue.py`; corrections are in SPEC §4.1 and `DEVIATIONS.md`. Headline differences from the first draft: 1024px then resized to 512, 25 steps, CFG 5.0, PNG, captioner is `llava:latest` (7B) not 13B, and no caption truncation.
2. **Layout.** SPEC.md, CLAUDE.md, DEVIATIONS.md, predictions.md, PANEL.md now live at the project root. Papers and the experiment docx stay in `Resources/` (git-ignored).
3. **Git.** Local repo on `main`, private remote: https://github.com/bradhinkel/ai_to_ai_loops. `runs/`, `logs/`, `data/`, `.env`, `.venv/` are ignored.
4. **A0 prediction** recorded in `predictions.md` (Brad's wording plus a quantified version tied to the §4.3 gate).
7. **Truncation (Brad, 2026-10-17).** A0 mimics Hintze: no 50-word truncation. A0-trunc (explicit 50-word cut) and A0-long (full caption past CLIP's 77 tokens) are optional ablations, each needing its own prediction first.
5. **Comparison baseline.** DONE. Hintze's T=0.9 data is downloaded and extracted in `data/hintze_figshare/`; the documentation subset and contact sheets are in `reports/hintze_reference/` (see `reports/hintze_reference.md` for the data structure and caveats). Delete the zip after A0.
6. **Web UI.** Localhost FastAPI over `runs/` and `logs/`, with run controls: start, pause, resume, stop, restart. See design below.

## Environment (checked 2026-10-16)
- WSL2 now sees 24 GB RAM (`.wslconfig` memory=24GB applied). 24 cores. RTX 5070 Laptop, 8151 MiB VRAM, driver 577.05.
- Ollama installed and serving (`systemctl` active). `llava:latest` pulled: digest 8dd30f6b0cb1, 7B, Q4_0, 4.7 GB (this is what Hintze's sweep used). Also `llava:13b` pulled: digest 0d0eb4d7f485, 8.0 GB, Q4_0, context 4096 (verify tag/quantization against the OSF code; log in DEVIATIONS.md if different).
- LLaVA smoke test (2026-10-16, synthetic 256x256 image, verbatim instruction, T=0.9, keep_alive 0): 21.8 s total, 5.7 s load, 92 tokens in 14.2 s (~6.5 tok/s); unloaded cleanly, VRAM back to ~1 GB. The caption was 68 words despite the 50-word instruction, so the truncation path matters from step 1.
- Python 3.11.15 via `uv`; `.venv` with PyTorch cu128 + diffusers stack installing (see `logs/venv_setup.log`). Versions will be pinned into `requirements.txt` after reconciling with Hintze's `requirements` from OSF; any upgrade forced by Blackwell goes in `DEVIATIONS.md`.
- SDXL base 1.0 fp16 downloaded to the HF cache (`~/.cache/huggingface`, ~7 GB). Default diffusers scheduler for it is EulerDiscreteScheduler (verify against OSF code).
- SDXL VRAM test, 512x512, 50 steps, CFG 7.5 (2026-10-16, `logs/sdxl_vram_check.log`):
  - everything on GPU: peak 8.24 GB allocated / 9.47 GB reserved, i.e. it spilled into system RAM (first image 16 s, second 45 s). This also shows the NVIDIA "Prefer No Sysmem Fallback" policy is NOT yet set, otherwise it would have OOM'd.
  - `enable_model_cpu_offload()`: peak 5.35 GB, 14 / 12.6 / 10.1 s per image (warming up). Use this mode.
  - text encoders on CPU, UNet+VAE on GPU: peak 6.60 GB / 7.71 GB reserved, 9.6 / 8.3 / 6.9 s. Too close to the limit once LLaVA's leftovers or a bigger batch appear; keep as an option.
- SDXL at Hintze's real settings (1024x1024, 25 steps, CFG 5.0, offload): 7.15 GB allocated but 9.5 to 10 GB reserved and 30 to 98 s per image (spilling). With `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`: 7.03 GB / 7.18 GB reserved, 20 to 23 s per image. VAE tiling and attention slicing: no effect. Still to test after the WSL restart: expandable segments without VAE tiling (expected to be the same), and whether "Prefer No Sysmem Fallback" now raises OOM instead of spilling.
- Throughput implication (revised for 1024px and the 7B captioner): ~10 s per image (SDXL) + ~20 s per caption (LLaVA, ~90-word captions at 6.5 tok/s) is ~30 s per trajectory-step. A0-pilot (2,000 steps) ~17 h and A0-core (10,000 steps) ~80 h, about twice SPEC §4.2's estimate. Pilot measurements decide; Ollama `OLLAMA_NUM_PARALLEL` and SDXL batching are the levers.
- Disk: 862 GB free (before the ~20 GB of models and data added today).
- Brad set "Prefer No Sysmem Fallback" on 2026-10-17 but fresh WSL processes still spilled; NVIDIA says the CUDA application must restart, and on WSL that means `wsl --shutdown` (and the setting must be under Global Settings). Retest after the restart.

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
1. DONE: OSF code fetched, parameters verified, DEVIATIONS.md written.
2. DONE: `.venv` CUDA works; SDXL fits with `enable_model_cpu_offload()` (5.35 GB peak).
3. DONE: no truncation in the code; captioner is `llava:latest` (7B Q4_0), not 13B.
4. Build `src/` runner (two-pass lockstep, atomic writes, resume, gpu.csv) + `configs/a0_pilot.yaml` + web UI.
5. 1 trajectory x 5 steps throughput test; kill/resume test; then the 20-trajectory pilot.
