# Attractor atlas: joint k = 16 over 400 final-step DINOv2 endpoints of a0_core, e1_cap, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100); e1_cap = qwen + sdxl (n 100); e1_gen = llava + hunyuan (n 100); e1_both = qwen + hunyuan (n 100).
'present' = >= 5% of a cell's endpoints and >= 2. Transit at one fixed radius 0.2 (hysteresis 1.25x): visited = trajectories ever inside, steps = trajectory-steps inside, hazard = exits / steps inside. r95 = cluster's 95th-percentile member distance; loose (r95 > 0.6) clusters are catch-alls, not attractors. Names from `archive/atlas_names.json` (hand-labelled from the sheets); blank = not yet named. Sheets: `cluster_<c>.jpg`, one row per cell. CLIP is not used.

## All clusters

| cluster | name | size | a0_core | e1_cap | e1_gen | e1_both | attribution | captioner fraction of the difference | r95 |
|---|---|---|---|---|---|---|---|---|---|
| 7 | catch-all: streets, objects, scenes (loose) | 71 (loose) | 21 (21%) | 20 (20%) | 25 (25%) | 5 (5%) | universal | 0.66 | 0.857 |
| 3 | sunset / mirror lakes and trees (loose) | 47 (loose) | 3 (3%) | 10 (10%) | 1 (1%) | 33 (33%) | captioner: qwen | 0.65 | 0.629 |
| 1 | gold-and-blue palatial salon | 45 | 32 (32%) | 11 (11%) | 1 (1%) | 1 (1%) | generator: sdxl | 0.34 | 0.425 |
| 10 | catch-all: lighthouses, canyons, silhouettes (loose) | 33 (loose) | 4 (4%) | 3 (3%) | 11 (11%) | 15 (15%) | generator: hunyuan | 0.14 | 0.693 |
| 13 | catch-all: animals, objects, mixed (loose) | 32 (loose) | 3 (3%) | 2 (2%) | 15 (15%) | 12 (12%) | generator: hunyuan | 0.15 | 0.792 |
| 12 | gothic cathedral nave | 25 | 11 (11%) | 2 (2%) | 11 (11%) | 1 (1%) | captioner: llava | 0.95 | 0.275 |
| 8 | dancers and ballerinas | 22 | 1 (1%) | 1 (1%) | 5 (5%) | 15 (15%) | generator: hunyuan | 0.36 | 0.57 |
| 14 | cosmic vortices and rainbow tunnels | 21 | 2 (2%) | 1 (1%) | 8 (8%) | 10 (10%) | generator: hunyuan | 0.06 | 0.562 |
| 15 | futuristic / neon galleries and skylines | 19 (loose) | 4 (4%) | 0 (0%) | 14 (14%) | 1 (1%) | pair: llava + hunyuan | 0.61 | 0.663 |
| 2 | East Asian garden, pagoda, Fuji | 17 | 2 (2%) | 10 (10%) | 1 (1%) | 4 (4%) | pair: qwen + sdxl | 0.61 | 0.489 |
| 9 | gnarled old tree in mist | 16 | 0 (0%) | 16 (16%) | 0 (0%) | 0 (0%) | pair: qwen + sdxl | 0.5 | 0.294 |
| 4 | pink-and-gold banquet hall | 15 | 2 (2%) | 13 (13%) | 0 (0%) | 0 (0%) | pair: qwen + sdxl | 0.42 | 0.231 |
| 0 | luxury canopy bedroom | 11 | 9 (9%) | 0 (0%) | 1 (1%) | 1 (1%) | pair: llava + sdxl | 0.56 | 0.335 |
| 11 | luxury bathroom | 11 | 0 (0%) | 9 (9%) | 0 (0%) | 2 (2%) | pair: qwen + sdxl | 0.61 | 0.267 |
| 6 | robots and figures | 9 (loose) | 1 (1%) | 1 (1%) | 7 (7%) | 0 (0%) | pair: llava + hunyuan | 0.58 | 0.618 |
| 5 | Victorian house with garden | 6 | 5 (5%) | 1 (1%) | 0 (0%) | 0 (0%) | pair: llava + sdxl | 0.4 | 0.458 |

