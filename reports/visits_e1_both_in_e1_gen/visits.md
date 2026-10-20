# Transient visits: e1_both attractors inside e1_gen's trajectories

Probes: k-means k=8 on e1_both step-99 DINOv2. Scan: every cached step 1..99 of e1_gen (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 6: [46, 52, 57, 58, 64, 87] | 0.529 | 4 | 0 | 4 | 23.0 | 2 | 0.458 |
| 1 | 11: [2, 4, 11, 15, 23, 28, 43, 51]… | 0.525 | 35 | 3 | 32 | 37.0 | 5 | 0.249 |
| 2 | 21: [7, 9, 13, 19, 24, 25, 40, 41]… | 0.672 | 29 | 4 | 25 | 21.0 | 24 | 0.233 |
| 3 | 12: [8, 10, 14, 17, 38, 39, 56, 67]… | 0.628 | 18 | 2 | 16 | 40.5 | 22 | 0.391 |
| 4 | 16: [12, 20, 31, 37, 44, 47, 50, 55]… | 0.376 | 8 | 2 | 6 | 17.0 | 24 | 0.144 |
| 5 | 11: [3, 5, 16, 22, 27, 54, 59, 63]… | 0.5 | 14 | 0 | 14 | 32.5 | 10 | 0.195 |
| 6 | 5: [6, 18, 21, 30, 34] | 0.498 | 17 | 3 | 14 | 40.0 | 6 | 0.244 |
| 7 | 18: [0, 1, 26, 29, 32, 33, 35, 36]… | 0.714 | 93 | 13 | 80 | 9.0 | 23 | 0.397 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
