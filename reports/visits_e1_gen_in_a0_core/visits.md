# Transient visits: e1_gen attractors inside a0_core's trajectories

Probes: k-means k=8 on e1_gen step-99 DINOv2. Scan: every cached step 1..99 of a0_core (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 14: [5, 6, 10, 30, 38, 42, 52, 58]… | 0.602 | 17 | 11 | 6 | 31.0 | 7 | 0.11 |
| 1 | 42: [4, 7, 9, 14, 15, 18, 22, 23]… | 0.813 | 97 | 52 | 45 | 7.0 | 89 | 0.585 |
| 2 | 10: [8, 21, 36, 40, 46, 60, 63, 64]… | 0.647 | 14 | 1 | 13 | 27.0 | 20 | 0.328 |
| 3 | 9: [0, 1, 12, 13, 16, 19, 71, 95]… | 0.517 | 1 | 1 | 0 | 69.0 | 0 | 0.413 |
| 4 | 4: [11, 41, 62, 92] | 0.523 | 0 | 0 | 0 | None | 0 | 0.541 |
| 5 | 4: [3, 53, 57, 96] | 0.2 | 3 | 0 | 3 | 62.0 | 13 | 0.083 |
| 6 | 7: [20, 28, 32, 43, 44, 47, 88] | 0.416 | 1 | 0 | 1 | 61.0 | 3 | 0.338 |
| 7 | 10: [2, 17, 29, 34, 39, 50, 55, 73]… | 0.671 | 12 | 3 | 9 | 7.5 | 43 | 0.283 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
