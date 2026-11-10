# ai_to_ai_loops

An independent replication and extension of Hintze, Proschinger Åström & Schossau, "Autonomous language-image generation loops converge to generic visual motifs" (*Patterns* 7, 101451; code and seeds at https://doi.org/10.17605/OSF.IO/WGDQ4).

A caption → image → caption loop (SDXL + LLaVA 7B in the reference setting) is run from Hintze's 100 seed prompts, then the same loop is varied one factor at a time: captioner, generator, caption instruction, prompt language, a selection rule, and seeded demographic attributes. The same loop is then run on text alone (story → 50-word summary → story) on Claude and on two 7B models, to see whether language models have attractors of their own. This is a hobby project by one person with Claude as the engineering and analysis collaborator; it is offered as a working draft for review, not as finished research.

**Status (2026-11-10).** Phase 1 (image loops, twelve runs, about 111,000 images) and the text-loop arm (E3, twenty cells, about 72,000 stories) are complete and reported in `reports/`. Nothing is running. Two working-draft write-ups on the image loops ("Gravity in AI-to-AI loops", "Bias in AI-to-AI loops") and one on the text loops ("Text loops: wells, the birthday law and model menus") are in `papers/` and are being circulated for comment; the replication and the gravity write-up were sent to the authors of the original paper on 2026-11-10. An introductory article is in preparation. Next is E5, a test of whether a captioner and generator fine-tuned on one theme (Dungeons & Dragons art) pull the image loop toward that theme (`docs/e5_runbook.md`; the prediction is drafted in `predictions.md`). `STATUS.md` is the dated log of every session.

## What was found (short version; every number is in `reports/`)
- **Replication.** The SDXL + LLaVA loop converges to Hintze's motifs (palatial salons, cathedral naves, canopy bedrooms, Victorian houses) with the same knee and plateau as his T = 0.9 data; a second replication with a different base seed gives the run-to-run noise floor (`reports/a0_core.md`, `reports/a0_core2.md`).
- **Gravity.** Attractors are temporary stops, not endpoints: every basin has a measurable escape hazard (0.03–0.20 per step), trajectories re-enter and leave repeatedly, and the hazard falls with depth into the basin. Memory of the seed has a half-life of 3–6 steps in every run (`reports/gravity_*.md`, `reports/memory_curve.md`, `reports/persistent_atlas*.md`).
- **Who owns the landscape.** In a 2×2 swap of captioner (LLaVA / Qwen2.5-VL) and generator (SDXL / Hunyuan-DiT), the generator sets the image-space attractors and the captioner sets the caption-space attractors; basin depth does not transfer across pairs (`reports/e1.md`).
- **Instruction and language.** A "realistic photograph" instruction halves the salon basin and leaves the cathedral alone (`reports/a0_photo.md`); a Chinese caption instruction keeps the convergence statistics but moves the content: faces turn East Asian within the first steps and latent pagoda / moon-bridge / misty-lake modes become basins (`reports/e2_qz.md`; the translated instruction still needs a professional review).
- **A failed intervention.** Rejecting images near an archive of visited attractors raises escape hazards 2–3× but does not stop convergence: candidates differ by less than the basin scale (`reports/bimg.md`).
- **Bias.** Seeded gender, age and skin tone are lost within a few steps and replaced by the loop's own default (a light-skinned man, then crowds and face collages), not by the occupation's one-shot prior; dark skin tone goes first (facial L* 25 → 50 at step 1). Nurses are relabelled "doctor" according to the rendered gender; pilots become military or astronauts (`reports/e6.md`, `reports/e6/occupations.md`).

## What the text loops showed (`reports/e3*.md`; the write-up has the full argument)
- **Wells, not a cathedral.** A story → 50-word summary → story loop on Claude Haiku has no attractor shared by two trajectories at 20 seeds, and a few dozen shared wells at 100 seeds. The wells are plots as specific as Hintze's cathedral: a shoebox of unopened letters from an estranged relative, a late relative's ledger of debts marked forgiven, an unfinished melody (`reports/e3_scale_width.md`, `reports/e3_s2.md`).
- **The birthday law.** The chance that any two trajectories share a well is constant as the sample grows (about 0.005 per pair for Haiku), so the number of sharing pairs grows with n², and the implied menu is a few hundred wells rather than a dozen. A second 100-seed sample replicates the rate and recurs on 6–7 of 13 wells as plot families.
- **Each model has its own menu.** Mistral 7B and Qwen2.5 7B never enter a Haiku well in 200 tries but do enter each other's: their wells are civic (a stranger revives a decaying town, a neglected place becomes a community hub), Haiku's are domestic. They share more per pair than Haiku through fewer wells, so a single number, wells per sharing pair (W-hat), orders the models: Qwen 39, Mistral 56, Haiku 165–215 (`reports/e3_s7b.md`).
- **Theme bottleneck.** Narrowing the summary to one sentence removes plot memory but leaves a stationary menu of about five morals per model, with strong per-trajectory moral memory; Sonnet shares Haiku's moral menu but spreads wider and flatter over it (`reports/e3_d.md`, `reports/e3_ds.md`).
- **Seeds leave a trace.** Same-seed pairs across two samples share a well 9 times in 100 against 0.5 expected; later cells use fresh seeds or report same-seed pairs separately. Essays keep their subject for 100 steps and converge in stance instead (`reports/e3_e.md`).
- **Predictions.** Every cell had a written prediction first; about a third failed and the failures are kept in `predictions.md` and in each gate report.

## Layout
```
SPEC.md SPEC2.md     design: arms, parameters, gates, measurements (SPEC2 §11 = future work)
CLAUDE.md            working rules for the Claude collaborator
predictions.md       predictions written before each run, never edited afterwards
DEVIATIONS.md        every departure from Hintze's code and settings (D1–D19)
STATUS.md            dated log of every session; "Where things stand" at the top
PANEL.md             provisional plan for a human rating panel (Phase 2)
RESEARCH_PROGRAM.md  the programme as a whole: questions, papers, order of work
docs/                runbooks for arms in preparation (E5)
papers/              public write-ups (PDF) and the endpoint contact sheets made for them
src/                 image runner (two-pass lockstep, atomic writes, idempotent resume), text runner, generators, captioners, embedders, candidate selection
configs/             one YAML per run (laptop and RunPod variants)
seeds/ data/         E6 seed tables (occupation × gender × age × skin tone); essay seeds (Wikipedia Vital Articles, pinned revisions)
scripts/             OSF fetch, RunPod setup/launch/queue/sync
analysis/            every figure and table is rebuilt from runs/ by these scripts
archive/             attractor centroids and names
reports/             gate reports (markdown + figures), one per run, plus cross-run atlases; reports/e3/ holds the text-loop sheets and judge archives
hintze_osf/          Hintze's OSF project, fetched locally (only our MANIFEST.tsv of checksums is tracked)
runs/ logs/ data/    experiment data, git-ignored (see below)
```

## Reproducing
1. Python 3.11, `uv venv .venv && uv pip install -r requirements.txt` (pinned; PyTorch 2.11 cu128, diffusers 0.41, transformers 5.20). Ollama with `llava:latest` (digest 8dd30f6b0cb1) for the reference captioner.
2. `python scripts/fetch_hintze_osf.py` downloads Hintze's code and seed reservoir into `hintze_osf/` and checks every file against `hintze_osf/MANIFEST.tsv`. The runner reads the seeds from there.
3. `.venv/bin/python -m src.runner configs/<run>.yaml` runs an image config and `.venv/bin/python -m src.text_runner configs/<run>.yaml` a text config; `scripts/runpod_*.sh` do the same on a RunPod pod. Claude runs and judges need `ANTHROPIC_API_KEY` in a git-ignored `.env`; the 7B text cells need Ollama with `mistral:7b` and `qwen2.5vl:7b` (digests in the run manifests).
4. `analysis/*.py` rebuild the reports from `runs/`; each script's docstring gives its command line.

## Data
`runs/` (about 111,000 images with their captions and step records, and about 72,000 stories with their summaries; 43 GB) is not in git. It is held on the author's machine and can be shared on request; archiving it with a DOI is planned. The judge outputs for E6 (`analysis/cache/e6_*/`), the per-step rows behind every E6 table (`reports/e6/*.json`) and the text-loop judge archives (`reports/e3/judge/`) are tracked so those results can be re-derived without the raw data. A few of Hintze et al.'s own published images and captions (figshare 30553604, CC BY 4.0) are reproduced in `reports/hintze_reference/` for side-by-side comparison.

## Working rules
Fidelity to Hintze's code first, with every departure logged. Predictions before results, never edited. Nothing that steers (CLIP, SigLIP) is used to grade; evaluation uses DINOv2 and MiniLM. Everything pinned. `runs/` is append-only. Each run stops at a gate and is reported before the next starts.

## Acknowledgement
The experiments were designed and judged by Brad Hinkel. Claude (Fable 5.1, with Sonnet 5.5 and Haiku 5.5 as captioner, story writer and judges) wrote the runner and analysis code, ran the pod, drafted the reports and the write-ups, and made quantified predictions alongside Brad's; the project notes record who contributed what and how often each side's predictions held. Brad takes responsibility for the claims.

## Licence
Code and text in this repository: MIT (see `LICENSE`). Hintze et al.'s OSF materials are not redistributed here; fetch them from OSF with the script above. Model weights (SDXL, LLaVA, Qwen2.5-VL, Hunyuan-DiT, DINOv2, MiniLM, SigLIP, CLIP) carry their own licences.
