# Seed memory curve

Seed identification at step k = share of trajectories whose step-k embedding is nearer to their own step-0 image/caption than to any other trajectory's (chance 1/n). Half-life = first step at or below 50%; lost = first step from which it never exceeds 2x chance. Excess self-similarity = mean cosine to own step 0 minus mean cosine to the others' step 0.

| run | space | ident. step 1 | 2 | 3 | 5 | 10 | 20 | 50 | 99 | half-life (step) | lost (step) | excess self-sim step 5 / 20 / 99 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a0_core | dinov2 | 0.79 | 0.66 | 0.51 | 0.41 | 0.20 | 0.12 | 0.12 | 0.08 | 4 | None | 0.249 / 0.095 / 0.041 |
| a0_core | minilm | 0.77 | 0.70 | 0.48 | 0.39 | 0.21 | 0.11 | 0.07 | 0.03 | 3 | None | 0.205 / 0.109 / 0.043 |
| e1_gen | dinov2 | 0.85 | 0.59 | 0.48 | 0.41 | 0.23 | 0.13 | 0.11 | 0.06 | 3 | None | 0.242 / 0.098 / 0.037 |
| e1_gen | minilm | 0.83 | 0.73 | 0.61 | 0.42 | 0.31 | 0.21 | 0.07 | 0.04 | 4 | None | 0.221 / 0.114 / 0.034 |
| e1_both | dinov2 | 0.90 | 0.68 | 0.52 | 0.43 | 0.26 | 0.12 | 0.06 | 0.07 | 5 | None | 0.234 / 0.096 / 0.031 |
| e1_both | minilm | 0.88 | 0.70 | 0.67 | 0.43 | 0.24 | 0.09 | 0.08 | 0.09 | 4 | None | 0.242 / 0.099 / 0.038 |

Figure: `memory_curve.png`.
