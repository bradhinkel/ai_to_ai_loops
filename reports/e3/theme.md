# E3-B: theme-layer coding of the six text cells

Judge claude-haiku-5-5 (effort low, default sampling, D16) on every story; second judge claude-sonnet-5-5 on a stratified subsample. Tuple = lead_age × conflict_type × ending_valence. Windows early (1, 10), late (50, 99). Atlas on theme-sentence MiniLM embeddings: joint k-means k 40, radius 0.15, hysteresis 1.25, dwell ≥ 5, ≥ 3 visits.

## Verdicts

| prediction | result | numbers |
|---|---|---|
| B1 collapse in E3-1 (eff. tuples late/early ≤ 0.5; modal late ≥ 0.25, early ≤ 0.15) | sonnet fails, qwen fails, llava fails | sonnet: ratio 1.17 (null 1.11), modal 0.10 → 0.07; qwen: ratio 0.84 (null 1.11), modal 0.23 → 0.26; llava: ratio 0.91 (null 1.05), modal 0.22 → 0.24 |
| B2 shared theme attractors (Sonnet ≥ 2, Qwen ≥ 1), multidimensional (≥ 3 fields ≥ 0.7) | fails | sonnet: shared 0, of which multidimensional 0; qwen: shared 0, of which multidimensional 0; llava: shared 0, of which multidimensional 0 |
| B3 attractors belong to the model (modal tuples differ; JS across models > within model) | fails | e3_1_sonnet: ('young_adult', 'interpersonal', 'hopeful') 0.07; e3_2_sonnet: ('young_adult', 'social_or_community', 'hopeful') 0.11; e3_1_qwen: ('unclear', 'none_or_unclear', 'hopeful') 0.26; e3_2_qwen: ('unclear', 'none_or_unclear', 'hopeful') 0.20; e3_1_llava: ('unclear', 'social_or_community', 'hopeful') 0.24; e3_2_llava: ('unclear', 'none_or_unclear', 'hopeful') 0.23; JS {"llava": {"within_model_loops": 0.193, "across_models_e3_1": {"qwen": 0.078, "sonnet": 0.399}}, "qwen": {"within_model_loops": 0.145, "across_models_e3_1": {"llava": 0.078, "sonnet": 0.439}}, "sonnet": {"within_model_loops": 0.244, "across_models_e3_1": {"llava": 0.399, "qwen": 0.439}}} |
| B4 setting place under Sonnet within ±20% entropy; setting time ≥ 80% present at 1–10 everywhere | fails | Sonnet place entropy change 0.030455886542270456; present share 1–10 sonnet 0.81, sonnet 0.75, qwen 0.53, qwen 0.53, llava 0.65, llava 0.65 |
| B5 rewrite cells do not move (JS early–late ≤ 0.05; ≥ 90% hold step-1 tuple at 99) | fails | sonnet: JS 0.061, hold 0.65; qwen: JS 0.073, hold 0.55; llava: JS 0.147, hold 0.15 |
| B6 theme memory: own step-0 tuple ≤ 0.5 by step 25; Sonnet > 0.2 at 99 | fails | sonnet: half 1, at 99 0.00; qwen: half 1, at 99 0.10; llava: half 2, at 99 0.10 |
| B7 reliability (≥ 6 of 10 fields κ ≥ 0.6; gender and death ≥ 0.8; heuristic agreement ≥ 0.85) | holds | n 286; fields ≥ 0.6: 8; κ lead_age 0.62, lead_gender 0.90, lead_role_class 0.76, setting_place 0.77, setting_time 0.42, conflict_type 0.79, ending_valence 0.63, secondary_character 0.59, death_present 0.85, reconciliation_present 0.76, nature_central 0.58; gender vs pronouns 0.89 |

## Tuple distribution per cell

