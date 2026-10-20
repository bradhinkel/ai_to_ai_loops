# Persistent-attractor atlas: joint k = 40 over all 39600 intermediate steps of a0_core, e1_cap, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories).
Membership: nearest centroid within radius 0.2 (DINOv2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (12 of 40) are transit states and omitted. Names from `archive/persistent_atlas_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | e1_cap | e1_gen | e1_both | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|
| 3 | gold-and-blue palatial salon | 90 / 39 / 23 / 12 / 0.13 | 14 / 9 / 3 / 9 / 0.23 | 0 / 0 / 0 / - / 0.40 | 0 / 0 / 0 / - / - | generator: sdxl | 0.42 |
| 32 | white-and-gold salon / ballroom | 44 / 26 / 5 / 10 / 0.19 | 39 / 20 / 5 / 12 / 0.13 | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | generator: sdxl | 0.06 |
| 13 | gothic cathedral nave | 20 / 11 / 11 / 28 / 0.02 | 15 / 7 / 2 / 18 / 0.08 | 33 / 14 / 8 / 9 / 0.20 | 2 / 1 / 0 / 6 / 0.18 | all but e1_both | 1.0 |
| 12 | ballerinas and dancers | 6 / 2 / 1 / 13 / 0.10 | 0 / 0 / 0 / - / - | 15 / 4 / 2 / 12 / 0.15 | 31 / 16 / 7 / 19 / 0.08 | all but e1_cap | 0.2 |
| 5 | lone tree in a mirror lake | 0 / 0 / 0 / - / - | 26 / 12 / 7 / 15 / 0.12 | 0 / 0 / 0 / - / - | 15 / 9 / 2 / 10 / 0.25 | captioner: qwen | 0.79 |
| 22 | luxury canopy bedroom | 26 / 15 / 7 / 13 / 0.12 | 4 / 2 / 0 / 8 / 0.27 | 5 / 1 / 1 / 12 / 0.11 | 0 / 0 / 1 / - / 0.25 | all but e1_both | 0.52 |
| 16 | luxury bathroom | 3 / 3 / 0 / 8 / 0.28 | 22 / 9 / 8 / 18 / 0.07 | 0 / 0 / 0 / - / - | 4 / 2 / 2 / 13 / 0.14 | all but e1_gen | 0.52 |
| 18 | pink-and-gold banquet hall | 0 / 0 / 1 / - / 0.60 | 25 / 16 / 12 / 20 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.5 |
| 0 | rainbow / neon tunnel with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 20 / 7 / 2 / 14 / 0.14 | 4 / 2 / 0 / 6 / 0.22 | generator: hunyuan | 0.4 |
| 19 | East Asian garden, pagoda, Fuji | 5 / 4 / 1 / 8 / 0.27 | 17 / 8 / 8 / 22 / 0.05 | 0 / 0 / 0 / - / 0.50 | 2 / 2 / 1 / 8 / 0.17 | generator: sdxl | 0.41 |
| 9 | gnarled old tree in mist | 0 / 0 / 0 / - / 0.38 | 20 / 13 / 8 / 18 / 0.10 | 0 / 0 / 0 / - / 0.40 | 1 / 1 / 0 / 6 / 0.20 | pair: qwen + sdxl | 0.53 |
| 30 | desert dunes | 6 / 3 / 0 / 20 / 0.07 | 13 / 5 / 1 / 16 / 0.10 | 1 / 1 / 0 / 7 / 0.36 | 1 / 1 / 0 / 7 / 0.35 | generator: sdxl | 0.29 |
| 10 | Victorian house with garden | 19 / 9 / 4 / 11 / 0.11 | 1 / 1 / 0 / 15 / 0.16 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.47 |
| 37 | robots and mechs | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 20 / 6 / 4 / 10 / 0.18 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 15 | cherry tree on an islet | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 6 / 0.22 | 0 / 0 / 0 / - / - | 16 / 9 / 6 / 11 / 0.09 | pair: qwen + hunyuan | 0.53 |
| 27 | soccer players, painterly | 7 / 2 / 1 / 10 / 0.21 | 0 / 0 / 0 / - / 1.00 | 9 / 2 / 2 / 11 / 0.07 | 0 / 0 / 0 / - / - | captioner: llava | 0.89 |
| 26 | sunset lake with forest reflection | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / 1.00 | 12 / 5 / 2 / 9 / 0.19 | pair: qwen + hunyuan | 0.5 |
| 11 | cosmic vortex with a figure | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 5 / 0.32 | 0 / 0 / 0 / - / - | 9 / 5 / 3 / 25 / 0.07 | pair: qwen + hunyuan | 0.56 |
| 17 | stained-glass saints | 1 / 1 / 0 / 7 / 0.58 | 0 / 0 / 0 / - / 0.33 | 8 / 4 / 1 / 14 / 0.17 | 0 / 0 / 0 / - / 0.50 | pair: llava + hunyuan | 0.56 |
| 14 | figure with raised arms in a light burst | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 8 / 5 / 2 / 11 / 0.26 | pair: qwen + hunyuan | 0.5 |
| 29 | gold corridor / grand hall (Hunyuan) | 1 / 1 / 0 / 5 / 0.57 | 1 / 1 / 0 / 5 / 0.46 | 4 / 3 / 0 / 8 / 0.27 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.67 |
| 8 | hooded figures in a misty forest | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.82 | 0 / 0 / 0 / - / - | 5 / 4 / 0 / 8 / 0.36 | pair: qwen + hunyuan | 0.5 |
| 31 | lighthouse in a storm | 4 / 2 / 1 / 18 / 0.13 | 1 / 1 / 0 / 35 / 0.05 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.38 |
| 21 | bald eagles in flight | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 3 / 2 / 2 / 51 / 0.02 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 23 | gold corridor with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 6 / 0.40 | none (below threshold everywhere) | 0.5 |
| 39 | boxers in a ring | 1 / 1 / 0 / 75 / 0.07 | 1 / 1 / 0 / 56 / 0.02 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |
| 4 | red moon over a desert | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 1 / 1 / 0 / 5 / 0.42 | none (below threshold everywhere) | 0.5 |
| 35 | colourful bottles | 1 / 1 / 0 / 90 / 0.02 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.5 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 3 | gold-and-blue palatial salon | 90 (90, 0) | 23 | generator: sdxl |
| 13 | gothic cathedral nave | 53 (20, 33) | 19 | all but e1_both |
| 32 | white-and-gold salon / ballroom | 44 (44, 0) | 5 | generator: sdxl |
| 22 | luxury canopy bedroom | 31 (26, 5) | 8 | all but e1_both |
| 12 | ballerinas and dancers | 21 (6, 15) | 3 | all but e1_cap |
| 0 | rainbow / neon tunnel with a figure | 20 (0, 20) | 2 | generator: hunyuan |
| 37 | robots and mechs | 20 (0, 20) | 4 | pair: llava + hunyuan |
| 10 | Victorian house with garden | 19 (19, 0) | 4 | pair: llava + sdxl |
| 27 | soccer players, painterly | 16 (7, 9) | 3 | captioner: llava |
| 17 | stained-glass saints | 9 (1, 8) | 1 | pair: llava + hunyuan |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 5 | lone tree in a mirror lake | 41 (26, 15) | 9 | captioner: qwen |
| 32 | white-and-gold salon / ballroom | 39 (39, 0) | 5 | generator: sdxl |
| 12 | ballerinas and dancers | 31 (0, 31) | 7 | all but e1_cap |
| 16 | luxury bathroom | 26 (22, 4) | 10 | all but e1_gen |
| 18 | pink-and-gold banquet hall | 25 (25, 0) | 12 | pair: qwen + sdxl |
| 9 | gnarled old tree in mist | 21 (20, 1) | 8 | pair: qwen + sdxl |
| 19 | East Asian garden, pagoda, Fuji | 19 (17, 2) | 9 | generator: sdxl |
| 15 | cherry tree on an islet | 17 (1, 16) | 7 | pair: qwen + hunyuan |
| 13 | gothic cathedral nave | 17 (15, 2) | 2 | all but e1_both |
| 3 | gold-and-blue palatial salon | 14 (14, 0) | 3 | generator: sdxl |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 12 | ballerinas and dancers | 46 (15, 31) | 9 | all but e1_cap |
| 13 | gothic cathedral nave | 35 (33, 2) | 8 | all but e1_both |
| 0 | rainbow / neon tunnel with a figure | 24 (20, 4) | 2 | generator: hunyuan |
| 37 | robots and mechs | 20 (20, 0) | 4 | pair: llava + hunyuan |
| 15 | cherry tree on an islet | 16 (0, 16) | 6 | pair: qwen + hunyuan |
| 5 | lone tree in a mirror lake | 15 (0, 15) | 2 | captioner: qwen |
| 26 | sunset lake with forest reflection | 12 (0, 12) | 2 | pair: qwen + hunyuan |
| 27 | soccer players, painterly | 9 (9, 0) | 2 | captioner: llava |
| 11 | cosmic vortex with a figure | 9 (0, 9) | 3 | pair: qwen + hunyuan |
| 17 | stained-glass saints | 8 (8, 0) | 1 | pair: llava + hunyuan |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 3 | gold-and-blue palatial salon | 104 (90, 14) | 26 | generator: sdxl |
| 32 | white-and-gold salon / ballroom | 83 (44, 39) | 10 | generator: sdxl |
| 13 | gothic cathedral nave | 35 (20, 15) | 13 | all but e1_both |
| 22 | luxury canopy bedroom | 30 (26, 4) | 7 | all but e1_both |
| 5 | lone tree in a mirror lake | 26 (0, 26) | 7 | captioner: qwen |
| 16 | luxury bathroom | 25 (3, 22) | 8 | all but e1_gen |
| 18 | pink-and-gold banquet hall | 25 (0, 25) | 13 | pair: qwen + sdxl |
| 19 | East Asian garden, pagoda, Fuji | 22 (5, 17) | 9 | generator: sdxl |
| 9 | gnarled old tree in mist | 20 (0, 20) | 8 | pair: qwen + sdxl |
| 10 | Victorian house with garden | 20 (19, 1) | 4 | pair: llava + sdxl |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 3 | gold-and-blue palatial salon | 90 (90) | 23 | generator: sdxl |
| 32 | white-and-gold salon / ballroom | 44 (44) | 5 | generator: sdxl |
| 22 | luxury canopy bedroom | 26 (26) | 7 | all but e1_both |
| 13 | gothic cathedral nave | 20 (20) | 11 | all but e1_both |
| 10 | Victorian house with garden | 19 (19) | 4 | pair: llava + sdxl |
| 27 | soccer players, painterly | 7 (7) | 1 | captioner: llava |
| 12 | ballerinas and dancers | 6 (6) | 1 | all but e1_cap |
| 30 | desert dunes | 6 (6) | 0 | generator: sdxl |
| 19 | East Asian garden, pagoda, Fuji | 5 (5) | 1 | generator: sdxl |
| 31 | lighthouse in a storm | 4 (4) | 1 | pair: llava + sdxl |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 32 | white-and-gold salon / ballroom | 39 (39) | 5 | generator: sdxl |
| 5 | lone tree in a mirror lake | 26 (26) | 7 | captioner: qwen |
| 18 | pink-and-gold banquet hall | 25 (25) | 12 | pair: qwen + sdxl |
| 16 | luxury bathroom | 22 (22) | 8 | all but e1_gen |
| 9 | gnarled old tree in mist | 20 (20) | 8 | pair: qwen + sdxl |
| 19 | East Asian garden, pagoda, Fuji | 17 (17) | 8 | generator: sdxl |
| 13 | gothic cathedral nave | 15 (15) | 2 | all but e1_both |
| 3 | gold-and-blue palatial salon | 14 (14) | 3 | generator: sdxl |
| 30 | desert dunes | 13 (13) | 1 | generator: sdxl |
| 22 | luxury canopy bedroom | 4 (4) | 0 | all but e1_both |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 13 | gothic cathedral nave | 33 (33) | 8 | all but e1_both |
| 0 | rainbow / neon tunnel with a figure | 20 (20) | 2 | generator: hunyuan |
| 37 | robots and mechs | 20 (20) | 4 | pair: llava + hunyuan |
| 12 | ballerinas and dancers | 15 (15) | 2 | all but e1_cap |
| 27 | soccer players, painterly | 9 (9) | 2 | captioner: llava |
| 17 | stained-glass saints | 8 (8) | 1 | pair: llava + hunyuan |
| 22 | luxury canopy bedroom | 5 (5) | 1 | all but e1_both |
| 29 | gold corridor / grand hall (Hunyuan) | 4 (4) | 0 | pair: llava + hunyuan |
| 21 | bald eagles in flight | 3 (3) | 2 | pair: llava + hunyuan |
| 30 | desert dunes | 1 (1) | 0 | generator: sdxl |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 12 | ballerinas and dancers | 31 (31) | 7 | all but e1_cap |
| 15 | cherry tree on an islet | 16 (16) | 6 | pair: qwen + hunyuan |
| 5 | lone tree in a mirror lake | 15 (15) | 2 | captioner: qwen |
| 26 | sunset lake with forest reflection | 12 (12) | 2 | pair: qwen + hunyuan |
| 11 | cosmic vortex with a figure | 9 (9) | 3 | pair: qwen + hunyuan |
| 14 | figure with raised arms in a light burst | 8 (8) | 2 | pair: qwen + hunyuan |
| 8 | hooded figures in a misty forest | 5 (5) | 0 | pair: qwen + hunyuan |
| 16 | luxury bathroom | 4 (4) | 2 | all but e1_gen |
| 0 | rainbow / neon tunnel with a figure | 4 (4) | 0 | generator: hunyuan |
| 13 | gothic cathedral nave | 2 (2) | 0 | all but e1_both |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 40% | 55% | 2.34 | 10 |
| e1_cap | 38% | 56% | 2.01 | 12 |
| e1_gen | 18% | 22% | 1.18 | 9 |
| e1_both | 20% | 26% | 1.13 | 8 |
