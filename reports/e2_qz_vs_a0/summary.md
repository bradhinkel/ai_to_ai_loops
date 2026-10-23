# E1 comparison: ref `a0_core` vs `e2_qz`

Built 2026-10-23T02:42:11. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 2 | 5 |
| e2_qz | 100 | 12 | 9 | 35.62 | 19 | 0.85 | 2 | 4 |

Joint k-means over 200 pooled final-step DINOv2 embeddings: k = 11 (elbow 11).

| joint cluster | size | label | a0_core | e2_qz |
|---|---|---|---|---|
| 0 | 12 | unique to e2_qz | 2 (17%) | 10 (83%) |
| 1 | 20 | unique to e2_qz | 0 (0%) | 20 (100%) |
| 2 | 9 | ref only | 9 (100%) | 0 (0%) |
| 3 | 28 | unique to e2_qz | 2 (7%) | 26 (93%) |
| 4 | 11 | ref only | 11 (100%) | 0 (0%) |
| 5 | 29 | unique to e2_qz | 5 (17%) | 24 (83%) |
| 6 | 5 | ref only | 5 (100%) | 0 (0%) |
| 7 | 6 | ref only | 6 (100%) | 0 (0%) |
| 8 | 34 | ref only | 34 (100%) | 0 (0%) |
| 9 | 6 | shared | 2 (33%) | 4 (67%) |
| 10 | 40 | shared | 24 (60%) | 16 (40%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_e2_qz.jpg`.

CLIP is used for steering only and does not appear in any number above.
