# Escaping Visual Elevator Music — Experiment Spec

Owner: Brad Hinkel · Version: 2026-10-16 · Source doc: "Escaping Visual Elevator Music: Experiment Spec" (Claude Docs). This file is the build version and supersedes the doc where they differ.

## 1. Objective

Find out whether adding a selection rule to Hintze et al.'s SDXL↔LLaVA loop changes where it converges, and whether what it finds instead is worth having. All selection arms generate the same number of candidates per step and differ only in how the next prompt is chosen, so each comparison is a single-variable test.

**Reference paper:** Hintze, Proschinger Åström & Schossau (2026), "Autonomous language-image generation loops converge to generic visual motifs," *Patterns* 7, 101451. Code and prompts: https://doi.org/10.17605/OSF.IO/WGDQ4. Images: https://doi.org/10.6084/m9.figshare.30553604

**What Hintze found:** 700 trajectories (7 temperatures × 100 seeds × 100 steps) converged to 12 pooled k-means clusters (lighthouses, urban night scenes, gothic cathedrals, palatial interiors, …). Step-to-step change stabilizes after ~20 iterations. In a 4×4 generator × captioner swap, the captioner explained 13.6% of the variance in step-to-step drift and the generator 0.2% (about 85% residual).

**Framing corrections that shape the design:**
1. Hintze's loop has no judge. It is a transmission chain (describe → regenerate), and iterated learning through a lossy channel converges to the learners' prior (Griffiths & Kalish 2007). This experiment adds the first evaluator.
2. "Loop vs. models" is a false dichotomy. The attractors are fixed points of the composed map caption∘generate: the models supply the prior and the loop drives trajectories to it.
3. The ANOVA shows the captioner changes the *rate* of drift. It does not show the generator plays no part in convergence: all four generators were trained on similar web data and share a prior, which shows up as zero between-generator variance.
4. "Breaking convergence" has three distinct outcomes: (a) new shared attractors, (b) private fixed points, one per trajectory, (c) perpetual drift. (c) under novelty pressure is a pathology, not a success.

## 2. Research questions and hypotheses

- **Q1 Replication.** Does a faithful rerun reproduce collapse to ~12 motifs by ~step 20?
- **Q1b Captioner swap (H1/H2).** With Claude Sonnet as captioner and everything else fixed:
  - H1: does the loop still converge to a small set of attractors?
  - H2: are they the *same* attractors as LLaVA's?
  - Brad's pre-registered prediction: it converges (H1 holds), but to different attractors (H2 fails).
- **Q2 Novelty pressure.** Does selecting away from known attractors (static archive) or from everything seen so far (dynamic archive) escape, and into outcome (a), (b) or (c)?
- **Q3 Interestingness judge.** Does an OMNI-style LLM judge help escape, or pull the loop back toward the mode?
- **Q4 Creativity.** Are less generic endpoints valued by people, or merely different? Creativity is defined as novel + valuable, with value judged by blind human raters (plus AI raters calibrated against them).
- **Q5 Persistence.** With selection switched off, do trajectories relapse into the old basins?

Record each prediction in `predictions.md` BEFORE running the arm it concerns.

## 3. Arms

| Arm | Captioner | Selection rule per step | Answers |
|---|---|---|---|
| A0 Replication | llava:13b (Ollama) | None: one caption, used as-is (Hintze verbatim) | Q1 |
| A0-S Sonnet captioner | Claude Sonnet (API) | None | Q1b (H1, H2) |
| A Random control | llava:13b | 4 candidates, pick one at random | Is extra sampling alone enough? |
| B Static archive | llava:13b | Candidate farthest from A0's centroids | Q2 |
| C Dynamic archive | llava:13b | Candidate farthest from all selected captions so far (shared, lockstep) | Q2 |
| D Judge only | llava:13b | LLM judge picks the most interesting, given archive history | Q3 |
| E Judge + archive | llava:13b | Judge marks each candidate interesting/boring; most novel interesting one wins (OMNI structure) | Q3, Q4 |
| R Release | — | Steps 101–150 of B to E revert to random | Q5 |

