# Persistent-attractor atlas (dinov2): joint k = 40 over all 49500 intermediate steps of a0_core, a0_photo, e1_cap, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); a0_photo = llava-photo + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories).
Membership: nearest centroid within radius 0.2 (dinov2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (12 of 40) are transit states and omitted. Names from `archive/persistent_atlas_photo_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | a0_photo | e1_cap | e1_gen | e1_both | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|---|
| 39 | white-and-gold salon / ballroom | 99 / 37 / 19 / 10 / 0.14 | 15 / 13 / 2 / 7 / 0.29 | 47 / 21 / 7 / 12 / 0.12 | 0 / 0 / 0 / - / 0.75 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 7 | gold-and-blue palatial salon | 52 / 32 / 7 / 9 / 0.21 | 83 / 26 / 17 / 10 / 0.15 | 1 / 1 / 1 / 5 / 0.49 | 2 / 1 / 0 / 10 / 0.31 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 8 | gothic cathedral nave | 20 / 11 / 11 / 29 / 0.02 | 22 / 12 / 12 / 27 / 0.02 | 15 / 7 / 2 / 18 / 0.08 | 28 / 13 / 8 / 8 / 0.26 | 2 / 1 / 0 / 5 / 0.20 | all but e1_both | 0.0 |
| 5 | ballerinas and dancers | 7 / 2 / 1 / 12 / 0.09 | 5 / 1 / 1 / 12 / 0.09 | 0 / 0 / 0 / - / - | 15 / 4 / 2 / 12 / 0.14 | 32 / 16 / 7 / 18 / 0.09 | all but e1_cap | 0.0 |
| 3 | lone tree in a mirror lake | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 23 / 10 / 5 / 13 / 0.14 | 0 / 0 / 0 / - / 1.00 | 17 / 10 / 3 / 9 / 0.26 | captioner: qwen | 0.0 |
| 20 | luxury canopy bedroom | 26 / 15 / 7 / 13 / 0.12 | 0 / 0 / 0 / - / 0.40 | 6 / 3 / 0 / 7 / 0.24 | 5 / 1 / 1 / 12 / 0.11 | 0 / 0 / 1 / - / 0.25 | mixed | 0.0 |
| 22 | luxury bathroom | 3 / 3 / 0 / 8 / 0.28 | 0 / 0 / 0 / - / - | 22 / 9 / 8 / 18 / 0.07 | 0 / 0 / 0 / - / - | 4 / 2 / 2 / 13 / 0.14 | mixed | 0.0 |
| 4 | pink-and-gold banquet hall | 1 / 1 / 2 / 5 / 0.55 | 1 / 1 / 0 / 5 / 0.69 | 26 / 15 / 12 / 20 / 0.07 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.0 |
| 0 | modern fitted kitchen (stock) | 2 / 1 / 1 / 7 / 0.18 | 23 / 7 / 5 / 10 / 0.15 | 0 / 0 / 0 / - / - | 0 / 0 / 1 / - / 0.67 | 0 / 0 / 0 / - / - | pair: llava-photo + sdxl | 0.0 |
| 19 | rainbow / neon tunnel with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 20 / 7 / 2 / 14 / 0.13 | 4 / 2 / 0 / 6 / 0.24 | mixed | 0.0 |
| 29 |  | 5 / 2 / 0 / 10 / 0.16 | 4 / 2 / 1 / 11 / 0.16 | 0 / 0 / 0 / - / - | 15 / 7 / 4 / 17 / 0.08 | 0 / 0 / 0 / - / 1.00 | mixed | 0.0 |
| 31 | East Asian garden, pagoda, Fuji | 5 / 4 / 1 / 7 / 0.31 | 0 / 0 / 0 / - / 0.67 | 17 / 8 / 8 / 22 / 0.05 | 0 / 0 / 0 / - / 1.00 | 2 / 2 / 1 / 8 / 0.17 | mixed | 0.0 |
| 25 | gnarled old tree in mist | 0 / 0 / 0 / - / 0.38 | 0 / 0 / 0 / - / - | 21 / 13 / 8 / 17 / 0.12 | 0 / 0 / 0 / - / 0.40 | 1 / 1 / 0 / 6 / 0.20 | pair: qwen + sdxl | 0.0 |
| 24 | lighthouse in a storm | 7 / 2 / 1 / 13 / 0.10 | 9 / 2 / 1 / 12 / 0.13 | 1 / 1 / 0 / 35 / 0.05 | 4 / 2 / 0 / 7 / 0.25 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 30 | desert dunes | 6 / 3 / 0 / 20 / 0.07 | 0 / 0 / 0 / - / 1.00 | 13 / 5 / 1 / 16 / 0.10 | 1 / 1 / 0 / 5 / 0.44 | 1 / 1 / 0 / 7 / 0.35 | mixed | 0.0 |
| 35 | supermarket produce aisle | 1 / 1 / 0 / 7 / 0.14 | 9 / 4 / 3 / 24 / 0.03 | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 8 / 0.22 | 0 / 0 / 0 / - / - | pair: llava-photo + sdxl | 0.0 |
| 33 | stained-glass saints | 1 / 1 / 0 / 7 / 0.56 | 1 / 1 / 0 / 5 / 0.30 | 0 / 0 / 0 / - / 0.40 | 8 / 4 / 1 / 14 / 0.19 | 1 / 1 / 0 / 5 / 0.42 | pair: llava + hunyuan | 0.0 |
| 17 | cosmic vortex with a figure | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 1 / - / 0.47 | 0 / 0 / 0 / - / - | 10 / 5 / 3 / 22 / 0.08 | pair: qwen + hunyuan | 0.0 |
| 21 |  | 3 / 1 / 0 / 11 / 0.20 | 3 / 1 / 0 / 13 / 0.12 | 2 / 1 / 1 / 48 / 0.01 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 27 | Native American portraits in feather headdress (vintage photo) | 1 / 1 / 0 / 24 / 0.08 | 7 / 3 / 3 / 23 / 0.03 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava-photo + sdxl | 0.0 |
| 26 | robots and mechs | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 6 / 4 / 3 / 6 / 0.36 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 13 |  | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.33 | 0 / 0 / 0 / - / - | 4 / 2 / 1 / 8 / 0.39 | pair: qwen + hunyuan | 0.0 |
| 16 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.33 | 5 / 5 / 1 / 6 / 0.31 | pair: qwen + hunyuan | 0.0 |
| 32 | boxers in a ring | 2 / 1 / 0 / 37 / 0.08 | 1 / 1 / 0 / 62 / 0.02 | 1 / 1 / 0 / 56 / 0.02 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |
| 9 | figure with raised arms in a light burst | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 3 / 2 / 1 / 6 / 0.47 | pair: qwen + hunyuan | 0.0 |
| 10 | hooded figures in a misty forest | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.62 | 0 / 0 / 0 / - / - | 3 / 3 / 0 / 6 / 0.42 | pair: qwen + hunyuan | 0.0 |
| 34 |  | 0 / 0 / 0 / - / 0.60 | 0 / 0 / 0 / - / - | 2 / 1 / 0 / 8 / 0.30 | 0 / 0 / 0 / - / 0.40 | 1 / 1 / 0 / 6 / 0.30 | none (below threshold everywhere) | 0.0 |
| 23 |  | 2 / 2 / 1 / 10 / 0.30 | 0 / 0 / 1 / - / 0.43 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 39 | white-and-gold salon / ballroom | 99 (99, 0) | 19 | mixed |
| 7 | gold-and-blue palatial salon | 54 (52, 2) | 7 | mixed |
| 8 | gothic cathedral nave | 48 (20, 28) | 19 | all but e1_both |
| 20 | luxury canopy bedroom | 31 (26, 5) | 8 | mixed |
| 5 | ballerinas and dancers | 22 (7, 15) | 3 | all but e1_cap |
| 19 | rainbow / neon tunnel with a figure | 20 (0, 20) | 2 | mixed |
| 29 |  | 20 (5, 15) | 4 | mixed |
| 24 | lighthouse in a storm | 11 (7, 4) | 1 | mixed |
| 33 | stained-glass saints | 9 (1, 8) | 1 | pair: llava + hunyuan |
| 30 | desert dunes | 7 (6, 1) | 0 | mixed |

### captioner llava-photo

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 7 | gold-and-blue palatial salon | 83 (83) | 17 | mixed |
| 0 | modern fitted kitchen (stock) | 23 (23) | 5 | pair: llava-photo + sdxl |
| 8 | gothic cathedral nave | 22 (22) | 12 | all but e1_both |
| 39 | white-and-gold salon / ballroom | 15 (15) | 2 | mixed |
| 24 | lighthouse in a storm | 9 (9) | 1 | mixed |
| 35 | supermarket produce aisle | 9 (9) | 3 | pair: llava-photo + sdxl |
| 27 | Native American portraits in feather headdress (vintage photo) | 7 (7) | 3 | pair: llava-photo + sdxl |
| 5 | ballerinas and dancers | 5 (5) | 1 | all but e1_cap |
| 29 |  | 4 (4) | 1 | mixed |
| 21 |  | 3 (3) | 0 | mixed |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 39 | white-and-gold salon / ballroom | 47 (47, 0) | 7 | mixed |
| 3 | lone tree in a mirror lake | 40 (23, 17) | 8 | captioner: qwen |
| 5 | ballerinas and dancers | 32 (0, 32) | 7 | all but e1_cap |
| 22 | luxury bathroom | 26 (22, 4) | 10 | mixed |
| 4 | pink-and-gold banquet hall | 26 (26, 0) | 12 | pair: qwen + sdxl |
| 25 | gnarled old tree in mist | 22 (21, 1) | 8 | pair: qwen + sdxl |
| 31 | East Asian garden, pagoda, Fuji | 19 (17, 2) | 9 | mixed |
| 8 | gothic cathedral nave | 17 (15, 2) | 2 | all but e1_both |
| 30 | desert dunes | 14 (13, 1) | 1 | mixed |
| 17 | cosmic vortex with a figure | 10 (0, 10) | 4 | pair: qwen + hunyuan |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 5 | ballerinas and dancers | 47 (15, 32) | 9 | all but e1_cap |
| 8 | gothic cathedral nave | 30 (28, 2) | 8 | all but e1_both |
| 19 | rainbow / neon tunnel with a figure | 24 (20, 4) | 2 | mixed |
| 3 | lone tree in a mirror lake | 17 (0, 17) | 3 | captioner: qwen |
| 29 |  | 15 (15, 0) | 4 | mixed |
| 17 | cosmic vortex with a figure | 10 (0, 10) | 3 | pair: qwen + hunyuan |
| 33 | stained-glass saints | 9 (8, 1) | 1 | pair: llava + hunyuan |
| 26 | robots and mechs | 6 (6, 0) | 3 | pair: llava + hunyuan |
| 20 | luxury canopy bedroom | 5 (5, 0) | 2 | mixed |
| 16 |  | 5 (0, 5) | 1 | pair: qwen + hunyuan |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 39 | white-and-gold salon / ballroom | 161 (99, 15, 47) | 28 | mixed |
| 7 | gold-and-blue palatial salon | 136 (52, 83, 1) | 25 | mixed |
| 8 | gothic cathedral nave | 57 (20, 22, 15) | 25 | all but e1_both |
| 20 | luxury canopy bedroom | 32 (26, 0, 6) | 7 | mixed |
| 4 | pink-and-gold banquet hall | 28 (1, 1, 26) | 14 | pair: qwen + sdxl |
| 22 | luxury bathroom | 25 (3, 0, 22) | 8 | mixed |
| 0 | modern fitted kitchen (stock) | 25 (2, 23, 0) | 6 | pair: llava-photo + sdxl |
| 3 | lone tree in a mirror lake | 23 (0, 0, 23) | 5 | captioner: qwen |
| 31 | East Asian garden, pagoda, Fuji | 22 (5, 0, 17) | 9 | mixed |
| 25 | gnarled old tree in mist | 21 (0, 0, 21) | 8 | pair: qwen + sdxl |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 39 | white-and-gold salon / ballroom | 99 (99) | 19 | mixed |
| 7 | gold-and-blue palatial salon | 52 (52) | 7 | mixed |
| 20 | luxury canopy bedroom | 26 (26) | 7 | mixed |
| 8 | gothic cathedral nave | 20 (20) | 11 | all but e1_both |
| 5 | ballerinas and dancers | 7 (7) | 1 | all but e1_cap |
| 24 | lighthouse in a storm | 7 (7) | 1 | mixed |
| 30 | desert dunes | 6 (6) | 0 | mixed |
| 29 |  | 5 (5) | 0 | mixed |
| 31 | East Asian garden, pagoda, Fuji | 5 (5) | 1 | mixed |
| 22 | luxury bathroom | 3 (3) | 0 | mixed |

### pair llava-photo + sdxl (a0_photo)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 7 | gold-and-blue palatial salon | 83 (83) | 17 | mixed |
| 0 | modern fitted kitchen (stock) | 23 (23) | 5 | pair: llava-photo + sdxl |
| 8 | gothic cathedral nave | 22 (22) | 12 | all but e1_both |
| 39 | white-and-gold salon / ballroom | 15 (15) | 2 | mixed |
| 24 | lighthouse in a storm | 9 (9) | 1 | mixed |
| 35 | supermarket produce aisle | 9 (9) | 3 | pair: llava-photo + sdxl |
| 27 | Native American portraits in feather headdress (vintage photo) | 7 (7) | 3 | pair: llava-photo + sdxl |
| 5 | ballerinas and dancers | 5 (5) | 1 | all but e1_cap |
| 29 |  | 4 (4) | 1 | mixed |
| 21 |  | 3 (3) | 0 | mixed |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 39 | white-and-gold salon / ballroom | 47 (47) | 7 | mixed |
| 4 | pink-and-gold banquet hall | 26 (26) | 12 | pair: qwen + sdxl |
| 3 | lone tree in a mirror lake | 23 (23) | 5 | captioner: qwen |
| 22 | luxury bathroom | 22 (22) | 8 | mixed |
| 25 | gnarled old tree in mist | 21 (21) | 8 | pair: qwen + sdxl |
| 31 | East Asian garden, pagoda, Fuji | 17 (17) | 8 | mixed |
| 8 | gothic cathedral nave | 15 (15) | 2 | all but e1_both |
| 30 | desert dunes | 13 (13) | 1 | mixed |
| 20 | luxury canopy bedroom | 6 (6) | 0 | mixed |
| 21 |  | 2 (2) | 1 | mixed |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 8 | gothic cathedral nave | 28 (28) | 8 | all but e1_both |
| 19 | rainbow / neon tunnel with a figure | 20 (20) | 2 | mixed |
| 5 | ballerinas and dancers | 15 (15) | 2 | all but e1_cap |
| 29 |  | 15 (15) | 4 | mixed |
| 33 | stained-glass saints | 8 (8) | 1 | pair: llava + hunyuan |
| 26 | robots and mechs | 6 (6) | 3 | pair: llava + hunyuan |
| 20 | luxury canopy bedroom | 5 (5) | 1 | mixed |
| 24 | lighthouse in a storm | 4 (4) | 0 | mixed |
| 7 | gold-and-blue palatial salon | 2 (2) | 0 | mixed |
| 35 | supermarket produce aisle | 2 (2) | 0 | pair: llava-photo + sdxl |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 5 | ballerinas and dancers | 32 (32) | 7 | all but e1_cap |
| 3 | lone tree in a mirror lake | 17 (17) | 3 | captioner: qwen |
| 17 | cosmic vortex with a figure | 10 (10) | 3 | pair: qwen + hunyuan |
| 16 |  | 5 (5) | 1 | pair: qwen + hunyuan |
| 22 | luxury bathroom | 4 (4) | 2 | mixed |
| 19 | rainbow / neon tunnel with a figure | 4 (4) | 0 | mixed |
| 13 |  | 4 (4) | 1 | pair: qwen + hunyuan |
| 9 | figure with raised arms in a light burst | 3 (3) | 1 | pair: qwen + hunyuan |
| 10 | hooded figures in a misty forest | 3 (3) | 0 | pair: qwen + hunyuan |
| 8 | gothic cathedral nave | 2 (2) | 0 | all but e1_both |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 37% | 51% | 2.43 | 9 |
| a0_photo | 30% | 46% | 1.83 | 9 |
| e1_cap | 38% | 54% | 1.98 | 12 |
| e1_gen | 17% | 22% | 1.06 | 8 |
| e1_both | 16% | 20% | 0.90 | 7 |
