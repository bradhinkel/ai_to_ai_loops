# E1 comparison: ref `a0_core` vs `a0_s`

Built 2026-10-21T14:35:47. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 5 | 2 |
| a0_s | 100 | 9 | 9 | 36.44 | 23 | 0.50 | 5 | 3 |

Joint k-means over 200 pooled final-step DINOv2 embeddings: k = 10 (elbow 10).

| joint cluster | size | label | a0_core | a0_s |
|---|---|---|---|---|
| 0 | 17 | unique to a0_s | 1 (6%) | 16 (94%) |
| 1 | 11 | unique to a0_s | 2 (18%) | 9 (82%) |
| 2 | 41 | shared | 32 (78%) | 9 (22%) |
| 3 | 14 | unique to a0_s | 1 (7%) | 13 (93%) |
| 4 | 12 | ref only | 10 (83%) | 2 (17%) |
| 5 | 23 | shared | 11 (48%) | 12 (52%) |
| 6 | 15 | shared | 6 (40%) | 9 (60%) |
| 7 | 18 | shared | 7 (39%) | 11 (61%) |
| 8 | 9 | ref only | 9 (100%) | 0 (0%) |
| 9 | 40 | shared | 21 (52%) | 19 (48%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_a0_s.jpg`.

CLIP is used for steering only and does not appear in any number above.
