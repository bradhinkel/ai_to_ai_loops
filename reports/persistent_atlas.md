# Persistent-attractor atlas: joint k = 40 over all 31680 intermediate steps of a0_core, e1_cap_pilot, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); e1_cap_pilot = qwen + sdxl (n 20 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories).
Membership: nearest centroid within radius 0.2 (DINOv2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (11 of 40) are transit states and omitted. Names from `archive/persistent_atlas_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | e1_cap_pilot | e1_gen | e1_both | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|
| 24 | white-and-gold palatial salon | 97 / 39 / 19 / 10 / 0.15 | 5 / 2 / 0 / 9 / 0.16 | 0 / 0 / 0 / - / 0.67 | 0 / 0 / 0 / - / - | generator: sdxl | 0.37 |
| 14 | red-blue-gold salon with chandeliers | 68 / 32 / 8 / 8 / 0.20 | 0 / 0 / 0 / - / 0.25 | 4 / 2 / 0 / 8 / 0.29 | 0 / 0 / 0 / - / - | captioner: llava | 0.53 |
| 12 | ballerinas and dancers | 7 / 2 / 1 / 12 / 0.09 | 2 / 1 / 0 / 12 / 0.14 | 15 / 4 / 2 / 12 / 0.14 | 32 / 16 / 7 / 18 / 0.09 | all but e1_cap_pilot | 0.4 |
| 26 | bright gothic nave (Hunyuan rendering) | 2 / 2 / 0 / 6 / 0.31 | 0 / 0 / 0 / - / - | 40 / 14 / 8 / 10 / 0.16 | 2 / 1 / 1 / 6 / 0.24 | pair: llava + hunyuan | 0.5 |
| 33 | luxury canopy bedroom | 26 / 15 / 7 / 13 / 0.12 | 0 / 0 / 0 / - / 1.00 | 5 / 1 / 1 / 12 / 0.12 | 0 / 0 / 1 / - / 0.25 | captioner: llava | 0.6 |
| 4 | gothic nave with stained-glass light (SDXL rendering) | 25 / 11 / 11 / 23 / 0.03 | 5 / 2 / 0 / 19 / 0.06 | 0 / 0 / 1 / - / 0.85 | 0 / 0 / 0 / - / - | generator: sdxl | 0.0 |
| 7 | lone tree in a mirror lake | 0 / 0 / 0 / - / - | 6 / 3 / 0 / 10 / 0.19 | 0 / 0 / 0 / - / - | 24 / 14 / 3 / 9 / 0.22 | captioner: qwen | 0.9 |
| 19 | rainbow / neon tunnel with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 19 / 7 / 2 / 16 / 0.12 | 4 / 2 / 0 / 6 / 0.24 | generator: hunyuan | 0.39 |
| 32 | green marble bathroom | 3 / 3 / 0 / 7 / 0.31 | 14 / 4 / 4 / 13 / 0.07 | 0 / 0 / 0 / - / - | 4 / 2 / 2 / 15 / 0.14 | all but e1_gen | 0.51 |
| 9 | robots and mechs | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 20 / 6 / 4 / 10 / 0.19 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 20 | Victorian house with garden | 19 / 9 / 4 / 11 / 0.10 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.5 |
| 5 | soccer players, painterly | 5 / 2 / 1 / 8 / 0.27 | 0 / 0 / 0 / - / - | 9 / 2 / 2 / 9 / 0.13 | 0 / 0 / 0 / - / - | captioner: llava | 0.78 |
| 17 | red-rock canyon river | 4 / 2 / 0 / 16 / 0.07 | 0 / 0 / 0 / - / 0.60 | 9 / 5 / 4 / 23 / 0.10 | 0 / 0 / 0 / - / 1.00 | captioner: llava | 0.72 |
| 22 | stained-glass saints | 1 / 1 / 0 / 7 / 0.59 | 0 / 0 / 0 / - / - | 9 / 5 / 1 / 15 / 0.15 | 0 / 0 / 0 / - / 0.62 | pair: llava + hunyuan | 0.56 |
| 11 | cosmic vortex with a figure | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 9 / 5 / 3 / 26 / 0.07 | pair: qwen + hunyuan | 0.5 |
| 15 | East Asian garden with pagoda | 5 / 5 / 1 / 11 / 0.26 | 3 / 1 / 0 / 10 / 0.18 | 0 / 0 / 0 / - / 0.43 | 1 / 1 / 0 / 9 / 0.38 | generator: sdxl | 0.37 |
| 23 | cherry tree on an islet | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 9 / 8 / 3 / 7 / 0.26 | pair: qwen + hunyuan | 0.5 |
| 28 | umbrellas (colour grid / over water) | 2 / 2 / 0 / 7 / 0.31 | 0 / 0 / 0 / - / - | 2 / 1 / 0 / 13 / 0.11 | 5 / 1 / 1 / 10 / 0.14 | pair: qwen + hunyuan | 0.17 |
| 0 | library / reading room | 6 / 4 / 0 / 8 / 0.28 | 1 / 1 / 0 / 10 / 0.21 | 0 / 0 / 0 / - / 1.00 | 1 / 1 / 0 / 5 / 0.56 | pair: llava + sdxl | 0.0 |
| 10 | desert dunes | 6 / 3 / 0 / 21 / 0.07 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.44 | 1 / 1 / 0 / 7 / 0.32 | pair: llava + sdxl | 0.6 |
| 16 | figure with raised arms in a light burst | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 8 / 5 / 2 / 11 / 0.27 | pair: qwen + hunyuan | 0.5 |
| 18 | sunset lake with forest reflection | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.60 | 0 / 0 / 0 / - / 1.00 | 8 / 5 / 2 / 25 / 0.07 | pair: qwen + hunyuan | 0.5 |
| 34 | harbour with sailboats | 6 / 2 / 1 / 15 / 0.05 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | pair: llava + sdxl | 0.5 |
| 6 | meditating figure at a lake | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.43 | 4 / 3 / 0 / 6 / 0.33 | pair: qwen + hunyuan | 0.5 |
| 30 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 3 / 2 / 2 / 51 / 0.02 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.5 |
| 3 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 2 / 0 / 6 / 0.48 | none (below threshold everywhere) | 0.5 |
| 13 |  | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 2 / 2 / 0 / 6 / 0.44 | none (below threshold everywhere) | 0.5 |
| 21 |  | 0 / 0 / 0 / - / 0.37 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 8 / 0.41 | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.5 |
| 27 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 7 / 0.47 | none (below threshold everywhere) | 0.5 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 24 | white-and-gold palatial salon | 97 (97, 0) | 19 | generator: sdxl |
| 14 | red-blue-gold salon with chandeliers | 72 (68, 4) | 8 | captioner: llava |
| 26 | bright gothic nave (Hunyuan rendering) | 42 (2, 40) | 8 | pair: llava + hunyuan |
| 33 | luxury canopy bedroom | 31 (26, 5) | 8 | captioner: llava |
| 4 | gothic nave with stained-glass light (SDXL rendering) | 25 (25, 0) | 12 | generator: sdxl |
| 12 | ballerinas and dancers | 22 (7, 15) | 3 | all but e1_cap_pilot |
| 9 | robots and mechs | 20 (0, 20) | 4 | pair: llava + hunyuan |
| 19 | rainbow / neon tunnel with a figure | 19 (0, 19) | 2 | generator: hunyuan |
| 20 | Victorian house with garden | 19 (19, 0) | 4 | pair: llava + sdxl |
| 5 | soccer players, painterly | 14 (5, 9) | 3 | captioner: llava |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 32 | green marble bathroom | 74 (70, 4) | 6 | all but e1_gen |
| 7 | lone tree in a mirror lake | 54 (30, 24) | 3 | captioner: qwen |
| 12 | ballerinas and dancers | 42 (10, 32) | 7 | all but e1_cap_pilot |
| 24 | white-and-gold palatial salon | 25 (25, 0) | 0 | generator: sdxl |
| 4 | gothic nave with stained-glass light (SDXL rendering) | 25 (25, 0) | 0 | generator: sdxl |
| 15 | East Asian garden with pagoda | 16 (15, 1) | 0 | generator: sdxl |
| 11 | cosmic vortex with a figure | 9 (0, 9) | 3 | pair: qwen + hunyuan |
| 23 | cherry tree on an islet | 9 (0, 9) | 3 | pair: qwen + hunyuan |
| 16 | figure with raised arms in a light burst | 8 (0, 8) | 2 | pair: qwen + hunyuan |
| 18 | sunset lake with forest reflection | 8 (0, 8) | 2 | pair: qwen + hunyuan |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 12 | ballerinas and dancers | 47 (15, 32) | 9 | all but e1_cap_pilot |
| 26 | bright gothic nave (Hunyuan rendering) | 42 (40, 2) | 9 | pair: llava + hunyuan |
| 7 | lone tree in a mirror lake | 24 (0, 24) | 3 | captioner: qwen |
| 19 | rainbow / neon tunnel with a figure | 23 (19, 4) | 2 | generator: hunyuan |
| 9 | robots and mechs | 20 (20, 0) | 4 | pair: llava + hunyuan |
| 5 | soccer players, painterly | 9 (9, 0) | 2 | captioner: llava |
| 17 | red-rock canyon river | 9 (9, 0) | 4 | captioner: llava |
| 22 | stained-glass saints | 9 (9, 0) | 1 | pair: llava + hunyuan |
| 11 | cosmic vortex with a figure | 9 (0, 9) | 3 | pair: qwen + hunyuan |
| 23 | cherry tree on an islet | 9 (0, 9) | 3 | pair: qwen + hunyuan |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 24 | white-and-gold palatial salon | 122 (97, 25) | 19 | generator: sdxl |
| 32 | green marble bathroom | 73 (3, 70) | 4 | all but e1_gen |
| 14 | red-blue-gold salon with chandeliers | 68 (68, 0) | 8 | captioner: llava |
| 4 | gothic nave with stained-glass light (SDXL rendering) | 50 (25, 25) | 11 | generator: sdxl |
| 7 | lone tree in a mirror lake | 30 (0, 30) | 0 | captioner: qwen |
| 33 | luxury canopy bedroom | 26 (26, 0) | 7 | captioner: llava |
| 15 | East Asian garden with pagoda | 20 (5, 15) | 1 | generator: sdxl |
| 20 | Victorian house with garden | 19 (19, 0) | 4 | pair: llava + sdxl |
| 12 | ballerinas and dancers | 17 (7, 10) | 1 | all but e1_cap_pilot |
| 0 | library / reading room | 11 (6, 5) | 0 | pair: llava + sdxl |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 24 | white-and-gold palatial salon | 97 (97) | 19 | generator: sdxl |
| 14 | red-blue-gold salon with chandeliers | 68 (68) | 8 | captioner: llava |
| 33 | luxury canopy bedroom | 26 (26) | 7 | captioner: llava |
| 4 | gothic nave with stained-glass light (SDXL rendering) | 25 (25) | 11 | generator: sdxl |
| 20 | Victorian house with garden | 19 (19) | 4 | pair: llava + sdxl |
| 12 | ballerinas and dancers | 7 (7) | 1 | all but e1_cap_pilot |
| 0 | library / reading room | 6 (6) | 0 | pair: llava + sdxl |
| 10 | desert dunes | 6 (6) | 0 | pair: llava + sdxl |
| 34 | harbour with sailboats | 6 (6) | 1 | pair: llava + sdxl |
| 5 | soccer players, painterly | 5 (5) | 1 | captioner: llava |

### pair qwen + sdxl (e1_cap_pilot)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 32 | green marble bathroom | 70 (70) | 4 | all but e1_gen |
| 7 | lone tree in a mirror lake | 30 (30) | 0 | captioner: qwen |
| 24 | white-and-gold palatial salon | 25 (25) | 0 | generator: sdxl |
| 4 | gothic nave with stained-glass light (SDXL rendering) | 25 (25) | 0 | generator: sdxl |
| 15 | East Asian garden with pagoda | 15 (15) | 0 | generator: sdxl |
| 12 | ballerinas and dancers | 10 (10) | 0 | all but e1_cap_pilot |
| 0 | library / reading room | 5 (5) | 0 | pair: llava + sdxl |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 26 | bright gothic nave (Hunyuan rendering) | 40 (40) | 8 | pair: llava + hunyuan |
| 9 | robots and mechs | 20 (20) | 4 | pair: llava + hunyuan |
| 19 | rainbow / neon tunnel with a figure | 19 (19) | 2 | generator: hunyuan |
| 12 | ballerinas and dancers | 15 (15) | 2 | all but e1_cap_pilot |
| 5 | soccer players, painterly | 9 (9) | 2 | captioner: llava |
| 17 | red-rock canyon river | 9 (9) | 4 | captioner: llava |
| 22 | stained-glass saints | 9 (9) | 1 | pair: llava + hunyuan |
| 33 | luxury canopy bedroom | 5 (5) | 1 | captioner: llava |
| 14 | red-blue-gold salon with chandeliers | 4 (4) | 0 | captioner: llava |
| 30 |  | 3 (3) | 2 | pair: llava + hunyuan |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 12 | ballerinas and dancers | 32 (32) | 7 | all but e1_cap_pilot |
| 7 | lone tree in a mirror lake | 24 (24) | 3 | captioner: qwen |
| 11 | cosmic vortex with a figure | 9 (9) | 3 | pair: qwen + hunyuan |
| 23 | cherry tree on an islet | 9 (9) | 3 | pair: qwen + hunyuan |
| 16 | figure with raised arms in a light burst | 8 (8) | 2 | pair: qwen + hunyuan |
| 18 | sunset lake with forest reflection | 8 (8) | 2 | pair: qwen + hunyuan |
| 28 | umbrellas (colour grid / over water) | 5 (5) | 1 | pair: qwen + hunyuan |
| 19 | rainbow / neon tunnel with a figure | 4 (4) | 0 | generator: hunyuan |
| 32 | green marble bathroom | 4 (4) | 2 | all but e1_gen |
| 6 | meditating figure at a lake | 4 (4) | 0 | pair: qwen + hunyuan |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 39% | 53% | 2.82 | 8 |
| e1_cap_pilot | 27% | 20% | 1.80 | 10 |
| e1_gen | 22% | 27% | 1.37 | 9 |
| e1_both | 21% | 25% | 1.17 | 9 |
