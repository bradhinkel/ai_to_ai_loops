# Transient visits: a0_core attractors inside e1_both's trajectories

Probes: archive/a0_core_centroids.npz. Scan: every cached step 1..99 of e1_both (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 11: [90, 17, 10, 88, 57, 59, 93, 9]… | 0.2 | 1 | 0 | 1 | 86.0 | 1 | 0.168 |
| 1 | 34: [5, 95, 92, 35, 82, 60, 58, 87]… | 0.323 | 1 | 0 | 1 | 59.0 | 2 | 0.227 |
| 2 | 9: [2, 97, 44, 26, 31, 13, 47, 75]… | 0.326 | 3 | 1 | 2 | 39.0 | 1 | 0.166 |
| 3 | 8: [6, 54, 65, 29, 55, 78, 46, 33] | 0.707 | 3 | 0 | 3 | 3.0 | 4 | 0.5 |
| 4 | 24: [24, 96, 36, 45, 15, 1, 69, 42]… | 0.793 | 97 | 75 | 22 | 2.0 | 67 | 0.511 |
| 5 | 4: [49, 91, 94, 8] | 0.455 | 0 | 0 | 0 | None | 0 | 0.749 |
| 6 | 5: [7, 34, 38, 21, 89] | 0.2 | 0 | 0 | 0 | None | 0 | 0.468 |
| 7 | 5: [39, 86, 67, 16, 25] | 0.589 | 14 | 3 | 11 | 24.5 | 18 | 0.5 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
