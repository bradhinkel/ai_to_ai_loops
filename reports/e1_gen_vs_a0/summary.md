# E1 comparison: ref `a0_core` vs `e1_cap_pilot`, `e1_gen`

Built 2026-10-19T15:34:42. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 6 | 1 |
| e1_cap_pilot | 20 | 10 | 9 | 11.79 | 20 | 0.45 | 2 | 0 |
| e1_gen | 100 | 8 | 11 | 58.86 | 22 | 0.37 | 5 | 1 |

Joint k-means over 220 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | a0_core | e1_cap_pilot | e1_gen |
|---|---|---|---|---|---|
| 0 | 65 | shared | 15 (23%) | 1 (2%) | 49 (75%) |
| 1 | 14 | shared | 9 (64%) | 4 (29%) | 1 (7%) |
| 2 | 15 | unique to e1_gen | 2 (13%) | 1 (7%) | 12 (80%) |
| 3 | 37 | ref only | 34 (92%) | 2 (5%) | 1 (3%) |
| 4 | 24 | shared | 11 (46%) | 1 (4%) | 12 (50%) |
| 5 | 7 | shared | 2 (29%) | 1 (14%) | 4 (57%) |
| 6 | 33 | shared | 16 (48%) | 10 (30%) | 7 (21%) |
| 7 | 25 | shared | 11 (44%) | 0 (0%) | 14 (56%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_e1_cap_pilot.jpg`, `endpoints_e1_gen.jpg`.

Warnings:
- e1_cap_pilot: only 20 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful

CLIP is used for steering only and does not appear in any number above.
