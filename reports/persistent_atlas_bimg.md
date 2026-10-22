# Persistent-attractor atlas (dinov2): joint k = 40 over all 23760 intermediate steps of a0_core, a0_core2, bimg, arm_a

Cells (captioner x generator): a0_core = llava + sdxl (n 100 trajectories); a0_core2 = llava + sdxl (n 100 trajectories); bimg = llava-bimg + sdxl (n 20 trajectories); arm_a = llava-armA + sdxl (n 20 trajectories).
Membership: nearest centroid within radius 0.2 (dinov2 cosine), hysteresis 1.25x. Persistent visit = >= 5 consecutive steps inside. 'present' in a cell = >= 3 persistent visits. Columns per cell: persistent visits / trajectories with one / endpoints (step 99) / mean dwell / escape hazard per step. 'captioner fraction' = share of the between-cell variation in visits-per-trajectory that lies on the captioner axis. Clusters with no persistent visit anywhere (13 of 40) are transit states and omitted. Names from `archive/persistent_atlas_bimg_names.json` (blank = unnamed). Sheets: `cluster_<c>.jpg`, one row per cell, thumbs = middle step of the longest persistent visits, labelled traj:step (dwell). CLIP is not used.

## Persistent attractors

| cluster | name | a0_core | a0_core2 | bimg | arm_a | attribution | captioner fraction |
|---|---|---|---|---|---|---|---|
| 1 | white-and-gold salon / ballroom | 72 / 36 / 12 / 10 / 0.16 | 65 / 29 / 12 / 10 / 0.15 | 4 / 4 / 2 / 6 / 0.36 | 6 / 4 / 1 / 9 / 0.20 | universal |  |
| 36 | gold-and-blue palatial salon | 58 / 32 / 13 / 12 / 0.13 | 66 / 38 / 13 / 13 / 0.11 | 10 / 6 / 4 / 7 / 0.24 | 4 / 3 / 1 / 17 / 0.09 | universal |  |
| 10 | luxury canopy bedroom | 31 / 16 / 8 / 12 / 0.12 | 20 / 11 / 6 / 10 / 0.17 | 3 / 2 / 0 / 5 / 0.33 | 4 / 2 / 1 / 9 / 0.14 | universal |  |
| 7 | gothic cathedral nave | 14 / 9 / 6 / 20 / 0.05 | 8 / 7 / 2 / 31 / 0.03 | 6 / 4 / 1 / 7 / 0.18 | 6 / 5 / 2 / 30 / 0.03 | universal |  |
| 14 |  | 16 / 9 / 4 / 12 / 0.12 | 7 / 4 / 3 / 12 / 0.15 | 7 / 3 / 0 / 9 / 0.17 | 3 / 2 / 1 / 11 / 0.09 | universal |  |
| 4 | gothic cathedral nave | 9 / 9 / 5 / 32 / 0.03 | 9 / 8 / 8 / 34 / 0.00 | 2 / 2 / 0 / 12 / 0.17 | 5 / 4 / 3 / 34 / 0.01 | all but bimg |  |
| 26 |  | 14 / 13 / 1 / 6 / 0.39 | 8 / 7 / 3 / 6 / 0.41 | 1 / 1 / 1 / 5 / 0.48 | 2 / 1 / 0 / 6 / 0.29 | mixed |  |
| 5 |  | 9 / 8 / 4 / 6 / 0.35 | 11 / 10 / 3 / 6 / 0.34 | 3 / 2 / 0 / 7 / 0.35 | 0 / 0 / 0 / - / 0.56 | all but arm_a |  |
| 12 |  | 8 / 2 / 1 / 8 / 0.23 | 9 / 2 / 0 / 10 / 0.19 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | mixed |  |
| 8 | modern fitted kitchen (stock) | 2 / 1 / 1 / 7 / 0.19 | 13 / 3 / 2 / 8 / 0.23 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + sdxl |  |
| 6 |  | 4 / 3 / 0 / 15 / 0.20 | 4 / 4 / 2 / 14 / 0.07 | 2 / 2 / 1 / 12 / 0.18 | 4 / 2 / 1 / 14 / 0.11 | all but bimg |  |
| 28 |  | 1 / 1 / 1 / 13 / 0.06 | 8 / 2 / 1 / 9 / 0.16 | 4 / 3 / 2 / 7 / 0.27 | 0 / 0 / 0 / - / - | mixed |  |
| 38 |  | 6 / 4 / 0 / 9 / 0.26 | 6 / 4 / 0 / 12 / 0.16 | 0 / 0 / 0 / - / 0.75 | 0 / 0 / 0 / - / - | mixed |  |
| 24 | ballerinas and dancers | 6 / 2 / 1 / 16 / 0.05 | 5 / 2 / 0 / 16 / 0.07 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | mixed |  |
| 16 |  | 3 / 3 / 1 / 8 / 0.32 | 2 / 2 / 0 / 5 / 0.41 | 1 / 1 / 0 / 6 / 0.21 | 4 / 3 / 1 / 7 / 0.27 | mixed |  |
| 29 | East Asian garden, pagoda, Fuji | 10 / 6 / 1 / 8 / 0.25 | 0 / 0 / 0 / - / 0.35 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + sdxl |  |
| 17 | stained-glass saints | 1 / 1 / 0 / 7 / 0.46 | 4 / 3 / 0 / 7 / 0.23 | 4 / 3 / 0 / 8 / 0.32 | 0 / 0 / 0 / - / - | mixed |  |
| 25 | gnarled old tree in mist | 0 / 0 / 0 / - / 0.36 | 7 / 2 / 1 / 10 / 0.18 | 2 / 1 / 0 / 10 / 0.10 | 0 / 0 / 0 / - / - | pair: llava + sdxl |  |
| 32 |  | 4 / 1 / 0 / 11 / 0.12 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 4 / 1 / 0 / 12 / 0.11 | mixed |  |
| 33 |  | 4 / 2 / 1 / 19 / 0.11 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | 2 / 1 / 0 / 20 / 0.10 | pair: llava + sdxl |  |
| 20 |  | 0 / 0 / 0 / - / 0.67 | 1 / 1 / 0 / 5 / 0.20 | 0 / 0 / 0 / - / - | 4 / 1 / 0 / 11 / 0.16 | pair: llava-armA + sdxl |  |
| 22 |  | 0 / 0 / 0 / - / 1.00 | 1 / 1 / 0 / 6 / 0.44 | 3 / 1 / 0 / 6 / 0.33 | 1 / 1 / 0 / 10 / 0.26 | pair: llava-bimg + sdxl |  |
| 27 |  | 3 / 2 / 0 / 15 / 0.22 | 1 / 1 / 0 / 5 / 0.44 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + sdxl |  |
| 2 |  | 0 / 0 / 0 / - / - | 3 / 2 / 1 / 5 / 0.21 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | pair: llava + sdxl |  |
| 23 |  | 2 / 1 / 0 / 37 / 0.08 | 1 / 1 / 0 / 47 / 0.04 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) |  |
| 39 |  | 1 / 1 / 1 / 95 / 0.00 | 1 / 1 / 1 / 99 / 0.00 | 0 / 0 / 0 / - / - | 0 / 0 / 0 / - / - | none (below threshold everywhere) |  |
| 30 |  | 1 / 1 / 0 / 5 / 0.60 | 0 / 0 / 0 / - / 0.55 | 0 / 0 / 1 / - / 0.58 | 0 / 0 / 0 / - / 0.56 | none (below threshold everywhere) |  |

