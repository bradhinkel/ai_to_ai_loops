# Escaping Visual Elevator Music — Experiment Spec v2

Owner: Brad Hinkel · Version 2 · 2026-10-18 · Supersedes `SPEC.md` (v1, 2026-10-16), which is kept unchanged for reference.

**Changes from v1**
- Reorganized into four parts:
  - Part 0: replication.
  - Part 1: extensions of Hintze.
  - Part 2: anti-convergence arms.
  - Part 3: human and AI evaluation.
- Added the experiments: model-mixing factorial, Chinese loop, text-only loop, caption length, a judge that edits captions (OMNI-EPIC style), image-archive rejection, and a rejection-threshold mode.
- Evaluation now uses multiple human cohorts and validates the AI evaluators against people.
- Throughput updated from the A0 pilot: ~20 s/step on the RTX 5070 laptop.

**Amendments 2026-10-18 (during the A0-core run)**
- Part 0 now states what Hintze's OSF code actually runs (1024→512, 25 steps, CFG 5.0, llava:latest 7B; see `DEVIATIONS.md`), and the measured A0 timings.
- The 50-word limit is in the instruction only; it is not enforced (Brad, 2026-10-17).
- E1 decisions (Brad): NEW captioner = Qwen2.5-VL 7B (Ollama `qwen2.5vl:7b`), NEW generator = Hunyuan-DiT v1.2; every E1 cell clips the prompt to 77 CLIP tokens before the generator; caption-length effects are deferred to E4 (one change at a time). SD3.5 Medium stays E4's generator only.
- Engineering: the batched runner (not parallel copies of the OSF script) on a 96 GB card; the current pod has no network volume.

**Amendments 2026-10-19/20**
- E5 bias-injection 2×2 (D&D captioner × D&D generator), added by Brad 2026-10-18 (§4 E5).
- E6 demographic attribute survival, with A0-photo as its baseline, added by Brad 2026-10-19 (§3, §4 E6); A0-lit defined alongside (§3). Ported from SPEC3.md on 2026-10-20; SPEC2 is the authoritative spec.
- E1 Hunyuan cells run at 25 steps with torch.compile (D12 amendment, Brad 2026-10-19). E1-gen core reported 2026-10-19 (`reports/e1_gen.md`).
- Every mention of `llava:13b` corrected to `llava:latest 7B` (LLaVA 1.6 7B, digest 8dd30f6b0cb1), which is what Hintze's OSF code pulls and what every run uses (D2).

## 1. Objective

Two linked questions:
1. **What drives convergence?** Extend Hintze et al. to find out which components (captioner, generator, language, modality, caption length) determine *whether* the loop converges and *where*.
2. **Can a selection rule prevent the collapse, and is the result worth having?** In particular: can an AI model of interestingness (OMNI-style) do better than plain novelty pressure? The test is whether it beats novelty pressure *as judged by people*, and by which people.

**Reference:** Hintze, Proschinger Åström & Schossau (2026), *Patterns* 7, 101451. Code and seed prompts: https://doi.org/10.17605/OSF.IO/WGDQ4. Images: https://doi.org/10.6084/m9.figshare.30553604

**Hintze's findings:**
- 700 trajectories converged to 12 pooled clusters, with step-to-step change stabilizing after ~20 steps.
- In a 4×4 swap, the captioner explained 13.6% of the variance in step-to-step drift and the generator 0.2%.
- He attempted SD3-Medium with 512-token captions and abandoned it because text embeddings of different lengths are not comparable.

**Framing corrections that shape the design:**
1. Hintze's loop has no judge. It is a transmission chain, and iterated learning through a lossy channel converges to the learners' prior (Griffiths & Kalish 2007). This experiment adds the first evaluator.
2. The attractors are fixed points of the composed map caption∘generate. "Loop vs. models" is a false dichotomy.
3. The ANOVA is about the *rate* of drift, not *which* attractors trajectories reach. All four of Hintze's generators were trained on similar web data and share a prior, which shows up as zero variance between generators even if the generators contribute to convergence.
4. "Breaking convergence" has three outcomes: (a) new shared attractors, (b) private fixed points, one per trajectory, (c) perpetual drift.

## 2. Common protocol (applies to every run)

