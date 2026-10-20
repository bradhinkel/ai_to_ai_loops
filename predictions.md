# Pre-registered predictions

Write each prediction before its arm runs. Never edit an entry after results exist; add a dated note instead.

## A0 (replication, llava:13b) — recorded 2026-10-16 by Brad
*Note added 2026-10-17, before any A0 results: the OSF code uses `llava:latest` (LLaVA 1.6 7B Q4_0), so A0 runs with that tag (DEVIATIONS D2). The prediction itself is unchanged.*

We will get similar results to Hintze: there should be about 12 resulting image attractors, and these should match the descriptions from Hintze (the same general images, lighthouses, urban night scenes, gothic cathedrals, palatial interiors and so on), but not a pixel match.

Quantified for the A0-core gate (SPEC §4.3), added by Claude with Brad's wording above as the source:
- Pooled elbow-optimal k on step-100 MiniLM caption embeddings lands in 10–16, with 12 as the point estimate.
- Most clusters (at least 8 of them) are visually recognisable as one of Hintze's named motifs on the contact sheets.
- Step-to-step cosine distance plateaus by about step 20–25, as in the paper.
- No cluster is a pixel-level or near-duplicate match to Hintze's images; the match is at the motif level only.

*Note added 2026-10-18 after the A0-core results (prediction above unchanged): the knee rule gives k = 7 on our 100 MiniLM endpoints, outside 10–16, and gives k = 8 on Hintze's own 100 T = 0.9 endpoints under the same rule; the 10–16 range was calibrated on his 700 pooled trajectories across temperatures. See `reports/a0_core.md`.*

## A0-S (Sonnet captioner) — recorded 2026-10-16 by Brad
- H1 (converges to a small attractor set): expected to hold.
- H2 (same attractors as A0's LLaVA): expected to FAIL; Sonnet's attractors will differ.

## Evaluation panels (SPEC §7b): PROPOSED by Claude, 2026-10-16. Brad to confirm or amend before the panel runs.
- P1: artist-panel agreement is higher than lay-panel agreement (expertise is a shared standard, not just individual taste).
- P2: the lay panel rates the A0 attractor images (lighthouses, cathedrals) as more interesting than the artist panel does.
- P3: preference models (PickScore, ImageReward, HPSv2) correlate more with the lay panel than with the artists; VLM-rubric raters fall in between; no AI rater matches the artists as well as the artists match each other.
- P4: the artist panel's interest peaks at higher novelty than the lay panel's.

## E1 model factorial (SPEC2 §4: Qwen2.5-VL 7B captioner, Hunyuan-DiT v1.2 generator, CLIP-77 clip in every cell) — drafted 2026-10-18 by Claude from Brad's hypotheses H1–H3 in SPEC2 §4. Brad to confirm or amend before the first E1 run starts.
- H1 (every cell converges): each of E1-cap, E1-gen, E1-both reaches a step-to-step DINOv2 drift plateau by about step 25 and a pooled elbow k below 20 on its final-step images.
- H2 (attractors differ by model): fewer than half of E1-both's endpoints fall inside A0's cluster radii in DINOv2 space, and the joint clustering shows clusters unique to E1-both.
- H3 (captioner dominates): E1-cap's overlap with A0 is lower than E1-gen's. Point estimate: E1-gen keeps most of A0's motifs (over half of its endpoints inside A0 radii), E1-cap keeps few (under a third).
- Interaction: if E1-both's attractor set differs from both single swaps, that is reported as an interaction, not forced into H3.
- Side prediction (Claude): Qwen obeys the 50-word instruction (median caption 40–55 words), so the CLIP-77 clip rarely fires in the Qwen cells and fires on nearly every LLaVA caption, as in A0.

*Confirmed by Brad, 2026-10-18, before any E1 run, in his words: H1 each of the cells will converge; H2 each of the models will drive to a different set of attractors (may have some overlap); H3 the captioner will dominate the source of attractors for these models. The operational thresholds above are Claude's and stand as written.*

*Note added 2026-10-19, before any Hunyuan run: Hunyuan-DiT runs at 25 steps with torch.compile instead of its 50-step default (D12 amendment, for cost); the E1-cap pilot (SDXL + Qwen) was already running. No prediction above changes.*

*Note added 2026-10-19, before any E1 core endpoint existed (E1-gen core at roughly step 40; its status-page frames and the E1-cap pilot had been looked at). Brad, in his words: "My speculation is that escape hazard tracks the attractor. The assumption is that attractors are more likely to track the captioner … the first glance at the e1_cap_pilot and the e1_gen images suggest that there are mixes between the captioner and the generator in the final matrix. The hypothesis is that more attractors will track to the captioner." Claude's alternative, stated the same day: for a shared attractor, escape hazard tracks the captioner. Operational test, using `analysis/gravity.py` with one fixed radius (0.20 DINOv2 cosine) and the A0 archive attractors plus each cell's own attractors as probes: for every attractor present in two or more cells, compare per-step escape hazard across the same-captioner pairs (A0/E1-gen, E1-cap/E1-both), the same-generator pairs (A0/E1-cap, E1-gen/E1-both) and the nothing-shared pair (A0/E1-both). Brad's claim holds if hazards agree within a factor of 2 across all pairs; Claude's holds if they agree only within a captioner. H3 ("more attractors track the captioner") is a count over endpoint attractors, separate from hazard, and stands as written.*

## A0-photo (SPEC3 §3: A0-core with the instruction's first sentence changed to "Describe this image as a realistic photograph, in plain, precise terms."; baseline for E6) — recorded 2026-10-20, before any run
- Brad (SPEC3, 2026-10-19): it converges at least as hard as A0, toward stock-photography attractors, since "photograph" points straight at the stock-heavy part of the training data.
- Claude: convergence and plateau unchanged (plateau by step 25, knee k in 6-10 under the elbow-table rule); Vendi within 20% of A0-core's 31.8. Attractor set shifts toward architecture, street and landscape photography; the gold-and-blue salon basin shrinks below half its A0 size; the cathedral persists (it has survived every change so far). Caption style vocabulary ("vibrant", "painted", "ethereal") falls from about 55% of A0-core captions to under 25%, and photographic vocabulary rises. People drain out of the loop at a similar rate to A0 (caption mentions of people halving by about step 25).
- A0-lit (instruction "Describe this image." + the verbatim remainder; not scheduled): if run, Claude expects it between A0-core and A0-photo on every measure above, closer to A0-photo, because LLaVA's own default register is descriptive rather than artistic.