| cell | judged (malformed) | eff. tuples 1–10 → 50–99 (null ratio) | modal tuple 50–99 (share) | top-5 late | tuple attractors (ii): tuple, trajectories, runs | hold step-1 at 99 | theme memory half / at 99 |
|---|---|---|---|---|---|---|---|
| e3_1_sonnet | 1996 (4) | 25.4 → 29.8 (1.11) | ('young_adult', 'interpersonal', 'hopeful') (0.07) | young_adult/interpersonal/hopeful 0.071; middle_aged/internal/hopeful 0.062; unclear/internal/hopeful 0.06; middle_aged/interpersonal/hopeful 0.059; older_adult/internal/bittersweet 0.058 | middle_aged/interpersonal/hopeful 3t 9r; unclear/external_physical/hopeful 3t 3r; young_adult/interpersonal/hopeful 3t 3r | 0.10 | 1 / 0.00 |
| e3_2_sonnet | 1971 (29) | 21.2 → 21.4 (1.03) | ('young_adult', 'social_or_community', 'hopeful') (0.11) | young_adult/social_or_community/hopeful 0.109; young_adult/interpersonal/hopeful 0.098; middle_aged/internal/hopeful 0.065; older_adult/internal/bittersweet 0.062; older_adult/internal/hopeful 0.061 | unclear/internal/bittersweet 3t 4r; middle_aged/internal/hopeful 3t 10r | 0.65 | 8 / 0.58 |
| e3_1_qwen | 2000 (0) | 12.1 → 10.1 (1.11) | ('unclear', 'none_or_unclear', 'hopeful') (0.26) | unclear/none_or_unclear/hopeful 0.258; unclear/social_or_community/hopeful 0.243; unclear/external_physical/hopeful 0.143; young_adult/social_or_community/hopeful 0.057; unclear/internal/hopeful 0.053 | unclear/social_or_community/hopeful 11t 30r; unclear/none_or_unclear/hopeful 8t 15r; unclear/external_physical/hopeful 5t 13r; unclear/internal/hopeful 3t 6r | 0.10 | 1 / 0.10 |
| e3_2_qwen | 2000 (0) | 13.8 → 10.7 (1.06) | ('unclear', 'none_or_unclear', 'hopeful') (0.20) | unclear/none_or_unclear/hopeful 0.197; unclear/internal/neutral_or_ambiguous 0.182; unclear/social_or_community/hopeful 0.165; young_adult/none_or_unclear/hopeful 0.101; unclear/external_physical/hopeful 0.092 | unclear/social_or_community/hopeful 5t 19r; unclear/none_or_unclear/hopeful 5t 11r; unclear/internal/neutral_or_ambiguous 4t 16r | 0.55 | 7 / 0.45 |
| e3_1_llava | 2000 (0) | 13.4 → 12.1 (1.05) | ('unclear', 'social_or_community', 'hopeful') (0.24) | unclear/social_or_community/hopeful 0.245; unclear/none_or_unclear/hopeful 0.221; unclear/external_physical/hopeful 0.115; unclear/internal/hopeful 0.095; unclear/internal/bittersweet 0.041 | unclear/none_or_unclear/hopeful 13t 31r; unclear/social_or_community/hopeful 8t 28r; unclear/internal/hopeful 7t 7r; unclear/external_physical/hopeful 5t 9r | 0.00 | 2 / 0.10 |
| e3_2_llava | 1999 (1) | 10.2 → 11.4 (1.06) | ('unclear', 'none_or_unclear', 'hopeful') (0.23) | unclear/none_or_unclear/hopeful 0.229; unclear/none_or_unclear/neutral_or_ambiguous 0.166; unclear/external_physical/hopeful 0.12; unclear/internal/hopeful 0.103; unclear/social_or_community/hopeful 0.099 | unclear/none_or_unclear/hopeful 10t 23r; unclear/social_or_community/hopeful 5t 13r; unclear/none_or_unclear/neutral_or_ambiguous 5t 13r; unclear/social_or_community/neutral_or_ambiguous 4t 4r | 0.15 | 7 / 0.25 |

## Per-field modal value and share, steps 1–10 → 50–99

