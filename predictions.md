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