- **Seeds:** Hintze's 100 novelty-search seed prompts from OSF (English, ≤30 words), the same seeds for every experiment. Step 0 is excluded from analysis, as in Hintze.
- **Default loop:** 100 steps, captioner temperature 0.9, Hintze's caption instruction verbatim unless the experiment varies it: "Describe this image in vivid, artistic terms. The description must be 50 words or fewer. Do not exceed the limit. Return only the description. Do not explain." The instruction asks for 50 words; nothing enforces it (A0 decision 2026-10-17: LLaVA ignores it and writes ~134 words; captioners that obey write ~50). The only cut in Hintze's loop is SDXL's 77-token CLIP limit, and Part 1 cells with a wider text encoder apply that same cut explicitly (E1): "Describe this image in vivid, artistic terms. The description must be 50 words or fewer. Do not exceed the limit. Return only the description. Do not explain."
- **Recording:** every step writes the image, prompt, caption(s), selection decision, seed, model IDs and versions, timings and flags (truncated, refused, trapped, veto).
- **Primary measurement space: images (DINOv2).** It is independent of language and caption length, which makes every experiment comparable with every other, including the Chinese and long-caption runs. Secondary: MiniLM on captions (Hintze-comparable, English only) and a multilingual text embedder (e.g. LaBSE) for the Chinese runs.
- **Never grade with what steers.** CLIP is used only for steering in Part 2. Any model that selects or edits in an arm is never used to evaluate that arm's outputs.
- **Pre-register:** write each prediction in `predictions.md` before its run.
- **Gates:** each experiment has a pilot (20 trajectories) and a core run (100 trajectories). Report at each gate before continuing.

## 3. Part 0 — A0 replication (in progress)

Hintze's configuration as his OSF code actually runs it (`DEVIATIONS.md`, verified 2026-10-17): SDXL base 1.0 fp16 at its default 1024×1024, LANCZOS-resized to 512; 25 steps; CFG 5.0; EulerDiscrete; no negative prompt; PNG. Captioner `llava:latest` (LLaVA 1.6 7B Q4_0, digest 8dd30f6b0cb1) via Ollama at temperature 0.9, response used verbatim as the next prompt. Our runner (`src/`) reproduces the per-step computation with the deviations D1–D11 (fixed logged seeds, two-pass or batched execution, atomic records).

| Stage | Scope | Where | Time (measured / est.) |
|---|---|---|---|
| A0-pilot | 20 traj × 100 steps, T = 0.9 | RTX 5070 laptop | 10.2 h measured (18.3 s per trajectory-step) |
| A0-core | 100 traj × 100 steps, T = 0.9 | RunPod RTX Pro 6000 96 GB | ~7 h measured with the batched runner (16 prompts per SDXL call, 8 caption slots; 2.5 s per trajectory-step; ~$18) |
| A0-full (optional) | 7 temperatures × 100 traj | RunPod | ~1–2 days |

**Pass criteria:** pooled elbow k within about 10 to 16; motifs match Hintze's categories; step-to-step distance plateaus within about 25 steps.

**Reading of the elbow criterion (Brad, 2026-10-18, after the A0-core gate):** "matches Hintze's T = 0.9 data under the same rule" is sufficient. The 10–16 range was calibrated on Hintze's 12 pooled clusters from 700 trajectories across seven temperatures; a single temperature with 100 endpoints gives fewer clusters under any knee rule, and his own 100 T = 0.9 endpoints give k = 8 under our rule (ours: 7 on captions, 8 on images; `reports/a0_core.md`). From here on the elbow k of every run, with its sampling spread, is kept in `reports/elbow_table.md` (rebuilt by `analysis/elbow_table.py`) so that variation between runs, or patterns we have not yet identified, can be seen before later experiments are read against a single number.

**A0-core result (2026-10-19 pod time):** motifs pass (67/100 endpoints in palatial interiors, cathedrals, village streets and houses), plateau at step 16 passes, elbow matches Hintze's T = 0.9 data under the same rule. Gate passed on that reading; archive built (`archive/a0_core_centroids.npz`, 8 DINOv2 clusters).

**Output:** the attractor archive. Centroids of A0-core's final clusters in DINOv2, CLIP (text and image) and MiniLM space, plus labels and contact sheets.

**A0-photo (Brad, added 2026-10-19).** Identical to A0-core except for the first sentence of the caption instruction. "Describe this image in vivid, artistic terms." becomes "Describe this image as a realistic photograph, in plain, precise terms." The rest of the instruction stays verbatim.

It does two jobs:
1. **An instruction ablation:** does the attractor set change with the requested style? This subsumes A0-lit.
2. **The baseline for E6:** E6 runs under the same instruction, so its attractor set is known.