## Top persistent attractors by component (persistent visits per trajectory, summed over the component's cells)

### captioner llava

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | white-and-gold salon / ballroom | 137 (72, 65) | 24 | universal |
| 36 | gold-and-blue palatial salon | 124 (58, 66) | 26 | universal |
| 10 | luxury canopy bedroom | 51 (31, 20) | 14 | universal |
| 14 |  | 23 (16, 7) | 7 | universal |
| 7 | gothic cathedral nave | 22 (14, 8) | 8 | universal |
| 26 |  | 22 (14, 8) | 4 | mixed |
| 5 |  | 20 (9, 11) | 7 | all but arm_a |
| 4 | gothic cathedral nave | 18 (9, 9) | 13 | all but bimg |
| 12 |  | 17 (8, 9) | 1 | mixed |
| 8 | modern fitted kitchen (stock) | 15 (2, 13) | 3 | pair: llava + sdxl |

### captioner llava-armA

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | white-and-gold salon / ballroom | 30 (30) | 1 | universal |
| 7 | gothic cathedral nave | 30 (30) | 2 | universal |
| 4 | gothic cathedral nave | 25 (25) | 3 | all but bimg |
| 36 | gold-and-blue palatial salon | 20 (20) | 1 | universal |
| 10 | luxury canopy bedroom | 20 (20) | 1 | universal |
| 6 |  | 20 (20) | 1 | all but bimg |
| 16 |  | 20 (20) | 1 | mixed |
| 32 |  | 20 (20) | 0 | mixed |
| 20 |  | 20 (20) | 0 | pair: llava-armA + sdxl |
| 14 |  | 15 (15) | 1 | universal |

### captioner llava-bimg

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 36 | gold-and-blue palatial salon | 50 (50) | 4 | universal |
| 14 |  | 35 (35) | 0 | universal |
| 7 | gothic cathedral nave | 30 (30) | 1 | universal |
| 1 | white-and-gold salon / ballroom | 20 (20) | 2 | universal |
| 28 |  | 20 (20) | 2 | mixed |
| 17 | stained-glass saints | 20 (20) | 0 | mixed |
| 10 | luxury canopy bedroom | 15 (15) | 0 | universal |
| 5 |  | 15 (15) | 0 | all but arm_a |
| 22 |  | 15 (15) | 0 | pair: llava-bimg + sdxl |
| 4 | gothic cathedral nave | 10 (10) | 0 | all but bimg |