Optional ablations: **B-img** (select on CLIP image embeddings by rendering all 4 candidates; 20 trajectories), **D-blind** (judge with no history; 20 trajectories), **A0-lit** (literal caption instruction instead of "vivid, artistic"; tests whether the instruction itself drives cliché).

**Execution order (gated):** A0-pilot → A0-core → A0-S → A → B → C → D/E → R → human panel. Do not start an arm until the previous gate passes.

## 4. Phase 1: A0 replication (local GPU, tinkerer configuration)

### 4.1 Parameters (must match Hintze exactly)

| Parameter | Value |
|---|---|
| Image generator | stabilityai/stable-diffusion-xl-base-1.0, 512×512, 50 inference steps, CFG 7.5 (verify the scheduler against the OSF code) |
| Captioner | llava:13b via Ollama (verify the exact tag and quantization against the OSF code) |
| Caption instruction (verbatim) | "Describe this image in vivid, artistic terms. The description must be 50 words or fewer. Do not exceed the limit. Return only the description. Do not explain." |
| Seed prompts | Hintze's 100 novelty-search prompts from OSF (do not regenerate) |
| Steps per trajectory | 100 |
| Image format | JPEG, as in the paper |
| Analysis embedding | sentence-transformers/all-MiniLM-L6-v2 on captions; exclude step 0 |
| Clustering | k-means on final-step caption embeddings, elbow method |

### 4.2 Stages

