# Transient visits: e1_cap_pilot attractors inside a0_core's trajectories

Probes: k-means k=10 on e1_cap_pilot step-99 DINOv2. Scan: every cached step 1..99 of a0_core (10000 steps, 100 trajectories), DINOv2 cosine distance. Radius = probe p95 member distance, floor 0.2. 'visited' = any step inside; 'stayed' = final step inside; 'transient' = visited, not stayed. Orange frame in the sheets = stayed.

| probe | members (probes run) | radius | visited | stayed | transient | median first visit step | longest transient dwell (steps) | nearest distance |
|---|---|---|---|---|---|---|---|---|
| 0 | 4: [0, 5, 8, 11] | 0.2 | 3 | 0 | 3 | 45.0 | 7 | 0.08 |
| 1 | 5: [9, 12, 17, 18, 19] | 0.2 | 0 | 0 | 0 | None | 0 | 0.279 |
| 2 | 2: [13, 16] | 0.201 | 0 | 0 | 0 | None | 0 | 0.271 |
| 3 | 2: [7, 10] | 0.2 | 0 | 0 | 0 | None | 0 | 0.275 |
| 4 | 1: [6] | 0.2 | 0 | 0 | 0 | None | 0 | 0.348 |
| 5 | 2: [2, 15] | 0.2 | 9 | 0 | 9 | 52.0 | 3 | 0.09 |
| 6 | 1: [4] | 0.2 | 0 | 0 | 0 | None | 0 | 0.398 |
| 7 | 1: [3] | 0.2 | 0 | 0 | 0 | None | 0 | 0.211 |
| 8 | 1: [14] | 0.2 | 2 | 0 | 2 | 54.0 | 1 | 0.146 |
| 9 | 1: [1] | 0.2 | 0 | 0 | 0 | None | 0 | 0.54 |

Sheets: `probe_<k>.jpg`, top row = the probe's members at step 99 in the probes run; rows 2-3 = the nearest intermediate images in the scanned run (one per trajectory, its closest step).
