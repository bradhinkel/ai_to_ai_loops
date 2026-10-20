# Attractor atlas: joint k = 16 over 320 final-step DINOv2 endpoints of a0_core, e1_cap_pilot, e1_gen, e1_both

Cells (captioner x generator): a0_core = llava + sdxl (n 100); e1_cap_pilot = qwen + sdxl (n 20); e1_gen = llava + hunyuan (n 100); e1_both = qwen + hunyuan (n 100).
'present' = >= 5% of a cell's endpoints and >= 2. Transit at one fixed radius 0.2 (hysteresis 1.25x): visited = trajectories ever inside, steps = trajectory-steps inside, hazard = exits / steps inside. r95 = cluster's 95th-percentile member distance; loose (r95 > 0.6) clusters are catch-alls, not attractors. Names from `archive/atlas_names.json` (hand-labelled from the sheets); blank = not yet named. Sheets: `cluster_<c>.jpg`, one row per cell. CLIP is not used.

## All clusters

| cluster | name | size | a0_core | e1_cap_pilot | e1_gen | e1_both | attribution | captioner fraction of the difference | r95 |
|---|---|---|---|---|---|---|---|---|---|
| 7 | gold-and-blue palatial salon | 38 | 31 (31%) | 3 (15%) | 2 (2%) | 2 (2%) | generator: sdxl | 0.28 | 0.537 |
| 8 | catch-all: objects, robots, lit corridors (loose) | 32 (loose) | 5 (5%) | 1 (5%) | 21 (21%) | 5 (5%) | all but e1_cap_pilot | 0.5 | 0.865 |
| 11 | catch-all: people, sport, stained glass, art (loose) | 32 (loose) | 7 (7%) | 1 (5%) | 18 (18%) | 6 (6%) | all but e1_cap_pilot | 0.54 | 0.8 |
| 2 | gothic cathedral nave | 25 | 11 (11%) | 1 (5%) | 12 (12%) | 1 (1%) | captioner: llava | 0.85 | 0.373 |
| 4 | lone tree in a mirror lake (lavender / cherry) | 25 | 0 (0%) | 6 (30%) | 0 (0%) | 19 (19%) | captioner: qwen | 0.82 | 0.476 |
| 5 | sunset lake with silhouettes and meditators (loose) | 23 (loose) | 0 (0%) | 0 (0%) | 5 (5%) | 18 (18%) | generator: hunyuan | 0.36 | 0.667 |
| 12 | dancers and ballerinas in light | 22 | 1 (1%) | 1 (5%) | 5 (5%) | 15 (15%) | generator: hunyuan | 0.5 | 0.425 |
| 13 | catch-all: tropical, forest, moonlit landscapes (loose) | 22 (loose) | 6 (6%) | 1 (5%) | 1 (1%) | 14 (14%) | mixed | 0.75 | 0.746 |
| 14 | old-town street / Victorian house / castle village | 19 (loose) | 14 (14%) | 1 (5%) | 4 (4%) | 0 (0%) | pair: llava + sdxl | 0.46 | 0.739 |
| 3 | cosmic light bursts, vortices, eyes | 18 | 2 (2%) | 0 (0%) | 4 (4%) | 12 (12%) | pair: qwen + hunyuan | 0.3 | 0.586 |
| 9 | neon tunnels, rainbow corridors, galleries | 15 (loose) | 3 (3%) | 0 (0%) | 11 (11%) | 1 (1%) | pair: llava + hunyuan | 0.59 | 0.651 |
| 15 | East Asian garden, pagoda, Fuji, bridge | 14 (loose) | 4 (4%) | 2 (10%) | 3 (3%) | 5 (5%) | captioner: qwen | 0.57 | 0.718 |
| 6 | luxury canopy bedroom | 11 | 9 (9%) | 0 (0%) | 1 (1%) | 1 (1%) | pair: llava + sdxl | 0.56 | 0.335 |
| 0 | futuristic skyline and landmarks | 10 (loose) | 2 (2%) | 0 (0%) | 8 (8%) | 0 (0%) | pair: llava + hunyuan | 0.62 | 0.655 |
| 1 | gold ballroom / opulent hall (loose) | 8 (loose) | 4 (4%) | 2 (10%) | 1 (1%) | 1 (1%) | pair: qwen + sdxl | 0.33 | 0.668 |
| 10 | red-rock canyon | 6 | 1 (1%) | 1 (5%) | 4 (4%) | 0 (0%) | none (below threshold everywhere) | 0.0 | 0.214 |

## Top attractors by component (endpoints in the component's cells; loose clusters excluded)

### captioner llava

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 7 | gold-and-blue palatial salon | 33 (31, 2) | generator: sdxl |
| 2 | gothic cathedral nave | 23 (11, 12) | captioner: llava |
| 6 | luxury canopy bedroom | 10 (9, 1) | pair: llava + sdxl |
| 12 | dancers and ballerinas in light | 6 (1, 5) | generator: hunyuan |
| 3 | cosmic light bursts, vortices, eyes | 6 (2, 4) | pair: qwen + hunyuan |
| 10 | red-rock canyon | 5 (1, 4) | none (below threshold everywhere) |

### captioner qwen

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 4 | lone tree in a mirror lake (lavender / cherry) | 25 (6, 19) | captioner: qwen |
| 12 | dancers and ballerinas in light | 16 (1, 15) | generator: hunyuan |
| 3 | cosmic light bursts, vortices, eyes | 12 (0, 12) | pair: qwen + hunyuan |
| 7 | gold-and-blue palatial salon | 5 (3, 2) | generator: sdxl |
| 2 | gothic cathedral nave | 2 (1, 1) | captioner: llava |
| 6 | luxury canopy bedroom | 1 (0, 1) | pair: llava + sdxl |
| 10 | red-rock canyon | 1 (1, 0) | none (below threshold everywhere) |

