# E3-P: 20-seed cells projected into the e3_1_haiku_100 atlas

Reference: anonymised MiniLM atlas of e3_1_haiku_100, k 198, 46 persistent clusters, 13 shared wells; the reference cell's own late-step inside share is 0.268 and 30 of 100 trajectories make a persistent visit to a shared well (raw atlas: k 198, 5 shared wells). Late = steps >= 25. Projected cells are anonymised with their own name filter and labelled against the reference centroids (radius 0.15, hysteresis 1.25); nothing is refit.

| cell | inside share, late (anon / raw) | trajectories with a persistent visit to a shared Haiku well (anon / raw) | trajectories touching a shared well at any step | distinct shared wells visited (anon) | median late distance to nearest shared well (anon) |
|---|---|---|---|---|---|
| e3_1_haiku | 0.064 / 0.007 | 3 / 0 of 20 | 6 | [16, 39, 46, 115] | 0.252 |
| e3_1_sonnet | 0.023 / 0.001 | 2 / 0 of 20 | 5 | [16, 39] | 0.281 |
| e3_1_mistral | 0.000 / 0.000 | 0 / 0 of 20 | 0 | [] | 0.513 |
| e3_1_qwen | 0.000 / 0.000 | 0 / 0 of 20 | 0 | [] | 0.495 |
| e3_1_llava | 0.000 / 0.000 | 0 / 0 of 20 | 0 | [] | 0.492 |
| e3_d_haiku | 0.049 / 0.001 | 0 / 0 of 20 | 17 | [] | 0.219 |
| e3_d_mistral | 0.000 / 0.000 | 0 / 0 of 20 | 0 | [] | 0.492 |

## Verdicts

- **P1_same_model**: {"traj_persistent": 3, "inside": 0.064, "ref_inside": 0.268, "holds": false}
- **P2_sonnet_overlaps**: {"traj_persistent": 2, "inside_ratio": 0.3541666666666667, "wells": [16, 39], "holds": true}
- **P3_e3_1_mistral**: {"traj_persistent": 0, "inside_ratio": 0.0, "holds": true}
- **P3_e3_1_qwen**: {"traj_persistent": 0, "inside_ratio": 0.0, "holds": true}
- **P3_e3_1_llava**: {"traj_persistent": 0, "inside_ratio": 0.0, "holds": true}
- **P4b_embedding**: {"nn_haiku_d": 0.2193859666384591, "nn_mistral_d": 0.49153486740122165, "haiku_d_touching": 17, "holds": true}

## Which wells (anon reference cluster ids, as in `sw_cluster_e3_1_haiku_100_anon.md`)

- e3_1_haiku: traj 5 -> wells {39: 1}; traj 6 -> wells {46: 1, 115: 1}; traj 9 -> wells {16: 1}
- e3_1_sonnet: traj 4 -> wells {16: 1}; traj 9 -> wells {39: 1}
