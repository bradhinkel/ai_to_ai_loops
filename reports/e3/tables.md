## Per-cell metrics (MiniLM on the stories)

| cell | plateau step | step drift first 5 / last 20 | dist. from step 1 at 99 (median) | half-life | ident. 1/2/3/5/10/20/50/99 | Vendi step 1 → 99 | attractors | steps inside | endpoints inside | median hazard | median dwell | visits / traj |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e3_1_sonnet | 11 | 0.216 / 0.205 | 0.45 | 45 | 0.95/0.95/0.95/0.80/0.80/0.70/0.65/0.45 | 10.8 → 10.3 | 0 | 0.00 | 0.00 | None | None | 0.00 |
| e3_2_sonnet | 11 | 0.081 / 0.053 | 0.27 | None | 1.00/1.00/1.00/1.00/1.00/1.00/0.95/0.95 | 12.0 → 11.4 | 0 | 0.00 | 0.00 | None | None | 0.00 |
| e3_1_qwen | 18 | 0.210 / 0.169 | 0.56 | 14 | 0.95/0.95/0.85/0.90/0.65/0.50/0.40/0.35 | 12.3 → 12.2 | 0 | 0.00 | 0.00 | None | None | 0.00 |
| e3_2_qwen | 67 | 0.046 / 0.056 | 0.30 | None | 1.00/1.00/1.00/1.00/1.00/1.00/1.00/0.95 | 12.3 → 13.1 | 3 | 0.11 | 0.10 | 0.038 | 16.0 | 0.55 |
| e3_1_llava | 19 | 0.167 / 0.124 | 0.64 | 22 | 1.00/0.95/0.95/0.90/0.70/0.55/0.40/0.25 | 13.5 → 11.6 | 0 | 0.00 | 0.00 | None | None | 0.00 |
| e3_2_llava | 21 | 0.059 / 0.069 | 0.41 | None | 1.00/1.00/1.00/1.00/1.00/1.00/1.00/0.85 | 14.7 → 15.3 | 2 | 0.07 | 0.00 | 0.066 | 7.5 | 0.40 |

## Persistent attractors (joint k 40, radius 0.15, dwell >= 5; per cell: visits / trajectories / endpoints / median dwell / hazard)

| cluster | e3_1_sonnet | e3_2_sonnet | e3_1_qwen | e3_2_qwen | e3_1_llava | e3_2_llava | attribution |
|---|---|---|---|---|---|---|---|
| 37 | – | – | – | 2 / 1 / 0 / 30 / 0.03 | – | 5 / 1 / 0 / 9 / 0.09 | cell: e3_2_llava |
| 1 | – | 1 / 1 / 1 / 96 / 0.00 | – | 5 / 1 / 0 / 16 / 0.06 | – | – | cell: e3_2_qwen |
| 24 | – | – | – | 3 / 1 / 1 / 6 / 0.04 | – | 2 / 1 / 0 / 13 / 0.08 | cell: e3_2_qwen |
| 7 | – | – | – | – | 2 / 1 / 0 / 20 / 0.15 | 1 / 1 / 1 / 99 / 0.00 | none |
| 15 | – | – | – | 3 / 1 / 1 / 42 / 0.02 | – | – | cell: e3_2_qwen |
| 28 | – | – | – | – | – | 3 / 1 / 0 / 6 / 0.04 | cell: e3_2_llava |
| 5 | – | – | – | 1 / 1 / 0 / 37 / 0.03 | – | 1 / 1 / 0 / 10 / 0.19 | none |
| 12 | – | 1 / 1 / 1 / 44 / 0.00 | – | 1 / 1 / 1 / 97 / 0.00 | – | – | none |
| 13 | – | 2 / 1 / 0 / 30 / 0.03 | – | – | – | – | none |
| 20 | – | – | – | – | – | 2 / 1 / 1 / 49 / 0.01 | none |
| 22 | – | – | – | 2 / 1 / 1 / 44 / 0.01 | – | – | none |
| 39 | – | – | – | – | 2 / 1 / 1 / 33 / 0.04 | – | none |
| 3 | – | – | – | 1 / 1 / 0 / 30 / 0.03 | – | – | none |
| 6 | – | – | – | 1 / 1 / 1 / 87 / 0.00 | – | – | none |
| 8 | – | – | – | 1 / 1 / 0 / 18 / 0.06 | – | – | none |
| 9 | 1 / 1 / 0 / 5 / 0.59 | – | – | – | – | – | none |
| 14 | – | – | – | – | – | 1 / 1 / 0 / 23 / 0.04 | none |
| 16 | – | 1 / 1 / 0 / 15 / 0.17 | – | – | – | – | none |
| 18 | – | – | – | 1 / 1 / 1 / 85 / 0.00 | – | – | none |
| 21 | – | – | – | 1 / 1 / 0 / 75 / 0.01 | – | – | none |
| 23 | – | 1 / 1 / 1 / 99 / 0.00 | – | – | – | – | none |
| 27 | – | – | – | 1 / 1 / 0 / 44 / 0.02 | – | – | none |
| 30 | – | – | – | – | – | 1 / 1 / 1 / 76 / 0.00 | none |
| 33 | – | – | – | – | – | 1 / 1 / 1 / 91 / 0.00 | none |
| 34 | – | 1 / 1 / 0 / 37 / 0.05 | – | – | – | – | none |
| 35 | – | 1 / 1 / 0 / 9 / 0.11 | – | – | – | – | none |
| 36 | – | – | 1 / 1 / 0 / 11 / 0.27 | – | – | – | none |
| 38 | – | 1 / 1 / 1 / 99 / 0.00 | – | – | – | – | none |