| cell | lead_age | lead_gender | lead_role_class | setting_place | setting_time | conflict_type | ending_valence | secondary_character | death_present | reconciliation_present | nature_central |
|---|---|---|---|---|---|---|---|---|---|---|---|
| e3_1_sonnet | unclear 0.32 → unclear 0.27 | woman 0.72 → woman 0.63 | worker_or_tradesperson 0.32 → worker_or_tradesperson 0.22 | institution 0.29 → home_interior 0.24 | present_day 0.81 → present_day 0.76 | internal 0.41 → internal 0.43 | hopeful 0.79 → hopeful 0.64 | other 0.20 → parent_or_grandparent 0.20 | False 0.71 → True 0.51 | False 0.70 → False 0.62 | False 0.79 → False 0.76 |
| e3_2_sonnet | young_adult 0.31 → young_adult 0.32 | woman 0.68 → woman 0.71 | professional 0.24 → other_or_unclear 0.28 | institution 0.39 → institution 0.39 | present_day 0.75 → present_day 0.76 | internal 0.39 → internal 0.36 | hopeful 0.69 → hopeful 0.69 | child 0.22 → child 0.20 | False 0.59 → False 0.54 | False 0.86 → False 0.82 | False 0.78 → False 0.76 |
| e3_1_qwen | unclear 0.70 → unclear 0.72 | woman 0.49 → woman 0.68 | professional 0.32 → professional 0.41 | institution 0.26 → small_town_or_village 0.23 | present_day 0.53 → present_day 0.55 | social_or_community 0.32 → social_or_community 0.39 | hopeful 0.95 → hopeful 0.93 | other 0.41 → other 0.46 | False 0.94 → False 0.90 | False 0.93 → False 0.94 | False 0.73 → False 0.64 |
| e3_2_qwen | unclear 0.69 → unclear 0.82 | woman 0.51 → woman 0.57 | other_or_unclear 0.30 → other_or_unclear 0.39 | institution 0.41 → institution 0.28 | unclear 0.53 → unclear 0.77 | internal 0.35 → none_or_unclear 0.35 | hopeful 0.68 → hopeful 0.70 | other 0.31 → other 0.29 | False 0.99 → False 0.96 | False 1.00 → False 0.94 | False 0.82 → False 0.93 |
| e3_1_llava | unclear 0.73 → unclear 0.76 | woman 0.49 → woman 0.46 | other_or_unclear 0.32 → professional 0.28 | other_or_unclear 0.32 → other_or_unclear 0.34 | unclear 0.65 → unclear 0.71 | none_or_unclear 0.31 → social_or_community 0.30 | hopeful 0.82 → hopeful 0.81 | other 0.33 → other 0.41 | False 0.88 → False 0.75 | False 1.00 → False 0.99 | False 0.81 → False 0.67 |
| e3_2_llava | unclear 0.83 → unclear 0.93 | woman 0.40 → other_or_unclear 0.36 | other_or_unclear 0.35 → other_or_unclear 0.43 | institution 0.35 → other_or_unclear 0.54 | unclear 0.65 → unclear 0.77 | social_or_community 0.35 → none_or_unclear 0.43 | hopeful 0.75 → hopeful 0.62 | none 0.34 → none 0.41 | False 0.94 → False 1.00 | False 0.99 → False 0.93 | False 0.85 → False 0.89 |

## Theme-sentence atlas and scale

| cell | persistent | shared by ≥ 2 traj | multidimensional | steps inside | nn-other median | within 0.15 | consecutive | Vendi first → last |
|---|---|---|---|---|---|---|---|---|
| e3_1_sonnet | 1 | 0 | 0 | 0.02 | 0.489 | 0.00 | 0.296 | 14.0 → 12.2 |
| e3_2_sonnet | 2 | 0 | 0 | 0.08 | 0.574 | 0.00 | 0.277 | 14.3 → 14.4 |
| e3_1_qwen | 0 | 0 | 0 | 0.00 | 0.400 | 0.00 | 0.251 | 15.4 → 13.9 |
| e3_2_qwen | 3 | 0 | 0 | 0.10 | 0.534 | 0.00 | 0.219 | 16.1 → 15.5 |
| e3_1_llava | 1 | 0 | 0 | 0.03 | 0.424 | 0.00 | 0.246 | 16.1 → 13.9 |
| e3_2_llava | 1 | 0 | 0 | 0.04 | 0.545 | 0.00 | 0.193 | 15.5 → 15.6 |

Shared theme attractors: `theme_cluster_NN.md` (theme sentences, field agreement, story openings). Codebook draft: `codebook.md`. Hand-coding sample for Brad: `handcode_sample.md`. Figure: `theme_curves.png`.

