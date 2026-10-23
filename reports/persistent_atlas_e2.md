# Persistent-attractor atlas (dinov2): joint k = 40 over all 49500 intermediate steps of a0_core, e1_cap, e1_gen, e1_both, e2_qz

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); e1_cap = qwen + sdxl (n 100 trajectories); e1_gen = llava + hunyuan (n 100 trajectories); e1_both = qwen + hunyuan (n 100 trajectories); e2_qz = qwen-zh + hunyuan (n 100 trajectories).
Membership: nearest centroid within radius 0.2 (dinov2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (12 of 40) are transit states and omitted. Names from `archive/persistent_atlas_e2_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | e1_cap | e1_gen | e1_both | e2_qz | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|---|
| 2 | white-and-gold salon / ballroom | 115 / 40 / 25 / 12 / 0.13 | 47 / 23 / 7 / 12 / 0.13 | 0 / 0 / 0 / - / 0.80 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 21 | gothic cathedral nave | 20 / 11 / 11 / 28 / 0.02 | 15 / 7 / 2 / 18 / 0.08 | 33 / 14 / 8 / 9 / 0.20 | 2 / 1 / 0 / 6 / 0.18 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 9 | ballerinas and dancers | 6 / 2 / 1 / 13 / 0.08 | 0 / 0 / 0 / - / - | 15 / 4 / 2 / 12 / 0.15 | 30 / 16 / 7 / 18 / 0.08 | 9 / 7 / 0 / 9 / 0.24 | all but e1_cap | 0.0 |
| 27 | lone tree in a mirror lake | 0 / 0 / 0 / - / - | 22 / 10 / 4 / 10 / 0.19 | 0 / 0 / 0 / - / 0.67 | 18 / 11 / 3 / 10 / 0.24 | 13 / 8 / 4 / 11 / 0.18 | mixed | 0.0 |
| 12 | dancer in a swirling gown | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 14 / 8 / 2 / 13 / 0.13 | 34 / 19 / 3 / 14 / 0.14 | mixed | 0.0 |
| 1 | lone boat on a misty lake | 1 / 1 / 0 / 9 / 0.25 | 8 / 3 / 2 / 9 / 0.20 | 0 / 0 / 0 / - / - | 3 / 2 / 1 / 26 / 0.07 | 27 / 12 / 8 / 9 / 0.18 | mixed | 0.0 |
| 39 | luxury canopy bedroom | 26 / 15 / 7 / 13 / 0.12 | 5 / 3 / 0 / 7 / 0.26 | 5 / 1 / 1 / 12 / 0.11 | 0 / 0 / 1 / - / 0.25 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 13 | luxury bathroom | 3 / 3 / 0 / 8 / 0.28 | 22 / 9 / 8 / 18 / 0.07 | 0 / 0 / 0 / - / - | 4 / 2 / 2 / 13 / 0.13 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 18 | pink-and-gold banquet hall | 0 / 0 / 2 / - / 0.55 | 27 / 16 / 12 / 19 / 0.08 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.0 |
| 8 | gnarled old tree in mist | 0 / 0 / 0 / - / 0.36 | 25 / 14 / 10 / 15 / 0.12 | 0 / 0 / 0 / - / 0.25 | 1 / 1 / 0 / 5 / 0.30 | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.0 |
| 16 | sunset lake with forest reflection | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / 0.33 | 14 / 6 / 3 / 8 / 0.22 | 12 / 11 / 4 / 8 / 0.31 | mixed | 0.0 |
| 11 | desert dunes | 6 / 3 / 0 / 20 / 0.07 | 13 / 5 / 1 / 16 / 0.10 | 1 / 1 / 0 / 5 / 0.50 | 2 / 2 / 0 / 6 / 0.29 | 2 / 2 / 0 / 12 / 0.21 | mixed | 0.0 |
| 4 | pagoda by a misty lake | 0 / 0 / 0 / - / 0.60 | 4 / 3 / 0 / 5 / 0.29 | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 26 / 0.17 | 17 / 7 / 3 / 11 / 0.17 | mixed | 0.0 |
| 14 | rainbow / neon tunnel with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 16 / 7 / 2 / 6 / 0.29 | 3 / 1 / 0 / 6 / 0.23 | 0 / 0 / 0 / - / - | mixed | 0.0 |
| 25 | gold corridor / grand hall (Hunyuan) | 12 / 10 / 1 / 6 / 0.41 | 2 / 2 / 1 / 12 / 0.31 | 5 / 3 / 0 / 10 / 0.18 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | captioner: llava | 0.0 |
| 15 |  | 4 / 2 / 0 / 16 / 0.07 | 0 / 0 / 0 / - / - | 11 / 6 / 4 / 20 / 0.10 | 0 / 0 / 0 / - / 0.75 | 1 / 1 / 0 / 12 / 0.08 | captioner: llava | 0.0 |
| 22 | East Asian garden, pagoda, Fuji | 2 / 2 / 0 / 8 / 0.41 | 13 / 8 / 7 / 30 / 0.04 | 0 / 0 / 0 / - / - | 1 / 1 / 1 / 7 / 0.12 | 0 / 0 / 0 / - / - | pair: qwen + sdxl | 0.0 |
| 33 | arched stone bridge under a full moon | 2 / 2 / 0 / 8 / 0.28 | 2 / 1 / 1 / 15 / 0.25 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 12 / 4 / 2 / 9 / 0.24 | pair: qwen-zh + hunyuan | 0.0 |
| 35 | stained-glass saints | 1 / 1 / 0 / 7 / 0.58 | 0 / 0 / 0 / - / 0.33 | 8 / 4 / 1 / 14 / 0.17 | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 28 | figure with raised arms in a light burst | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 8 / 5 / 1 / 7 / 0.32 | 0 / 0 / 0 / - / 1.00 | pair: qwen + hunyuan | 0.0 |
| 3 |  | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 4 / 2 / 0 / 6 / 0.28 | 2 / 1 / 0 / 6 / 0.29 | 0 / 0 / 0 / - / 0.64 | pair: llava + hunyuan | 0.0 |
| 24 |  | 3 / 1 / 0 / 11 / 0.20 | 2 / 1 / 1 / 48 / 0.01 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 24 / 0.04 | pair: llava + sdxl | 0.0 |
| 10 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 5 / 4 / 2 / 10 / 0.12 | 0 / 0 / 0 / - / 0.25 | 0 / 0 / 0 / - / - | pair: llava + hunyuan | 0.0 |
| 5 | gold corridor with a figure | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 3 / 2 / 1 / 6 / 0.44 | 0 / 0 / 0 / - / 0.50 | pair: qwen + hunyuan | 0.0 |
| 0 | hooded figures in a misty forest | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.25 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.59 | 1 / 1 / 0 / 8 / 0.50 | none (below threshold everywhere) | 0.0 |
| 7 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 5 / 0.43 | none (below threshold everywhere) | 0.0 |
| 32 |  | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 0.50 | 0 / 0 / 0 / - / - | 1 / 1 / 0 / 15 / 0.20 | 0 / 0 / 1 / - / 0.57 | none (below threshold everywhere) | 0.0 |
| 37 | colourful bottles | 1 / 1 / 0 / 90 / 0.02 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / 1.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) | 0.0 |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 2 | white-and-gold salon / ballroom | 115 (115, 0) | 25 | mixed |
| 21 | gothic cathedral nave | 53 (20, 33) | 19 | mixed |
| 39 | luxury canopy bedroom | 31 (26, 5) | 8 | mixed |
| 9 | ballerinas and dancers | 21 (6, 15) | 3 | all but e1_cap |
| 25 | gold corridor / grand hall (Hunyuan) | 17 (12, 5) | 1 | captioner: llava |
| 14 | rainbow / neon tunnel with a figure | 16 (0, 16) | 2 | mixed |
| 15 |  | 15 (4, 11) | 4 | captioner: llava |
| 35 | stained-glass saints | 9 (1, 8) | 1 | pair: llava + hunyuan |
| 11 | desert dunes | 7 (6, 1) | 0 | mixed |
| 10 |  | 5 (0, 5) | 2 | pair: llava + hunyuan |

### captioner qwen

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 2 | white-and-gold salon / ballroom | 47 (47, 0) | 7 | mixed |
| 27 | lone tree in a mirror lake | 40 (22, 18) | 7 | mixed |
| 9 | ballerinas and dancers | 30 (0, 30) | 7 | all but e1_cap |
| 18 | pink-and-gold banquet hall | 27 (27, 0) | 12 | pair: qwen + sdxl |
| 13 | luxury bathroom | 26 (22, 4) | 10 | mixed |
| 8 | gnarled old tree in mist | 26 (25, 1) | 10 | pair: qwen + sdxl |
| 21 | gothic cathedral nave | 17 (15, 2) | 2 | mixed |
| 11 | desert dunes | 15 (13, 2) | 1 | mixed |
| 12 | dancer in a swirling gown | 14 (0, 14) | 2 | mixed |
| 16 | sunset lake with forest reflection | 14 (0, 14) | 3 | mixed |

### captioner qwen-zh

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 12 | dancer in a swirling gown | 34 (34) | 3 | mixed |
| 1 | lone boat on a misty lake | 27 (27) | 8 | mixed |
| 4 | pagoda by a misty lake | 17 (17) | 3 | mixed |
| 27 | lone tree in a mirror lake | 13 (13) | 4 | mixed |
| 16 | sunset lake with forest reflection | 12 (12) | 4 | mixed |
| 33 | arched stone bridge under a full moon | 12 (12) | 2 | pair: qwen-zh + hunyuan |
| 9 | ballerinas and dancers | 9 (9) | 0 | all but e1_cap |
| 11 | desert dunes | 2 (2) | 0 | mixed |
| 15 |  | 1 (1) | 0 | captioner: llava |
| 24 |  | 1 (1) | 0 | pair: llava + sdxl |

### generator hunyuan

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 9 | ballerinas and dancers | 54 (15, 30, 9) | 9 | all but e1_cap |
| 12 | dancer in a swirling gown | 48 (0, 14, 34) | 5 | mixed |
| 21 | gothic cathedral nave | 35 (33, 2, 0) | 8 | mixed |
| 27 | lone tree in a mirror lake | 31 (0, 18, 13) | 7 | mixed |
| 1 | lone boat on a misty lake | 30 (0, 3, 27) | 9 | mixed |
| 16 | sunset lake with forest reflection | 26 (0, 14, 12) | 7 | mixed |
| 14 | rainbow / neon tunnel with a figure | 19 (16, 3, 0) | 2 | mixed |
| 4 | pagoda by a misty lake | 18 (0, 1, 17) | 4 | mixed |
| 15 |  | 12 (11, 0, 1) | 4 | captioner: llava |
| 33 | arched stone bridge under a full moon | 12 (0, 0, 12) | 2 | pair: qwen-zh + hunyuan |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 2 | white-and-gold salon / ballroom | 162 (115, 47) | 32 | mixed |
| 21 | gothic cathedral nave | 35 (20, 15) | 13 | mixed |
| 39 | luxury canopy bedroom | 31 (26, 5) | 7 | mixed |
| 18 | pink-and-gold banquet hall | 27 (0, 27) | 14 | pair: qwen + sdxl |
| 13 | luxury bathroom | 25 (3, 22) | 8 | mixed |
| 8 | gnarled old tree in mist | 25 (0, 25) | 10 | pair: qwen + sdxl |
| 27 | lone tree in a mirror lake | 22 (0, 22) | 4 | mixed |
| 11 | desert dunes | 19 (6, 13) | 1 | mixed |
| 22 | East Asian garden, pagoda, Fuji | 15 (2, 13) | 7 | pair: qwen + sdxl |
| 25 | gold corridor / grand hall (Hunyuan) | 14 (12, 2) | 2 | captioner: llava |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 2 | white-and-gold salon / ballroom | 115 (115) | 25 | mixed |
| 39 | luxury canopy bedroom | 26 (26) | 7 | mixed |
| 21 | gothic cathedral nave | 20 (20) | 11 | mixed |
| 25 | gold corridor / grand hall (Hunyuan) | 12 (12) | 1 | captioner: llava |
| 9 | ballerinas and dancers | 6 (6) | 1 | all but e1_cap |
| 11 | desert dunes | 6 (6) | 0 | mixed |
| 15 |  | 4 (4) | 0 | captioner: llava |
| 13 | luxury bathroom | 3 (3) | 0 | mixed |
| 24 |  | 3 (3) | 0 | pair: llava + sdxl |
| 22 | East Asian garden, pagoda, Fuji | 2 (2) | 0 | pair: qwen + sdxl |

### pair qwen + sdxl (e1_cap)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 2 | white-and-gold salon / ballroom | 47 (47) | 7 | mixed |
| 18 | pink-and-gold banquet hall | 27 (27) | 12 | pair: qwen + sdxl |
| 8 | gnarled old tree in mist | 25 (25) | 10 | pair: qwen + sdxl |
| 27 | lone tree in a mirror lake | 22 (22) | 4 | mixed |
| 13 | luxury bathroom | 22 (22) | 8 | mixed |
| 21 | gothic cathedral nave | 15 (15) | 2 | mixed |
| 11 | desert dunes | 13 (13) | 1 | mixed |
| 22 | East Asian garden, pagoda, Fuji | 13 (13) | 7 | pair: qwen + sdxl |
| 1 | lone boat on a misty lake | 8 (8) | 2 | mixed |
| 39 | luxury canopy bedroom | 5 (5) | 0 | mixed |

### pair llava + hunyuan (e1_gen)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 21 | gothic cathedral nave | 33 (33) | 8 | mixed |
| 14 | rainbow / neon tunnel with a figure | 16 (16) | 2 | mixed |
| 9 | ballerinas and dancers | 15 (15) | 2 | all but e1_cap |
| 15 |  | 11 (11) | 4 | captioner: llava |
| 35 | stained-glass saints | 8 (8) | 1 | pair: llava + hunyuan |
| 39 | luxury canopy bedroom | 5 (5) | 1 | mixed |
| 25 | gold corridor / grand hall (Hunyuan) | 5 (5) | 0 | captioner: llava |
| 10 |  | 5 (5) | 2 | pair: llava + hunyuan |
| 3 |  | 4 (4) | 0 | pair: llava + hunyuan |
| 11 | desert dunes | 1 (1) | 0 | mixed |

### pair qwen + hunyuan (e1_both)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 9 | ballerinas and dancers | 30 (30) | 7 | all but e1_cap |
| 27 | lone tree in a mirror lake | 18 (18) | 3 | mixed |
| 12 | dancer in a swirling gown | 14 (14) | 2 | mixed |
| 16 | sunset lake with forest reflection | 14 (14) | 3 | mixed |
| 28 | figure with raised arms in a light burst | 8 (8) | 1 | pair: qwen + hunyuan |
| 13 | luxury bathroom | 4 (4) | 2 | mixed |
| 1 | lone boat on a misty lake | 3 (3) | 1 | mixed |
| 14 | rainbow / neon tunnel with a figure | 3 (3) | 0 | mixed |
| 5 | gold corridor with a figure | 3 (3) | 1 | pair: qwen + hunyuan |
| 21 | gothic cathedral nave | 2 (2) | 0 | mixed |

### pair qwen-zh + hunyuan (e2_qz)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 12 | dancer in a swirling gown | 34 (34) | 3 | mixed |
| 1 | lone boat on a misty lake | 27 (27) | 8 | mixed |
| 4 | pagoda by a misty lake | 17 (17) | 3 | mixed |
| 27 | lone tree in a mirror lake | 13 (13) | 4 | mixed |
| 16 | sunset lake with forest reflection | 12 (12) | 4 | mixed |
| 33 | arched stone bridge under a full moon | 12 (12) | 2 | pair: qwen-zh + hunyuan |
| 9 | ballerinas and dancers | 9 (9) | 0 | all but e1_cap |
| 11 | desert dunes | 2 (2) | 0 | mixed |
| 15 |  | 1 (1) | 0 | captioner: llava |
| 24 |  | 1 (1) | 0 | pair: llava + sdxl |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 35% | 47% | 2.02 | 10 |
| e1_cap | 38% | 56% | 2.07 | 11 |
| e1_gen | 15% | 20% | 1.03 | 7 |
| e1_both | 18% | 23% | 1.08 | 8 |
| e2_qz | 19% | 25% | 1.30 | 8 |