## Content audit by step window (English stories only; CJK stories counted separately)

### e3_1_sonnet (CJK stories 0, exact copies 0, flags {'story_refusal': 557, 'summary_over_50_words': 274})

| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-10 | 200 (200) | 557.0 | 0.98 | 134 : 61 | 4393 : 2443 | 0.28 | 0.43 | 4.4 | 0.19 | years, sat, marguerite, i'm, stood, people, small, time, mara, left | Marguerite 16, Mara 12, Dev 10, Hartwell 7, Desmond 7 |
| 11-25 | 300 (300) | 557.0 | 0.98 | 220 : 80 | 7056 : 3975 | 0.4 | 0.31 | 4.6 | 0.2 | years, sat, stood, people, i'm, mara, long, man, hands, time | Mara 20, Marguerite 16, Marisol 12, Pip 10, Gary 10 |
| 26-50 | 500 (500) | 556.0 | 0.99 | 344 : 152 | 10817 : 6872 | 0.37 | 0.32 | 4.4 | 0.22 | years, sat, stood, i'm, man, hands, mara, left, took, time | Mara 35, Marisol 25, Okafor 20, Dev 20, Pip 16 |
| 51-75 | 500 (500) | 556.0 | 1.0 | 300 : 198 | 10224 : 7972 | 0.42 | 0.19 | 4.2 | 0.22 | years, i'm, sat, stood, took, mara, know, hand, hands, man | Mara 44, Dev 26, Priya 23, Pip 22, Frank 19 |
| 76-89 | 280 (280) | 558.0 | 1.0 | 169 : 111 | 5651 : 4601 | 0.48 | 0.2 | 4.2 | 0.2 | years, sat, mara, hand, stood, took, hands, know, i'm, didn't | Mara 23, Pip 12, Priya 12, Dev 12, Marisol 12 |
| 90-99 | 200 (200) | 559.0 | 0.98 | 125 : 74 | 4091 : 3169 | 0.47 | 0.26 | 4.3 | 0.19 | years, sat, stood, took, i'm, mara, hands, hand, didn't, know | Mara 18, Marguerite 11, Julian 8, Pip 8, Marisol 8 |

Names 50–99: 994 leads, 162 distinct; top 10 cover 0.40: Mara 87, Pip 43, Dev 40, Priya 39, Marisol 37, Maxim 33, Amara 31, Julian 30, Marin 30, Marguerite 30; LLM-set hits ['Amara']; seed names {'trajectories_with_seed_names': 1, 'gone_by_10': 1}; compliance {'summaries': 2000, 'summary_le50_share': 0.863, 'story_lt400_share': 0.0, 'length_ratio_step99_median': 1.0434999999999999}

### e3_2_sonnet (CJK stories 0, exact copies 2, flags {'story_refusal': 200})

| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-10 | 200 (200) | 527.5 | 1.0 | 115 : 71 | 3090 : 2266 | 0.36 | 0.64 | 5.0 | 0.11 | people, years, stood, long, hand, room, sat, line, turned, asked | Dev 16, Marchetti 10, Eli 10, Secretary 10, Odalys 10 |
| 11-25 | 300 (300) | 526.5 | 1.0 | 168 : 102 | 4509 : 3489 | 0.38 | 0.65 | 5.0 | 0.11 | people, years, stood, long, hand, held, line, sat, turned, small | Dev 30, Theo 15, Secretary 15, Odalys 15, Latin 15 |
| 26-50 | 500 (500) | 529.5 | 1.0 | 292 : 160 | 8080 : 5435 | 0.36 | 0.67 | 5.0 | 0.12 | years, people, hand, held, stood, long, sat, turned, line, small | Dev 49, Calloway 43, Secretary 25, Odalys 25, Latin 25 |
| 51-75 | 500 (500) | 529.0 | 1.0 | 288 : 165 | 8443 : 5251 | 0.3 | 0.7 | 5.0 | 0.12 | years, people, hand, held, long, sat, stood, asked, line, small | Calloway 48, Dev 47, Tobias 36, Secretary 25, Odalys 25 |
| 76-89 | 280 (280) | 532.0 | 1.0 | 153 : 91 | 4825 : 2865 | 0.37 | 0.72 | 5.0 | 0.12 | years, people, hand, held, long, sat, asked, stood, small, turned | Dev 17, Marguerite 16, Calloway 14, Tobias 14, Secretary 14 |
| 90-99 | 200 (200) | 534.0 | 1.0 | 115 : 60 | 3487 : 2022 | 0.4 | 0.72 | 4.9 | 0.12 | years, people, held, long, sat, hand, turned, stood, asked, small | Odalys 13, Calloway 10, Tobias 10, Secretary 10, Latin 10 |

Names 50–99: 1000 leads, 40 distinct; top 10 cover 0.56: Dev 75, Calloway 74, Tobias 61, Odalys 53, Secretary 50, Latin 50, Funmi 50, Philomena 50, Reyes 50, Crane 50; LLM-set hits []; seed names {'trajectories_with_seed_names': 1, 'gone_by_10': 0}; compliance {'summaries': 0, 'summary_le50_share': None, 'story_lt400_share': 0.0, 'length_ratio_step99_median': 1.001}

### e3_1_qwen (CJK stories 78, exact copies 0, flags {'summary_over_50_words': 151, 'story_cjk': 78, 'summary_cjk': 85, 'story_refusal': 8})

| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-10 | 200 (199) | 458.0 | 0.98 | 101 : 74 | 2325 : 1249 | 0.15 | 0.97 | 9.6 | 0.14 | sarah, began, alex, new, community, heart, place, world, eyes, stories | Alex 24, Sarah 19, Ella 17, Lily 16, James 13 |
| 11-25 | 300 (300) | 456.0 | 0.99 | 161 : 99 | 3143 : 1546 | 0.15 | 0.95 | 10.1 | 0.16 | sarah, began, community, world, alex, life, stories, heart, new, old | Alex 34, Sarah 27, Eliza 17, Meadowbrook 15, Anna 14 |
| 26-50 | 500 (486) | 451.0 | 0.99 | 330 : 94 | 5152 : 1359 | 0.14 | 0.97 | 10.5 | 0.2 | sarah, community, began, life, village, old, heart, new, world, ancient | Sarah 79, Alex 32, Eliza 28, Lisa 22, Anna 21 |
| 51-75 | 500 (475) | 441.0 | 0.98 | 343 : 104 | 5038 : 1411 | 0.16 | 0.99 | 10.2 | 0.19 | sarah, community, began, hope, life, village, heart, elara, new, people | Sarah 82, Elara 30, Smith 23, Linda 23, Mindscape 21 |
| 76-89 | 280 (260) | 447.0 | 1.0 | 161 : 73 | 2163 : 1577 | 0.19 | 0.96 | 10.4 | 0.2 | community, began, elara, sarah, life, people, world, old, new, heart | Sarah 22, Mark 19, Elara 15, Willow 15, Verde 13 |
| 90-99 | 200 (182) | 437.5 | 0.99 | 125 : 39 | 1606 : 847 | 0.15 | 0.97 | 10.3 | 0.19 | community, sarah, elara, began, life, new, city, heart, hope, old | Willowbrook 17, Sarah 17, Elara 12, Willow 12, Verde 10 |

Names 50–99: 926 leads, 73 distinct; top 10 cover 0.51: Sarah 125, Elara 57, Willow 44, Linda 44, Willowbrook 37, Mark 37, Kael 35, Eliza 34, Smith 33, Xia 29; LLM-set hits ['Elara']; seed names {'trajectories_with_seed_names': 1, 'gone_by_10': 1}; compliance {'summaries': 2000, 'summary_le50_share': 0.9245, 'story_lt400_share': 0.25814931650893796, 'length_ratio_step99_median': 0.95}

### e3_2_qwen (CJK stories 169, exact copies 276, flags {'story_cjk': 169})

| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-10 | 200 (191) | 251.0 | 0.84 | 90 : 84 | 1340 : 999 | 0.1 | 0.9 | 8.9 | 0.08 | eyes, sarah, stood, old, room, filled, love, tech, charm, mansion | Sarah 20, Lily 20, Ella 20, Kael 10, Jose 10 |
| 11-25 | 300 (282) | 189.5 | 0.84 | 132 : 145 | 1650 : 1236 | 0.11 | 0.85 | 9.0 | 0.09 | sarah, eyes, room, old, day, stood, sun, love, secrets, filled | Sarah 43, Ella 30, Lily 29, Kael 15, Jose 15 |
| 26-50 | 500 (450) | 142.0 | 0.82 | 224 : 220 | 2092 : 1678 | 0.11 | 0.8 | 9.2 | 0.07 | eyes, room, charm, mansion, lily, old, office, voice, health, truth | Sarah 50, Lily 48, Ella 37, Kael 25, Jose 25 |
| 51-75 | 500 (449) | 114.0 | 0.76 | 223 : 177 | 1534 : 1491 | 0.12 | 0.76 | 9.2 | 0.08 | charm, mansion, lily, room, secrets, truth, office, sarah, light, sweet | Sarah 49, Lily 47, David 25, Kael 25, Jose 25 |
| 76-89 | 280 (252) | 90.0 | 0.72 | 126 : 109 | 759 : 718 | 0.09 | 0.73 | 8.9 | 0.06 | charm, room, lily, sarah, office, deep, secrets, mansion, voice, moment | Sarah 30, Lily 28, Kael 14, Eldershire 14, Jose 14 |
| 90-99 | 200 (187) | 89.0 | 0.68 | 97 : 70 | 589 : 477 | 0.1 | 0.73 | 9.3 | 0.04 | room, charm, secrets, sarah, office, lily, mansion, forward, light, history | Lily 20, Sarah 18, Tom 10, Kael 10, Eldershire 10 |

Names 50–99: 743 leads, 23 distinct; top 10 cover 0.79: Sarah 149, Lily 96, Kael 50, Jose 50, Eldan 50, Jenkins 45, Voss 42, James 36, Eldershire 35, Ella 32; LLM-set hits []; seed names {'trajectories_with_seed_names': 1, 'gone_by_10': 1}; compliance {'summaries': 0, 'summary_le50_share': None, 'story_lt400_share': 0.9486471562672557, 'length_ratio_step99_median': 0.18}

### e3_1_llava (CJK stories 0, exact copies 0, flags {'summary_over_50_words': 1207, 'story_refusal': 15, 'story_length_cutoff': 1})

| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-10 | 200 (200) | 348.0 | 0.7 | 100 : 69 | 2757 : 1575 | 0.05 | 0.91 | 7.9 | 0.14 | people, world, began, time, day, love, make, work, sense, continued | Sarah 21, John 13, Jack 13, Riley 10, Michael 10 |
| 11-25 | 300 (300) | 360.0 | 0.93 | 140 : 91 | 3485 : 2384 | 0.08 | 0.98 | 8.4 | 0.16 | sarah, people, world, work, day, began, help, new, community, jack | Sarah 46, Jack 30, John 20, Leo 15, Riley 15 |
| 26-50 | 500 (500) | 352.5 | 0.95 | 195 : 185 | 4214 : 4988 | 0.11 | 0.97 | 8.4 | 0.2 | world, sarah, work, people, continued, day, help, jack, make, began | Sarah 74, Emily 38, Jack 36, Leo 35, Jill 25 |
| 51-75 | 500 (500) | 349.0 | 0.99 | 185 : 163 | 4707 : 4022 | 0.03 | 0.91 | 8.3 | 0.19 | sarah, people, jack, work, world, community, music, day, make, began | Sarah 132, Sam 56, Jack 50, Jill 25, Emily 25 |
| 76-89 | 280 (280) | 345.0 | 0.96 | 121 : 73 | 2929 : 2097 | 0.05 | 0.92 | 8.4 | 0.2 | people, jack, work, sarah, world, community, began, make, life, day | Sarah 67, Jack 36, Sam 25, Sara 14, Emily 14 |
| 90-99 | 200 (200) | 341.5 | 0.99 | 96 : 48 | 2084 : 1456 | 0.03 | 0.96 | 8.6 | 0.19 | people, work, sarah, world, jack, began, community, continued, years, day | Sarah 42, Jack 22, Sam 19, Lily 15, John 10 |

Names 50–99: 980 leads, 40 distinct; top 10 cover 0.73: Sarah 245, Jack 110, Sam 101, Emily 50, Sophia 49, Amelia 37, Sara 35, Jill 33, Lily 30, Max 30; LLM-set hits []; seed names {'trajectories_with_seed_names': 1, 'gone_by_10': 1}; compliance {'summaries': 2000, 'summary_le50_share': 0.3965, 'story_lt400_share': 0.7318181818181818, 'length_ratio_step99_median': 0.8225}

