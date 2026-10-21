# Persistent-attractor atlas (dinov2): joint k = 40 over all 69300 intermediate steps of a0_core, a0_core2, a0_photo, e1_cap, e1_gen, e1_both, a0_s

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); a0_core2 = llava + sdxl (n 100 trajectories); a0_photo = llava-photo + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories); a0_s = sonnet + sdxl (n 100 trajectories).
Membership: nearest centroid within radius 0.2 (dinov2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (15 of 40) are transit states and omitted. Names from `archive/persistent_atlas_s_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | a0_core2 | a0_photo | e1_cap | e1_gen | e1_both | a0_s | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 73 / 37 / 12 / 11 / 0.15 | 80 / 31 / 14 / 10 / 0.14 | 8 / 8 / 0 / 7 / 0.32 | 44 / 20 / 6 / 12 / 0.12 | 0 / 0 / 0 / - / 0.75 | 0 / 0 / 0 / - / - | 25 / 11 / 4 / 10 / 0.18 | mixed | 0.0 |
| 1 | gold-and-blue palatial salon | 65 / 35 / 14 / 11 / 0.16 | 75 / 37 / 13 / 11 / 0.13 | 77 / 26 / 16 / 11 / 0.13 | 5 / 4 / 2 / 7 / 0.33 | 0 / 0 / 0 / - / 0.38 | 0 / 0 / 0 / - / - | 5 / 5 / 1 / 11 / 0.27 | mixed | 0.0 |
| 6 | gothic cathedral nave | 20 / 11 / 11 / 29 / 0.02 | 13 / 10 / 8 / 42 / 0.01 | 23 / 12 / 12 / 26 / 0.02 | 14 / 7 / 2 / 19 / 0.08 | 23 / 12 / 8 / 8 / 0.28 | 2 / 1 / 0 / 5 / 0.20 | 38 / 18 / 11 / 21 / 0.07 | all but e1_both | 0.0 |
| 8 | ballerinas and dancers | 7 / 2 / 1 / 12 / 0.08 | 7 / 2 / 0 / 10 / 0.13 | 5 / 1 / 1 / 12 / 0.09 | 0 / 0 / 0 / - / - | 15 / 4 / 2 / 12 / 0.14 | 33 / 16 / 7 / 17 / 0.09 | 1 / 1 / 0 / 7 / 0.30 | mixed | 0.0 |
| 34 | luxury canopy bedroom | 30 / 16 / 8 / 12 / 0.11 | 21 / 11 / 5 / 9 / 0.18 | 0 / 0 / 0 / - / 0.40 | 5 / 3 / 0 / 7 / 0.26 | 5 / 1 / 1 / 12 / 0.12 | 0 / 0 / 1 / - / 0.25 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 21 | lone tree in a mirror lake | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / 0.29 | 0 / 0 / 0 / - / 1.00 | 27 / 12 / 7 / 14 / 0.14 | 0 / 0 / 0 / - / - | 8 / 5 / 1 / 8 / 0.37 | 14 / 6 / 2 / 10 / 0.18 | mixed | 0.0 |
| 16 | pink-and-gold banquet hall | 0 / 0 / 2 / - / 0.57 | 3 / 3 / 2 / 5 / 0.43 | 1 / 1 / 0 / 5 / 0.67 | 29 / 16 / 12 / 18 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 13 / 10 / 9 / 15 / 0.12 | mixed | 0.0 |
| 26 | gnarled old tree in mist | 0 / 0 / 0 / - / 0.42 | 3 / 2 / 1 / 9 / 0.28 | 0 / 0 / 0 / - / 0.50 | 19 / 11 / 8 / 11 / 0.19 | 0 / 0 / 0 / - / 0.40 | 0 / 0 / 0 / - / 0.43 | 24 / 12 / 4 / 13 / 0.16 | mixed | 0.0 |
| 11 | modern fitted kitchen (stock) | 2 / 1 / 1 / 7 / 0.19 | 14 / 3 / 2 / 7 / 0.22 | 23 / 7 / 5 / 9 / 0.17 | 0 / 0 / 0 / - / - | 0 / 0 / 1 / - / 0.67 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 15 | luxury bathroom | 3 / 3 / 0 / 8 / 0.25 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 22 / 9 / 8 / 18 / 0.07 | 0 / 0 / 0 / - / - | 4 / 2 / 2 / 13 / 0.13 | 4 / 1 / 1 / 11 / 0.11 | mixed | 0.0 |
| 33 | desert dunes | 6 / 3 / 0 / 20 / 0.07 | 2 / 1 / 0 / 11 / 0.17 | 0 / 0 / 0 / - / 1.00 | 13 / 5 / 1 / 16 / 0.10 | 1 / 1 / 0 / 5 / 0.44 | 1 / 1 / 0 / 7 / 0.35 | 5 / 3 / 2 / 34 / 0.03 | mixed | 0.0 |
| 13 |  | 17 / 9 / 3 / 11 / 0.12 | 8 / 4 / 3 / 8 / 0.20 | 1 / 1 / 0 / 9 / 0.11 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / 0.60 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.57 | captioner: llava | 0.0 |
| 14 |  | 3 / 1 / 0 / 5 / 0.29 | 1 / 1 / 0 / 5 / 0.36 | 4 / 2 / 0 / 10 / 0.14 | 0 / 0 / 0 / - / - | 17 / 7 / 3 / 13 / 0.12 | 0 / 0 / 0 / - / 0.67 | 1 / 1 / 0 / 6 / 0.31 | mixed | 0.0 |
| 39 | rainbow / neon tunnel with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 22 / 7 / 2 / 12 / 0.14 | 4 / 2 / 0 / 7 / 0.21 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 4 |  | 1 / 1 / 0 / 9 / 0.33 | 3 / 2 / 0 / 7 / 0.20 | 0 / 0 / 0 / - / - | 8 / 3 / 2 / 9 / 0.22 | 0 / 0 / 0 / - / - | 4 / 2 / 0 / 18 / 0.09 | 9 / 5 / 3 / 16 / 0.12 | mixed | 0.0 |
| 5 | East Asian garden, pagoda, Fuji | 5 / 4 / 1 / 8 / 0.29 | 0 / 0 / 0 / - / 0.42 | 0 / 0 / 0 / - / 0.67 | 17 / 8 / 8 / 22 / 0.05 | 0 / 0 / 0 / - / 1.00 | 2 / 2 / 1 / 8 / 0.17 | 0 / 0 / 0 / - / 1.00 | mixed | 0.0 |
| 12 |  | 6 / 6 / 2 / 6 / 0.45 | 2 / 2 / 3 / 6 / 0.55 | 4 / 4 / 5 / 6 / 0.39 | 2 / 2 / 0 / 8 / 0.39 | 4 / 2 / 0 / 9 / 0.22 | 0 / 0 / 0 / - / - | 3 / 3 / 0 / 7 / 0.29 | mixed | 0.0 |
| 38 |  | 0 / 0 / 0 / - / - | 2 / 1 / 0 / 21 / 0.08 | 0 / 0 / 0 / - / - | 7 / 6 / 2 / 27 / 0.08 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.45 | 11 / 5 / 3 / 16 / 0.09 | mixed | 0.0 |
| 25 | stained-glass saints | 0 / 0 / 0 / - / 0.57 | 5 / 4 / 0 / 6 / 0.24 | 1 / 1 / 0 / 5 / 0.22 | 0 / 0 / 0 / - / 0.29 | 9 / 5 / 1 / 13 / 0.14 | 0 / 0 / 0 / - / 0.58 | 0 / 0 / 0 / - / 0.65 | captioner: llava | 0.0 |
| 27 |  | 6 / 2 / 1 / 15 / 0.09 | 0 / 0 / 0 / - / - | 4 / 2 / 0 / 11 / 0.25 | 1 / 1 / 0 / 35 / 0.05 | 0 / 0 / 0 / - / 0.60 | 0 / 0 / 0 / - / - | 3 / 1 / 1 / 15 / 0.07 | mixed | 0.0 |
| 18 | supermarket produce aisle | 0 / 0 / 0 / - / 0.40 | 0 / 0 / 0 / - / 0.50 | 10 / 4 / 3 / 17 / 0.07 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.44 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava-photo + sdxl | 0.0 |
| 22 |  | 1 / 1 / 1 / 96 / 0.00 | 1 / 1 / 1 / 99 / 0.00 | 3 / 1 / 1 / 26 / 0.04 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 1 / 0 / 6 / 0.24 | pair: llava-photo + sdxl | 0.0 |
| 24 | cosmic vortex with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 6 / 4 / 2 / 10 / 0.27 | 0 / 0 / 0 / - / - | pair: qwen + hunyuan | 0.0 |
| 19 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.53 | none (below threshold everywhere) | 0.0 |
| 35 |  | 0 / 0 / 0 / - / 0.61 | 1 / 1 / 0 / 5 / 0.62 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 153 (73, 80, 0) | 26 | mixed |
| 1 | gold-and-blue palatial salon | 140 (65, 75, 0) | 27 | mixed |
| 6 | gothic cathedral nave | 56 (20, 13, 23) | 27 | all but e1_both |
| 34 | luxury canopy bedroom | 56 (30, 21, 5) | 14 | mixed |
| 8 | ballerinas and dancers | 29 (7, 7, 15) | 3 | mixed |
| 13 |  | 25 (17, 8, 0) | 6 | captioner: llava |
| 39 | rainbow / neon tunnel with a figure | 22 (0, 0, 22) | 2 | mixed |
| 14 |  | 21 (3, 1, 17) | 3 | mixed |
| 11 | modern fitted kitchen (stock) | 16 (2, 14, 0) | 4 | mixed |
| 25 | stained-glass saints | 14 (0, 5, 9) | 1 | captioner: llava |

### captioner llava-photo

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 77 (77) | 16 | mixed |
| 6 | gothic cathedral nave | 23 (23) | 12 | all but e1_both |
| 11 | modern fitted kitchen (stock) | 23 (23) | 5 | mixed |
| 18 | supermarket produce aisle | 10 (10) | 3 | pair: llava-photo + sdxl |
| 31 | white-and-gold salon / ballroom | 8 (8) | 0 | mixed |
| 8 | ballerinas and dancers | 5 (5) | 1 | mixed |
| 14 |  | 4 (4) | 0 | mixed |
| 12 |  | 4 (4) | 5 | mixed |
| 27 |  | 4 (4) | 0 | mixed |
| 22 |  | 3 (3) | 1 | pair: llava-photo + sdxl |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 44 (44, 0) | 6 | mixed |
| 21 | lone tree in a mirror lake | 35 (27, 8) | 8 | mixed |
| 8 | ballerinas and dancers | 33 (0, 33) | 7 | mixed |
| 16 | pink-and-gold banquet hall | 29 (29, 0) | 12 | mixed |
| 15 | luxury bathroom | 26 (22, 4) | 10 | mixed |
| 26 | gnarled old tree in mist | 19 (19, 0) | 8 | mixed |
| 5 | East Asian garden, pagoda, Fuji | 19 (17, 2) | 9 | mixed |
| 6 | gothic cathedral nave | 16 (14, 2) | 2 | all but e1_both |
| 33 | desert dunes | 14 (13, 1) | 1 | mixed |
| 4 |  | 12 (8, 4) | 2 | mixed |

### captioner sonnet

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 6 | gothic cathedral nave | 38 (38) | 11 | all but e1_both |
| 31 | white-and-gold salon / ballroom | 25 (25) | 4 | mixed |
| 26 | gnarled old tree in mist | 24 (24) | 4 | mixed |
| 21 | lone tree in a mirror lake | 14 (14) | 2 | mixed |
| 16 | pink-and-gold banquet hall | 13 (13) | 9 | mixed |
| 38 |  | 11 (11) | 3 | mixed |
| 4 |  | 9 (9) | 3 | mixed |
| 1 | gold-and-blue palatial salon | 5 (5) | 1 | mixed |
| 33 | desert dunes | 5 (5) | 2 | mixed |
| 15 | luxury bathroom | 4 (4) | 1 | mixed |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 8 | ballerinas and dancers | 48 (15, 33) | 9 | mixed |
| 39 | rainbow / neon tunnel with a figure | 26 (22, 4) | 2 | mixed |
| 6 | gothic cathedral nave | 25 (23, 2) | 8 | all but e1_both |
| 14 |  | 17 (17, 0) | 3 | mixed |
| 25 | stained-glass saints | 9 (9, 0) | 1 | captioner: llava |
| 21 | lone tree in a mirror lake | 8 (0, 8) | 1 | mixed |
| 24 | cosmic vortex with a figure | 6 (0, 6) | 2 | pair: qwen + hunyuan |
| 34 | luxury canopy bedroom | 5 (5, 0) | 2 | mixed |
| 15 | luxury bathroom | 4 (0, 4) | 2 | mixed |
| 4 |  | 4 (0, 4) | 0 | mixed |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 230 (73, 80, 8, 44, 25) | 36 | mixed |
| 1 | gold-and-blue palatial salon | 227 (65, 75, 77, 5, 5) | 46 | mixed |
| 6 | gothic cathedral nave | 108 (20, 13, 23, 14, 38) | 44 | all but e1_both |
| 34 | luxury canopy bedroom | 56 (30, 21, 0, 5, 0) | 13 | mixed |
| 16 | pink-and-gold banquet hall | 46 (0, 3, 1, 29, 13) | 25 | mixed |
| 26 | gnarled old tree in mist | 46 (0, 3, 0, 19, 24) | 13 | mixed |
| 21 | lone tree in a mirror lake | 41 (0, 0, 0, 27, 14) | 9 | mixed |
| 11 | modern fitted kitchen (stock) | 39 (2, 14, 23, 0, 0) | 8 | mixed |
| 15 | luxury bathroom | 29 (3, 0, 0, 22, 4) | 9 | mixed |
| 33 | desert dunes | 26 (6, 2, 0, 13, 5) | 3 | mixed |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 73 (73) | 12 | mixed |
| 1 | gold-and-blue palatial salon | 65 (65) | 14 | mixed |
| 34 | luxury canopy bedroom | 30 (30) | 8 | mixed |
| 6 | gothic cathedral nave | 20 (20) | 11 | all but e1_both |
| 13 |  | 17 (17) | 3 | captioner: llava |
| 8 | ballerinas and dancers | 7 (7) | 1 | mixed |
| 33 | desert dunes | 6 (6) | 0 | mixed |
| 12 |  | 6 (6) | 2 | mixed |
| 27 |  | 6 (6) | 1 | mixed |
| 5 | East Asian garden, pagoda, Fuji | 5 (5) | 1 | mixed |

### pair llava + sdxl (a0_core2)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 80 (80) | 14 | mixed |
| 1 | gold-and-blue palatial salon | 75 (75) | 13 | mixed |
| 34 | luxury canopy bedroom | 21 (21) | 5 | mixed |
| 11 | modern fitted kitchen (stock) | 14 (14) | 2 | mixed |
| 6 | gothic cathedral nave | 13 (13) | 8 | all but e1_both |
| 13 |  | 8 (8) | 3 | captioner: llava |
| 8 | ballerinas and dancers | 7 (7) | 0 | mixed |
| 25 | stained-glass saints | 5 (5) | 0 | captioner: llava |
| 16 | pink-and-gold banquet hall | 3 (3) | 2 | mixed |
| 26 | gnarled old tree in mist | 3 (3) | 1 | mixed |

### pair llava-photo + sdxl (a0_photo)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 77 (77) | 16 | mixed |
| 6 | gothic cathedral nave | 23 (23) | 12 | all but e1_both |
| 11 | modern fitted kitchen (stock) | 23 (23) | 5 | mixed |
| 18 | supermarket produce aisle | 10 (10) | 3 | pair: llava-photo + sdxl |
| 31 | white-and-gold salon / ballroom | 8 (8) | 0 | mixed |
| 8 | ballerinas and dancers | 5 (5) | 1 | mixed |
| 14 |  | 4 (4) | 0 | mixed |
| 12 |  | 4 (4) | 5 | mixed |
| 27 |  | 4 (4) | 0 | mixed |
| 22 |  | 3 (3) | 1 | pair: llava-photo + sdxl |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 31 | white-and-gold salon / ballroom | 44 (44) | 6 | mixed |
| 16 | pink-and-gold banquet hall | 29 (29) | 12 | mixed |
| 21 | lone tree in a mirror lake | 27 (27) | 7 | mixed |
| 15 | luxury bathroom | 22 (22) | 8 | mixed |
| 26 | gnarled old tree in mist | 19 (19) | 8 | mixed |
| 5 | East Asian garden, pagoda, Fuji | 17 (17) | 8 | mixed |
| 6 | gothic cathedral nave | 14 (14) | 2 | all but e1_both |
| 33 | desert dunes | 13 (13) | 1 | mixed |
| 4 |  | 8 (8) | 2 | mixed |
| 38 |  | 7 (7) | 2 | mixed |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 6 | gothic cathedral nave | 23 (23) | 8 | all but e1_both |
| 39 | rainbow / neon tunnel with a figure | 22 (22) | 2 | mixed |
| 14 |  | 17 (17) | 3 | mixed |
| 8 | ballerinas and dancers | 15 (15) | 2 | mixed |
| 25 | stained-glass saints | 9 (9) | 1 | captioner: llava |
| 34 | luxury canopy bedroom | 5 (5) | 1 | mixed |
| 12 |  | 4 (4) | 0 | mixed |
| 33 | desert dunes | 1 (1) | 0 | mixed |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 8 | ballerinas and dancers | 33 (33) | 7 | mixed |
| 21 | lone tree in a mirror lake | 8 (8) | 1 | mixed |
| 24 | cosmic vortex with a figure | 6 (6) | 2 | pair: qwen + hunyuan |
| 15 | luxury bathroom | 4 (4) | 2 | mixed |
| 39 | rainbow / neon tunnel with a figure | 4 (4) | 0 | mixed |
| 4 |  | 4 (4) | 0 | mixed |
| 6 | gothic cathedral nave | 2 (2) | 0 | all but e1_both |
| 5 | East Asian garden, pagoda, Fuji | 2 (2) | 1 | mixed |
| 33 | desert dunes | 1 (1) | 0 | mixed |
| 38 |  | 1 (1) | 0 | mixed |

### pair sonnet + sdxl (a0_s)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 6 | gothic cathedral nave | 38 (38) | 11 | all but e1_both |
| 31 | white-and-gold salon / ballroom | 25 (25) | 4 | mixed |
| 26 | gnarled old tree in mist | 24 (24) | 4 | mixed |
| 21 | lone tree in a mirror lake | 14 (14) | 2 | mixed |
| 16 | pink-and-gold banquet hall | 13 (13) | 9 | mixed |
| 38 |  | 11 (11) | 3 | mixed |
| 4 |  | 9 (9) | 3 | mixed |
| 1 | gold-and-blue palatial salon | 5 (5) | 1 | mixed |
| 33 | desert dunes | 5 (5) | 2 | mixed |
| 15 | luxury bathroom | 4 (4) | 1 | mixed |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 39% | 57% | 2.45 | 9 |
| a0_core2 | 36% | 52% | 2.41 | 9 |
| a0_photo | 27% | 43% | 1.64 | 8 |
| e1_cap | 39% | 58% | 2.13 | 11 |
| e1_gen | 15% | 18% | 0.96 | 8 |
| e1_both | 12% | 14% | 0.65 | 10 |
| a0_s | 29% | 41% | 1.59 | 10 |
