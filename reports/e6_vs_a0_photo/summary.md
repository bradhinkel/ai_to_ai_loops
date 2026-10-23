# E1 comparison: ref `a0_photo` vs `e6_photo`, `e6_track`

Built 2026-10-23T09:40:47. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 6 clusters, pooled r95 = 0.783.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_photo (ref) | 100 | 6 | 8 | 43.89 | 15 | 0.91 | 2 | 1 |
| e6_photo | 192 | 10 | 8 | 48.38 | – | 0.30 | 2 | 4 |
| e6_track | 192 | 8 | 8 | 43.05 | – | 0.49 | 1 | 5 |

Joint k-means over 484 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | a0_photo | e6_photo | e6_track |
|---|---|---|---|---|---|
| 0 | 81 | unique to e6_photo+e6_track | 1 (1%) | 34 (42%) | 46 (57%) |
| 1 | 42 | unique to e6_photo+e6_track | 0 (0%) | 22 (52%) | 20 (48%) |
| 2 | 50 | unique to e6_photo+e6_track | 1 (2%) | 37 (74%) | 12 (24%) |
| 3 | 41 | shared | 23 (56%) | 14 (34%) | 4 (10%) |
| 4 | 138 | shared | 60 (44%) | 43 (31%) | 35 (25%) |
| 5 | 56 | unique to e6_photo+e6_track | 2 (4%) | 37 (66%) | 17 (30%) |
| 6 | 64 | unique to e6_track | 1 (2%) | 5 (8%) | 58 (91%) |
| 7 | 12 | ref only | 12 (100%) | 0 (0%) | 0 (0%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_photo.jpg`, `endpoints_e6_photo.jpg`, `endpoints_e6_track.jpg`.

Warnings:
- e6_photo: only 19 steps in the drift series; plateau needs >= 30
- e6_track: only 19 steps in the drift series; plateau needs >= 30

CLIP is used for steering only and does not appear in any number above.
