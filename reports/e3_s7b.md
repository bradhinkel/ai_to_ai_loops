# E3-S7B gate: 100-seed Mistral and Qwen compress–expand cells (2026-11-06)

Prediction: predictions.md "E3-S7B" (written 2026-11-03 before either cell ran; Brad: "a similar level of attractors as the Haiku runs but
with different topics/themes"). Cells `e3_1_mistral_100` (mistral:7b, digest 6577803aa9a0) and `e3_1_qwen_100` (qwen2.5vl:7b text-only,
digest 5ced39dfa4ba), the E3-1 loop (story → ≤ 50-word summary → ~500-word story), Hintze seeds 0–99 × 100 steps, Ollama parallel 2 on
the laptop, run in sequence by `scripts/e3_7b_queue.sh`: Mistral 2026-11-03 16:02 → 11-05 03:43 PST (35.7 h, 12.9 s per trajectory-step),
Qwen 11-05 03:43 → 11-06 17:31 PST (37.8 h, 13.6 s per trajectory-step). One start each, no crash, no resume. Haiku theme judge on both
(20,000 stories, ≈ $9.4). Reference: the pooled Haiku atlas (E3-S2: samples A + B, anonymised, k 396, 51 shared wells), projection
without refit. Measurement files: `reports/e3/s7b.{md,json}` (`analysis/e3s7b_report.py`), own-atlas sheets
`reports/e3/sw_cluster_e3_1_{mistral,qwen}_100_{raw,anon}.md`, hand reads `reports/e3/s7b_handread.md` (each recorded before its
projection), auxiliary cross-7B projection `reports/e3/s7b_cross7b.json`, judge archives `reports/e3/judge/e3_1_{mistral,qwen}_100.theme_judge.jsonl.gz`.

## Verdict

**M2 holds for both models and M4 holds for both; M1 fails upward for both; M3 holds for Mistral and fails for Qwen.** The second half
of Brad's prediction is exactly right: neither 7B model dwells in a single Haiku well (0 of 100 trajectories each, median late distance to
the nearest Haiku well 0.46 against the 0.35 line), the judge fields differ on all three pre-registered fields, and the menus are civic
where Haiku's is domestic. The first half is off in a specific direction: both 7B cells share *more* than Haiku per pair (rates 0.018 and
0.026 against Haiku's 0.005) through *fewer* wells (W-hat 56 and 39 against Haiku's 165–215). The exclusion rule removed no trajectory
from either cell.

| clause | needs | Mistral | Qwen | verdict |
|---|---|---|---|---|
| M1 anonymised pair-sharing rate | 0.003–0.012 | **0.0178** (88 of 4,950) | **0.0255** (126 of 4,950) | fails, both upward |
| M1 anonymised shared wells (k 198) | ≥ 8 | 35 | 33 | holds |
| M1 max multiplicity / raw shared wells | ≥ 3 / ≥ 3 | 4 / 4 | 7 / 10 | holds |
| M1 W-hat (pairs / sharing pairs) | 80–330 | **56** | **39** | fails, both low |
| M1 no-wells clause (< 0.002) / D-like clause (> 0.03) | not triggered | no / no | no / no | |
| M2 trajectories with a persistent stay in a Haiku shared well | ≤ 3 | 0 | 0 | holds |
| M2 median late distance to nearest Haiku shared well | ≥ 0.35 | 0.457 | 0.460 | holds |
| M2 judge fields differing from pooled Haiku by ≥ 0.15 | ≥ 2 of 3 | 3 of 3 (lead_age 0.49, conflict_type 0.39, setting_place 0.25) | 3 of 3 (lead_age 0.35, conflict_type 0.34, setting_place 0.23) | holds |
| M3 Mistral rate 0.01–0.03 with W-hat ≤ 100 | | 0.0178, 56 | | holds |
| M3 Qwen inside the band after 3–10 exclusions | | | 0 exclusions, rate 0.0255 | fails |
| M3 half-lives Mistral 15–30, Qwen 8–20 | | 12 | 8 | Mistral fails |
| M4 same-seed pairs with Haiku A sharing a joint well | ≤ 2 of 100 | 0 | 0 | holds |
| M4 same-seed late-distance gap vs Haiku A | < 0.02 | −0.023 | −0.000 | holds |
| Mistral vs Qwen same-seed pairs sharing a joint well (k 396) | reported | 0 of 100 (gap −0.024; 13 cross-model pairs among 68 joint wells) | | |

## The two menus

Both are one civic macro-plot with instrument-level wells, read from the anonymised sheets before projection (`s7b_handread.md`).

**Mistral: a stranger revives a decaying town.** A newcomer, usually an artist, a musician or a festival-maker, arrives in a fading town
and restores its spirit; 35 wells differ by the instrument (a mural, a concert, a bakery, a bookstore, a garden) and by what decayed.
**Qwen: a neglected place becomes a community hub.** A gardener, an urban planner or a young artist turns a neglected lot, park, manor,
general store or schoolhouse into a community space, often with a sustainability programme that goes national; about 26 of 33 wells, the
rest archaeology, a magic forest, a return to a grandmother's farm, a fear overcome. Both menus end hopeful almost without exception;
neither has a grief well, a family-secret well or an object-plot. Haiku's wells are domestic object-plots (a shoebox of unopened letters,
a dead relative's ledger of forgiven debts, an unfinished melody) with grief and reconciliation at the centre.

