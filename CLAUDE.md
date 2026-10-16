# CLAUDE.md — AI-to-AI loop experiment

Read `SPEC.md` before doing anything. It defines the arms, parameters, gates and measurements. Reference papers are the PDFs in this folder.

## Current scope
Phase 1 only: A0-pilot, then A0-core (SPEC §4). Then A0-S (SPEC §5) once A0-core passes. Do not build or run arms A–E until Brad says so.

## Hard rules
1. **Fidelity first.** Reuse Hintze's OSF code and his 100 seed prompts (https://doi.org/10.17605/OSF.IO/WGDQ4). Do not reimplement what the OSF code already does. Use the caption instruction verbatim. Any departure from Hintze (versions, scheduler, quantization, image format) goes in `DEVIATIONS.md` with the reason.
2. **Gates.** Stop at each gate in SPEC §3 and §4.2 and report the results to Brad; don't start the next stage. A0-core must meet all three pass criteria in §4.3.
3. **Predictions before results.** Before running any arm, make sure its prediction is written in `predictions.md`. Never edit a prediction after seeing results.
4. **Never grade with what steers.** CLIP is for steering only. Evaluation uses MiniLM and DINOv2 (SPEC §7).
5. **Pin everything.** Model IDs, Ollama tags, package versions. Log them in every step record and in the run manifest.
6. **Data is append-only.** Never overwrite or delete anything in `runs/`. A rerun goes in a new run directory.

## Hardware: RTX 5070 laptop, 8 GB VRAM, Windows 11
- Work inside WSL2 (Ubuntu). PyTorch ≥ 2.7 with CUDA 12.8 (Blackwell).
- Two-pass lockstep mode is mandatory with llava:13b. Never load SDXL and LLaVA at the same time. Free VRAM between passes (`del pipe`, `torch.cuda.empty_cache()`, Ollama `keep_alive: 0`).
- Stay under ~7 GB of VRAM. Don't rely on Windows' fallback to system memory: keep the CUDA Sysmem Fallback Policy at "Prefer No Sysmem Fallback," so out-of-memory fails loudly instead of thrashing.
- This machine has hard-rebooted under GPU load before. Every run must survive a power cut: atomic writes, idempotent resume, the GPU health log running (SPEC §8). Test resume by killing the process during the pilot.
- Long runs go in the background (tmux or nohup inside WSL), with progress written to `logs/`. Check in on the run rather than watching it.

## Claude API (A0-S, judge arms)
- Use `ANTHROPIC_API_KEY` from the Console org linked to Brad's Max plan (monthly API credits). Never put the key in code or commit it; read it from the environment or a git-ignored `.env`.
- Use concurrent standard Messages calls (one per trajectory per step). Retry with backoff on 429 and 5xx errors. Log every refusal and empty response.

## Layout
```
SPEC.md  CLAUDE.md  DEVIATIONS.md  predictions.md
hintze_osf/          # untouched copy of the OSF code
src/                 # pipeline (runner, generators, captioners, selectors, embeddings)
configs/             # one YAML per arm/stage
runs/<arm>/<traj>/   # step_NNN.jpg + step_NNN.json
archive/             # attractor centroids
analysis/            # scripts that rebuild every figure from runs/
logs/                # run logs, gpu.csv
reports/             # gate reports for Brad (markdown + figures)
```

## Reporting
At each gate, write `reports/<stage>.md` with:
- the metrics against the pass criteria;
- the drift curves;
- cluster contact sheets;
- measured throughput (s/step);
- any deviations, and the crash/resume log.

Keep it short and lead with pass/fail.
