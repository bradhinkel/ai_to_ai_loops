# ai_to_ai_loops

An independent replication and extension of Hintze, Proschinger Åström & Schossau, "Autonomous language-image generation loops converge to generic visual motifs" (*Patterns* 7, 101451; code and seeds at https://doi.org/10.17605/OSF.IO/WGDQ4).

A caption → image → caption loop (SDXL + LLaVA 7B in the reference setting) is run from Hintze's 100 seed prompts, then the same loop is varied one factor at a time: captioner, generator, caption instruction, prompt language, a selection rule, and seeded demographic attributes. The question behind the project is whether such loops can be kept out of their attractors (Phase 2, not started). This is a hobby project by one person with Claude as the engineering and analysis collaborator; it is offered as a working draft for review, not as finished research.

**Status (2026-10-25): Phase 1 complete, project paused.** Twelve runs, about 94,000 trajectory-steps, all reported in `reports/`. Two working-draft write-ups ("Gravity in AI-to-AI loops" and "Bias in AI-to-AI loops") are being circulated for comment; ask Brad for a copy. `STATUS.md` ("Where things stand") is the entry point for picking the work up again.

## What was found (short version; every number is in `reports/`)
- **Replication.** The SDXL + LLaVA loop converges to Hintze's motifs (palatial salons, cathedral naves, canopy bedrooms, Victorian houses) with the same knee and plateau as his T = 0.9 data; a second replication with a different base seed gives the run-to-run noise floor (`reports/a0_core.md`, `reports/a0_core2.md`).
- **Gravity.** Attractors are temporary stops, not endpoints: every basin has a measurable escape hazard (0.03–0.20 per step), trajectories re-enter and leave repeatedly, and the hazard falls with depth into the basin. Memory of the seed has a half-life of 3–6 steps in every run (`reports/gravity_*.md`, `reports/memory_curve.md`, `reports/persistent_atlas*.md`).
- **Who owns the landscape.** In a 2×2 swap of captioner (LLaVA / Qwen2.5-VL) and generator (SDXL / Hunyuan-DiT), the generator sets the image-space attractors and the captioner sets the caption-space attractors; basin depth does not transfer across pairs (`reports/e1.md`).
- **Instruction and language.** A "realistic photograph" instruction halves the salon basin and leaves the cathedral alone (`reports/a0_photo.md`); a Chinese caption instruction keeps the convergence statistics but moves the content: faces turn East Asian within the first steps and latent pagoda / moon-bridge / misty-lake modes become basins (`reports/e2_qz.md`; the translated instruction still needs a professional review).
- **A failed intervention.** Rejecting images near an archive of visited attractors raises escape hazards 2–3× but does not stop convergence: candidates differ by less than the basin scale (`reports/bimg.md`).
- **Bias.** Seeded gender, age and skin tone are lost within a few steps and replaced by the loop's own default (a light-skinned man, then crowds and face collages), not by the occupation's one-shot prior; dark skin tone goes first (facial L* 25 → 50 at step 1). Nurses are relabelled "doctor" according to the rendered gender; pilots become military or astronauts (`reports/e6.md`, `reports/e6/occupations.md`).

## Layout
```
SPEC.md SPEC2.md     design: arms, parameters, gates, measurements (SPEC2 §11 = future work)
CLAUDE.md            working rules for the Claude collaborator
predictions.md       predictions written before each run, never edited afterwards
DEVIATIONS.md        every departure from Hintze's code and settings (D1–D18)
STATUS.md            dated log of every session; "Where things stand" at the top
PANEL.md             provisional plan for a human rating panel (Phase 2)
src/                 runner (two-pass lockstep, atomic writes, idempotent resume), generators, captioners, embedders, candidate selection
configs/             one YAML per run (laptop and RunPod variants)
seeds/               E6 seed tables (occupation × gender × age × skin tone)
scripts/             OSF fetch, RunPod setup/launch/queue/sync
analysis/            every figure and table is rebuilt from runs/ by these scripts
archive/             attractor centroids and names
reports/             gate reports (markdown + figures), one per run, plus cross-run atlases
hintze_osf/          Hintze's OSF project, fetched locally (only our MANIFEST.tsv of checksums is tracked)
runs/ logs/ data/    experiment data, git-ignored (see below)
```

## Reproducing
1. Python 3.11, `uv venv .venv && uv pip install -r requirements.txt` (pinned; PyTorch 2.11 cu128, diffusers 0.41, transformers 5.20). Ollama with `llava:latest` (digest 8dd30f6b0cb1) for the reference captioner.
2. `python scripts/fetch_hintze_osf.py` downloads Hintze's code and seed reservoir into `hintze_osf/` and checks every file against `hintze_osf/MANIFEST.tsv`. The runner reads the seeds from there.
3. `.venv/bin/python -m src.runner configs/<run>.yaml` runs a config; `scripts/runpod_*.sh` do the same on a RunPod pod. Claude captioner and judge runs need `ANTHROPIC_API_KEY` in a git-ignored `.env`.
4. `analysis/*.py` rebuild the reports from `runs/`; each script's docstring gives its command line.

## Data
`runs/` (about 114,000 images with their captions and step records, 42 GB) is not in git. It is held on the author's machine and on a RunPod network volume, and can be shared on request; archiving it with a DOI is planned. The judge outputs for E6 (`analysis/cache/e6_*/`) and the per-step rows behind every E6 table (`reports/e6/*.json`) are tracked so the bias results can be re-derived without the images.

## Working rules
Fidelity to Hintze's code first, with every departure logged. Predictions before results, never edited. Nothing that steers (CLIP, SigLIP) is used to grade; evaluation uses DINOv2 and MiniLM. Everything pinned. `runs/` is append-only. Each run stops at a gate and is reported before the next starts.

## Acknowledgement
The experiments were designed and judged by Brad Hinkel. Claude (Fable 5.1, with Sonnet 5.5 and Haiku 5.5 as captioner and judges) wrote the runner and analysis code, ran the pod, drafted the reports and the white papers, and made quantified predictions alongside Brad's; the project notes record who contributed what and how often each side's predictions held. Brad takes responsibility for the claims.

## Licence
Code and text in this repository: MIT (see `LICENSE`). Hintze et al.'s OSF materials are not redistributed here; fetch them from OSF with the script above. Model weights (SDXL, LLaVA, Qwen2.5-VL, Hunyuan-DiT, DINOv2, MiniLM, SigLIP, CLIP) carry their own licences.