### generator sdxl

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 36 | gold-and-blue palatial salon | 194 (58, 66, 50, 20) | 31 | universal |
| 1 | white-and-gold salon / ballroom | 187 (72, 65, 20, 30) | 27 | universal |
| 10 | luxury canopy bedroom | 86 (31, 20, 15, 20) | 15 | universal |
| 7 | gothic cathedral nave | 82 (14, 8, 30, 30) | 11 | universal |
| 14 |  | 73 (16, 7, 35, 15) | 8 | universal |
| 4 | gothic cathedral nave | 53 (9, 9, 10, 25) | 16 | all but bimg |
| 6 |  | 38 (4, 4, 10, 20) | 4 | all but bimg |
| 26 |  | 37 (14, 8, 5, 10) | 5 | mixed |
| 5 |  | 35 (9, 11, 15, 0) | 7 | all but arm_a |
| 16 |  | 30 (3, 2, 5, 20) | 2 | mixed |

### pair llava + sdxl (a0_core)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | white-and-gold salon / ballroom | 72 (72) | 12 | universal |
| 36 | gold-and-blue palatial salon | 58 (58) | 13 | universal |
| 10 | luxury canopy bedroom | 31 (31) | 8 | universal |
| 14 |  | 16 (16) | 4 | universal |
| 7 | gothic cathedral nave | 14 (14) | 6 | universal |
| 26 |  | 14 (14) | 1 | mixed |
| 29 | East Asian garden, pagoda, Fuji | 10 (10) | 1 | pair: llava + sdxl |
| 4 | gothic cathedral nave | 9 (9) | 5 | all but bimg |
| 5 |  | 9 (9) | 4 | all but arm_a |
| 12 |  | 8 (8) | 1 | mixed |

### pair llava + sdxl (a0_core2)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 36 | gold-and-blue palatial salon | 66 (66) | 13 | universal |
| 1 | white-and-gold salon / ballroom | 65 (65) | 12 | universal |
| 10 | luxury canopy bedroom | 20 (20) | 6 | universal |
| 8 | modern fitted kitchen (stock) | 13 (13) | 2 | pair: llava + sdxl |
| 5 |  | 11 (11) | 3 | all but arm_a |
| 4 | gothic cathedral nave | 9 (9) | 8 | all but bimg |
| 12 |  | 9 (9) | 0 | mixed |
| 7 | gothic cathedral nave | 8 (8) | 2 | universal |
| 26 |  | 8 (8) | 3 | mixed |
| 28 |  | 8 (8) | 1 | mixed |

### pair llava-bimg + sdxl (bimg)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 36 | gold-and-blue palatial salon | 50 (50) | 4 | universal |
| 14 |  | 35 (35) | 0 | universal |
| 7 | gothic cathedral nave | 30 (30) | 1 | universal |
| 1 | white-and-gold salon / ballroom | 20 (20) | 2 | universal |
| 28 |  | 20 (20) | 2 | mixed |
| 17 | stained-glass saints | 20 (20) | 0 | mixed |
| 10 | luxury canopy bedroom | 15 (15) | 0 | universal |
| 5 |  | 15 (15) | 0 | all but arm_a |
| 22 |  | 15 (15) | 0 | pair: llava-bimg + sdxl |
| 4 | gothic cathedral nave | 10 (10) | 0 | all but bimg |

### pair llava-armA + sdxl (arm_a)

| cluster | name | visits per 100 trajectories (per cell) | endpoints | attribution |
|---|---|---|---|---|
| 1 | white-and-gold salon / ballroom | 30 (30) | 1 | universal |
| 7 | gothic cathedral nave | 30 (30) | 2 | universal |
| 4 | gothic cathedral nave | 25 (25) | 3 | all but bimg |
| 36 | gold-and-blue palatial salon | 20 (20) | 1 | universal |
| 10 | luxury canopy bedroom | 20 (20) | 1 | universal |
| 6 |  | 20 (20) | 1 | all but bimg |
| 16 |  | 20 (20) | 1 | mixed |
| 32 |  | 20 (20) | 0 | mixed |
| 20 |  | 20 (20) | 0 | pair: llava-armA + sdxl |
| 14 |  | 15 (15) | 1 | universal |

## Time spent in persistent attractors, per cell

| cell | share of trajectory-steps inside any persistent attractor | share of endpoints inside one | persistent visits per trajectory | median dwell |
|---|---|---|---|---|
| a0_core | 44% | 61% | 2.79 | 8 |
| a0_core2 | 41% | 58% | 2.60 | 9 |
| bimg | 33% | 60% | 2.60 | 7 |
| arm_a | 46% | 55% | 2.45 | 10 |