## Post-hoc checks (added after the verdicts above were read; not predictions)

**Tuple B = lead_gender × conflict_type × ending_valence.** lead_age is the judge's weakest field: on the reliability subsample Haiku codes it 'unclear' far more often than Sonnet does (shares below), so the predicted tuple is dominated by 'unclear' in the 7B cells. Tuple B uses three fields with κ ≥ 0.63.

| cell | eff. tuples 1–10 → 50–99 (null ratio) | modal late (share) | top-3 late | JS early–late | hold step-1 at 99 | memory half / at 99 |
|---|---|---|---|---|---|---|
| e3_1_sonnet | 12.4 → 15.5 (1.05) | woman/interpersonal/hopeful (0.15) | woman/interpersonal/hopeful 0.154; woman/internal/hopeful 0.135; woman/internal/bittersweet 0.117 | 0.093 | 0.20 | 1 / 0.16 |
| e3_2_sonnet | 14.8 → 14.0 (1.02) | woman/internal/hopeful (0.16) | woman/internal/hopeful 0.161; woman/social_or_community/hopeful 0.138; woman/interpersonal/hopeful 0.114 | 0.041 | 0.75 | 9 / 0.58 |
| e3_1_qwen | 12.0 → 9.3 (1.06) | woman/none_or_unclear/hopeful (0.27) | woman/none_or_unclear/hopeful 0.273; woman/social_or_community/hopeful 0.235; woman/external_physical/hopeful 0.118 | 0.102 | 0.00 | 1 / 0.00 |
| e3_2_qwen | 14.5 → 14.2 (1.06) | woman/none_or_unclear/hopeful (0.24) | woman/none_or_unclear/hopeful 0.241; woman/internal/neutral_or_ambiguous 0.096; woman/internal/hopeful 0.089 | 0.047 | 0.55 | 5 / 0.45 |
| e3_1_llava | 15.3 → 16.5 (1.08) | other_or_unclear/external_physical/hopeful (0.11) | other_or_unclear/external_physical/hopeful 0.108; man/social_or_community/hopeful 0.106; woman/none_or_unclear/hopeful 0.099 | 0.094 | 0.05 | 1 / 0.10 |
| e3_2_llava | 14.0 → 18.9 (1.03) | other_or_unclear/none_or_unclear/hopeful (0.12) | other_or_unclear/none_or_unclear/hopeful 0.123; other_or_unclear/none_or_unclear/neutral_or_ambiguous 0.115; woman/none_or_unclear/hopeful 0.094 | 0.174 | 0.15 | 20 / 0.15 |

**Seed memory in theme-sentence space** (own step-0 theme nearest among the 20 step-0 themes; the gate's memory curve on the judge's sentences): e3_1_sonnet half-life 40, at 10 / 50 / 99 0.76 / 0.41 / 0.41; e3_2_sonnet half-life None, at 10 / 50 / 99 1.0 / 1.0 / 1.0; e3_1_qwen half-life 11, at 10 / 50 / 99 0.65 / 0.35 / 0.15; e3_2_qwen half-life None, at 10 / 50 / 99 1.0 / 1.0 / 0.9; e3_1_llava half-life 18, at 10 / 50 / 99 0.75 / 0.4 / 0.35; e3_2_llava half-life None, at 10 / 50 / 99 1.0 / 0.95 / 0.79.

**Judge noise.** Haiku test-retest on the same 287 stories (κ / raw agreement): lead_age 0.86/0.92, lead_gender 0.94/0.96, lead_role_class 0.90/0.92, setting_place 0.90/0.92, setting_time 0.78/0.88, conflict_type 0.88/0.91, ending_valence 0.88/0.95, secondary_character 0.77/0.80, death_present 0.92/0.98, reconciliation_present 0.90/0.98, nature_central 0.93/0.98.
Haiku–Sonnet raw agreement: lead_age 0.73, lead_gender 0.94, lead_role_class 0.80, setting_place 0.81, setting_time 0.71, conflict_type 0.84, ending_valence 0.88, secondary_character 0.65, death_present 0.96, reconciliation_present 0.96, nature_central 0.90. Share of lead_age coded 'unclear' on the subsample: Haiku 0.60, sonnet 0.38.