## Top attractors by component (endpoints in the component's cells; loose clusters excluded)

### captioner llava

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 1 | gold-and-blue palatial salon | 33 (32, 1) | generator: sdxl |
| 12 | gothic cathedral nave | 22 (11, 11) | captioner: llava |
| 14 | cosmic vortices and rainbow tunnels | 10 (2, 8) | generator: hunyuan |
| 0 | luxury canopy bedroom | 10 (9, 1) | pair: llava + sdxl |
| 8 | dancers and ballerinas | 6 (1, 5) | generator: hunyuan |
| 5 | Victorian house with garden | 5 (5, 0) | pair: llava + sdxl |
| 2 | East Asian garden, pagoda, Fuji | 3 (2, 1) | pair: qwen + sdxl |
| 4 | pink-and-gold banquet hall | 2 (2, 0) | pair: qwen + sdxl |

### captioner qwen

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 8 | dancers and ballerinas | 16 (1, 15) | generator: hunyuan |
| 9 | gnarled old tree in mist | 16 (16, 0) | pair: qwen + sdxl |
| 2 | East Asian garden, pagoda, Fuji | 14 (10, 4) | pair: qwen + sdxl |
| 4 | pink-and-gold banquet hall | 13 (13, 0) | pair: qwen + sdxl |
| 1 | gold-and-blue palatial salon | 12 (11, 1) | generator: sdxl |
| 14 | cosmic vortices and rainbow tunnels | 11 (1, 10) | generator: hunyuan |
| 11 | luxury bathroom | 11 (9, 2) | pair: qwen + sdxl |
| 12 | gothic cathedral nave | 3 (2, 1) | captioner: llava |

### generator hunyuan

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 8 | dancers and ballerinas | 20 (5, 15) | generator: hunyuan |
| 14 | cosmic vortices and rainbow tunnels | 18 (8, 10) | generator: hunyuan |
| 12 | gothic cathedral nave | 12 (11, 1) | captioner: llava |
| 2 | East Asian garden, pagoda, Fuji | 5 (1, 4) | pair: qwen + sdxl |
| 1 | gold-and-blue palatial salon | 2 (1, 1) | generator: sdxl |
| 0 | luxury canopy bedroom | 2 (1, 1) | pair: llava + sdxl |
| 11 | luxury bathroom | 2 (0, 2) | pair: qwen + sdxl |

### generator sdxl

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 1 | gold-and-blue palatial salon | 43 (32, 11) | generator: sdxl |
| 9 | gnarled old tree in mist | 16 (0, 16) | pair: qwen + sdxl |
| 4 | pink-and-gold banquet hall | 15 (2, 13) | pair: qwen + sdxl |
| 12 | gothic cathedral nave | 13 (11, 2) | captioner: llava |
| 2 | East Asian garden, pagoda, Fuji | 12 (2, 10) | pair: qwen + sdxl |
| 0 | luxury canopy bedroom | 9 (9, 0) | pair: llava + sdxl |
| 11 | luxury bathroom | 9 (0, 9) | pair: qwen + sdxl |
| 5 | Victorian house with garden | 6 (5, 1) | pair: llava + sdxl |

### pair llava + sdxl (a0_core)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 1 | gold-and-blue palatial salon | 32 (32) | generator: sdxl |
| 12 | gothic cathedral nave | 11 (11) | captioner: llava |
| 0 | luxury canopy bedroom | 9 (9) | pair: llava + sdxl |
| 5 | Victorian house with garden | 5 (5) | pair: llava + sdxl |
| 14 | cosmic vortices and rainbow tunnels | 2 (2) | generator: hunyuan |
| 2 | East Asian garden, pagoda, Fuji | 2 (2) | pair: qwen + sdxl |
| 4 | pink-and-gold banquet hall | 2 (2) | pair: qwen + sdxl |
| 8 | dancers and ballerinas | 1 (1) | generator: hunyuan |

