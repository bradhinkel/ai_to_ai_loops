# Transient visits: e1_both attractors inside a0_core's trajectories

Probes: k-means k=8 on e1_both step-99 DINOv2. Scan: every cached step 1..99 of a0_core (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 6: [46, 52, 57, 58, 64, 87] | 0.529 | 2 | 1 | 1 | 71.0 | 1 | 0.394 |
| 1 | 11: [2, 4, 11, 15, 23, 28, 43, 51]… | 0.525 | 2 | 1 | 1 | 82.5 | 1 | 0.401 |
| 2 | 21: [7, 9, 13, 19, 24, 25, 40, 41]… | 0.672 | 27 | 2 | 25 | 29.0 | 26 | 0.28 |
| 3 | 12: [8, 10, 14, 17, 38, 39, 56, 67]… | 0.628 | 12 | 0 | 12 | 24.0 | 11 | 0.454 |
| 4 | 16: [12, 20, 31, 37, 44, 47, 50, 55]… | 0.376 | 2 | 1 | 1 | 21.5 | 21 | 0.228 |
| 5 | 11: [3, 5, 16, 22, 27, 54, 59, 63]… | 0.5 | 4 | 0 | 4 | 7.0 | 1 | 0.427 |
| 6 | 5: [6, 18, 21, 30, 34] | 0.498 | 6 | 0 | 6 | 17.0 | 2 | 0.427 |
| 7 | 18: [0, 1, 26, 29, 32, 33, 35, 36]… | 0.714 | 34 | 1 | 33 | 17.5 | 17 | 0.499 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
