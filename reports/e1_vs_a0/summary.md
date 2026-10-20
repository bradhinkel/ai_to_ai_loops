# E1 comparison: ref `a0_core` vs `e1_cap`, `e1_gen`, `e1_both`

Built 2026-10-20T11:26:31. Final step 99 (or each trajectory's last complete step). Step 0 excluded. Spaces: DINOv2 `facebook/dinov2-base` @ f9e44c81 (primary), MiniLM `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 (secondary). Ref archive: 8 clusters, pooled r95 = 0.747.

| run | n traj | elbow k DINOv2 | elbow k MiniLM | Vendi (DINOv2) | plateau step (DINOv2) | share inside A0 radii | # shared clusters | # unique clusters |
|---|---|---|---|---|---|---|---|---|
| a0_core (ref) | 100 | 8 | 7 | 31.83 | 15 | 0.92 | 4 | 0 |
| e1_cap | 100 | 8 | 6 | 32.27 | 32 | 0.53 | 3 | 3 |
| e1_gen | 100 | 8 | 11 | 58.86 | 22 | 0.37 | 2 | 2 |
| e1_both | 100 | 8 | 7 | 39.23 | 25 | 0.78 | 0 | 4 |

Joint k-means over 400 pooled final-step DINOv2 embeddings: k = 9 (elbow 9).

| joint cluster | size | label | a0_core | e1_cap | e1_gen | e1_both |
|---|---|---|---|---|---|---|
| 0 | 33 | unique to e1_cap+e1_both | 2 (6%) | 12 (36%) | 2 (6%) | 17 (52%) |
| 1 | 48 | shared | 35 (73%) | 11 (23%) | 1 (2%) | 1 (2%) |
| 2 | 26 | shared | 11 (42%) | 2 (8%) | 12 (46%) | 1 (4%) |
| 3 | 91 | unique to e1_gen+e1_both | 9 (10%) | 6 (7%) | 31 (34%) | 45 (50%) |
| 4 | 114 | shared | 34 (30%) | 26 (23%) | 48 (42%) | 6 (5%) |
| 5 | 31 | unique to e1_cap+e1_both | 0 (0%) | 20 (64%) | 0 (0%) | 11 (36%) |
| 6 | 15 | unique to e1_cap | 2 (13%) | 13 (87%) | 0 (0%) | 0 (0%) |
| 7 | 23 | unique to e1_gen+e1_both | 1 (4%) | 1 (4%) | 5 (22%) | 16 (70%) |
| 8 | 19 | shared | 6 (32%) | 9 (47%) | 1 (5%) | 3 (16%) |

Figures: `drift_dinov2.png`, `drift_minilm.png`, `elbow.png`, `joint_clusters.jpg`, `endpoints_a0_core.jpg`, `endpoints_e1_cap.jpg`, `endpoints_e1_gen.jpg`, `endpoints_e1_both.jpg`.

CLIP is used for steering only and does not appear in any number above.
