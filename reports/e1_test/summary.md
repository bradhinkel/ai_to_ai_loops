# E1 comparison: ref `a0_pilot` vs `a0_smoke`, `a0_batchtest2`

Built 2026-10-18T17:49:25. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 10 clusters, pooled r95 = 0.212.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_pilot (ref) | 20 | 10 | 8 | 12.43 | 23 | 0.90 | 1 | 8 |
| a0_smoke | 2 | – | – | 1.98 | – | 0.00 | 1 | 1 |
| a0_batchtest2 | 4 | – | – | 3.99 | – | 0.00 | 1 | 3 |

Joint k-means over 26 pooled final-step DINOv2 embeddings: k = 12 (elbow 14).

| joint cluster | size | label | a0_pilot | a0_smoke | a0_batchtest2 |
|---|---|---|---|---|---|
| 0 | 5 | ref only | 5 (100%) | 0 (0%) | 0 (0%) |
| 1 | 4 | ref only | 4 (100%) | 0 (0%) | 0 (0%) |
| 2 | 1 | ref only | 1 (100%) | 0 (0%) | 0 (0%) |
| 3 | 3 | ref only | 3 (100%) | 0 (0%) | 0 (0%) |
| 4 | 2 | ref only | 2 (100%) | 0 (0%) | 0 (0%) |
| 5 | 2 | unique to a0_smoke+a0_batchtest2 | 0 (0%) | 1 (50%) | 1 (50%) |
| 6 | 3 | shared | 1 (33%) | 1 (33%) | 1 (33%) |
| 7 | 1 | unique to a0_batchtest2 | 0 (0%) | 0 (0%) | 1 (100%) |
| 8 | 2 | ref only | 2 (100%) | 0 (0%) | 0 (0%) |
| 9 | 1 | ref only | 1 (100%) | 0 (0%) | 0 (0%) |
| 10 | 1 | ref only | 1 (100%) | 0 (0%) | 0 (0%) |
| 11 | 1 | unique to a0_batchtest2 | 0 (0%) | 0 (0%) | 1 (100%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_pilot.jpg`, `endpoints_a0_smoke.jpg`, `endpoints_a0_batchtest2.jpg`.

Warnings:
- a0_pilot: only 20 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful
- a0_smoke: only 2 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful
- a0_batchtest2: only 4 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful
- a0_smoke: only 2 steps in the drift series; plateau needs >= 30
- a0_batchtest2: only 0 steps in the drift series; plateau needs >= 30
- joint clustering pools only 26 endpoints; its k and labels are not meaningful

CLIP is used for steering only and does not appear in any number above.
