# Transient visits: a0_core attractors inside e1_cap_pilot's trajectories

Probes: archive/a0_core_centroids.npz. Scan: every cached step 1..99 of e1_cap_pilot (2000 steps, 20 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 11: [90, 17, 10, 88, 57, 59, 93, 9]… | 0.2 | 2 | 0 | 2 | 11.5 | 24 | 0.052 |
| 1 | 34: [5, 95, 92, 35, 82, 60, 58, 87]… | 0.323 | 4 | 0 | 4 | 19.5 | 16 | 0.132 |
| 2 | 9: [2, 97, 44, 26, 31, 13, 47, 75]… | 0.326 | 2 | 0 | 2 | 22.0 | 5 | 0.098 |
| 3 | 8: [6, 54, 65, 29, 55, 78, 46, 33] | 0.707 | 3 | 1 | 2 | 10.0 | 8 | 0.525 |
| 4 | 24: [24, 96, 36, 45, 15, 1, 69, 42]… | 0.793 | 20 | 9 | 11 | 5.5 | 79 | 0.533 |
| 5 | 4: [49, 91, 94, 8] | 0.455 | 0 | 0 | 0 | None | 0 | 0.679 |
| 6 | 5: [7, 34, 38, 21, 89] | 0.2 | 0 | 0 | 0 | None | 0 | 0.222 |
| 7 | 5: [39, 86, 67, 16, 25] | 0.589 | 1 | 0 | 1 | 47.0 | 10 | 0.526 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
