# Persistent-attractor atlas (minilm): joint k = 40 over all 39600 intermediate steps of a0_core, e1_cap, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories).
Membership: nearest centroid within radius 0.15 (minilm cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (5 of 40) are transit states and omitted. Names from `archive/persistent_atlas_minilm_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | e1_cap | e1_gen | e1_both | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|
| 5 |  | 67 / 41 / 40 / 40 / 0.02 | 0 / 0 / 0 / - / - | 10 / 5 / 2 / 20 / 0.08 | 0 / 0 / 0 / - / - | captioner: llava | 0.57 |
| 1 |  | 0 / 0 / 0 / - / - | 67 / 27 / 9 / 10 / 0.17 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.61 | pair: qwen + sdxl | 0.5 |
| 6 |  | 23 / 11 / 11 / 26 / 0.03 | 7 / 6 / 1 / 7 / 0.31 | 28 / 15 / 13 / 22 / 0.06 | 0 / 0 / 0 / - / 1.00 | all but e1_both | 0.96 |
| 4 |  | 0 / 0 / 0 / - / - | 23 / 10 / 5 / 11 / 0.19 | 0 / 0 / 0 / - / - | 18 / 13 / 3 / 12 / 0.17 | captioner: qwen | 0.89 |
| 2 |  | 28 / 11 / 5 / 10 / 0.22 | 0 / 0 / 0 / - / - | 11 / 5 / 0 / 9 / 0.17 | 0 / 0 / 0 / - / - | captioner: llava | 0.7 |
| 15 |  | 3 / 3 / 0 / 6 / 0.25 | 30 / 9 / 7 / 11 / 0.13 | 0 / 0 / 0 / - / - | 4 / 2 / 0 / 7 / 0.30 | all but e1_gen | 0.52 |
| 10 |  | 0 / 0 / 0 / - / - | 24 / 11 / 9 / 11 / 0.13 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.5 |
| 23 |  | 0 / 0 / 1 / - / 0.00 | 24 / 12 / 11 / 17 / 0.09 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.5 |
| 9 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 23 / 10 / 2 / 15 / 0.10 | 0 / 0 / 0 / - / 1.00 | pair: llava + hunyuan | 0.5 |
| 37 |  | 0 / 0 / 0 / - / 0.71 | 4 / 3 / 4 / 6 / 0.51 | 1 / 1 / 0 / 6 / 0.43 | 18 / 11 / 5 / 13 / 0.31 | captioner: qwen | 0.58 |
| 22 |  | 0 / 0 / 0 / - / - | 19 / 9 / 7 / 17 / 0.08 | 0 / 0 / 0 / - / - | 2 / 1 / 2 / 7 / 0.31 | pair: qwen + sdxl | 0.55 |
| 34 |  | 19 / 5 / 2 / 9 / 0.15 | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 12 / 0.33 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.53 |
| 36 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 20 / 9 / 4 / 15 / 0.15 | pair: qwen + hunyuan | 0.5 |
| 19 |  | 9 / 2 / 2 / 15 / 0.09 | 0 / 0 / 0 / - / - | 8 / 3 / 2 / 11 / 0.16 | 0 / 0 / 0 / - / - | captioner: llava | 0.94 |
| 17 |  | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 5 / 0.50 | 14 / 7 / 3 / 7 / 0.29 | pair: qwen + hunyuan | 0.46 |
| 28 |  | 5 / 3 / 2 / 20 / 0.04 | 0 / 0 / 0 / - / - | 10 / 5 / 4 / 21 / 0.07 | 0 / 0 / 0 / - / - | captioner: llava | 0.75 |
| 29 |  | 6 / 4 / 1 / 12 / 0.20 | 0 / 0 / 0 / - / - | 9 / 6 / 1 / 12 / 0.23 | 0 / 0 / 0 / - / - | captioner: llava | 0.83 |
| 7 |  | 11 / 7 / 0 / 15 / 0.13 | 0 / 0 / 0 / - / 1.00 | 2 / 2 / 1 / 8 / 0.16 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.59 |
| 21 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 13 / 6 / 0 / 7 / 0.27 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 20 |  | 3 / 1 / 0 / 6 / 0.23 | 0 / 0 / 0 / - / - | 9 / 5 / 2 / 15 / 0.10 | 0 / 0 / 0 / - / - | captioner: llava | 0.67 |
| 30 |  | 11 / 6 / 0 / 7 / 0.31 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / 0.40 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.5 |
| 32 |  | 1 / 1 / 0 / 7 / 0.60 | 0 / 0 / 0 / - / - | 10 / 7 / 1 / 7 / 0.34 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.55 |
| 14 |  | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 5 / 0.48 | 0 / 0 / 0 / - / - | 8 / 4 / 0 / 7 / 0.35 | pair: qwen + hunyuan | 0.62 |
| 3 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 8 / 7 / 1 / 6 / 0.50 | pair: qwen + hunyuan | 0.5 |
| 18 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 8 / 2 / 1 / 9 / 0.17 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 38 |  | 5 / 4 / 0 / 7 / 0.34 | 0 / 0 / 0 / - / 0.50 | 3 / 3 / 0 / 7 / 0.19 | 0 / 0 / 0 / - / 0.75 | captioner: llava | 0.8 |
| 0 |  | 2 / 1 / 0 / 15 / 0.16 | 5 / 1 / 1 / 16 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.3 |
| 27 |  | 0 / 0 / 0 / - / 0.65 | 0 / 0 / 0 / - / - | 7 / 6 / 1 / 8 / 0.30 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 8 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.53 | 0 / 0 / 0 / - / - | 6 / 3 / 2 / 9 / 0.26 | pair: qwen + hunyuan | 0.5 |
| 24 |  | 0 / 0 / 0 / - / - | 6 / 2 / 0 / 8 / 0.23 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.5 |
| 11 |  | 1 / 1 / 0 / 5 / 0.42 | 0 / 0 / 0 / - / - | 4 / 4 / 0 / 8 / 0.33 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.62 |
| 12 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 5 / 3 / 1 / 22 / 0.08 | pair: qwen + hunyuan | 0.5 |
| 13 |  | 0 / 0 / 1 / - / 0.50 | 3 / 2 / 0 / 7 / 0.38 | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 8 / 0.34 | pair: qwen + sdxl | 0.83 |
| 26 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 5 / 0.38 | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.5 |
| 31 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 1 / 1 / 2 / 5 / 0.51 | none (below threshold everywhere) | 0.5 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 5 |  | 77 (67, 10) | 42 | captioner: llava |
| 6 |  | 51 (23, 28) | 24 | all but e1_both |
| 2 |  | 39 (28, 11) | 5 | captioner: llava |
| 9 |  | 23 (0, 23) | 2 | pair: llava + hunyuan |
| 34 |  | 20 (19, 1) | 3 | pair: llava + sdxl |
| 19 |  | 17 (9, 8) | 4 | captioner: llava |
| 28 |  | 15 (5, 10) | 6 | captioner: llava |
| 29 |  | 15 (6, 9) | 2 | captioner: llava |
| 7 |  | 13 (11, 2) | 1 | pair: llava + sdxl |
| 21 |  | 13 (0, 13) | 0 | pair: llava + hunyuan |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 |  | 67 (67, 0) | 9 | pair: qwen + sdxl |
| 4 |  | 41 (23, 18) | 8 | captioner: qwen |
| 15 |  | 34 (30, 4) | 7 | all but e1_gen |
| 10 |  | 24 (24, 0) | 9 | pair: qwen + sdxl |
| 23 |  | 24 (24, 0) | 11 | pair: qwen + sdxl |
| 37 |  | 22 (4, 18) | 9 | captioner: qwen |
| 22 |  | 21 (19, 2) | 9 | pair: qwen + sdxl |
| 36 |  | 20 (0, 20) | 4 | pair: qwen + hunyuan |
| 17 |  | 14 (0, 14) | 3 | pair: qwen + hunyuan |
| 14 |  | 10 (2, 8) | 0 | pair: qwen + hunyuan |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 6 |  | 28 (28, 0) | 13 | all but e1_both |
| 9 |  | 23 (23, 0) | 2 | pair: llava + hunyuan |
| 36 |  | 20 (0, 20) | 4 | pair: qwen + hunyuan |
| 37 |  | 19 (1, 18) | 5 | captioner: qwen |
| 4 |  | 18 (0, 18) | 3 | captioner: qwen |
| 17 |  | 15 (1, 14) | 4 | pair: qwen + hunyuan |
| 21 |  | 13 (13, 0) | 0 | pair: llava + hunyuan |
| 2 |  | 11 (11, 0) | 0 | captioner: llava |
| 5 |  | 10 (10, 0) | 2 | captioner: llava |
| 28 |  | 10 (10, 0) | 4 | captioner: llava |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 5 |  | 67 (67, 0) | 40 | captioner: llava |
| 1 |  | 67 (0, 67) | 9 | pair: qwen + sdxl |
| 15 |  | 33 (3, 30) | 7 | all but e1_gen |
| 6 |  | 30 (23, 7) | 12 | all but e1_both |
| 2 |  | 28 (28, 0) | 5 | captioner: llava |
| 10 |  | 24 (0, 24) | 9 | pair: qwen + sdxl |
| 23 |  | 24 (0, 24) | 12 | pair: qwen + sdxl |
| 4 |  | 23 (0, 23) | 5 | captioner: qwen |
| 22 |  | 19 (0, 19) | 7 | pair: qwen + sdxl |
| 34 |  | 19 (19, 0) | 2 | pair: llava + sdxl |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 5 |  | 67 (67) | 40 | captioner: llava |
| 2 |  | 28 (28) | 5 | captioner: llava |
| 6 |  | 23 (23) | 11 | all but e1_both |
| 34 |  | 19 (19) | 2 | pair: llava + sdxl |
| 7 |  | 11 (11) | 0 | pair: llava + sdxl |
| 30 |  | 11 (11) | 0 | pair: llava + sdxl |
| 19 |  | 9 (9) | 2 | captioner: llava |
| 29 |  | 6 (6) | 1 | captioner: llava |
| 28 |  | 5 (5) | 2 | captioner: llava |
| 38 |  | 5 (5) | 0 | captioner: llava |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 |  | 67 (67) | 9 | pair: qwen + sdxl |
| 15 |  | 30 (30) | 7 | all but e1_gen |
| 10 |  | 24 (24) | 9 | pair: qwen + sdxl |
| 23 |  | 24 (24) | 11 | pair: qwen + sdxl |
| 4 |  | 23 (23) | 5 | captioner: qwen |
| 22 |  | 19 (19) | 7 | pair: qwen + sdxl |
| 6 |  | 7 (7) | 1 | all but e1_both |
| 24 |  | 6 (6) | 0 | pair: qwen + sdxl |
| 0 |  | 5 (5) | 1 | pair: qwen + sdxl |
| 37 |  | 4 (4) | 4 | captioner: qwen |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 6 |  | 28 (28) | 13 | all but e1_both |
| 9 |  | 23 (23) | 2 | pair: llava + hunyuan |
| 21 |  | 13 (13) | 0 | pair: llava + hunyuan |
| 2 |  | 11 (11) | 0 | captioner: llava |
| 5 |  | 10 (10) | 2 | captioner: llava |
| 28 |  | 10 (10) | 4 | captioner: llava |
| 32 |  | 10 (10) | 1 | pair: llava + hunyuan |
| 29 |  | 9 (9) | 1 | captioner: llava |
| 20 |  | 9 (9) | 2 | captioner: llava |
| 19 |  | 8 (8) | 2 | captioner: llava |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 36 |  | 20 (20) | 4 | pair: qwen + hunyuan |
| 4 |  | 18 (18) | 3 | captioner: qwen |
| 37 |  | 18 (18) | 5 | captioner: qwen |
| 17 |  | 14 (14) | 3 | pair: qwen + hunyuan |
| 14 |  | 8 (8) | 0 | pair: qwen + hunyuan |
| 3 |  | 8 (8) | 1 | pair: qwen + hunyuan |
| 8 |  | 6 (6) | 2 | pair: qwen + hunyuan |
| 12 |  | 5 (5) | 1 | pair: qwen + hunyuan |
| 15 |  | 4 (4) | 0 | all but e1_gen |
| 22 |  | 2 (2) | 2 | pair: qwen + sdxl |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 50% | 65% | 1.94 | 13 |
| e1_cap | 33% | 54% | 2.14 | 9 |
| e1_gen | 29% | 32% | 1.60 | 9 |
| e1_both | 19% | 23% | 1.06 | 8 |
