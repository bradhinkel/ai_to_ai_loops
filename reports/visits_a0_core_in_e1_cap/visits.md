# Transient visits: a0_core attractors inside e1_cap's trajectories

Probes: archive/a0_core_centroids.npz. Scan: every cached step 1..99 of e1_cap (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 11: [90, 17, 10, 88, 57, 59, 93, 9]… | 0.2 | 8 | 2 | 6 | 41.0 | 20 | 0.045 |
| 1 | 34: [5, 95, 92, 35, 82, 60, 58, 87]… | 0.323 | 34 | 9 | 25 | 18.0 | 52 | 0.08 |
| 2 | 9: [2, 97, 44, 26, 31, 13, 47, 75]… | 0.326 | 8 | 0 | 8 | 43.5 | 13 | 0.105 |
| 3 | 8: [6, 54, 65, 29, 55, 78, 46, 33] | 0.707 | 17 | 2 | 15 | 36.0 | 19 | 0.222 |
| 4 | 24: [24, 96, 36, 45, 15, 1, 69, 42]… | 0.793 | 94 | 41 | 53 | 4.0 | 54 | 0.56 |
| 5 | 4: [49, 91, 94, 8] | 0.455 | 2 | 0 | 2 | 39.5 | 11 | 0.306 |
| 6 | 5: [7, 34, 38, 21, 89] | 0.2 | 2 | 0 | 2 | 66.5 | 8 | 0.106 |
| 7 | 5: [39, 86, 67, 16, 25] | 0.589 | 4 | 0 | 4 | 11.0 | 5 | 0.458 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