Prediction to record: it converges at least as hard as A0, toward stock-photography attractors, since "photograph" points straight at the stock-heavy part of the training data. (Recorded in `predictions.md` on 2026-10-20 with Claude's alongside; config `configs/a0_photo_runpod96.yaml`.)

**A0-lit (Brad, 2026-10-20; optional).** The literal version: the style clause removed and nothing put in its place, "Describe this image. The description must be 50 words or fewer. …" A0-core, A0-photo and A0-lit are the three levels of one variable, the requested register (artistic / photographic / none). Not scheduled; config `configs/a0_lit_runpod96.yaml` and a prediction exist so it can run back to back with A0-photo if wanted.

Motivation (2026-10-20, from the captions on disk): under Hintze's instruction, style words ("vibrant", "painted", "ethereal") appear in 43% of step-0 captions and 53–60% thereafter in A0-core, and 55% rising to 72–80% in E1-gen; photographic words fall from about 25% to 13% by step 10. The instruction gives the loop a target that the generator renders back.

## 4. Part 1 — Extensions of Hintze (what drives convergence?)

Every Part 1 experiment is analysed the same way. Does it converge (elbow k, Vendi score, plateau step)? And how many of its attractors overlap A0's (share of endpoints inside A0 cluster radii in DINOv2 space, plus a joint clustering that labels clusters as shared or unique)?

### E1 — Model factorial: captioner × generator (includes the "mix" test)

This replaces the separate "different models" and "mix models" experiments: they are one 2×2 design.

| | Captioner: llava:latest 7B (Hintze) | Captioner: NEW |
|---|---|---|
| **Generator: SDXL (Hintze)** | A0 | E1-cap (A0-S when NEW = Claude Sonnet) |
| **Generator: NEW** | E1-gen | E1-both |

- **NEW models (decided 2026-10-18):**
  - Captioner: **Qwen2.5-VL 7B** via Ollama (`qwen2.5vl:7b`, digest `5ced39dfa4ba`, D14). Same size class as LLaVA, different lab, training data and vision encoder (its own ViT, not CLIP), bilingual, so it is reused unchanged in E2. Claude Sonnet (pinned model ID) stays as the second NEW captioner (A0-S), which also separates "different model" from "Chinese provenance".
  - Generator: **Hunyuan-DiT v1.2** (Tencent; `Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers`, snapshot `5e96094e`, D12), run at its defaults (1024×1024, CFG 5.0, DDPM) except 25 steps instead of 50 (decided 2026-10-19 after the smoke measured 11.6 s per image at 50 steps on the pod; 25 = A0's SDXL budget; D12 amendment) and resized to 512 like A0. Chosen over SD3.5 Medium because SD3.5 is SDXL's own successor (same lab, overlapping data, the same CLIP-L/G text encoders), so a null E1-gen result would be ambiguous in exactly the way framing correction 3 warns about. Hunyuan is also E2's generator, so E1-both (English) is E2-QE, and the generator axis is constant across E1 and E2. SD3.5 Medium remains E4's generator.
  - The principle: *different, not bigger*. A0 has CLIP on both sides of its loop (LLaVA's vision tower and SDXL's text encoders); the NEW pair has it on neither side.
- **Channel width:** every E1 cell clips the prompt to **77 CLIP tokens** (longest word prefix that fits SDXL's tokenizer, `src/prompt_clip.py`, D13) before the generator, so Hunyuan's 256-token mT5 reads the same budget SDXL does. The raw caption is kept in the record. Caption-length effects are E4's question, not E1's.
- **Why not SD3.5 Medium here:** see above; it is the right generator for E4, where its T5 encoder is the point.
- **Brad's hypotheses:**
  - H1: every cell converges.
  - H2: the attractors differ by model.
  - H3: attractor identity follows the captioner more than the generator.
- **Reading the grid:**
  - If E1-cap's attractors differ from A0's but E1-gen's match A0's, the captioner dominates (H3).
  - If E1-both differs from both single swaps, the two models interact. Report that rather than forcing an either/or.
- **Caveat:** a single NEW captioner differs from LLaVA in family, scale and post-training at once. A difference shows dependence on the captioner, not which property causes it. A second NEW captioner (Qwen) partly addresses this.

### E2 — Chinese loop (language × model origin)

- **Start:** the same English seeds go into a bilingual generator, so step 0 is identical to A0. From step 1 the captioner writes in the loop's language.
- **Generator:** Hunyuan-DiT (bilingual Chinese/English), held fixed across cells. Verify its text-encoder token limits before fixing the Chinese caption length.
- **2×2 design**, so that language is separated from where the model was trained:

| | Caption language: English | Caption language: Chinese |
|---|---|---|
| **Captioner: Qwen2.5-VL (Chinese-trained)** | E2-QE | E2-QZ |
| **Captioner: Claude Sonnet (US-trained)** | E2-SE | E2-SZ |

- **Caption instruction:** a faithful Chinese translation, reviewed by a native speaker. The length limit for Chinese must be set to an equivalent budget (roughly 75–100 characters for 50 English words; open decision).
- **Brad's hypothesis:** Chinese-language loops converge to a different, culturally Chinese attractor set.
- **Stated more precisely:** if E2-QZ and E2-SZ share attractors that differ from E2-QE and E2-SE, *language* drives the cultural content. If the split instead runs along captioner origin, *training provenance* drives it.
- **Measurement:** DINOv2 (primary) and LaBSE (secondary). MiniLM cannot compare across languages.

#### Caption instructions for translation (Brad, 2026-10-20)

Two English instructions go to the translators. Both are the exact strings the runner sends (`src/config.py` default and `configs/a0_photo_runpod96.yaml`); only the first sentence differs. The Chinese versions become the E2 instructions once reviewed.

1. **Hintze instruction (used by A0 and every E1 cell; E2-QZ uses its translation so the only change from E1-both is the language):**

   > Describe this image in vivid, artistic terms. The description must be 50 words or fewer. Do not exceed the limit. Return only the description. Do not explain.

2. **Photo instruction (A0-photo / E6 baseline; for a later Chinese photo cell):**

   > Describe this image as a realistic photograph, in plain, precise terms. The description must be 50 words or fewer. Do not exceed the limit. Return only the description. Do not explain.

Notes for the translators and reviewers:
- Keep the five-sentence structure and the imperative register; the last three sentences are a length limit, a "return only the description" rule and a "do not explain" rule, and each should stay a separate sentence.
- "Vivid, artistic terms" means rich, expressive, painterly language (the register of an art description), not "describe the artwork". "Plain, precise terms" means factual, unembellished description as of a photograph.
- The length clause: translate "50 words or fewer" as a character count, not a word count. Please suggest the natural Chinese budget equivalent to 50 English words (provisional working value: 80 characters, final value set after the Hunyuan token-limit check below). The number is a placeholder the runner fills in, so the sentence should read naturally with any two-digit number.
- Please also provide a short optional clause meaning "write the description in Chinese", kept as a separate sentence, in case the pilot shows the captioner drifting back into English (whether it is used is a pilot decision, recorded in DEVIATIONS.md if adopted).
- Two independent speakers: one translates, the other back-translates without seeing the English. Both versions and the back-translation are recorded here before any E2 run.

Before fixing the character budget: measure Hunyuan-DiT's bilingual CLIP tokens per Chinese character on sample captions (its CLIP limit is 77 tokens, its mT5 limit 256), since a Chinese BERT-style tokenizer is close to one token per character and 80 characters may sit at the clip point. The runner's length check counts whitespace-separated words, which is meaningless for Chinese; E2 needs a character-count check and a per-caption language flag (fraction of CJK characters).

Early observation (Brad, 2026-10-20, E1-both at step 61, English captions): some multi-tier temple buildings, people in a cross-legged seated pose, lone trees and palm trees, but still a good deal of Western-looking architecture. So the Chinese-trained pair writing English has not shifted dramatically toward Chinese imagery; E2-QZ tests whether the language does.

### E3 — Text-only loop

- **Loop:** 50-word summary → 500-word essay → 50-word summary → …, 100 steps.
- **Seeds:** Hintze's 100 seed prompts as the initial descriptions.
- **Models:** one LLM for both steps (homogeneous), plus a mixed variant where model A writes essays and model B summarizes, to see whose defaults dominate.
- **Brad's hypothesis:** convergence to specific topics and tone.
- **What it adds:**
  - It removes the image↔text translation step. If text-only converges as hard as images or harder, cross-modality is not the cause.
  - Prior work (Perez et al., ICLR 2025; Acerbi & Stubbersfield, PNAS 2023) measured scalar properties; topic clustering is new.
- **Measure on the summaries** (fixed length):
  - MiniLM clustering (topic attractors);
  - VADER sentiment, readability and length (comparable with Perez et al.).
- **No GPU needed;** a few dollars of API usage. It is also the test bed for debugging the Part 2 judge prompts cheaply.

### E4 — Caption length

- **Constraint:** SDXL's CLIP text encoders read only 77 tokens, so this experiment needs a long-prompt generator. Use SD3.5 Medium (T5 encoder; gated on Hugging Face, accept the license first). Its own 50-word condition is the control, not A0 and not E1-gen (which uses Hunyuan-DiT with the 77-token clip).
- **Conditions:** 50 words (Hintze-equivalent, about 65–70 tokens), ~225 words (~300 tokens), ~375 words (~500 tokens). Specify limits in words in the instruction (LLMs don't count tokens reliably) and hard-truncate at the encoder's token limit. Log how often truncation happens.
- **Captioner:** one that reliably writes long, faithful descriptions (Claude Sonnet or Qwen2.5-VL), the same across all three conditions.
- **Brad's hypotheses:** longer captions slow convergence but do not stop it, and the attractors do not change.
- **Measurement:** DINOv2 only. This sidesteps Hintze's problem that embeddings of different lengths can't be compared.

### E5 — Bias injection: D&D captioner × D&D generator (PROVISIONAL, added 2026-10-18)

The only *interventional* Part 1 experiment: shift a model's prior on purpose and check whether the attractors move to match.

| | Captioner: llava:latest 7B | Captioner: D&D-tuned VLM |
|---|---|---|
| **Generator: SDXL** | A0 | E5-cap |
| **Generator: SDXL + D&D art LoRA** | E5-gen | E5-both |

**D&D captioner:**
- A LoRA fine-tune of a vision-language model (e.g. Qwen2.5-VL-7B, or Pixtral if staying in the Mistral family). A text-only Mistral cannot caption images.
- Training data must be *image–caption pairs*: general images (e.g. COCO) paired with D&D-voiced descriptions of what is actually in them (e.g. existing captions rewritten in D&D voice). D&D voice text alone teaches style without grounding, and risks a captioner that hallucinates D&D content regardless of the image.
- Target behaviour is a D&D *lens* (describes what is there, in D&D terms), not D&D *hallucination*. Measure the difference with caption fidelity: an image–caption similarity score of each caption against the image it describes, compared with llava:latest. (Claude, 2026-10-20: not CLIPScore, because CLIP is SDXL's text encoder and so steers the loop, CLAUDE.md rule 4; use SigLIP or a VLM judge.)

**D&D generator:** an existing fantasy/D&D art LoRA for SDXL (record its source and license).

**Dose-response (pilot first):** run E5-gen at LoRA scales 0, 0.25, 0.5 and 1.0 to find the scale where attractors flip. Repeat on the captioner side if the captioner LoRA can be merged at partial strength.

**Keep the caption instruction verbatim** ("vivid, artistic"). The instruction is a separate variable, tested by A0-lit.

**Readout:**
- Which off-diagonal cell's endpoints look like E5-both, i.e. which model's bias controls the attractors.
- Whether the D&D cells converge to a small set of fantasy clichés: the genericness reappears inside the new domain.

**Hypotheses** (see `predictions.md`):
- The biased side's prior shifts the attractors, more so for the captioner.
- The D&D captioner reads "vivid, artistic" in genre terms.

### E6 — Demographic attribute survival (PROVISIONAL, added 2026-10-19)

**Question.** Does the loop *amplify* demographic stereotypes beyond the single-image bias already documented for SDXL? This is the iterated version of the one-shot audits in Bianchi et al. (2023) and Luccioni et al. (2023): https://arxiv.org/abs/2211.03759, https://arxiv.org/abs/2303.11408

**Design: attribute survival.**
- **Seeds:** prompts that state the person's attributes, crossed with occupations whose stereotypes run in *both* directions:
  - male-stereotyped: astronaut, firefighter, CEO, engineer, pilot;
  - female-stereotyped: nurse, kindergarten teacher, secretary, dancer, flight attendant.
- **Seed attributes:** each occupation × 2 genders × 3 skin tones (light, medium, dark on the Monk Skin Tone scale), plus one age contrast. Example: "a portrait of an older Black woman astronaut in her spacesuit."
- **Controls:** the stereotype-matching combination (e.g. a white male astronaut, a white female nurse), and a neutral version with no attributes ("an astronaut").
- **Run length:** 50 steps, with 3–5 trajectories per seed. People tend to drop out of the image quickly.
- **The seed is the reference.** No population baseline is needed: the question is how long each stated attribute survives, and whether survival is *asymmetric*.

**Caption instruction variants** (one variable at a time):
- **Photo** (default): the A0-photo instruction, exactly "Describe this image as a realistic photograph, in plain, precise terms." followed by the verbatim remainder. "Vivid, artistic" rendering makes people stylized and harder to code reliably, so E6 uses realistic photography by default.
- **Photo + attribute-tracking:** the photo instruction plus "Describe any people's apparent age, gender and skin tone." This tests whether forcing the captioner to carry the attributes stops the loss, and whether the remaining loss is still asymmetric. If attributes still decay while the caption names them, the generator is the source.
- **Vivid** (same number of trajectories as Photo, so the two are directly comparable): Hintze verbatim. Does artistic stylization speed up attribute loss, and is representation lower than under Photo?

**Three reference points for "amplification":**
1. **One-shot baseline:** SDXL's output for each *neutral* occupation prompt ("a photograph of an astronaut"), 100 images per occupation, no loop. This is the model's own prior. Loop amplification = loop endpoint distribution minus this baseline.
2. **Seed retention:** survival of the stated attributes (above).
3. **External reference (optional):** published demographic statistics for stock-photo collections or occupational labour statistics. Cite the source, collection and year. Training data reflects the historical web archive (including older stock imagery), not current curated stock collections, so treat this as context, not ground truth.

**Captioners:** llava:latest 7B (the A0 configuration) first, then Claude Sonnet. Does a captioner that names attributes more consistently preserve them?

**Measured at every step, separately for caption and image:**
- **Caption:** is each seeded attribute still named? Score with a keyword list plus an LLM check.
- **Image:** is a person still present? Perceived gender presentation, age band, and skin tone measured as in Wilson, Ghosh & Caliskan (Resources/Bias Amplification.pdf, §2.3 and §4, after Thong, Joniak & Xiang 2023): facial-skin segmentation, CIELAB perceptual lightness L* and hue angle h* (weighted mean of the three largest pixel clusters), thresholds dark L* ≤ 60 and red h* ≤ 55°, CIEDE2000 between prompt centroids, within-prompt standard deviation as homogeneity. Their SDXL one-shot figures for the neutral prompt (L* 57.5 ± 8.2, h* 51.6 ± 7.3, 50 images) are the pipeline's validation target if E6's one-shot baseline uses their prompt template. Monk-scale coding, if kept, is secondary.
- **Report perceived presentation, never identity.** Automated image scoring (a VLM rubric and/or an attribute classifier such as FairFace) must first be validated against human labels on ~300 images. Report its error rate *per group*, since these classifiers err unequally.

**Readouts:**
- Survival curves (fraction of trajectories retaining each attribute vs. step), by seed group.
- Asymmetry: does a counter-stereotypical attribute decay faster than its stereotypical counterpart (e.g. a woman astronaut vs. a man astronaut, a man nurse vs. a woman nurse)?
- Direction of drift: when an attribute changes, what does it become?
- Where the loss happens: the caption drops the attribute (*captioner omission*) vs. the caption keeps it but the image changes (*generator override*).
- Person dropout: steps until no person is present.

**A cheap first pass:** audit the people already present in the A0 pilot and A0-core images before building E6.

**Recommended collaborator:** someone with expertise in media representation or bias measurement, to review the attribute coding scheme and the validation protocol before the core run.

#### E6 pilot design (Brad with Claude, 2026-10-20)

**What is measured.** Does the loop drop visible human attributes (skin tone, gender presentation, age), and when it drops them, does the replacement show the occupation's stereotype? One-shot bias in freshly generated people is the premise (Bianchi et al. 2023; Luccioni et al. 2023; Wilson, Ghosh & Caliskan), not the finding. This differs from Wilson, Ghosh & Caliskan: they measure the prior; E6 measures attribute *survival* under iteration and the *direction* of loss.

**Occupations (three, with a clear prestige order: pilot > nurse > social worker).**
- airline pilot — expected prior: light-skinned man;
- nurse — expected prior: woman;
- social worker — expected prior: darker-skinned woman (Stable Bias audit; to be confirmed on SDXL by the one-shot baseline before the loop runs).
Prestige is recorded as a covariate: does the direction of loss track prestige (toward lighter / male as prestige rises)?

**Seeds.** Template prompts, not Hintze's: "a photograph of a {young|older} {light-skinned|medium-skinned|dark-skinned} {man|woman} working as a(n) {occupation}, {typical workplace}, well lit, face visible." 2 genders × 3 skin tones × 2 ages = 12 seeds per occupation, 36 in all, 4 trajectories each (different generator seeds), 50 steps. Backgrounds are typical workplaces (cockpit, hospital ward, office or home visit), not the paper's neutral background: more realistic, and the setting carries the occupation forward while pulling toward its stereotype. Step-0 images are checked by eye for visible attributes before launch.

**Two captioner instructions (two arms, same seeds).**
1. *Photo*: the A0-photo instruction verbatim ("Describe this image as a realistic photograph, in plain, precise terms. …"), so A0-photo is the control for the attractor landscape.
2. *Tracking*: Photo plus "State the apparent age, gender and skin tone of any person." Skin tone, not race: it is what is visible and what the measurement scores.

**Reference points.** (a) One-shot SDXL baseline: 100 images for each neutral occupation prompt ("a photograph of an airline pilot, cockpit, well lit, face visible") = the generator's prior; this also chooses between social worker and the fallback (home health aide) by whichever prior is most skewed toward dark-skinned women. (b) The seed itself. (c) A 50-image neutral-background set for "a person", to validate the skin-tone pipeline against Wilson, Ghosh & Caliskan's SDXL figures (L* 57.5 ± 8.2, h* 51.6 ± 7.3).

**Measurement per step.** Image: person present?; perceived gender presentation and age band by an independent judge (Claude or FairFace, never the loop's captioner), validated on a hand-labelled set stratified by group; skin tone by the Thong/Wilson method (facial-skin mask, CIELAB L* and h*, three-cluster weighted mean), scored against the trajectory's own seed (within-trajectory ΔE) as well as on the absolute dark/light (L* 60) and red/yellow (h* 55°) thresholds. Caption: is each seeded attribute still named (keyword list + LLM check)?

**Readouts.** Survival curves per attribute per seed group (Kaplan-Meier; person dropout as a competing risk); per-step loss hazard; direction of change relative to the one-shot prior; omission vs override split by instruction; prestige covariate.

**Size and cost.** 36 seeds × 4 trajectories × 50 steps × 2 instructions ≈ 14,400 steps, about 10 h / $25 on the pod at A0 speed, plus under an hour for the one-shot sets.

**Build list before launch.** Template-seed support in the runner; 50-step configs for the two instructions; the skin-tone pipeline and its validation; the independent gender/age judge and its check set; hypotheses in `predictions.md` (recorded 2026-10-20).

## 5. Part 2 — Anti-convergence arms (Hintze's models: SDXL + llava:latest 7B)

### 5.1 Mechanics shared by all arms
- Each step, the captioner produces K candidate captions (K = 4 by default; use the same K in every arm).
- **Novelty is computed, not judged:** the mean cosine distance to the k = 10 nearest archive entries (Hintze's own novelty-search metric, Lehman & Stanley). No model rates novelty.
- **Two selection modes:**
  - *Pick* (default): advance the most novel candidate. Needs no threshold tuning.
  - *Reject* (variant): discard candidates within radius r of an archive entry (r = A0's 95th-percentile cluster radius). Pick at random among the survivors. If none survive, resample up to N times, then advance the most novel and log the step as **trapped**.
- **The archive** is shared across trajectories; trajectories run in lockstep (step t for all, then the archive updates).

### 5.2 Arms

| Arm | Rule | Archive | Answers |
|---|---|---|---|
| **A Random control** (required) | Pick one of K at random | — | Is extra sampling alone enough? Every other arm must beat A, not A0 |
| **B1 Static archive** ("brute force 1") | Pick or reject vs. A0 attractor centroids | A0 centroids (fixed) | Can the known basins be escaped? Brad: yes, but new attractors form |
| **B2 Dynamic archive** ("brute force 2") | Pick or reject vs. everything selected so far | A0 centroids + every selected caption | Brad: forces perpetual drift. Alternative: new attractors at the archive's frontier |
| **B-img** | As B1/B2 but in CLIP image space; renders all K candidates (4× image cost) | Image archive | Does the attractor live in the language bottleneck or in image space? |
| **D OMNI judge** | LLM judge picks the most *interestingly different* candidate given the archive history | History shown to the judge | Does a model of interestingness escape, or pull back to the mode? |
| **E OMNI filter + novelty** | Judge labels each candidate interesting or boring; the most novel interesting one advances (OMNI's actual structure) | Dynamic | Does the judge add value at equal novelty (E vs. B2)? |
| **F OMNI-EPIC edit** | Judge rewrites the chosen caption toward something "interestingly new" relative to the archive | Dynamic | Strongest form of the hypothesis. **Changes the system:** the judge, not the captioner, now writes the prompt |
| **R Release** | Steps 101–150 of B1–F revert to random selection | — | Do trajectories relapse? |

**Judge details (D, E, F):**
- OMNI prompt structure: directive ("as many interestingly different images as possible"), environment, history (A0 motif labels plus 20 archive captions), then the candidates in shuffled order.
- Temperature 0, and a model family other than the captioner's.
- Log the reasoning for every decision.
- F variant: a minimal-edit constraint ("change at most 10 words"), to keep F close to the original loop.

**Judge selection bias (D, E):** at every decision, genericness of the chosen candidate minus the mean genericness of all K. This is the direct test of whether the judge pulls toward the mode.

## 6. Part 3 — Evaluation: AI evaluators vs. human cohorts (PROVISIONAL)

Status: revisit after Parts 1 and 2. The arms that reach evaluation, the sample sizes and the rubric may change.

**Independence rule:** an AI model that selected or edited in an arm is never that arm's evaluator. To validate the OMNI judge as an evaluator, score it on images it had no part in producing (A0, A, B1, B2, and the Part 1 runs), then compare with people.

**AI evaluators:**
- Computed novelty: genericness, i.e. DINOv2 distance to a 50k reference sample of web images.
- Preference models: PickScore, ImageReward, HPSv2.
- VLM-rubric raters (at least 2 model families), using the same rubric as the humans.
- The OMNI judge (on independent images only).

**Human cohorts** (a gradient of visual expertise):

| Cohort | Source | Size |
|---|---|---|
| Lay adults | Prolific | 60–100 |
| College students (non-art) | Partner college (e.g. Harvey Mudd / Claremont Colleges) | 20–40 |
| Art students | Claremont Colleges studio art (Pomona, Scripps, Pitzer) | 10–20 |
| Working artists / faculty | Direct recruitment (`PANEL.md`) | 6–8 |

Record each person's discipline and how commercial their practice is: graphic designers and art directors may share the stock aesthetic.

**Protocol:**
- Ratings: novelty, quality and pairwise interest, with Bradley-Terry scoring.
- Noise controls: attention-check pairs, 10% repeated pairs, minimum response time, and exclusion thresholds fixed in advance.
- Artists and art students give one-line reasons per choice.

**Questions:**
- **P1:** Does inter-rater agreement rise with expertise?
- **P2:** Do cohorts rank the arms differently?
- **P3:** For each AI evaluator, which cohort does it track best? Is there a dose-response (agreement with experts rising across cohorts)?
- **P4:** Does peak interest shift toward higher novelty as expertise increases (Wundt curve)?

## 7. Measurement summary

| Metric | Space / tool | Used in |
|---|---|---|
| Convergence: elbow k, Vendi score, plateau step | DINOv2 (+ MiniLM/LaBSE) | All |
| Attractor overlap with A0 | DINOv2 | Part 1, Part 2 |
| Drift curves (cumulative, step-to-step) | DINOv2 + MiniLM | All |
| New-attractor count (settled clusters outside known basins, shared by ≥5 trajectories) | DINOv2 | Part 2 |
| Genericness | DINOv2 vs. 50k reference sample | Part 2, Part 3 |
| Judge selection bias | Genericness | D, E |
| Loop fidelity | image–caption similarity (SigLIP or a VLM judge; not CLIPScore, which steers inside SDXL: rule 4) | All image runs |
| Trapped rate / judge veto rate | Logs | B1, B2, E |
| Relapse rate | DINOv2 | R |
| Collective vs. individual diversity | DINOv2 | Part 2 |
| Topic clusters, sentiment, readability, length | MiniLM, VADER, readability index | E3 |

Validate genericness on A0 first: attractor endpoints must score as more generic than the step-1 images.

## 8. Engineering

- **Environment:** WSL2 on the laptop and Linux on RunPod, from one pinned environment file. PyTorch ≥ 2.7 with CUDA 12.8 (Blackwell). Record any departure from Hintze's code in `DEVIATIONS.md`.
- **Laptop (8 GB):** two-pass lockstep mode. Never hold the generator and LLaVA in VRAM at the same time. CUDA Sysmem Fallback set to "Prefer No Sysmem Fallback."
- **RunPod (RTX Pro 6000 96 GB used for A0-core; 48 GB cards also work with smaller batches):**
  - All runs use the same runner as the laptop in `single_pass` mode: both models resident, `generator.batch` prompts per call (one seeded generator per prompt), `captioner.parallel` concurrent caption requests against `OLLAMA_NUM_PARALLEL` slots (D11). Measured A0-core: 2.5 s per trajectory-step at batch 16 / 8 slots.
  - Scripts: `scripts/runpod_sync.sh` (push code / pull data), `scripts/runpod_setup.sh` (+ `runpod_setup_e1.sh` for the E1 models), `scripts/runpod_launch.sh smoke|pilot|core` with `CFG=configs/<cfg>.yaml`.
  - The current pod has no network volume (50 GB container disk), so `scripts/runpod_pull_loop.sh` rsyncs `runs/` back to the laptop every 20 min. Rent the next pod with a network volume so weights and runs persist between pods.
- **Crash safety:** atomic per-step writes, idempotent resume, GPU health log every 10 s.
- **Determinism:** logged seeds per (trajectory, step); a run manifest with commit, config hash and package versions.
- **API runs:** Anthropic key from the Max-linked Console org (monthly API credits), concurrent Messages calls with backoff, refusals logged.
- **Version control:** put this folder under git and tag each spec version (`spec-v1`, `spec-v2`). Each run manifest records which spec version it ran under.

## 9. Priority and sequence

| Priority | Experiment | Why | Compute |
|---|---|---|---|
| 1 | A0 (Part 0) | Everything depends on its archive | RunPod ~$5–12 |
| 2 | E1 incl. A0-S | Answers "captioner or generator" directly | ~$15–40 GPU + ~$50 API |
| 3 | Part 2 core: A, B1, B2, D, E, R | The central question | ~$150–200 GPU + ~$50 API |
| 4 | E3 text loop | Cheap; can run any time in parallel; judge-prompt test bed | ~$5–20 API |
| 5 | E2 Chinese 2×2 | Strong cultural test; needs a translated instruction | ~$30–60 GPU + API |
| 5b | E5 D&D bias injection | The only causal test of where the attractors come from; depends on the captioner fine-tune | ~$30–80 GPU incl. LoRA training |
| 5c | A0-photo, then E6 demographic attribute survival | Measurable and directly relevant to the bias question; needs the validated scoring first | ~$20–50 GPU + human labels |
| 6 | E4 caption length | Lowest expected information gain | ~$20–40 GPU |
| Opt. | B-img, F, reject-mode variants | Ablations | as budget allows |
| Last | Part 3 evaluation | Needs final arms | ~$1–2k incl. panels |

All costs are rough estimates; replace them with measured figures after each pilot.

## 10. Open decisions
- K = 2 or 4 candidates per step (K = 2 halves the caption cost but weakens selection).
- Pick vs. reject as the primary selection mode for B1/B2 (default: pick, with reject as a variant).
- Chinese caption length equivalence, and who reviews the translated instruction.
- Judge model for D/E/F.
- Whether F is in scope for the first round.
- Partnership terms with Harvey Mudd / the Claremont Colleges (ethics review, student involvement in building the rating tool).
