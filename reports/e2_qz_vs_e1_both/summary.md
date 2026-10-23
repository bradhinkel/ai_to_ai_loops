# E1 comparison: ref `e1_both` vs `e2_qz`

Built 2026-10-23T02:41:57. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.673.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| e1_both (ref) | 100 | 8 | 7 | 39.23 | 25 | 0.94 | 6 | 0 |
| e2_qz | 100 | 12 | 9 | 35.62 | 19 | 0.79 | 6 | 2 |

Joint k-means over 200 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | e1_both | e2_qz |
|---|---|---|---|---|
| 0 | 19 | shared | 13 (68%) | 6 (32%) |
| 1 | 20 | shared | 5 (25%) | 15 (75%) |
| 2 | 18 | shared | 10 (56%) | 8 (44%) |
| 3 | 58 | shared | 26 (45%) | 32 (55%) |
| 4 | 29 | shared | 19 (66%) | 10 (34%) |
| 5 | 12 | unique to e2_qz | 2 (17%) | 10 (83%) |
| 6 | 28 | shared | 22 (79%) | 6 (21%) |
| 7 | 16 | unique to e2_qz | 3 (19%) | 13 (81%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_e1_both.jpg`, `endpoints_e2_qz.jpg`.

CLIP is used for steering only and does not appear in any number above.
