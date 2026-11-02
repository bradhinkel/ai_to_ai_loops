# E3-C: absolute-length rewrite and the new models

Cells: e3_1_haiku, e3_2b_haiku, e3_1_mistral, e3_2b_mistral, e3_2b_qwen. Same measurements as the E3 gate; gate cells in grey in `c_curves.png`. Atlas: joint k-means over these cells only (k 40), radius 0.15, hysteresis 1.25, dwell ≥ 5, ≥ 3 visits; shared = ≥ 2 trajectories. nn-other = median cosine distance (steps ≥ 25) to the nearest step of any other trajectory. Theme tuple = lead_age × conflict_type × ending_valence from the Haiku judge (reported, never fed back); tuple B swaps lead_age for lead_gender (post-hoc robustness, see theme.md).

## Verdicts

| cell | prediction | holds | numbers |
|---|---|---|---|
| e3_1_haiku | C1_length_450_550 | yes | {"words_median_99": 501.5, "band": [450, 550]} |
| e3_1_haiku | C4_size_axis | yes | {"half_life": 11, "sonnet_half": 45, "half_le_30": true, "top10_cover": 0.542, "sonnet_cover": 0.402, "cover_ge_05": true, "words_99": 501.5, "holds_500": true, "modal_tuple": ["young_adult", "internal", "hopeful"], "sonnet_modal": ["young_adult", "interpersonal", "hopeful"], "fields_agree": 2, "agree_ge2": true, "tuple_b_haiku": ["woman", "internal", "hopeful"], "tuple_b_sonnet": ["woman", "interpersonal", "hopeful"], "tuple_b_agree": 2} |
| e3_2b_haiku | C1_length_450_550 | no | {"words_median_99": 555.5, "band": [450, 550]} |
| e3_2b_haiku | C2_rewrite_reproduces | no | {"half_life": null, "half_gt_99": true, "cum99": 0.093, "own_e3_1_cum99": 0.487, "cum99_below_e3_1": true, "shared": 1, "self_share": 1.0} |
| e3_1_mistral | C3_mistral_distinct | no | {"shared": 1, "nn_other": 0.33, "nn_in_band": false, "half_life": 22, "qwen_half": 14, "sonnet_half": 45, "half_between": true, "top10_cover": 0.503, "cover_ge_05": true, "shared_names_with_qwen": ["Elara"], "le3_shared": true, "cjk_stories": 0, "no_code_switch": true, "modal_tuple": ["unclear", "social_or_community", "hopeful"], "qwen_modal": ["unclear", "none_or_unclear", "hopeful"], "differs_ge1": true} |
| e3_2b_mistral | C1_length_450_550 | no | {"words_median_99": 308.0, "band": [400, 600]} |
| e3_2b_mistral | C2_rewrite_reproduces | yes | {"half_life": null, "half_gt_99": true, "cum99": 0.237, "own_e3_1_cum99": 0.482, "cum99_below_e3_1": true, "shared": 0, "self_share": 0.995} |
| e3_2b_qwen | C1_length_450_550 | no | {"words_median_99": 285.5, "band": [450, 550]} |
| e3_2b_qwen | C1_copies_below_half_of_E3_2 | yes | {"copies": 65, "e3_2": 276} |
| e3_2b_qwen | C2_rewrite_reproduces | yes | {"half_life": null, "half_gt_99": true, "cum99": 0.23, "own_e3_1_cum99": 0.559, "cum99_below_e3_1": true, "shared": 0, "self_share": 0.964} |

## Cells

| cell | plateau | step drift first 5 → last 20 | dist from step 1 at 99 | half-life | own seed at 10 / 50 / 99 | Vendi 1 → 99 | persistent (shared) | steps inside | nn-other | self-share 50–99 | words at 99 (min–max) | exact copies | CJK | top-10 names cover | top names 50–99 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e3_1_haiku | 12 | 0.222 → 0.185 | 0.487 | 11 | 0.6 / 0.45 / 0.2 | 10.3 → 9.5 | 2 (0) | 0.07 | 0.342 | 0.66 | 502 (399–576) | 0 | 0 | 0.54 | Maya 200, Nora 55, Daniel 52, Priya 43, Mara 39, Walt 37 |
| e3_2b_haiku | 11 | 0.019 → 0.010 | 0.093 | None | 1.0 / 1.0 / 1.0 | 11.3 → 10.6 | 1 (1) | 0.08 | 0.451 | 1.00 | 556 (447–625) | 631 | 0 | 0.59 | Eli 50, Ilse 50, Jenna 50, Mara 50, Eleanor 50, Trafalgar 50 |
| e3_1_mistral | 18 | 0.169 → 0.120 | 0.482 | 22 | 0.85 / 0.3 / 0.3 | 9.6 → 9.1 | 1 (1) | 0.03 | 0.330 | 0.87 | 388 (321–451) | 0 | 0 | 0.50 | Meadowgrove 68, Amelia 67, Mia 56, Aurora 50, Eldoria 46, Elara 45 |
| e3_2b_mistral | 11 | 0.085 → 0.090 | 0.237 | None | 1.0 / 1.0 / 1.0 | 10.4 → 9.8 | 6 (0) | 0.20 | 0.394 | 0.99 | 308 (222–381) | 7 | 0 | 0.83 | Victor 50, Alex 50, Eloria 50, Tech 50, Henry 50, Mina 50 |
| e3_2b_qwen | 11 | 0.048 → 0.043 | 0.230 | None | 1.0 / 1.0 / 0.95 | 11.7 → 11.1 | 5 (0) | 0.14 | 0.419 | 0.96 | 286 (171–446) | 65 | 27 | 0.71 | Sarah 92, Ella 78, Lily 59, Mark 50, Kael 50, Eldershire 50 |

