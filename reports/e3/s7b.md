# E3-S7B: 100-seed Mistral and Qwen cells against predictions.md "E3-S7B" (2026-11-03)

Pooled Haiku reference: ('e3_1_haiku_100', 'e3_1_haiku_100b'), anonymised, k 396, 51 shared wells. Atlas rules as E3-S. Exclusion rule applied before the atlas.

## e3_1_mistral_100: 100 of 100 trajectories kept (0 degenerate)

**M1 (same level as Haiku): fails** — anon rate 0.0178 (88 of 4950; band 0.003–0.012), shared wells 35, max multiplicity 4, W-hat 56, raw shared 4; no-wells clause False, D-like clause False.
**M2 (different themes): holds** — 0 trajectories dwell in a Haiku well (wells []), median late distance to the nearest Haiku shared well 0.457 (≥ 0.35), inside any Haiku persistent cluster late 0.000; judge max share difference vs Haiku {'lead_age': 0.4866283754259143, 'conflict_type': 0.38981537911227004, 'setting_place': 0.2503793221526663} (fields ≥ 0.15: 3).
**M3 (Claude's alternative)** — rate in 0.01–0.03: True; W-hat ≤ 100: True; excluded 0; half-life 12.
**M4 (cross-model seed trace vs Haiku A): holds** — same-seed pairs sharing a joint well 0 of 100 (≤ 2), late-distance gap -0.023 (< 0.02).

Cell: half-life 12, own seed 10 / 50 / 99 0.56 / 0.23 / 0.2, nn-other raw / anon 0.288 / 0.188, within 0.15 0.004 / 0.202, Vendi story 99 19.0, words 99 379, summaries ≤ 50 0.2641, top-10 name cover 0.21 (Elara), modal tuple unclear × social_or_community × hopeful (0.389), woman 0.32, hopeful 0.9.

| field | value | this cell | Haiku pooled |
|---|---|---|---|
| lead_age | unclear | 0.86 | 0.38 |
| lead_age | young_adult | 0.04 | 0.25 |
| lead_age | older_adult | 0.04 | 0.11 |
| lead_age | child | 0.04 | 0.04 |
| lead_age | teen | 0.02 | 0.04 |
| lead_age | middle_aged | 0.00 | 0.19 |
| conflict_type | social_or_community | 0.46 | 0.21 |
| conflict_type | external_physical | 0.33 | 0.12 |
| conflict_type | none_or_unclear | 0.14 | 0.01 |
| conflict_type | internal | 0.05 | 0.44 |
| conflict_type | interpersonal | 0.02 | 0.22 |
| setting_place | city | 0.36 | 0.12 |
| setting_place | small_town_or_village | 0.30 | 0.14 |
| setting_place | other_or_unclear | 0.12 | 0.10 |
| setting_place | wilderness_or_mountain | 0.10 | 0.03 |
| setting_place | institution | 0.05 | 0.17 |
| setting_place | rural_or_farmland | 0.05 | 0.14 |
| setting_place | coast_or_sea | 0.01 | 0.03 |
| setting_place | road_or_journey | 0.01 | 0.01 |
| setting_place | home_interior | 0.00 | 0.25 |

