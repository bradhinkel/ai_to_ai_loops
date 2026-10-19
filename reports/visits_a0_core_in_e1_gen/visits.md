# Transient visits: a0_core attractors inside e1_gen's trajectories

Probes: archive/a0_core_centroids.npz. Scan: every cached step 1..99 of e1_gen (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 11: [90, 17, 10, 88, 57, 59, 93, 9]… | 0.2 | 15 | 2 | 13 | 64.0 | 2 | 0.094 |
| 1 | 34: [5, 95, 92, 35, 82, 60, 58, 87]… | 0.323 | 5 | 1 | 4 | 21.0 | 9 | 0.132 |
| 2 | 9: [2, 97, 44, 26, 31, 13, 47, 75]… | 0.326 | 1 | 1 | 0 | 8.0 | 0 | 0.097 |
| 3 | 8: [6, 54, 65, 29, 55, 78, 46, 33] | 0.707 | 9 | 0 | 9 | 38.0 | 32 | 0.324 |
| 4 | 24: [24, 96, 36, 45, 15, 1, 69, 42]… | 0.793 | 94 | 31 | 63 | 4.0 | 51 | 0.505 |
| 5 | 4: [49, 91, 94, 8] | 0.455 | 1 | 1 | 0 | 84.0 | 0 | 0.349 |
| 6 | 5: [7, 34, 38, 21, 89] | 0.2 | 0 | 0 | 0 | None | 0 | 0.257 |
| 7 | 5: [39, 86, 67, 16, 25] | 0.589 | 10 | 4 | 6 | 25.0 | 21 | 0.319 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
