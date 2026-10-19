# E1 comparison: ref `a0_core` vs `e1_cap_pilot`

Built 2026-10-19T00:31:47. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 2 | 5 |
| e1_cap_pilot | 20 | 10 | 9 | 11.79 | 20 | 0.45 | 2 | 1 |

Joint k-means over 120 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | a0_core | e1_cap_pilot |
|---|---|---|---|---|
| 0 | 6 | shared | 2 (33%) | 4 (67%) |
| 1 | 5 | unique to e1_cap_pilot | 0 (0%) | 5 (100%) |
| 2 | 9 | ref only | 9 (100%) | 0 (0%) |
| 3 | 10 | shared | 7 (70%) | 3 (30%) |
| 4 | 12 | ref only | 11 (92%) | 1 (8%) |
| 5 | 27 | ref only | 27 (100%) | 0 (0%) |
| 6 | 36 | ref only | 30 (83%) | 6 (17%) |
| 7 | 15 | ref only | 14 (93%) | 1 (7%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_e1_cap_pilot.jpg`.

Warnings:
- e1_cap_pilot: only 20 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful

CLIP is used for steering only and does not appear in any number above.
