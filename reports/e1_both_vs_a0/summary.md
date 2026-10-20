# E1 comparison: ref `a0_core` vs `e1_cap_pilot`, `e1_gen`, `e1_both`

Built 2026-10-20T03:53:35. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 4 | 1 |
| e1_cap_pilot | 20 | 10 | 9 | 11.79 | 20 | 0.45 | 1 | 0 |
| e1_gen | 100 | 8 | 11 | 58.86 | 22 | 0.37 | 3 | 2 |
| e1_both | 100 | 8 | 7 | 39.23 | 25 | 0.78 | 2 | 3 |

Joint k-means over 320 pooled final-step DINOv2 embeddings: k = 8 (elbow 8).

| joint cluster | size | label | a0_core | e1_cap_pilot | e1_gen | e1_both |
|---|---|---|---|---|---|---|
| 0 | 115 | shared | 31 (27%) | 4 (4%) | 54 (47%) | 26 (23%) |
| 1 | 37 | ref only | 34 (92%) | 2 (5%) | 1 (3%) | 0 (0%) |
| 2 | 18 | shared | 9 (50%) | 4 (22%) | 1 (6%) | 4 (22%) |
| 3 | 57 | unique to e1_gen+e1_both | 7 (12%) | 1 (2%) | 23 (40%) | 26 (46%) |
| 4 | 23 | unique to e1_gen+e1_both | 1 (4%) | 1 (4%) | 5 (22%) | 16 (70%) |
| 5 | 33 | unique to e1_both | 0 (0%) | 6 (18%) | 0 (0%) | 27 (82%) |
| 6 | 25 | shared | 11 (44%) | 1 (4%) | 12 (48%) | 1 (4%) |
| 7 | 12 | shared | 7 (58%) | 1 (8%) | 4 (33%) | 0 (0%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_e1_cap_pilot.jpg`, `endpoints_e1_gen.jpg`, `endpoints_e1_both.jpg`.

Warnings:
- e1_cap_pilot: only 20 trajectories; elbow k needs >= 30 and k-means/Vendi/overlap shares are not meaningful

CLIP is used for steering only and does not appear in any number above.