### generator hunyuan

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 12 | dancers and ballerinas in light | 20 (5, 15) | generator: hunyuan |
| 4 | lone tree in a mirror lake (lavender / cherry) | 19 (0, 19) | captioner: qwen |
| 3 | cosmic light bursts, vortices, eyes | 16 (4, 12) | pair: qwen + hunyuan |
| 2 | gothic cathedral nave | 13 (12, 1) | captioner: llava |
| 7 | gold-and-blue palatial salon | 4 (2, 2) | generator: sdxl |
| 10 | red-rock canyon | 4 (4, 0) | none (below threshold everywhere) |
| 6 | luxury canopy bedroom | 2 (1, 1) | pair: llava + sdxl |

### generator sdxl

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 7 | gold-and-blue palatial salon | 34 (31, 3) | generator: sdxl |
| 2 | gothic cathedral nave | 12 (11, 1) | captioner: llava |
| 6 | luxury canopy bedroom | 9 (9, 0) | pair: llava + sdxl |
| 4 | lone tree in a mirror lake (lavender / cherry) | 6 (0, 6) | captioner: qwen |
| 12 | dancers and ballerinas in light | 2 (1, 1) | generator: hunyuan |
| 3 | cosmic light bursts, vortices, eyes | 2 (2, 0) | pair: qwen + hunyuan |
| 10 | red-rock canyon | 2 (1, 1) | none (below threshold everywhere) |

### pair llava + sdxl (a0_core)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 7 | gold-and-blue palatial salon | 31 (31) | generator: sdxl |
| 2 | gothic cathedral nave | 11 (11) | captioner: llava |
| 6 | luxury canopy bedroom | 9 (9) | pair: llava + sdxl |
| 3 | cosmic light bursts, vortices, eyes | 2 (2) | pair: qwen + hunyuan |
| 12 | dancers and ballerinas in light | 1 (1) | generator: hunyuan |
| 10 | red-rock canyon | 1 (1) | none (below threshold everywhere) |

### pair qwen + sdxl (e1_cap_pilot)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 4 | lone tree in a mirror lake (lavender / cherry) | 6 (6) | captioner: qwen |
| 7 | gold-and-blue palatial salon | 3 (3) | generator: sdxl |
| 2 | gothic cathedral nave | 1 (1) | captioner: llava |
| 12 | dancers and ballerinas in light | 1 (1) | generator: hunyuan |
| 10 | red-rock canyon | 1 (1) | none (below threshold everywhere) |

### pair llava + hunyuan (e1_gen)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 2 | gothic cathedral nave | 12 (12) | captioner: llava |
| 12 | dancers and ballerinas in light | 5 (5) | generator: hunyuan |
| 3 | cosmic light bursts, vortices, eyes | 4 (4) | pair: qwen + hunyuan |
| 10 | red-rock canyon | 4 (4) | none (below threshold everywhere) |
| 7 | gold-and-blue palatial salon | 2 (2) | generator: sdxl |
| 6 | luxury canopy bedroom | 1 (1) | pair: llava + sdxl |

### pair qwen + hunyuan (e1_both)

| cluster | name | endpoints in these cells | attribution |
|---|---|---|---|
| 4 | lone tree in a mirror lake (lavender / cherry) | 19 (19) | captioner: qwen |
| 12 | dancers and ballerinas in light | 15 (15) | generator: hunyuan |
| 3 | cosmic light bursts, vortices, eyes | 12 (12) | pair: qwen + hunyuan |
| 7 | gold-and-blue palatial salon | 2 (2) | generator: sdxl |
| 2 | gothic cathedral nave | 1 (1) | captioner: llava |
| 6 | luxury canopy bedroom | 1 (1) | pair: llava + sdxl |

## Transit and escape hazard per cell (fixed radius)

| cluster | name | a0_core: stayed / visited / steps / hazard | e1_cap_pilot: stayed / visited / steps / hazard | e1_gen: stayed / visited / steps / hazard | e1_both: stayed / visited / steps / hazard |
|---|---|---|---|---|---|
| 7 | gold-and-blue palatial salon | 27 / 41 / 1737 / 0.119 | 0 / 3 / 38 / 0.237 | 0 / 3 / 8 / 0.750 | 0 / 0 / 0 / - |
| 2 | gothic cathedral nave | 11 / 11 / 579 / 0.028 | 0 / 2 / 100 / 0.040 | 8 / 16 / 411 / 0.180 | 1 / 1 / 12 / 0.167 |
| 4 | lone tree in a mirror lake (lavender / cherry) | 0 / 0 / 0 / - | 1 / 4 / 59 / 0.288 | 0 / 1 / 1 / 1.000 | 6 / 18 / 193 / 0.259 |
| 12 | dancers and ballerinas in light | 1 / 2 / 66 / 0.106 | 0 / 1 / 24 / 0.167 | 1 / 5 / 189 / 0.127 | 8 / 20 / 646 / 0.094 |
| 3 | cosmic light bursts, vortices, eyes | 0 / 0 / 0 / - | 0 / 0 / 0 / - | 0 / 0 / 0 / - | 2 / 9 / 82 / 0.220 |
| 6 | luxury canopy bedroom | 8 / 19 / 393 / 0.125 | 0 / 2 / 3 / 1.000 | 1 / 1 / 66 / 0.136 | 1 / 1 / 4 / 0.250 |
| 10 | red-rock canyon | 1 / 3 / 72 / 0.028 | 1 / 1 / 8 / 0.375 | 4 / 8 / 202 / 0.079 | 0 / 0 / 0 / - |
