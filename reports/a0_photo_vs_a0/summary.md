# E1 comparison: ref `a0_core` vs `a0_photo`

Built 2026-10-20T21:34:50. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 6 | 1 |
| a0_photo | 100 | 6 | 8 | 43.89 | 15 | 0.48 | 6 | 1 |

Joint k-means over 200 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | a0_core | a0_photo |
|---|---|---|---|---|
| 0 | 42 | shared | 16 (38%) | 26 (62%) |
| 1 | 23 | shared | 11 (48%) | 12 (52%) |
| 2 | 37 | shared | 26 (70%) | 11 (30%) |
| 3 | 50 | shared | 21 (42%) | 29 (58%) |
| 4 | 20 | shared | 8 (40%) | 12 (60%) |
| 5 | 9 | unique to a0_photo | 1 (11%) | 8 (89%) |
| 6 | 9 | ref only | 9 (100%) | 0 (0%) |
| 7 | 10 | shared | 8 (80%) | 2 (20%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_a0_photo.jpg`.

CLIP is used for steering only and does not appear in any number above.