### e3_2_llava (CJK stories 0, exact copies 162, flags {'story_length_cutoff': 3})

| window | n (English) | words median | named char. | lead female : male | female : male words | elderly | VADER | FK grade | Jaccard top-50 | top content words | top leads |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-10 | 200 (200) | 170.5 | 0.47 | 71 : 54 | 1087 : 712 | 0.01 | 0.81 | 8.5 | 0.08 | day, life, students, johnson, began, anchor, travelers, clara, kate, love | John 10, Riley 10, Clara 10, Chen 10, Jasmine 10 |
| 11-25 | 300 (300) | 102.5 | 0.45 | 103 : 63 | 893 : 661 | 0.0 | 0.8 | 9.7 | 0.05 | life, despite, group, john, people, help, tomato, stood, health, true | John 15, Trafalgar 15, Clara 15, Chen 15, Riley 14 |
| 26-50 | 500 (500) | 97.0 | 0.37 | 131 : 124 | 1178 : 976 | 0.03 | 0.72 | 10.4 | 0.05 | despite, life, people, concert, students, began, room, land, john, realm | John 29, Chen 25, Alex 22, Jasmine 19, Trafalgar 18 |
| 51-75 | 500 (500) | 84.0 | 0.39 | 149 : 114 | 1444 : 841 | 0.01 | 0.72 | 10.8 | 0.06 | life, room, world, clock, app, despite, people, concert, john, unwavering | John 25, Smith 25, Trafalgar 25, Chen 25, Jasmine 25 |
| 76-89 | 280 (280) | 78.0 | 0.35 | 94 : 71 | 719 : 532 | 0.01 | 0.72 | 10.9 | 0.06 | life, world, realm, time, peace, despite, people, guardian, app, traveler | Smith 14, Trafalgar 14, Kate 14, Clara 12, Emily 10 |
| 90-99 | 200 (200) | 75.0 | 0.38 | 60 : 65 | 499 : 392 | 0.02 | 0.66 | 10.4 | 0.06 | world, room, emily, life, time, realm, happiness, left, true, unwavering | John 10, Smith 10, Chen 10, Kate 10, Jasmine 10 |

Names 50–99: 374 leads, 11 distinct; top 10 cover 0.98: Smith 49, Trafalgar 48, John 45, Kate 45, Chen 43, Jasmine 40, Clara 35, Emily 28, Alex 22, Riley 12; LLM-set hits ['Clara']; seed names {'trajectories_with_seed_names': 1, 'gone_by_10': 1}; compliance {'summaries': 0, 'summary_le50_share': None, 'story_lt400_share': 0.9858585858585859, 'length_ratio_step99_median': 0.198}


## Scale controls (MiniLM; radius 0.15)

| cell | n | consecutive median | self-centroid share 50-99 | nearest other-trajectory: median / share <= 0.15 | summary space: nn-other median / share / self-centroid / half-life |
|---|---|---|---|---|---|
| e3_1_sonnet | 20 | 0.196 | 0.58 | 0.381 / 0.000 (min 0.21) | 0.520 / 0.000 / 0.81 / None |
| e3_2_sonnet | 20 | 0.035 | 0.96 | 0.468 / 0.000 (min 0.32) | – |
| e3_1_qwen | 20 | 0.166 | 0.49 | 0.369 / 0.002 (min 0.13) | 0.450 / 0.000 / 0.45 / 15 |
| e3_2_qwen | 20 | 0.032 | 0.94 | 0.469 / 0.000 (min 0.37) | – |
| e3_1_llava | 20 | 0.121 | 0.58 | 0.409 / 0.000 (min 0.22) | 0.440 / 0.000 / 0.54 / 23 |
| e3_2_llava | 20 | 0.051 | 0.88 | 0.561 / 0.000 (min 0.28) | – |
| a0_s | 100 | 0.152 | 0.74 | 0.188 / 0.355 (20-traj subsamples; full n: 0.121 / 0.628; half-life sub20 median 6, range [3, 11]) | – |
| e1_cap | 100 | 0.199 | 0.55 | 0.189 / 0.358 (20-traj subsamples; full n: 0.137 / 0.568; half-life sub20 median 6, range [3, 12]) | – |
| a0_core | 100 | 0.162 | 0.70 | 0.150 / 0.508 (20-traj subsamples; full n: 0.104 / 0.689; half-life sub20 median 6, range [4, 10]) | – |

## Verdict numbers

