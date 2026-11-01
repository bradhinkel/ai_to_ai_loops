# E3-A: anonymised re-embedding control

Names and places (the gate's filter, per cell) replaced by "X"; MiniLM re-embedding; the same procedure on both columns (joint k-means k 40 per text kind, radius 0.15, hysteresis 1.25, dwell ≥ 5, ≥ 3 visits). nn-other = median cosine distance from each trajectory-step (steps ≥ 25) to the nearest step of any other trajectory in the cell; within = share of those ≤ 0.15; shared = persistent clusters visited by ≥ 2 trajectories. shift = median distance between a text's original and anonymised embedding.

| cell | text | names | tokens replaced | shift anon / rand | nn-other orig → anon / rand | within 0.15 orig → anon / rand | Vendi@99 orig → anon / rand | persistent (shared) orig → anon / rand | steps inside orig → anon / rand |
|---|---|---|---|---|---|---|---|---|---|
| e3_1_sonnet | stories | 577 | 36419 | 0.150 / 0.036 | 0.381 → 0.293 / 0.350 | 0.00 → 0.00 / 0.00 | 10.3 → 8.0 / 9.0 | 0 (0) → 1 (0) / 0 (0) | 0.00 → 0.03 / 0.00 |
| e3_1_sonnet | summaries | 577 | 6749 | 0.238 / 0.071 | 0.520 → 0.383 / 0.449 | 0.00 → 0.00 / 0.00 | 14.0 → 9.5 / 11.0 | 5 (0) → 5 (1) / 4 (0) | 0.19 → 0.19 / 0.13 |
| e3_2_sonnet | stories | 296 | 27677 | 0.125 / 0.032 | 0.468 → 0.390 / 0.431 | 0.00 → 0.00 / 0.00 | 11.4 → 9.0 / 10.3 | 0 (0) → 1 (0) / 2 (0) | 0.00 → 0.03 / 0.04 |
| e3_1_qwen | stories | 268 | 25944 | 0.159 / 0.032 | 0.369 → 0.264 / 0.341 | 0.00 → 0.01 / 0.00 | 12.2 → 9.5 / 11.3 | 0 (0) → 0 (0) / 0 (0) | 0.00 → 0.00 / 0.00 |
| e3_1_qwen | summaries | 268 | 5168 | 0.244 / 0.057 | 0.450 → 0.328 / 0.403 | 0.00 → 0.01 / 0.00 | 13.8 → 10.4 / 12.3 | 2 (0) → 3 (2) / 4 (0) | 0.06 → 0.08 / 0.13 |
| e3_2_qwen | stories | 45 | 7199 | 0.087 / 0.024 | 0.469 → 0.431 / 0.457 | 0.00 → 0.00 / 0.00 | 13.1 → 11.1 / 12.1 | 3 (0) → 2 (0) / 2 (0) | 0.11 → 0.05 / 0.07 |
| e3_1_llava | stories | 106 | 21444 | 0.181 / 0.038 | 0.409 → 0.305 / 0.374 | 0.00 → 0.02 / 0.00 | 11.6 → 8.4 / 10.2 | 0 (0) → 2 (1) / 1 (0) | 0.00 → 0.07 / 0.02 |
| e3_1_llava | summaries | 106 | 4727 | 0.283 / 0.044 | 0.440 → 0.313 / 0.408 | 0.00 → 0.05 / 0.00 | 13.1 → 9.0 / 11.9 | 4 (0) → 6 (1) / 5 (0) | 0.10 → 0.21 / 0.13 |
| e3_2_llava | stories | 18 | 3488 | 0.000 / 0.000 | 0.561 → 0.485 / 0.533 | 0.00 → 0.00 / 0.00 | 15.3 → 14.0 / 15.0 | 2 (0) → 4 (0) / 3 (0) | 0.07 → 0.13 / 0.10 |

**A1 (fails as written)**: largest fall in nn-other 0.137 (e3_1_sonnet, summaries); largest names-specific fall beyond the random-replacement null 0.096. Shared persistent attractors in E3-1 cells, anonymised / null: e3_1_sonnet stories 0 / 0, e3_1_sonnet summaries 1 / 0, e3_1_qwen stories 0 / 0, e3_1_qwen summaries 2 / 0, e3_1_llava stories 1 / 0, e3_1_llava summaries 1 / 0. A1 as written: fall >= 0.10 or any shared attractor in an E3-1 cell -> names were the barrier. The rand column is the null added after the first pass (same token budget, random content words): the names-specific effect is anon minus rand.

Shared-cluster texts: `anon_clusters.md`.
