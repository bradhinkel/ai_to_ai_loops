# E3-S (100 seeds) and E3-W (20-word summary): Haiku compress–expand

Predictions: predictions.md "E3 scale and bottleneck width" (2026-11-02). Pair-sharing rule and k scaling as stated there; anonymised = names → X (E3-A filter).

**Speculation 1 (numerous wells): in between: sharing pairs present but no well reused by >= 4 (W > 500 at this n).** S1_wells_numerous fails; S2_replication_first20 fails; S3_density fails; S4_seed_trace fails

## Cells

| cell | n | half-life | own seed 10 / 50 / 99 | nn-other raw / anon | within 0.15 raw / anon | Vendi story / summary at 99 | words at 99 | summary words (≤20 / ≤50) | top-10 cover | top names 50–99 | modal tuple (share) | woman / hopeful |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e3_1_sonnet | 20 | 45 | 0.8 / 0.65 / 0.45 | 0.381 / 0.293 | 0.000 / 0.000 | 10.3 / 14.0 | 558 | 48.0 (0.00 / 0.86) | 0.40 | Mara 87, Pip 43, Dev 40, Priya 39, Marisol 37 | young_adult × interpersonal × hopeful (0.07) | 0.62 / 0.61 |
| e3_d_sonnet | 20 | 1 | 0.0 / 0.05 / 0.0 | 0.227 / 0.192 | 0.105 / 0.219 | 7.0 / 7.5 | 542 | 22.0 (0.30 / 1.00) | 0.57 | Marta 148, Marguerite 98, Daniel 78, Walter 76, Dev 36 | older_adult × internal × hopeful (0.15) | 0.82 / 0.72 |

## E3-S: pair sharing at n = 20 (k 40)

| atlas | persistent | shared (≥ 2 traj) | sharing pairs / pairs | rate | max trajectories in one cluster | W-hat | steps inside |
|---|---|---|---|---|---|---|---|
| raw | 1 | 0 | 0 / 190 | 0.0000 | 0 | None | 0.01 |
| anon | 5 | 5 | 13 / 190 | 0.0684 | 4 | 15 | 0.17 |

Random 20-trajectory subsamples (5, k 40): shared clusters median raw 0 (IQR [0.0, 0.0]), anon 5 (IQR [5.0, 5.0]); mean sharing pairs raw 0.00, anon 13.00; largest multiplicity raw 0, anon 4. The 20-trajectory cell e3_1_haiku had 0 shared (raw).

Sharing pairs vs n (mean over 10 draws, k scaled): n 10: raw 0.0, anon 12.2 of 45; n 20: raw 0.0, anon 13.0 of 190. A fixed well count gives pairs ∝ n(n−1)/2.

Fresh sample of seeds 0–19: half-life 1 (20-trajectory subsample median over all 100: 1, IQR [1.0, 1.0]); nn-other 0.227; words 542; top-10 cover 0.57, top names Marta 148, Marguerite 98, Daniel 78, Walter 76, Dev 36; modal tuple older_adult × internal × hopeful (0.15).

Same-seed check (base vs scale, seeds 0–19, steps 50–99, median nearest-step distance): same-seed 0.437 vs different-seed 0.440 (gap 0.003; anonymised gap 0.005); 0 of 20 same-seed pairs share a persistent cluster in the joint atlas (k 79, 0 shared clusters, 0 sharing pairs).

Shared-cluster sheets: `sw_cluster_e3_d_sonnet_raw.md`, `sw_cluster_e3_d_sonnet_anon.md`.

## Verdicts

- **S1_wells_numerous**: {"anon_sharing_pairs": 13, "anon_rate": 0.06842105263157895, "anon_shared_clusters": 5, "anon_max_mult": 4, "raw_shared_clusters": 0, "raw_sharing_pairs": 0, "W_hat_anon": 14.615384615384615, "sub_raw_shared_median": 0.0, "sub_anon_shared_median": 5.0, "holds": false, "fails": false}
- **S2_replication_first20**: {"half_life": 1, "half_in_8_15": false, "cover": 0.571715145436309, "cover_in_band": true, "top_name": "Marta", "maya_top": false, "words": 542.5, "words_in_band": false, "modal": ["older_adult", "internal", "hopeful"], "base_modal": ["young_adult", "interpersonal", "hopeful"], "modal_same": false, "all100": {"half_life_sub_median": 1.0, "cover": 0.571715145436309, "words": 542.5}, "holds": false}
- **S3_density**: {"nn_other": 0.22712790198591565, "base_nn": 0.38108370731356606, "nn_in_band": false, "within_015": 0.10533333333333333, "within_in_band": false, "holds": false, "continuum": false}
- **S4_seed_trace**: {"gap_raw": 0.0030844105431340196, "gap_anon": 0.005105251318978654, "gap_in_band": false, "same_seed_pairs_sharing": 0, "le_1": true, "holds": false}
- **speculation_1**: in between: sharing pairs present but no well reused by >= 4 (W > 500 at this n)

![curves](d_sonnet_alone.png)

