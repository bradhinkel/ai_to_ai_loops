# E6 judge check set — status 2026-10-21

150 blind, numbered images (`sheet_01.jpg` … `sheet_08.jpg`, 20 per sheet, 320 px thumbnails) drawn from the E6 starting images:
50 No-Stigma validation renders (`runs/e6_oneshot` trajectories 400–449), 72 seeded occupation step-0 renders (2 per gender × skin × age × occupation cell, `runs/e6_step0`),
12 seeded portrait renders (1 per cell) and 16 one-shot occupation renders (4 per occupation). Built by `analysis/make_check_set.py` (seed 20261021); `key.json` maps each id to its run, trajectory and seeded attributes.

**To label (Brad):** open `labels.xlsx` (dropdowns; `labels.csv` is the same table) next to the sheets and fill person_present, gender, age, skin for every id. Label what you perceive, not what the prompt asked for. Do not open `key.json` until done. The agreement script compares your labels with both judges and with the seeds.

## Judge agreement before human labels (Sonnet 5.5 vs Haiku 5.5, same prompt, same 150 images)

| field | n both judged | agreement | Cohen's kappa |
|---|---|---|---|
| gender presentation | 149 | 0.95 | 0.92 |
| age band | 149 | 0.93 | 0.88 |
| skin tone (3 bands) | 149 | 0.89 | 0.84 |

Both judges found a person in every image they parsed (149 both; one Sonnet response did not parse). Haiku's first pass left 29 images unparsed because its long occupation-cue lists hit the 600-token output cap; the cap is now 1,200 (commit 93d749a) and the rerun parsed all 150. Cost: about 110 k input and 15 k output tokens per Sonnet pass over 150 images.

## Judges vs the seeded attributes (84 seeded images; the seed is the prompt, not ground truth)

| field | Sonnet agrees with seed | Haiku agrees with seed |
|---|---|---|
| gender | 83/84 | 84/84 |
| age (young / older) | 79/84 | 80/84 |
| skin (light / medium / dark) | 54/84 | 49/84 |

Skin disagreements are almost all one band darker than the seed (seed light → judge medium 11, seed medium → judge dark 11, seed light → judge dark 5). The pixel measurement says the renders, not the judge, are the reason: facial L* on the same 84 images is light 47.3 ± 11.8, medium 42.0 ± 13.0, dark 26.1 ± 6.7 (mean ± sd), so SDXL separates "dark-skinned" from the rest but renders "light-skinned" and "medium-skinned" as overlapping distributions. Grouped by Sonnet's band instead, L* is light 54.0 (n 13), medium 47.4 (n 26), dark 28.8 (n 44): the judge's bands are monotone in measured lightness. Consequence for E6: the seeded skin label is a weak manipulation at the light/medium boundary; report skin by measured L* and by the judge's band, not by the seed alone.

## Skin-tone pipeline validation (No-Stigma set)

All 50 faces detected; mean facial L* 55.5 (sd 7.7), mean hue angle h* 57.1, against the published SDXL means of 58.1 and 55.0 (Wilson / Ghosh / Caliskan method as implemented in `analysis/skin_tone.py`). Within three units on both axes with a different SDXL seed, 25 steps and 512-px resize; accepted.

## Decision pending Brad's labels

Judge choice (Sonnet vs Haiku) and the per-group error rates come from the human labels. Target: kappa ≥ 0.7 against Brad on gender and age, and error rates reported per seeded group (SPEC2 E6).
