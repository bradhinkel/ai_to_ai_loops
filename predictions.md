# Pre-registered predictions

Write each prediction before its arm runs. Never edit an entry after results exist; add a dated note instead.

## A0 (replication, llava:13b) — recorded 2026-10-16 by Brad
We will get similar results to Hintze: there should be about 12 resulting image attractors, and these should match the descriptions from Hintze (the same general images, lighthouses, urban night scenes, gothic cathedrals, palatial interiors and so on), but not a pixel match.

Quantified for the A0-core gate (SPEC §4.3), added by Claude with Brad's wording above as the source:
- Pooled elbow-optimal k on step-100 MiniLM caption embeddings lands in 10–16, with 12 as the point estimate.
- Most clusters (at least 8 of them) are visually recognisable as one of Hintze's named motifs on the contact sheets.
- Step-to-step cosine distance plateaus by about step 20–25, as in the paper.
- No cluster is a pixel-level or near-duplicate match to Hintze's images; the match is at the motif level only.

## A0-S (Sonnet captioner) — recorded 2026-10-16 by Brad
- H1 (converges to a small attractor set): expected to hold.
- H2 (same attractors as llava:13b): expected to FAIL; Sonnet's attractors will differ.

## Evaluation panels (SPEC §7b): PROPOSED by Claude, 2026-10-16. Brad to confirm or amend before the panel runs.
- P1: artist-panel agreement is higher than lay-panel agreement (expertise is a shared standard, not just individual taste).
- P2: the lay panel rates the A0 attractor images (lighthouses, cathedrals) as more interesting than the artist panel does.
- P3: preference models (PickScore, ImageReward, HPSv2) correlate more with the lay panel than with the artists; VLM-rubric raters fall in between; no AI rater matches the artists as well as the artists match each other.
- P4: the artist panel's interest peaks at higher novelty than the lay panel's.