```
{
 "p1": {
  "e3_1_sonnet": {
   "plateau_le_25": true,
   "plateau": 11,
   "half_life": 45,
   "half_life_3_5": false,
   "share_inside": 0.0,
   "share_30_50": false,
   "n_attractors": 0,
   "ge_3": false,
   "median_hazard": null
  },
  "e3_1_qwen": {
   "plateau_le_25": true,
   "plateau": 18,
   "half_life": 14,
   "half_life_3_5": false,
   "share_inside": 0.0,
   "share_30_50": false,
   "n_attractors": 0,
   "ge_3": false,
   "median_hazard": null
  },
  "e3_1_llava": {
   "plateau_le_25": true,
   "plateau": 19,
   "half_life": 22,
   "half_life_3_5": false,
   "share_inside": 0.0,
   "share_30_50": false,
   "n_attractors": 0,
   "ge_3": false,
   "median_hazard": null
  },
  "sonnet_hazard_below_a0s": false,
  "qwen_hazard_below_e1cap": false
 },
 "p2": {
  "sonnet": {
   "half_life_e3_1": 45,
   "half_life_e3_2": null,
   "ratio": 2.2222222222222223,
   "ratio_ge_2": true,
   "e3_2_half_ge_8": true,
   "share_inside_e3_1": 0.0,
   "share_inside_e3_2": 0.0,
   "share_at_most_half": true,
   "cum99_e3_1": 0.44772573070809213,
   "cum99_e3_2": 0.27390685519106495,
   "cum99_lower": true,
   "branch": "bottleneck (>= 1.5)"
  },
  "qwen": {
   "half_life_e3_1": 14,
   "half_life_e3_2": null,
   "ratio": 7.142857142857143,
   "ratio_ge_2": true,
   "e3_2_half_ge_8": true,
   "share_inside_e3_1": 0.0,
   "share_inside_e3_2": 0.11464646464646465,
   "share_at_most_half": false,
   "cum99_e3_1": 0.5589132026387191,
   "cum99_e3_2": 0.29946777349030684,
   "cum99_lower": true,
   "branch": "bottleneck (>= 1.5)"
  },
  "llava": {
   "half_life_e3_1": 22,
   "half_life_e3_2": null,
   "ratio": 4.545454545454546,
   "ratio_ge_2": true,
   "e3_2_half_ge_8": true,
   "share_inside_e3_1": 0.0,
   "share_inside_e3_2": 0.06767676767676768,
   "share_at_most_half": false,
   "cum99_e3_1": 0.6374352440829099,
   "cum99_e3_2": 0.4145661580074209,
   "cum99_lower": true,
   "branch": "bottleneck (>= 1.5)"
  }
 },
 "p3": {
  "sonnet": {
   "jaccard_1_10": 0.1111111111111111,
   "jaccard_90_99": 0.12359550561797752,
   "doubled": false,
   "length_ratio_99": 1.001,
   "words_median_1_10": 527.5,
   "words_median_90_99": 534.0
  },
  "qwen": {
   "jaccard_1_10": 0.08111266947171575,
   "jaccard_90_99": 0.041666666666666664,
   "doubled": false,
   "length_ratio_99": 0.18,
   "words_median_1_10": 251.0,
   "words_median_90_99": 89.0
  },
  "llava": {
   "jaccard_1_10": 0.07526881720430108,
   "jaccard_90_99": 0.06382978723404255,
   "doubled": false,
   "length_ratio_99": 0.198,
   "words_median_1_10": 170.5,
   "words_median_90_99": 75.0
  }
 },
 "p4": {
  "sonnet": {
   "joint_share": null,
   "own_centroid_share": null,
   "cross_model_share": null
  },
  "qwen": {
   "joint_share": 0.0,
   "own_centroid_share": 0.0,
   "cross_model_share": 0.0
  },
  "llava": {
   "joint_share": 0.0,
   "own_centroid_share": 0.0,
   "cross_model_share": 0.0
  }
 },
 "p5": {
  "e3_1_sonnet": {
   "a0s_named_with_persistent_visit": 0,
   "steps_inside_named": 0
  },
  "e3_2_sonnet": {
   "a0s_named_with_persistent_visit": 0,
   "steps_inside_named": 0
  },
  "e3_1_qwen": {
   "a0s_named_with_persistent_visit": 0,
   "steps_inside_named": 0
  },
  "e3_2_qwen": {
   "a0s_named_with_persistent_visit": 0,
   "steps_inside_named": 0
  },
  "e3_1_llava": {
   "a0s_named_with_persistent_visit": 0,
   "steps_inside_named": 0
  },
  "e3_2_llava": {
   "a0s_named_with_persistent_visit": 0,
   "steps_inside_named": 0
  }
 },
 "p6": {
  "e3_1_sonnet": {
   "named_90_99": 0.985,
   "lead_female_90_99": 125,
   "lead_male_90_99": 74,
   "vader_1_10": 0.43413799999999997,
   "vader_90_99": 0.25897549999999997,
   "vader_up": false,
   "fk_by_window": {
    "1-10": 4.4082404829112,
    "11-25": 4.5549282108941025,
    "26-50": 4.377153983735678,
    "51-75": 4.165595959444461,
    "76-89": 4.225548200072144,
    "90-99": 4.260378333622468
   },
   "elderly_1_10": 0.275,
   "elderly_90_99": 0.47,
   "elderly_doubled": false
  },
  "e3_2_sonnet": {
   "named_90_99": 1.0,
   "lead_female_90_99": 115,
   "lead_male_90_99": 60,
   "vader_1_10": 0.6427435,
   "vader_90_99": 0.7201664999999999,
   "vader_up": true,
   "fk_by_window": {
    "1-10": 5.004717959082027,
    "11-25": 4.997221555217632,
    "26-50": 4.951329401019391,
    "51-75": 5.006279069767441,
    "76-89": 4.992622731942834,
    "90-99": 4.914120318096733
   },
   "elderly_1_10": 0.365,
   "elderly_90_99": 0.4,
   "elderly_doubled": false
  },
  "e3_1_qwen": {
   "named_90_99": 0.989010989010989,
   "lead_female_90_99": 125,
   "lead_male_90_99": 39,
   "vader_1_10": 0.9739241206030151,
   "vader_90_99": 0.9732153846153845,
   "vader_up": false,
   "fk_by_window": {
    "1-10": 9.616969696969697,
    "11-25": 10.076509952340905,
    "26-50": 10.497313380990299,
    "51-75": 10.1810580158837,
    "76-89": 10.369894454700372,
    "90-99": 10.323245638323991
   },
   "elderly_1_10": 0.1507537688442211,
   "elderly_90_99": 0.15384615384615385,
   "elderly_doubled": false
  },
  "e3_2_qwen": {
   "named_90_99": 0.6844919786096256,
   "lead_female_90_99": 97,
   "lead_male_90_99": 70,
   "vader_1_10": 0.9005853403141361,
   "vader_90_99": 0.7251096256684493,
   "vader_up": false,
   "fk_by_window": {
    "1-10": 8.853232758620692,
    "11-25": 8.990483688621138,
    "26-50": 9.232353137516691,
    "51-75": 9.212857142857143,
    "76-89": 8.945604938271606,
    "90-99": 9.296778711484595
   },
   "elderly_1_10": 0.09947643979057591,
   "elderly_90_99": 0.0962566844919786,
   "elderly_doubled": false
  },
  "e3_1_llava": {
   "named_90_99": 0.995,
   "lead_female_90_99": 96,
   "lead_male_90_99": 48,
   "vader_1_10": 0.9070374999999999,
   "vader_90_99": 0.9579079999999999,
   "vader_up": true,
   "fk_by_window": {
    "1-10": 7.909614379093,
    "11-25": 8.421426004891705,
    "26-50": 8.360718706176455,
    "51-75": 8.25824731918624,
    "76-89": 8.430361133500949,
    "90-99": 8.553537303982074
   },
   "elderly_1_10": 0.05,
   "elderly_90_99": 0.025,
   "elderly_doubled": false
  },
  "e3_2_llava": {
   "named_90_99": 0.375,
   "lead_female_90_99": 60,
   "lead_male_90_99": 65,
   "vader_1_10": 0.8120559999999999,
   "vader_90_99": 0.6555195,
   "vader_up": false,
   "fk_by_window": {
    "1-10": 8.466777259576862,
    "11-25": 9.737967926689576,
    "26-50": 10.408147920087575,
    "51-75": 10.801958333333333,
    "76-89": 10.892164069264071,
    "90-99": 10.405973346200687
   },
   "elderly_1_10": 0.01,
   "elderly_90_99": 0.02,
   "elderly_doubled": true
  }
 },
 "p7": {
  "e3_1_sonnet": {
   "summary_le50": 0.863,
   "story_lt400": 0.0
  },
  "e3_1_qwen": {
   "summary_le50": 0.9245,
   "story_lt400": 0.25814931650893796
  },
  "e3_1_llava": {
   "summary_le50": 0.3965,
   "story_lt400": 0.7318181818181818
  }
 },
 "p8": {
  "sonnet_half": 45,
  "qwen_half": 14,
  "flag": false
 },
 "p9": {
  "e3_1_sonnet": {
   "n_leads": 994,
   "distinct": 162,
   "top10": [
    [
     "Mara",
     87
    ],
    [
     "Pip",
     43
    ],
    [
     "Dev",
     40
    ],
    [
     "Priya",
     39
    ],
    [
     "Marisol",
     37
    ],
    [
     "Maxim",
     33
    ],
    [
     "Amara",
     31
    ],
    [
     "Julian",
     30
    ],
    [
     "Marin",
     30
    ],
    [
     "Marguerite",
     30
    ]
   ],
   "top10_cover": 0.4024144869215292,
   "llm_set_hits": [
    "Amara"
   ],
   "seed_names": {
    "trajectories_with_seed_names": 1,
    "gone_by_10": 1
   }
  },
  "e3_2_sonnet": {
   "n_leads": 1000,
   "distinct": 40,
   "top10": [
    [
     "Dev",
     75
    ],
    [
     "Calloway",
     74
    ],
    [
     "Tobias",
     61
    ],
    [
     "Odalys",
     53
    ],
    [
     "Secretary",
     50
    ],
    [
     "Latin",
     50
    ],
    [
     "Funmi",
     50
    ],
    [
     "Philomena",
     50
    ],
    [
     "Reyes",
     50
    ],
    [
     "Crane",
     50
    ]
   ],
   "top10_cover": 0.563,
   "llm_set_hits": [],
   "seed_names": {
    "trajectories_with_seed_names": 1,
    "gone_by_10": 0
   }
  },
  "e3_1_qwen": {
   "n_leads": 926,
   "distinct": 73,
   "top10": [
    [
     "Sarah",
     125
    ],
    [
     "Elara",
     57
    ],
    [
     "Willow",
     44
    ],
    [
     "Linda",
     44
    ],
    [
     "Willowbrook",
     37
    ],
    [
     "Mark",
     37
    ],
    [
     "Kael",
     35
    ],
    [
     "Eliza",
     34
    ],
    [
     "Smith",
     33
    ],
    [
     "Xia",
     29
    ]
   ],
   "top10_cover": 0.5129589632829373,
   "llm_set_hits": [
    "Elara"
   ],
   "seed_names": {
    "trajectories_with_seed_names": 1,
    "gone_by_10": 1
   }
  },
  "e3_2_qwen": {
   "n_leads": 743,
   "distinct": 23,
   "top10": [
    [
     "Sarah",
     149
    ],
    [
     "Lily",
     96
    ],
    [
     "Kael",
     50
    ],
    [
     "Jose",
     50
    ],
    [
     "Eldan",
     50
    ],
    [
     "Jenkins",
     45
    ],
    [
     "Voss",
     42
    ],
    [
     "James",
     36
    ],
    [
     "Eldershire",
     35
    ],
    [
     "Ella",
     32
    ]
   ],
   "top10_cover": 0.7873485868102288,
   "llm_set_hits": [],
   "seed_names": {
    "trajectories_with_seed_names": 1,
    "gone_by_10": 1
   }
  },
  "e3_1_llava": {
   "n_leads": 980,
   "distinct": 40,
   "top10": [
    [
     "Sarah",
     245
    ],
    [
     "Jack",
     110
    ],
    [
     "Sam",
     101
    ],
    [
     "Emily",
     50
    ],
    [
     "Sophia",
     49
    ],
    [
     "Amelia",
     37
    ],
    [
     "Sara",
     35
    ],
    [
     "Jill",
     33
    ],
    [
     "Lily",
     30
    ],
    [
     "Max",
     30
    ]
   ],
   "top10_cover": 0.7346938775510204,
   "llm_set_hits": [],
   "seed_names": {
    "trajectories_with_seed_names": 1,
    "gone_by_10": 1
   }
  },
  "e3_2_llava": {
   "n_leads": 374,
   "distinct": 11,
   "top10": [
    [
     "Smith",
     49
    ],
    [
     "Trafalgar",
     48
    ],
    [
     "John",
     45
    ],
    [
     "Kate",
     45
    ],
    [
     "Chen",
     43
    ],
    [
     "Jasmine",
     40
    ],
    [
     "Clara",
     35
    ],
    [
     "Emily",
     28
    ],
    [
     "Alex",
     22
    ],
    [
     "Riley",
     12
    ]
   ],
   "top10_cover": 0.9812834224598931,
   "llm_set_hits": [
    "Clara"
   ],
   "seed_names": {
    "trajectories_with_seed_names": 1,
    "gone_by_10": 1
   }
  },
  "qwen_vs_sonnet_top10_differ": 10
 }
}
```