The two 7B menus are closer to each other than either is to Haiku. Auxiliary projection (not pre-registered; each cell's anonymised
steps labelled on the other cell's own k-198 atlas, no refit): 7 Qwen trajectories stay persistently in 2 Mistral wells (the artists'
haven and the revived town garden), 10 Mistral trajectories stay in 7 Qwen wells (garden revival, murals that revive a town, a village
reforested or re-watered, a grove healed by ritual); median late distance to the other 7B model's wells 0.30 and 0.28 against 0.46 to
Haiku's. Same-seed pairs across the two 7B cells: 0 of 100, so the shared ground is the models', not the seeds'.

## More sharing through fewer wells

The level clause was written as a per-pair rate, and on that number the 7B cells are three to five times Haiku. But the rate is pairs per
well menu: Haiku's 200 trajectories spread over a menu of ≈ 165–215 wells (W-hat), Mistral's 100 over ≈ 56, Qwen's 100 over ≈ 39, and a
smaller menu means more pairs meet. Qwen's largest well holds 7 trajectories (Haiku's largest 4), and its raw atlas already has 10
shared wells where Haiku's has 4–5, because the same names recur (Sarah, Elara, Eliza; Willowbrook, Willow Creek, Maplewood). Reading
M1 as "the same law" rather than "the same rate": the birthday-law structure is there in all three models (sharing grows with pairs,
wells recur as plot families), and the number of wells orders the models Qwen 39 < Mistral 56 < Haiku 165–215, which is the direction
of Brad's 2026-11-05 speculation that the well count rises with model scale, now seen across families and at the theme layer within the
Claude family (E3-DS: W-hat Haiku D 5.4 < Sonnet D 14.6). The counter-reading, that the 7B wells are coarser (a whole macro-plot rather
than an object), is the same fact from the other side: fewer, wider wells.

## Cells

| cell | half-life | own seed 10 / 50 / 99 | nn-other raw / anon | words at 99 | summaries ≤ 50 words | top name cover | modal tuple (share) | woman / hopeful |
|---|---|---|---|---|---|---|---|---|
| e3_1_haiku_100 (A) | 12 | 0.57 / 0.29 / 0.13 | 0.314 / 0.243 | 512 | — | — | young_adult × internal × hopeful (0.09) | 0.67 / 0.70 |
| e3_1_mistral_100 | 12 | 0.56 / 0.23 / 0.20 | 0.288 / 0.188 | 379 | 0.26 | 0.21 (Elara) | unclear × social_or_community × hopeful (0.39) | 0.32 / 0.90 |
| e3_1_qwen_100 | 8 | 0.46 / 0.14 / 0.06 | 0.301 / 0.206 | 444 | 0.94 | 0.40 (Sarah) | unclear × social_or_community × hopeful (0.31) | 0.70 / 0.98 |

## Judge field shares, Qwen vs pooled Haiku (steps 50–99)

| field | value | this cell | Haiku pooled |
|---|---|---|---|
| lead_age | unclear | 0.73 | 0.38 |
| lead_age | young_adult | 0.17 | 0.25 |
| lead_age | older_adult | 0.05 | 0.11 |
| lead_age | middle_aged | 0.02 | 0.19 |
| lead_age | child | 0.02 | 0.04 |
| lead_age | teen | 0.01 | 0.04 |
| conflict_type | social_or_community | 0.43 | 0.21 |
| conflict_type | none_or_unclear | 0.35 | 0.01 |
| conflict_type | external_physical | 0.12 | 0.12 |
| conflict_type | internal | 0.10 | 0.44 |
| conflict_type | interpersonal | 0.01 | 0.22 |
| setting_place | small_town_or_village | 0.37 | 0.14 |
| setting_place | city | 0.20 | 0.12 |
| setting_place | other_or_unclear | 0.13 | 0.10 |
| setting_place | institution | 0.12 | 0.17 |
| setting_place | wilderness_or_mountain | 0.10 | 0.03 |
| setting_place | home_interior | 0.04 | 0.25 |
| setting_place | rural_or_farmland | 0.03 | 0.14 |
| setting_place | coast_or_sea | 0.02 | 0.03 |
| setting_place | road_or_journey | 0.00 | 0.01 |

Mistral's table is in `reports/e3/s7b.md`. Both 7B cells put the lead's age out of view (unclear 0.86 and 0.73 against Haiku's 0.38), the conflict in the community (0.46 and 0.43 against 0.21) and the setting in a city or a small town rather than a home; Qwen's leads are women 0.70 of the time (Mistral 0.32, Haiku 0.67) and its endings hopeful 0.98.

## Deviations and notes

- Procedure as pre-registered; the cross-7B projection and the W-hat reading of M1 are post hoc and labelled so. M3's half-life clause
  was a guess from the 20-seed cells and missed for Mistral (12, not 15–30).
- Mistral ignores the 50-word limit in three summaries of four (median summary longer than Haiku's); Qwen code-switched into Chinese in
  22 late stories spread over 18 trajectories (max 3 in one), far below the exclusion line of 10.
- The laptop ran both cells without a reboot (73.5 h). GPU log in `logs/gpu.csv`.

## What this gate changes

The 7B half of the text-loop story is now measured at 100 seeds: wells, the birthday law and plot-family recurrence are present in every
model tried; the menus are model-specific between families (civic for the 7B models, domestic for Claude) and shared within (E3-DS); and
the number of wells is the quantity that orders models. The credit-request exhibit can carry the three-model W-hat line (Qwen 39,
Mistral 56, Haiku ≈ 190) and ask for Sonnet, Opus and Fable at 100 seeds to extend it. Next in the queue, none started: the exhibit and the
two letters; the thesis-bottleneck essay pilot (prediction first); the D cell on Qwen.
