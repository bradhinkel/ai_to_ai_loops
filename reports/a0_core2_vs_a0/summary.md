# E1 comparison: ref `a0_core` vs `a0_core2`, `a0_photo`

Built 2026-10-21T07:50:33. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 7 | 0 |
| a0_core2 | 100 | 10 | 8 | 34.76 | 14 | 0.62 | 7 | 0 |
| a0_photo | 100 | 6 | 8 | 43.89 | 15 | 0.48 | 5 | 1 |

Joint k-means over 300 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | a0_core | a0_core2 | a0_photo |
|---|---|---|---|---|---|
| 0 | 91 | shared | 34 (37%) | 34 (37%) | 23 (25%) |
| 1 | 33 | shared | 11 (33%) | 10 (30%) | 12 (36%) |
| 2 | 10 | shared | 5 (50%) | 5 (50%) | 0 (0%) |
| 3 | 14 | shared | 6 (43%) | 5 (36%) | 3 (21%) |
| 4 | 97 | shared | 23 (24%) | 30 (31%) | 44 (45%) |
| 5 | 15 | shared | 9 (60%) | 6 (40%) | 0 (0%) |
| 6 | 11 | unique to a0_photo | 1 (9%) | 2 (18%) | 8 (73%) |
| 7 | 29 | shared | 11 (38%) | 8 (28%) | 10 (34%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_a0_core2.jpg`, `endpoints_a0_photo.jpg`.

CLIP is used for steering only and does not appear in any number above.