Gate references: e3_1_sonnet: half-life 45, dist@99 0.448, words@99 558, copies 0, cover 0.40; e3_2_sonnet: half-life None, dist@99 0.274, words@99 533, copies 2, cover 0.56; e3_1_qwen: half-life 14, dist@99 0.559, words@99 431, copies 0, cover 0.51; e3_2_qwen: half-life None, dist@99 0.299, words@99 83, copies 276, cover 0.79; e3_1_llava: half-life 22, dist@99 0.637, words@99 354, copies 0, cover 0.73; e3_2_llava: half-life None, dist@99 0.415, words@99 89, copies 162, cover 0.98

## Theme tuple (Haiku judge)

| cell | judged | eff. tuples 1–10 → 50–99 | modal late tuple (share) | tuple B modal late (share) | modal fields late |
|---|---|---|---|---|---|
| e3_1_haiku | 2000 | 23.3 → 23.6 | young_adult/internal/hopeful (0.16) | woman/internal/hopeful (0.30) | lead_age unclear 0.32, lead_gender woman 0.70, lead_role_class other_or_unclear 0.37, setting_place home_interior 0.28, setting_time present_day 0.71, conflict_type internal 0.52, ending_valence hopeful 0.73, secondary_character parent_or_grandparent 0.29, death_present False 0.57, reconciliation_present False 0.74, nature_central False 0.77 |
| e3_2b_haiku | 2000 | 22.2 → 21.3 | teen/internal/hopeful (0.09) | woman/internal/hopeful (0.25) | lead_age young_adult 0.32, lead_gender woman 0.75, lead_role_class other_or_unclear 0.30, setting_place institution 0.38, setting_time present_day 0.78, conflict_type internal 0.43, ending_valence hopeful 0.66, secondary_character other 0.24, death_present False 0.82, reconciliation_present False 0.90, nature_central False 0.80 |
| e3_1_mistral | 2000 | 9.9 → 7.5 | unclear/social_or_community/hopeful (0.33) | man/social_or_community/hopeful (0.19) | lead_age unclear 0.87, lead_gender man 0.44, lead_role_class artist_or_craftsperson 0.26, setting_place city 0.39, setting_time unclear 0.66, conflict_type social_or_community 0.39, ending_valence hopeful 0.88, secondary_character other 0.53, death_present False 0.90, reconciliation_present False 0.95, nature_central False 0.61 |
| e3_2b_mistral | 1994 | 13.6 → 11.5 | unclear/social_or_community/hopeful (0.16) | woman/none_or_unclear/hopeful (0.16) | lead_age unclear 0.78, lead_gender man 0.46, lead_role_class other_or_unclear 0.36, setting_place city 0.37, setting_time unclear 0.51, conflict_type none_or_unclear 0.38, ending_valence hopeful 0.71, secondary_character none 0.26, death_present False 1.00, reconciliation_present False 1.00, nature_central False 0.80 |
| e3_2b_qwen | 2000 | 15.7 → 13.4 | unclear/internal/neutral_or_ambiguous (0.18) | woman/none_or_unclear/hopeful (0.17) | lead_age unclear 0.72, lead_gender woman 0.58, lead_role_class other_or_unclear 0.32, setting_place institution 0.38, setting_time unclear 0.52, conflict_type none_or_unclear 0.31, ending_valence hopeful 0.66, secondary_character other 0.28, death_present False 1.00, reconciliation_present False 0.99, nature_central False 0.78 |

Compliance / flags: e3_1_haiku: {'summaries': 2000, 'summary_le50_share': 0.55, 'story_lt400_share': 0.02878787878787879, 'length_ratio_step99_median': 1.0335} flags {'story_refusal': 368, 'summary_over_50_words': 900, 'story_empty': 1}; e3_2b_haiku: {'summaries': 0, 'summary_le50_share': None, 'story_lt400_share': 0.0, 'length_ratio_step99_median': 1.1355} flags {'story_refusal': 100}; e3_1_mistral: {'summaries': 2000, 'summary_le50_share': 0.238, 'story_lt400_share': 0.6333333333333333, 'length_ratio_step99_median': 0.8325} flags {'summary_over_50_words': 1524, 'story_refusal': 8}; e3_2b_mistral: {'summaries': 0, 'summary_le50_share': None, 'story_lt400_share': 0.8767676767676768, 'length_ratio_step99_median': 0.6555} flags {'story_refusal': 96}; e3_2b_qwen: {'summaries': 0, 'summary_le50_share': None, 'story_lt400_share': 0.8904249871991807, 'length_ratio_step99_median': 0.639} flags {'story_cjk': 27}

Cluster sheets: `c_cluster_NN.md`. Figure: `c_curves.png`.