| Stage | Scope | Rough laptop time | Gate |
|---|---|---|---|
| A0-pilot | 20 trajectories × 100 steps, T = 0.9 | ~6–8 h | Pipeline runs end to end; resume after a forced kill works |
| A0-core | 100 trajectories × 100 steps, T = 0.9 | ~25–40 h | Pass criteria below |
| A0-full (optional) | 7 temperatures × 100 trajectories (Hintze's full 700) | ~7–10 days continuous; RunPod recommended | Temperature-invariance check |

Times are estimates for an RTX 5070 laptop (8 GB) in two-pass mode. Measure the real throughput in the pilot and update this table.

### 4.3 Pass criteria (A0-core)
1. Pooled elbow-optimal k lands within about 10 to 16.
2. Endpoint motifs visibly match Hintze's categories (contact sheet of the step-100 images, grouped by cluster).
3. Step-to-step cosine distance plateaus within about 25 steps.

### 4.4 Outputs used downstream
- The attractor archive: centroids of A0-core's final clusters in MiniLM (caption), CLIP ViT-L/14 text and image, and DINOv2 image space, saved to `archive/a0_centroids.npz` with labels.
- Contact sheets per cluster, and the drift curves (cumulative and step-to-step).

## 5. Phase 1b: A0-S, Sonnet as captioner

- Same seeds, generator, instruction, steps and analysis as A0-core. Only the captioner changes.
- Model: a pinned Claude Sonnet model ID, temperature 0.9, image sent as the same 512×512 JPEG. Log the exact model ID in every record.
- Billing: Anthropic API key from the Console organization linked to the Max plan, which draws from its monthly API credits. Never route these calls through `claude -p` on plan login.
- No VRAM is needed for captioning, so SDXL stays loaded: single-pass mode.
- Log every refusal, empty response and over-50-word caption. Truncate to 50 words exactly as the A0 pipeline would, and flag the record.
- Analysis:
  - H1: elbow k, Vendi score and the plateau step.
  - H2: share of A0-S endpoints falling inside A0's cluster radii (95th percentile), plus a joint clustering of A0 and A0-S endpoints showing which clusters are shared and which are unique to one captioner.
- Caveat to state in the write-up: Sonnet differs from LLaVA in model family, scale and post-training at once. A difference shows the attractors depend on the captioner; it cannot say which of those properties is responsible.
- Estimated API cost: ~$25–50 for 10k captions (verify current pricing).

## 6. Phases 2 and 3: selection arms (A to E, then R)

- **Candidates:** 4 captions per step from llava:13b at T = 0.9. Selection acts on captions, where the ANOVA locates the drift.
- **Novelty score:** mean cosine distance to the k = 10 nearest archive entries, in CLIP ViT-L/14 text space. For B, use distance to the nearest A0 centroid.
- **Dynamic archive (C, E):** starts with A0's centroids and adds every selected caption. It is shared across trajectories, which run in lockstep: all trajectories complete step t, then the archive updates.
- **Trapped log:** flag any step where all 4 candidates fall inside a known basin.
- **Judge (D, E):**
  - OMNI-style prompt: directive ("help this image-description chain produce as many interestingly different images as possible"), environment description, history (A0 motif labels plus 20 archive captions), then the candidates in shuffled order.
  - Temperature 0. Use a model family other than the captioner's. Log one sentence of reasoning per decision.
  - E: drop the candidates marked boring, then pick the most novel; if all 4 are boring, pick the most novel and log a judge veto.
- **Judge selection bias:** at every decision, genericness of the chosen candidate minus the mean genericness of all 4.
- **Release (R):** steps 101–150 revert to random selection.
- Recommended hardware: RunPod RTX Pro 6000 (48 GB, ~$1.20/h). All models stay resident.

## 7. Measurement

Rule: no metric is computed in an embedding space any arm steers on (CLIP), and no model that selects is ever used to grade.

| Metric | Space / tool | Answers |
|---|---|---|
| Basin occupancy (share of endpoints within A0 cluster radii) | DINOv2 (images), MiniLM (captions) | Q1, Q1b, Q2, Q3 |
| Effective diversity: elbow k plus Vendi score | same | Q1, Q2 |
| Drift curves: cumulative and step-to-step | MiniLM (Hintze-comparable) | Q1, Q2, Q5 |
| New-attractor count: settled clusters outside known basins shared by ≥5 trajectories | DINOv2 + MiniLM | Q2 |
| Genericness: mean distance to the 10 nearest images in a fixed 50k reference sample of web images | DINOv2 | Q3, Q4 |
| Loop fidelity | CLIPScore, image vs. its generating caption | Q4 |
| Relapse rate: occupancy at step 150 vs. step 100 | DINOv2 | Q5 |
| Collective vs. individual diversity | DINOv2 | Q2, Q4 |
| Human panel: novelty, quality, pairwise interest; Bradley-Terry scoring; attention checks; repeated pairs | Prolific | Q4 |
| AI rater panel: the same rubric as the humans, at least 2 model families, calibrated against the human panel | VLM APIs + preference models | Q4 |

Validate the genericness metric on A0 before using it: A0's attractor endpoints must score as more generic than the seed prompts' step-1 images.

## 7b. Evaluation panels: two-panel design (PROVISIONAL)

Status: provisional. Revisit after A0, A0-S and the selection arms, before any panel is recruited. The arms that reach the panel, the number of images and the rubric may all change with Phase 1–3 results.

**Why two panels.** The training corpus is not human taste. It is what got photographed, posted and captioned, which over-represents stock and tourist imagery. Lay raters may still reward the familiar because familiar images are easier to take in. Artists see far more imagery, so their peak interest likely sits further toward the novel (Martindale's habituation account, in Elgammal et al.). The panels are not "right" and "wrong" judges; they sit at different points on the same novelty–interest curve.

**Panels.**

| Panel | Who | Size | Source |
|---|---|---|---|
| Lay | Adults, no screening for art background | ~60–100 raters, ~50 judgements each | Prolific |
| Artist | Working visual artists with a verifiable portfolio or teaching role (fine-art photographers, painters, illustrators, art faculty, curators) | 6–8 | Direct recruitment (see PANEL.md) |

Record each artist's discipline and whether their work is mainly commercial. Commercial art directors may share the stock aesthetic, so this field is an analysis covariate, not an exclusion.

**Protocol (both panels).**
- The same images: a stratified sample of endpoints per arm, shuffled, no arm labels. All images are AI-generated, and raters are told so.
- The same judgements:
  - novelty ("Have you seen images like this before?");
  - quality ("Is this coherent and well made?");
  - pairwise interest ("Which would you look at longer?").
- Interest is scored with a Bradley-Terry model.
- Noise controls:
  - attention-check pairs (garbled vs. clean);
  - 10% repeated pairs to measure each rater's self-consistency;
  - a minimum response time.
  - Drop lay raters who fail the attention checks or fall below the consistency threshold, with the threshold fixed before data collection.
- Artist panel only: a one-line reason per pairwise choice, coded afterwards for recurring criteria.

**Questions the two panels answer.**
- **P1 Expertise as a construct:** is inter-rater agreement (Krippendorff's α) higher within the artist panel than within the lay panel?
- **P2 Panel divergence:** do the two panels rank arms differently on interest?
- **P3 AI raters:** for each AI rater (preference models, VLM-rubric raters), which panel does it agree with more (Spearman correlation on per-image scores)? If none tracks the artists, expert taste is not recoverable from these AI raters.
- **P4 The Wundt curve per panel:** plot each panel's interest against measured novelty. Is the artist panel's peak further toward novelty?

Proposed predictions are in `predictions.md`. Confirm or amend them before the panel runs.

## 8. Engineering requirements

- **Environment:** Windows 11 with WSL2 (Ubuntu), so the laptop and RunPod run the same Linux stack. Python 3.11, PyTorch ≥ 2.7 built for CUDA 12.8 (required for Blackwell, sm_120). One `environment.yml` or `requirements.txt` with pinned versions.
- **Known deviation:** if Hintze's code pins an older PyTorch or diffusers, upgrade to the Blackwell-compatible versions and record it in `DEVIATIONS.md`.
- **Two-pass lockstep mode (8 GB GPUs):** for each step: load SDXL → generate step t for all active trajectories → unload and free VRAM → caption with Ollama (`keep_alive: 0`) → next step. Never hold both models in VRAM. Single-pass mode (both resident) is a config flag for ≥24 GB cards and for API captioners.
- **Crash safety:**
  - Write each step atomically (temp file, then rename).
  - The runner is idempotent and resumes from the last complete step after any crash or reboot.
  - A pilot gate is to kill the process mid-run and verify a clean resume.
- **Record per step:** `runs/<arm>/<traj_id>/step_<NNN>.jpg` plus `.json` holding prompt, caption(s), the selected index, SDXL seed, model IDs and versions, temperature, timings, and flags (truncated, refused, trapped, veto).
- **GPU health log:** sample `nvidia-smi` (temperature, power, VRAM, clocks) every 10 s to `logs/gpu.csv` during runs.
- **Determinism:** fixed, logged SDXL seeds per (trajectory, step); a run manifest with git commit, config hash and package versions.
- **Analysis:** reproducible scripts (`analysis/`) that regenerate every figure and table from `runs/` alone.

## 9. Budget (approximate)

| Item | Cost |
|---|---|
| A0-pilot and A0-core on the laptop | electricity only |
| A0-S Sonnet captions (10k) | ~$25–50, from Max API credits |
| Arms A to E plus R on RunPod RTX Pro 6000 | ~$150–200 |
| Judge API calls | ~$35–60 |
| Lay panel (Prolific, with attention checks) | ~$400–800 |
| Artist panel (6–8 people, ~90 min each, honorarium) | ~$500–1,000 |

## 10. Open decisions
- Archive shared across trajectories (collective diversity, the default) or per trajectory?
- Judge model: small and cheap, or frontier?
- Panel: both (SPEC §7b, provisional). Finalize the arms, sample size and rubric after Phase 3.
- Run A0-full (all 700 trajectories) on the laptop, on RunPod, or skip it?
