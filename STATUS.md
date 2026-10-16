# Project status — 2026-10-16 (session 2)

## Decisions made by Brad (2026-10-16)
1. **OSF down (503, maintenance).** Wait. First step once it is back: clone Hintze's OSF code (WGDQ4) into `hintze_osf/` untouched, then build `src/` around it. Do not reimplement from the paper.
2. **Layout.** SPEC.md, CLAUDE.md, DEVIATIONS.md, predictions.md, PANEL.md now live at the project root. Papers and the experiment docx stay in `Resources/` (git-ignored).
3. **Git.** Local repo on `main`, private remote: https://github.com/bradhinkel/ai_to_ai_loops. `runs/`, `logs/`, `data/`, `.env`, `.venv/` are ignored.
4. **A0 prediction** recorded in `predictions.md` (Brad's wording plus a quantified version tied to the §4.3 gate).
5. **Comparison baseline.** Hintze's T=0.9 images (figshare file 59352803, 775 MB) go in `data/hintze_figshare/`. Keep a small documentation subset (a few trajectories at steps 0, 1, 10, 50, 100) in `reports/hintze_reference/`; the full zip can be deleted afterwards.
6. **Web UI.** Localhost FastAPI over `runs/` and `logs/`, with run controls: start, pause, resume, stop, restart. See design below.

## Environment (checked 2026-10-16)
- WSL2 now sees 24 GB RAM (`.wslconfig` memory=24GB applied). 24 cores. RTX 5070 Laptop, 8151 MiB VRAM, driver 577.05.
- Ollama installed and serving (`systemctl` active). `llava:13b` pulled: digest 0d0eb4d7f485, 8.0 GB, Q4_0, context 4096 (verify tag/quantization against the OSF code; log in DEVIATIONS.md if different).
- LLaVA smoke test (2026-10-16, synthetic 256x256 image, verbatim instruction, T=0.9, keep_alive 0): 21.8 s total, 5.7 s load, 92 tokens in 14.2 s (~6.5 tok/s); unloaded cleanly, VRAM back to ~1 GB. The caption was 68 words despite the 50-word instruction, so the truncation path matters from step 1.
- Python 3.11.15 via `uv`; `.venv` with PyTorch cu128 + diffusers stack installing (see `logs/venv_setup.log`). Versions will be pinned into `requirements.txt` after reconciling with Hintze's `requirements` from OSF; any upgrade forced by Blackwell goes in `DEVIATIONS.md`.
- Disk: 862 GB free.
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
2. Verify `.venv` CUDA works and SDXL base fits at 512x512 under ~7 GB (fp16, attention slicing / VAE tiling if needed).
3. Unzip `temps_0.9.zip`; extract the documentation subset; write `reports/hintze_reference.md`.
4. Build `src/` runner (two-pass lockstep, atomic writes, resume, gpu.csv) + `configs/a0_pilot.yaml` + web UI.
5. 1 trajectory x 5 steps throughput test; kill/resume test; then the 20-trajectory pilot.
