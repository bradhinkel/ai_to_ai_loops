# E1 comparison: ref `a0_core` vs `bimg`, `arm_a`

Built 2026-10-22T11:04:54. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 3 | 3 |
| bimg | 20 | 10 | 10 | 12.66 | 35 | 0.80 | 1 | 0 |
| arm_a | 20 | 10 | 8 | 13.78 | 32 | 0.75 | 2 | 0 |

Joint k-means over 140 pooled final-step DINOv2 embeddings: k = 6 (elbow 6).

| joint cluster | size | label | a0_core | bimg | arm_a |
|---|---|---|---|---|---|
| 0 | 11 | ref only | 9 (82%) | 1 (9%) | 1 (9%) |
| 1 | 8 | shared | 5 (62%) | 1 (12%) | 2 (25%) |
| 2 | 45 | ref only | 34 (76%) | 8 (18%) | 3 (7%) |
| 3 | 18 | shared | 11 (61%) | 2 (11%) | 5 (28%) |
| 4 | 40 | ref only | 32 (80%) | 2 (5%) | 6 (15%) |
| 5 | 18 | shared | 9 (50%) | 6 (33%) | 3 (17%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_bimg.jpg`, `endpoints_arm_a.jpg`.

Warnings:
- bimg: only 20 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful
- arm_a: only 20 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful

CLIP is used for steering only and does not appear in any number above.