### pair qwen + sdxl (e1_cap)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 9 | gnarled old tree in mist | 16 (16) | pair: qwen + sdxl |
| 4 | pink-and-gold banquet hall | 13 (13) | pair: qwen + sdxl |
| 1 | gold-and-blue palatial salon | 11 (11) | generator: sdxl |
| 2 | East Asian garden, pagoda, Fuji | 10 (10) | pair: qwen + sdxl |
| 11 | luxury bathroom | 9 (9) | pair: qwen + sdxl |
| 12 | gothic cathedral nave | 2 (2) | captioner: llava |
| 8 | dancers and ballerinas | 1 (1) | generator: hunyuan |
| 14 | cosmic vortices and rainbow tunnels | 1 (1) | generator: hunyuan |

### pair llava + hunyuan (e1_gen)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 12 | gothic cathedral nave | 11 (11) | captioner: llava |
| 14 | cosmic vortices and rainbow tunnels | 8 (8) | generator: hunyuan |
| 8 | dancers and ballerinas | 5 (5) | generator: hunyuan |
| 1 | gold-and-blue palatial salon | 1 (1) | generator: sdxl |
| 2 | East Asian garden, pagoda, Fuji | 1 (1) | pair: qwen + sdxl |
| 0 | luxury canopy bedroom | 1 (1) | pair: llava + sdxl |

### pair qwen + hunyuan (e1_both)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 8 | dancers and ballerinas | 15 (15) | generator: hunyuan |
| 14 | cosmic vortices and rainbow tunnels | 10 (10) | generator: hunyuan |
| 2 | East Asian garden, pagoda, Fuji | 4 (4) | pair: qwen + sdxl |
| 11 | luxury bathroom | 2 (2) | pair: qwen + sdxl |
| 1 | gold-and-blue palatial salon | 1 (1) | generator: sdxl |
| 12 | gothic cathedral nave | 1 (1) | captioner: llava |
| 0 | luxury canopy bedroom | 1 (1) | pair: llava + sdxl |

## Transit and escape hazard per cell (fixed radius)

| cluster | name | a0_core: stayed / visited / steps / hazard | e1_cap: stayed / visited / steps / hazard | e1_gen: stayed / visited / steps / hazard | e1_both: stayed / visited / steps / hazard |
|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 27 / 41 / 1773 / 0.115 | 8 / 29 / 646 / 0.144 | 0 / 3 / 9 / 0.778 | 0 / 0 / 0 / - |
| 12 | gothic cathedral nave | 11 / 11 / 580 / 0.028 | 2 / 8 / 283 / 0.081 | 8 / 16 / 369 / 0.225 | 0 / 1 / 11 / 0.182 |
| 8 | dancers and ballerinas | 1 / 2 / 59 / 0.119 | 0 / 0 / 0 / - | 1 / 5 / 174 / 0.144 | 8 / 20 / 649 / 0.094 |
| 14 | cosmic vortices and rainbow tunnels | 0 / 0 / 0 / - | 0 / 0 / 0 / - | 0 / 0 / 0 / - | 3 / 11 / 133 / 0.195 |
| 2 | East Asian garden, pagoda, Fuji | 0 / 5 / 21 / 0.429 | 8 / 9 / 398 / 0.043 | 0 / 1 / 1 / 1.000 | 1 / 2 / 20 / 0.150 |
| 9 | gnarled old tree in mist | 0 / 3 / 12 / 0.333 | 11 / 24 / 405 / 0.240 | 0 / 0 / 0 / - | 0 / 4 / 9 / 0.444 |
| 4 | pink-and-gold banquet hall | 1 / 17 / 40 / 0.575 | 12 / 18 / 503 / 0.070 | 0 / 0 / 0 / - | 0 / 0 / 0 / - |
| 0 | luxury canopy bedroom | 8 / 19 / 393 / 0.125 | 0 / 6 / 50 / 0.280 | 1 / 1 / 66 / 0.136 | 1 / 1 / 4 / 0.250 |
| 11 | luxury bathroom | 0 / 4 / 34 / 0.235 | 8 / 9 / 420 / 0.052 | 0 / 0 / 0 / - | 2 / 2 / 57 / 0.140 |
| 5 | Victorian house with garden | 5 / 9 / 166 / 0.187 | 0 / 2 / 19 / 0.158 | 0 / 0 / 0 / - | 0 / 0 / 0 / - |
