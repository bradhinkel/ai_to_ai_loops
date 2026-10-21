# Persistent-attractor atlas (minilm): joint k = 40 over all 49500 intermediate steps of a0_core, e1_cap, e1_gen, e1_both, a0_s

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories); a0_s = sonnet + sdxl (n 100 trajectories).
Membership: nearest centroid within radius 0.15 (minilm cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (10 of 40) are transit states and omitted. Names from `archive/persistent_atlas_minilm_s_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | e1_cap | e1_gen | e1_both | a0_s | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|---|
| 0 |  | 0 / 0 / 0 / - / - | 85 / 27 / 16 / 9 / 0.19 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.70 | 0 / 0 / 0 / - / 1.00 | pair: qwen + sdxl | 0.0 |
| 15 |  | 67 / 41 / 41 / 40 / 0.02 | 0 / 0 / 0 / - / 1.00 | 10 / 5 / 2 / 20 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 2 |  | 23 / 11 / 11 / 26 / 0.03 | 6 / 5 / 1 / 7 / 0.34 | 28 / 15 / 13 / 22 / 0.05 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 16 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 41 / 14 / 5 / 13 / 0.12 | pair: sonnet + sdxl | 0.0 |
| 5 |  | 0 / 0 / 0 / - / - | 21 / 10 / 5 / 11 / 0.19 | 0 / 0 / 0 / - / - | 18 / 13 / 3 / 11 / 0.16 | 0 / 0 / 0 / - / 0.75 | captioner: qwen | 0.0 |
| 26 |  | 3 / 3 / 0 / 6 / 0.22 | 31 / 9 / 7 / 10 / 0.13 | 0 / 0 / 0 / - / - | 4 / 2 / 0 / 7 / 0.29 | 0 / 0 / 0 / - / 0.75 | mixed | 0.0 |
| 18 |  | 28 / 11 / 4 / 9 / 0.23 | 0 / 0 / 0 / - / - | 9 / 5 / 0 / 12 / 0.13 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 14 |  | 0 / 0 / 0 / - / 1.00 | 2 / 2 / 1 / 6 / 0.53 | 1 / 1 / 0 / 9 / 0.43 | 32 / 13 / 6 / 9 / 0.32 | 0 / 0 / 0 / - / - | pair: qwen + hunyuan | 0.0 |
| 11 |  | 0 / 0 / 0 / - / - | 12 / 6 / 6 / 7 / 0.29 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 20 / 8 / 2 / 8 / 0.25 | mixed | 0.0 |
| 38 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.67 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 28 / 15 / 10 / 27 / 0.03 | pair: sonnet + sdxl | 0.0 |
| 12 |  | 0 / 0 / 0 / - / - | 0 / 0 / 1 / - / 0.79 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.80 | 27 / 13 / 1 / 9 / 0.25 | pair: sonnet + sdxl | 0.0 |
| 34 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 27 / 15 / 9 / 7 / 0.29 | pair: sonnet + sdxl | 0.0 |
| 32 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 26 / 14 / 8 / 18 / 0.10 | pair: sonnet + sdxl | 0.0 |
| 39 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 24 / 10 / 2 / 14 / 0.10 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 36 |  | 0 / 0 / 0 / - / 0.58 | 20 / 9 / 7 / 18 / 0.08 | 0 / 0 / 0 / - / 0.50 | 2 / 1 / 1 / 11 / 0.08 | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.0 |
| 10 |  | 16 / 5 / 1 / 11 / 0.15 | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 9 / 0.35 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.0 |
| 23 |  | 9 / 2 / 2 / 17 / 0.06 | 0 / 0 / 0 / - / - | 9 / 3 / 2 / 13 / 0.14 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 35 |  | 4 / 2 / 1 / 6 / 0.42 | 0 / 0 / 0 / - / - | 12 / 8 / 1 / 9 / 0.28 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 13 |  | 5 / 3 / 2 / 20 / 0.04 | 0 / 0 / 0 / - / - | 10 / 5 / 4 / 21 / 0.07 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 6 |  | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.52 | 13 / 6 / 3 / 7 / 0.29 | 0 / 0 / 0 / - / - | pair: qwen + hunyuan | 0.0 |
| 25 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 13 / 6 / 0 / 7 / 0.27 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 1 |  | 3 / 3 / 1 / 11 / 0.35 | 0 / 0 / 0 / - / - | 7 / 4 / 1 / 12 / 0.23 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 27 |  | 0 / 0 / 0 / - / - | 2 / 2 / 1 / 6 / 0.43 | 0 / 0 / 0 / - / - | 4 / 2 / 1 / 15 / 0.12 | 2 / 2 / 0 / 6 / 0.39 | pair: qwen + hunyuan | 0.0 |
| 20 |  | 7 / 3 / 0 / 10 / 0.20 | 0 / 0 / 0 / - / 0.58 | 0 / 0 / 0 / - / 0.57 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.80 | pair: llava + sdxl | 0.0 |
| 30 |  | 0 / 0 / 0 / - / 0.61 | 0 / 0 / 0 / - / - | 7 / 6 / 1 / 8 / 0.30 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 7 |  | 2 / 1 / 0 / 14 / 0.21 | 2 / 1 / 0 / 19 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 1 / 0 / 41 / 0.02 | none (below threshold everywhere) | 0.0 |
| 8 |  | 1 / 1 / 0 / 5 / 0.44 | 0 / 0 / 0 / - / - | 4 / 4 / 0 / 8 / 0.33 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 19 |  | 4 / 1 / 1 / 20 / 0.07 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.41 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.0 |
| 9 |  | 0 / 0 / 0 / - / 0.83 | 0 / 0 / 0 / - / 0.56 | 0 / 0 / 0 / - / 0.44 | 1 / 1 / 0 / 7 / 0.35 | 1 / 1 / 0 / 5 / 0.44 | none (below threshold everywhere) | 0.0 |
| 31 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.91 | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 5 / 0.67 | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 15 |  | 77 (67, 10) | 43 | captioner: llava |
| 2 |  | 51 (23, 28) | 24 | mixed |
| 18 |  | 37 (28, 9) | 4 | captioner: llava |
| 39 |  | 24 (0, 24) | 2 | pair: llava + hunyuan |
| 10 |  | 18 (16, 2) | 1 | pair: llava + sdxl |
| 23 |  | 18 (9, 9) | 4 | captioner: llava |
| 35 |  | 16 (4, 12) | 2 | captioner: llava |
| 13 |  | 15 (5, 10) | 6 | captioner: llava |
| 25 |  | 13 (0, 13) | 0 | pair: llava + hunyuan |
| 1 |  | 10 (3, 7) | 2 | captioner: llava |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 0 |  | 85 (85, 0) | 16 | pair: qwen + sdxl |
| 5 |  | 39 (21, 18) | 8 | captioner: qwen |
| 26 |  | 35 (31, 4) | 7 | mixed |
| 14 |  | 34 (2, 32) | 7 | pair: qwen + hunyuan |
| 36 |  | 22 (20, 2) | 8 | pair: qwen + sdxl |
| 6 |  | 13 (0, 13) | 3 | pair: qwen + hunyuan |
| 11 |  | 12 (12, 0) | 6 | mixed |
| 2 |  | 6 (6, 0) | 1 | mixed |
| 27 |  | 6 (2, 4) | 2 | pair: qwen + hunyuan |
| 7 |  | 2 (2, 0) | 0 | none (below threshold everywhere) |

### captioner sonnet

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 16 |  | 41 (41) | 5 | pair: sonnet + sdxl |
| 38 |  | 28 (28) | 10 | pair: sonnet + sdxl |
| 12 |  | 27 (27) | 1 | pair: sonnet + sdxl |
| 34 |  | 27 (27) | 9 | pair: sonnet + sdxl |
| 32 |  | 26 (26) | 8 | pair: sonnet + sdxl |
| 11 |  | 20 (20) | 2 | mixed |
| 27 |  | 2 (2) | 0 | pair: qwen + hunyuan |
| 7 |  | 2 (2) | 0 | none (below threshold everywhere) |
| 9 |  | 1 (1) | 0 | none (below threshold everywhere) |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 14 |  | 33 (1, 32) | 6 | pair: qwen + hunyuan |
| 2 |  | 28 (28, 0) | 13 | mixed |
| 39 |  | 24 (24, 0) | 2 | pair: llava + hunyuan |
| 5 |  | 18 (0, 18) | 3 | captioner: qwen |
| 6 |  | 14 (1, 13) | 3 | pair: qwen + hunyuan |
| 25 |  | 13 (13, 0) | 0 | pair: llava + hunyuan |
| 35 |  | 12 (12, 0) | 1 | captioner: llava |
| 15 |  | 10 (10, 0) | 2 | captioner: llava |
| 13 |  | 10 (10, 0) | 4 | captioner: llava |
| 18 |  | 9 (9, 0) | 0 | captioner: llava |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 0 |  | 85 (0, 85, 0) | 16 | pair: qwen + sdxl |
| 15 |  | 67 (67, 0, 0) | 41 | captioner: llava |
| 16 |  | 41 (0, 0, 41) | 5 | pair: sonnet + sdxl |
| 26 |  | 34 (3, 31, 0) | 7 | mixed |
| 11 |  | 32 (0, 12, 20) | 8 | mixed |
| 2 |  | 29 (23, 6, 0) | 12 | mixed |
| 18 |  | 28 (28, 0, 0) | 4 | captioner: llava |
| 38 |  | 28 (0, 0, 28) | 10 | pair: sonnet + sdxl |
| 12 |  | 27 (0, 0, 27) | 2 | pair: sonnet + sdxl |
| 34 |  | 27 (0, 0, 27) | 9 | pair: sonnet + sdxl |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 15 |  | 67 (67) | 41 | captioner: llava |
| 18 |  | 28 (28) | 4 | captioner: llava |
| 2 |  | 23 (23) | 11 | mixed |
| 10 |  | 16 (16) | 1 | pair: llava + sdxl |
| 23 |  | 9 (9) | 2 | captioner: llava |
| 20 |  | 7 (7) | 0 | pair: llava + sdxl |
| 13 |  | 5 (5) | 2 | captioner: llava |
| 35 |  | 4 (4) | 1 | captioner: llava |
| 19 |  | 4 (4) | 1 | pair: llava + sdxl |
| 26 |  | 3 (3) | 0 | mixed |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 0 |  | 85 (85) | 16 | pair: qwen + sdxl |
| 26 |  | 31 (31) | 7 | mixed |
| 5 |  | 21 (21) | 5 | captioner: qwen |
| 36 |  | 20 (20) | 7 | pair: qwen + sdxl |
| 11 |  | 12 (12) | 6 | mixed |
| 2 |  | 6 (6) | 1 | mixed |
| 14 |  | 2 (2) | 1 | pair: qwen + hunyuan |
| 27 |  | 2 (2) | 1 | pair: qwen + hunyuan |
| 7 |  | 2 (2) | 0 | none (below threshold everywhere) |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 2 |  | 28 (28) | 13 | mixed |
| 39 |  | 24 (24) | 2 | pair: llava + hunyuan |
| 25 |  | 13 (13) | 0 | pair: llava + hunyuan |
| 35 |  | 12 (12) | 1 | captioner: llava |
| 15 |  | 10 (10) | 2 | captioner: llava |
| 13 |  | 10 (10) | 4 | captioner: llava |
| 18 |  | 9 (9) | 0 | captioner: llava |
| 23 |  | 9 (9) | 2 | captioner: llava |
| 1 |  | 7 (7) | 1 | captioner: llava |
| 30 |  | 7 (7) | 1 | pair: llava + hunyuan |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 14 |  | 32 (32) | 6 | pair: qwen + hunyuan |
| 5 |  | 18 (18) | 3 | captioner: qwen |
| 6 |  | 13 (13) | 3 | pair: qwen + hunyuan |
| 26 |  | 4 (4) | 0 | mixed |
| 27 |  | 4 (4) | 1 | pair: qwen + hunyuan |
| 36 |  | 2 (2) | 1 | pair: qwen + sdxl |
| 9 |  | 1 (1) | 0 | none (below threshold everywhere) |
| 31 |  | 1 (1) | 1 | none (below threshold everywhere) |

### pair sonnet + sdxl (a0_s)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 16 |  | 41 (41) | 5 | pair: sonnet + sdxl |
| 38 |  | 28 (28) | 10 | pair: sonnet + sdxl |
| 12 |  | 27 (27) | 1 | pair: sonnet + sdxl |
| 34 |  | 27 (27) | 9 | pair: sonnet + sdxl |
| 32 |  | 26 (26) | 8 | pair: sonnet + sdxl |
| 11 |  | 20 (20) | 2 | mixed |
| 27 |  | 2 (2) | 0 | pair: qwen + hunyuan |
| 7 |  | 2 (2) | 0 | none (below threshold everywhere) |
| 9 |  | 1 (1) | 0 | none (below threshold everywhere) |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 47% | 64% | 1.72 | 16 |
| e1_cap | 27% | 45% | 1.81 | 8 |
| e1_gen | 26% | 26% | 1.38 | 10 |
| e1_both | 11% | 15% | 0.75 | 7 |
| a0_s | 31% | 35% | 1.74 | 9 |
