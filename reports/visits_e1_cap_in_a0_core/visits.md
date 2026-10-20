# Transient visits: e1_cap attractors inside a0_core's trajectories

Probes: k-means k=8 on e1_cap step-99 DINOv2. Scan: every cached step 1..99 of a0_core (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 16: [1, 4, 10, 14, 37, 38, 45, 55]… | 0.72 | 24 | 2 | 22 | 23.0 | 27 | 0.26 |
| 1 | 23: [3, 7, 8, 17, 27, 31, 32, 35]… | 0.815 | 70 | 17 | 53 | 7.0 | 56 | 0.461 |
| 2 | 13: [6, 28, 30, 42, 47, 52, 53, 58]… | 0.207 | 17 | 0 | 17 | 50.0 | 3 | 0.1 |
| 3 | 9: [2, 11, 19, 44, 63, 71, 87, 88]… | 0.206 | 4 | 0 | 4 | 51.0 | 9 | 0.061 |
| 4 | 9: [15, 21, 22, 25, 48, 61, 72, 92]… | 0.2 | 3 | 0 | 3 | 36.0 | 3 | 0.113 |
| 5 | 11: [13, 16, 20, 43, 50, 56, 74, 75]… | 0.453 | 43 | 35 | 8 | 22.0 | 73 | 0.064 |
| 6 | 7: [0, 5, 24, 33, 51, 60, 91] | 0.666 | 23 | 11 | 12 | 37.0 | 4 | 0.416 |
| 7 | 12: [9, 12, 18, 23, 26, 29, 34, 39]… | 0.274 | 3 | 0 | 3 | 44.0 | 4 | 0.095 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
