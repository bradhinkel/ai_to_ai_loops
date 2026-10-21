# Persistent-attractor atlas (dinov2): joint k = 40 over all 59400 intermediate steps of a0_core, a0_core2, a0_photo, e1_cap, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); a0_core2 = llava + sdxl (n 100 trajectories); a0_photo = llava-photo + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories).
Membership: nearest centroid within radius 0.2 (dinov2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (13 of 40) are transit states and omitted. Names from `archive/persistent_atlas_rep_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | a0_core2 | a0_photo | e1_cap | e1_gen | e1_both | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 80 / 37 / 19 / 11 / 0.15 | 87 / 38 / 16 / 12 / 0.12 | 78 / 26 / 18 / 12 / 0.13 | 6 / 4 / 2 / 8 / 0.31 | 0 / 0 / 0 / - / 0.47 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 22 | white-and-gold salon / ballroom | 58 / 29 / 8 / 10 / 0.18 | 69 / 31 / 13 / 9 / 0.16 | 5 / 5 / 0 / 7 / 0.35 | 44 / 20 / 6 / 12 / 0.13 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 4 | gothic cathedral nave | 20 / 11 / 11 / 29 / 0.02 | 14 / 10 / 9 / 39 / 0.01 | 21 / 12 / 12 / 29 / 0.02 | 15 / 7 / 2 / 17 / 0.09 | 24 / 13 / 8 / 8 / 0.28 | 2 / 1 / 0 / 5 / 0.20 | all but e1_both | 0.0 |
| 25 | ballerinas and dancers | 7 / 2 / 1 / 13 / 0.08 | 7 / 2 / 0 / 10 / 0.13 | 5 / 1 / 1 / 12 / 0.09 | 0 / 0 / 0 / - / - | 15 / 4 / 2 / 13 / 0.13 | 33 / 16 / 7 / 17 / 0.09 | all but e1_cap | 0.0 |
| 24 | luxury canopy bedroom | 30 / 16 / 8 / 12 / 0.11 | 21 / 11 / 5 / 9 / 0.18 | 0 / 0 / 0 / - / 0.40 | 6 / 3 / 0 / 7 / 0.25 | 5 / 1 / 1 / 12 / 0.12 | 0 / 0 / 1 / - / 0.33 | mixed | 0.0 |
| 17 | lone tree in a mirror lake | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / 0.33 | 0 / 0 / 0 / - / - | 24 / 10 / 5 / 12 / 0.14 | 0 / 0 / 0 / - / - | 17 / 10 / 3 / 9 / 0.26 | captioner: qwen | 0.0 |
| 16 | modern fitted kitchen (stock) | 2 / 1 / 1 / 7 / 0.19 | 14 / 3 / 2 / 8 / 0.21 | 23 / 7 / 5 / 9 / 0.17 | 0 / 0 / 0 / - / - | 0 / 0 / 1 / - / 0.67 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 10 | pink-and-gold banquet hall | 1 / 1 / 2 / 6 / 0.54 | 2 / 2 / 2 / 6 / 0.43 | 2 / 2 / 0 / 5 / 0.62 | 27 / 15 / 12 / 19 / 0.07 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.0 |
| 15 | luxury bathroom | 3 / 3 / 0 / 8 / 0.28 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 22 / 9 / 8 / 18 / 0.07 | 0 / 0 / 0 / - / - | 4 / 2 / 2 / 13 / 0.13 | mixed | 0.0 |
| 32 | gnarled old tree in mist | 0 / 0 / 0 / - / 0.38 | 6 / 2 / 1 / 14 / 0.14 | 0 / 0 / 0 / - / - | 20 / 12 / 8 / 18 / 0.11 | 0 / 0 / 0 / - / 0.40 | 1 / 1 / 0 / 6 / 0.20 | mixed | 0.0 |
| 19 |  | 5 / 2 / 0 / 11 / 0.14 | 2 / 2 / 0 / 10 / 0.18 | 4 / 2 / 1 / 11 / 0.17 | 0 / 0 / 0 / - / - | 15 / 7 / 4 / 17 / 0.08 | 0 / 0 / 0 / - / 1.00 | mixed | 0.0 |
| 23 |  | 16 / 9 / 4 / 12 / 0.12 | 7 / 4 / 3 / 10 / 0.19 | 1 / 1 / 0 / 9 / 0.11 | 2 / 1 / 0 / 7 / 0.22 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 39 |  | 8 / 2 / 1 / 8 / 0.24 | 9 / 2 / 0 / 10 / 0.18 | 1 / 1 / 0 / 9 / 0.18 | 0 / 0 / 0 / - / 1.00 | 8 / 2 / 2 / 10 / 0.11 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 18 | East Asian garden, pagoda, Fuji | 5 / 4 / 1 / 8 / 0.31 | 0 / 0 / 0 / - / 0.45 | 0 / 0 / 0 / - / 0.67 | 17 / 8 / 8 / 22 / 0.05 | 0 / 0 / 0 / - / 1.00 | 2 / 2 / 1 / 8 / 0.17 | mixed | 0.0 |
| 31 | desert dunes | 6 / 2 / 0 / 20 / 0.09 | 2 / 1 / 0 / 10 / 0.15 | 0 / 0 / 0 / - / 0.33 | 11 / 4 / 0 / 17 / 0.10 | 1 / 1 / 0 / 5 / 0.55 | 1 / 1 / 0 / 6 / 0.40 | mixed | 0.0 |
| 9 |  | 6 / 5 / 0 / 7 / 0.30 | 5 / 3 / 0 / 10 / 0.22 | 4 / 3 / 0 / 6 / 0.30 | 0 / 0 / 0 / - / 0.58 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.57 | mixed | 0.0 |
| 27 | stained-glass saints | 1 / 1 / 0 / 7 / 0.55 | 4 / 3 / 0 / 7 / 0.27 | 1 / 1 / 0 / 5 / 0.30 | 0 / 0 / 0 / - / 0.33 | 8 / 4 / 1 / 14 / 0.19 | 0 / 0 / 0 / - / 0.52 | captioner: llava | 0.0 |
| 28 | supermarket produce aisle | 1 / 1 / 0 / 8 / 0.12 | 1 / 1 / 0 / 7 / 0.14 | 9 / 4 / 3 / 22 / 0.04 | 0 / 0 / 0 / - / - | 3 / 2 / 0 / 5 / 0.26 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 34 | cosmic vortex with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 8 / 4 / 2 / 10 / 0.23 | pair: qwen + hunyuan | 0.0 |
| 38 |  | 0 / 0 / 0 / - / - | 3 / 1 / 1 / 22 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 3 / 2 / 2 / 51 / 0.02 | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 30 |  | 1 / 1 / 0 / 5 / 0.20 | 3 / 2 / 0 / 6 / 0.34 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.0 |
| 26 | rainbow / neon tunnel with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 6 / 0.51 | 1 / 1 / 0 / 5 / 0.50 | none (below threshold everywhere) | 0.0 |
| 37 |  | 1 / 1 / 1 / 5 / 0.39 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 6 / 0.27 | 1 / 1 / 0 / 7 / 0.30 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |
| 12 |  | 1 / 1 / 0 / 5 / 0.61 | 0 / 0 / 0 / - / 0.72 | 0 / 0 / 2 / - / 0.57 | 0 / 0 / 0 / - / 0.69 | 1 / 1 / 0 / 8 / 0.40 | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |
| 7 |  | 1 / 1 / 0 / 6 / 0.44 | 0 / 0 / 0 / - / 0.86 | 0 / 0 / 0 / - / 0.75 | 0 / 0 / 0 / - / 0.33 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |
| 11 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.33 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | none (below threshold everywhere) | 0.0 |
| 21 | hooded figures in a misty forest | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.67 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.59 | none (below threshold everywhere) | 0.0 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 167 (80, 87, 0) | 35 | mixed |
| 22 | white-and-gold salon / ballroom | 127 (58, 69, 0) | 21 | mixed |
| 4 | gothic cathedral nave | 58 (20, 14, 24) | 28 | all but e1_both |
| 24 | luxury canopy bedroom | 56 (30, 21, 5) | 14 | mixed |
| 25 | ballerinas and dancers | 29 (7, 7, 15) | 3 | all but e1_cap |
| 39 |  | 25 (8, 9, 8) | 3 | mixed |
| 23 |  | 23 (16, 7, 0) | 7 | captioner: llava |
| 19 |  | 22 (5, 2, 15) | 4 | mixed |
| 16 | modern fitted kitchen (stock) | 16 (2, 14, 0) | 4 | mixed |
| 27 | stained-glass saints | 13 (1, 4, 8) | 1 | captioner: llava |

### captioner llava-photo

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 78 (78) | 18 | mixed |
| 16 | modern fitted kitchen (stock) | 23 (23) | 5 | mixed |
| 4 | gothic cathedral nave | 21 (21) | 12 | all but e1_both |
| 28 | supermarket produce aisle | 9 (9) | 3 | mixed |
| 22 | white-and-gold salon / ballroom | 5 (5) | 0 | mixed |
| 25 | ballerinas and dancers | 5 (5) | 1 | all but e1_cap |
| 19 |  | 4 (4) | 1 | mixed |
| 9 |  | 4 (4) | 0 | mixed |
| 10 | pink-and-gold banquet hall | 2 (2) | 0 | pair: qwen + sdxl |
| 23 |  | 1 (1) | 0 | captioner: llava |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 22 | white-and-gold salon / ballroom | 44 (44, 0) | 6 | mixed |
| 17 | lone tree in a mirror lake | 41 (24, 17) | 8 | captioner: qwen |
| 25 | ballerinas and dancers | 33 (0, 33) | 7 | all but e1_cap |
| 10 | pink-and-gold banquet hall | 27 (27, 0) | 12 | pair: qwen + sdxl |
| 15 | luxury bathroom | 26 (22, 4) | 10 | mixed |
| 32 | gnarled old tree in mist | 21 (20, 1) | 8 | mixed |
| 18 | East Asian garden, pagoda, Fuji | 19 (17, 2) | 9 | mixed |
| 4 | gothic cathedral nave | 17 (15, 2) | 2 | all but e1_both |
| 31 | desert dunes | 12 (11, 1) | 0 | mixed |
| 34 | cosmic vortex with a figure | 8 (0, 8) | 2 | pair: qwen + hunyuan |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 25 | ballerinas and dancers | 48 (15, 33) | 9 | all but e1_cap |
| 4 | gothic cathedral nave | 26 (24, 2) | 8 | all but e1_both |
| 17 | lone tree in a mirror lake | 17 (0, 17) | 3 | captioner: qwen |
| 19 |  | 15 (15, 0) | 4 | mixed |
| 39 |  | 8 (8, 0) | 2 | mixed |
| 27 | stained-glass saints | 8 (8, 0) | 1 | captioner: llava |
| 34 | cosmic vortex with a figure | 8 (0, 8) | 2 | pair: qwen + hunyuan |
| 24 | luxury canopy bedroom | 5 (5, 0) | 2 | mixed |
| 15 | luxury bathroom | 4 (0, 4) | 2 | mixed |
| 28 | supermarket produce aisle | 3 (3, 0) | 0 | mixed |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 251 (80, 87, 78, 6) | 55 | mixed |
| 22 | white-and-gold salon / ballroom | 176 (58, 69, 5, 44) | 27 | mixed |
| 4 | gothic cathedral nave | 70 (20, 14, 21, 15) | 34 | all but e1_both |
| 24 | luxury canopy bedroom | 57 (30, 21, 0, 6) | 13 | mixed |
| 16 | modern fitted kitchen (stock) | 39 (2, 14, 23, 0) | 8 | mixed |
| 10 | pink-and-gold banquet hall | 32 (1, 2, 2, 27) | 16 | pair: qwen + sdxl |
| 32 | gnarled old tree in mist | 26 (0, 6, 0, 20) | 9 | mixed |
| 23 |  | 26 (16, 7, 1, 2) | 7 | captioner: llava |
| 15 | luxury bathroom | 25 (3, 0, 0, 22) | 8 | mixed |
| 17 | lone tree in a mirror lake | 24 (0, 0, 0, 24) | 5 | captioner: qwen |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 80 (80) | 19 | mixed |
| 22 | white-and-gold salon / ballroom | 58 (58) | 8 | mixed |
| 24 | luxury canopy bedroom | 30 (30) | 8 | mixed |
| 4 | gothic cathedral nave | 20 (20) | 11 | all but e1_both |
| 23 |  | 16 (16) | 4 | captioner: llava |
| 39 |  | 8 (8) | 1 | mixed |
| 25 | ballerinas and dancers | 7 (7) | 1 | all but e1_cap |
| 31 | desert dunes | 6 (6) | 0 | mixed |
| 9 |  | 6 (6) | 0 | mixed |
| 19 |  | 5 (5) | 0 | mixed |

### pair llava + sdxl (a0_core2)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 87 (87) | 16 | mixed |
| 22 | white-and-gold salon / ballroom | 69 (69) | 13 | mixed |
| 24 | luxury canopy bedroom | 21 (21) | 5 | mixed |
| 4 | gothic cathedral nave | 14 (14) | 9 | all but e1_both |
| 16 | modern fitted kitchen (stock) | 14 (14) | 2 | mixed |
| 39 |  | 9 (9) | 0 | mixed |
| 25 | ballerinas and dancers | 7 (7) | 0 | all but e1_cap |
| 23 |  | 7 (7) | 3 | captioner: llava |
| 32 | gnarled old tree in mist | 6 (6) | 1 | mixed |
| 9 |  | 5 (5) | 0 | mixed |

### pair llava-photo + sdxl (a0_photo)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 78 (78) | 18 | mixed |
| 16 | modern fitted kitchen (stock) | 23 (23) | 5 | mixed |
| 4 | gothic cathedral nave | 21 (21) | 12 | all but e1_both |
| 28 | supermarket produce aisle | 9 (9) | 3 | mixed |
| 22 | white-and-gold salon / ballroom | 5 (5) | 0 | mixed |
| 25 | ballerinas and dancers | 5 (5) | 1 | all but e1_cap |
| 19 |  | 4 (4) | 1 | mixed |
| 9 |  | 4 (4) | 0 | mixed |
| 10 | pink-and-gold banquet hall | 2 (2) | 0 | pair: qwen + sdxl |
| 23 |  | 1 (1) | 0 | captioner: llava |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 22 | white-and-gold salon / ballroom | 44 (44) | 6 | mixed |
| 10 | pink-and-gold banquet hall | 27 (27) | 12 | pair: qwen + sdxl |
| 17 | lone tree in a mirror lake | 24 (24) | 5 | captioner: qwen |
| 15 | luxury bathroom | 22 (22) | 8 | mixed |
| 32 | gnarled old tree in mist | 20 (20) | 8 | mixed |
| 18 | East Asian garden, pagoda, Fuji | 17 (17) | 8 | mixed |
| 4 | gothic cathedral nave | 15 (15) | 2 | all but e1_both |
| 31 | desert dunes | 11 (11) | 0 | mixed |
| 1 | gold-and-blue palatial salon | 6 (6) | 2 | mixed |
| 24 | luxury canopy bedroom | 6 (6) | 0 | mixed |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 4 | gothic cathedral nave | 24 (24) | 8 | all but e1_both |
| 25 | ballerinas and dancers | 15 (15) | 2 | all but e1_cap |
| 19 |  | 15 (15) | 4 | mixed |
| 39 |  | 8 (8) | 2 | mixed |
| 27 | stained-glass saints | 8 (8) | 1 | captioner: llava |
| 24 | luxury canopy bedroom | 5 (5) | 1 | mixed |
| 28 | supermarket produce aisle | 3 (3) | 0 | mixed |
| 38 |  | 3 (3) | 2 | captioner: llava |
| 26 | rainbow / neon tunnel with a figure | 2 (2) | 0 | none (below threshold everywhere) |
| 31 | desert dunes | 1 (1) | 0 | mixed |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 25 | ballerinas and dancers | 33 (33) | 7 | all but e1_cap |
| 17 | lone tree in a mirror lake | 17 (17) | 3 | captioner: qwen |
| 34 | cosmic vortex with a figure | 8 (8) | 2 | pair: qwen + hunyuan |
| 15 | luxury bathroom | 4 (4) | 2 | mixed |
| 4 | gothic cathedral nave | 2 (2) | 0 | all but e1_both |
| 18 | East Asian garden, pagoda, Fuji | 2 (2) | 1 | mixed |
| 32 | gnarled old tree in mist | 1 (1) | 0 | mixed |
| 31 | desert dunes | 1 (1) | 0 | mixed |
| 26 | rainbow / neon tunnel with a figure | 1 (1) | 0 | none (below threshold everywhere) |
| 21 | hooded figures in a misty forest | 1 (1) | 0 | none (below threshold everywhere) |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 39% | 57% | 2.53 | 9 |
| a0_core2 | 37% | 52% | 2.56 | 9 |
| a0_photo | 26% | 42% | 1.55 | 9 |
| e1_cap | 36% | 51% | 1.96 | 11 |
| e1_gen | 15% | 21% | 0.85 | 8 |
| e1_both | 12% | 16% | 0.70 | 9 |
