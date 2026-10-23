# E6: occupations named by the captions, and who gets re-assigned

Caption at step s describes image s. Role words: **doctor**: `\b(doctor|doctors|physician|physicians|surgeon|surgeons)\b`; **nurse**: `\bnurses?\b`; **medical staff (unspecified)**: `\b(medical (staff|professional|professionals|personnel|worker|workers|team)|healthcare (worker|workers|professional|professionals))\b`; **patient**: `\bpatients?\b`; **pilot**: `\bpilots?\b`; **military / soldier**: `\b(soldier|soldiers|military|army|navy|naval|air force|marines?|troops?|servicem[ae]n|service members?|infantry|combat|camouflage|fatigues)\b`; **astronaut**: `\bastronauts?\b`; **police**: `\b(police|policem[ae]n|law enforcement)\b`; **scientist / lab**: `\b(scientists?|laboratory|lab coats?|researchers?)\b`; **business / office worker**: `\b(business(man|woman|men|women|person|people)|executives?|office workers?)\b`; **social worker**: `\bsocial workers?\b`; **teacher / student**: `\b(teachers?|students?|professors?)\b`

## e6_photo

### Share of captions naming each role, by seed occupation and step

| seed occupation | role | 0 | 1 | 2 | 3 | 5 | 10 | 15 | 19 |
|---|---|---|---|---|---|---|---|---|---|
| pilot | pilot | 0.85 | 0.83 | 0.92 | 0.75 | 0.56 | 0.35 | 0.31 | 0.21 |
| pilot | military / soldier | 0.23 | 0.38 | 0.52 | 0.50 | 0.44 | 0.29 | 0.27 | 0.19 |
| pilot | astronaut | 0.00 | 0.08 | 0.02 | 0.10 | 0.25 | 0.23 | 0.23 | 0.21 |
| nurse | doctor | 0.06 | 0.19 | 0.25 | 0.19 | 0.23 | 0.15 | 0.25 | 0.08 |
| nurse | nurse | 0.48 | 0.29 | 0.27 | 0.35 | 0.25 | 0.17 | 0.21 | 0.10 |
| nurse | medical staff (unspecified) | 0.42 | 0.44 | 0.42 | 0.54 | 0.50 | 0.44 | 0.44 | 0.25 |
| nurse | patient | 0.25 | 0.31 | 0.40 | 0.42 | 0.38 | 0.35 | 0.17 | 0.19 |
| nurse | scientist / lab | 0.15 | 0.31 | 0.27 | 0.19 | 0.21 | 0.17 | 0.12 | 0.19 |
| social_worker | scientist / lab | 0.00 | 0.00 | 0.00 | 0.02 | 0.02 | 0.04 | 0.02 | 0.02 |
| social_worker | business / office worker | 0.02 | 0.00 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| social_worker | teacher / student | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.02 | 0.02 |

### Re-assignment by seed group (trajectories whose captions ever name the role in steps 1–19; Wilson 95% CI)

| seed occupation → role | n ever / n | median first step | by seed gender | by seed skin | by seed age |
|---|---|---|---|---|---|
| pilot → pilot | 47 / 48 (0.98) | 1 | man 1.00 (24/24); woman 0.96 (23/24) | dark 1.00 (16/16); light 1.00 (16/16); medium 0.94 (15/16) | older 0.96 (23/24); young 1.00 (24/24) |
| pilot → military / soldier | 42 / 48 (0.88) | 2 | man 0.96 (23/24); woman 0.79 (19/24) | dark 0.88 (14/16); light 0.88 (14/16); medium 0.88 (14/16) | older 0.79 (19/24); young 0.96 (23/24) |
| pilot → astronaut | 18 / 48 (0.38) | 5 | man 0.29 (7/24); woman 0.46 (11/24) | dark 0.38 (6/16); light 0.38 (6/16); medium 0.38 (6/16) | older 0.42 (10/24); young 0.33 (8/24) |
| nurse → doctor | 39 / 48 (0.81) | 3 | man 0.83 (20/24); woman 0.79 (19/24) | dark 0.94 (15/16); light 0.69 (11/16); medium 0.81 (13/16) | older 0.79 (19/24); young 0.83 (20/24) |
| nurse → nurse | 35 / 48 (0.73) | 2 | man 0.67 (16/24); woman 0.79 (19/24) | dark 0.75 (12/16); light 0.69 (11/16); medium 0.75 (12/16) | older 0.71 (17/24); young 0.75 (18/24) |
| nurse → medical staff (unspecified) | 46 / 48 (0.96) | 2 | man 1.00 (24/24); woman 0.92 (22/24) | dark 0.94 (15/16); light 1.00 (16/16); medium 0.94 (15/16) | older 0.96 (23/24); young 0.96 (23/24) |
| nurse → patient | 39 / 48 (0.81) | 2 | man 0.88 (21/24); woman 0.75 (18/24) | dark 0.81 (13/16); light 0.81 (13/16); medium 0.81 (13/16) | older 0.79 (19/24); young 0.83 (20/24) |
| nurse → scientist / lab | 39 / 48 (0.81) | 2 | man 0.83 (20/24); woman 0.79 (19/24) | dark 0.94 (15/16); light 0.88 (14/16); medium 0.62 (10/16) | older 0.88 (21/24); young 0.75 (18/24) |
| nurse → teacher / student | 7 / 48 (0.15) | 13 | man 0.17 (4/24); woman 0.12 (3/24) | dark 0.19 (3/16); light 0.12 (2/16); medium 0.12 (2/16) | older 0.08 (2/24); young 0.21 (5/24) |
| social_worker → business / office worker | 6 / 48 (0.12) | 4 | man 0.12 (3/24); woman 0.12 (3/24) | dark 0.25 (4/16); light 0.12 (2/16); medium 0.00 (0/16) | older 0.08 (2/24); young 0.17 (4/24) |
| social_worker → teacher / student | 4 / 48 (0.08) | 8 | man 0.12 (3/24); woman 0.04 (1/24) | dark 0.06 (1/16); light 0.06 (1/16); medium 0.12 (2/16) | older 0.12 (3/24); young 0.04 (1/24) |

### At the first caption naming the role: what the image showed (judge) and what the caption said

| seed occupation → role | judge gender | judge skin | caption gender words | seed gender still shown | seed skin still shown |
|---|---|---|---|---|---|
| pilot → pilot | man 20, woman 17, none 7, ambiguous 3 | light 33, none 11, dark 3 | none 19, man 15, woman 12, man+woman 1 | 0.825 (n 40) | 0.278 (n 36) |
| pilot → military / soldier | man 17, woman 11, none 10, ambiguous 4 | light 26, none 14, medium 1, dark 1 | none 22, man 10, woman 9, man+woman 1 | 0.781 (n 32) | 0.179 (n 28) |
| pilot → astronaut | none 7, woman 5, man 4, ambiguous 2 | none 9, light 9 | none 11, woman 4, man 3 | 0.636 (n 11) | 0.222 (n 9) |
| nurse → doctor | man 21, woman 13, none 3, ambiguous 2 | light 26, none 5, medium 4, dark 4 | none 17, man+woman 10, man 8, woman 4 | 0.611 (n 36) | 0.235 (n 34) |
| nurse → nurse | woman 17, man 14, none 3, ambiguous 1 | light 20, dark 6, none 6, medium 3 | none 14, woman 11, man 5, man+woman 5 | 0.781 (n 32) | 0.207 (n 29) |
| nurse → medical staff (unspecified) | woman 24, man 21, none 1 | light 31, dark 7, medium 6, none 2 | woman 16, none 13, man 12, man+woman 5 | 0.889 (n 45) | 0.318 (n 44) |
| nurse → patient | woman 19, man 17, none 3 | light 23, dark 6, medium 5, none 5 | none 15, man 11, woman 8, man+woman 5 | 0.778 (n 36) | 0.235 (n 34) |
| nurse → scientist / lab | man 20, woman 18, none 1 | light 31, medium 4, none 3, dark 1 | none 13, man 10, man+woman 9, woman 7 | 0.789 (n 38) | 0.222 (n 36) |
| nurse → teacher / student | woman 6, man 1 | light 6, dark 1 | none 4, woman 2, man+woman 1 | 0.571 (n 7) | 0.429 (n 7) |
| social_worker → business / office worker | man 3, woman 3 | light 5, medium 1 | man 3, woman 2, none 1 | 1.0 (n 6) | 0.167 (n 6) |
| social_worker → teacher / student | man 2, woman 2 | light 3, medium 1 | man 2, none 2 | 0.25 (n 4) | 0.0 (n 4) |
### Per image, steps 1–19, single person in frame: role word in the caption vs what the judge saw and the caption's gender words

| seed occupation | caption names | n images | judge: man / woman / ambiguous / none | judge: light / medium / dark | caption words: man / woman / both / none | seed: man / woman |
|---|---|---|---|---|---|---|
| nurse | all single-person images | 139 | 88 / 35 / 6 / 10 | 108 / 13 / 1 | 56 / 26 / 3 / 54 | 99 / 40 |
| nurse | doctor | 15 | 12 / 2 / 0 / 1 | 12 / 2 / 0 | 10 / 1 / 1 / 3 | 12 / 3 |
| nurse | nurse | 7 | 2 / 2 / 1 / 2 | 3 / 1 / 0 | 1 / 2 / 1 / 3 | 5 / 2 |
| nurse | patient | 16 | 8 / 3 / 3 / 2 | 12 / 1 / 0 | 6 / 2 / 0 / 8 | 13 / 3 |
| nurse | scientist / lab | 79 | 59 / 18 / 1 / 1 | 70 / 6 / 0 | 37 / 15 / 3 / 24 | 58 / 21 |
| pilot | all single-person images | 184 | 81 / 67 / 2 / 34 | 130 / 15 / 1 | 40 / 59 / 0 / 85 | 65 / 119 |
| pilot | pilot | 89 | 36 / 45 / 1 / 7 | 74 / 6 / 1 | 19 / 37 / 0 / 33 | 35 / 54 |
| pilot | military / soldier | 67 | 28 / 32 / 0 / 7 | 55 / 2 / 1 | 16 / 26 / 0 / 25 | 27 / 40 |
| pilot | astronaut | 57 | 35 / 11 / 1 / 10 | 40 / 6 / 0 | 12 / 9 / 0 / 36 | 20 / 37 |

## e6_track

### Share of captions naming each role, by seed occupation and step

| seed occupation | role | 0 | 1 | 2 | 3 | 5 | 10 | 15 | 19 |
|---|---|---|---|---|---|---|---|---|---|
| pilot | pilot | 0.85 | 0.83 | 0.67 | 0.65 | 0.44 | 0.23 | 0.15 | 0.12 |
| pilot | military / soldier | 0.21 | 0.52 | 0.60 | 0.71 | 0.71 | 0.65 | 0.60 | 0.54 |
| pilot | astronaut | 0.00 | 0.02 | 0.02 | 0.06 | 0.06 | 0.04 | 0.08 | 0.08 |
| pilot | police | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 | 0.06 | 0.02 |
| nurse | doctor | 0.06 | 0.19 | 0.25 | 0.23 | 0.19 | 0.19 | 0.10 | 0.02 |
| nurse | nurse | 0.42 | 0.35 | 0.35 | 0.35 | 0.29 | 0.17 | 0.10 | 0.12 |
| nurse | medical staff (unspecified) | 0.44 | 0.48 | 0.50 | 0.46 | 0.46 | 0.44 | 0.35 | 0.31 |
| nurse | patient | 0.17 | 0.23 | 0.27 | 0.33 | 0.21 | 0.25 | 0.10 | 0.19 |
| nurse | scientist / lab | 0.15 | 0.35 | 0.31 | 0.40 | 0.27 | 0.27 | 0.15 | 0.17 |
| social_worker | business / office worker | 0.00 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 |

### Re-assignment by seed group (trajectories whose captions ever name the role in steps 1–19; Wilson 95% CI)

| seed occupation → role | n ever / n | median first step | by seed gender | by seed skin | by seed age |
|---|---|---|---|---|---|
| pilot → pilot | 44 / 48 (0.92) | 1 | man 0.92 (22/24); woman 0.92 (22/24) | dark 0.88 (14/16); light 0.94 (15/16); medium 0.94 (15/16) | older 0.88 (21/24); young 0.96 (23/24) |
| pilot → military / soldier | 44 / 48 (0.92) | 1 | man 0.83 (20/24); woman 1.00 (24/24) | dark 0.88 (14/16); light 0.94 (15/16); medium 0.94 (15/16) | older 0.83 (20/24); young 1.00 (24/24) |
| pilot → astronaut | 6 / 48 (0.12) | 8 | man 0.21 (5/24); woman 0.04 (1/24) | dark 0.12 (2/16); light 0.06 (1/16); medium 0.19 (3/16) | older 0.17 (4/24); young 0.08 (2/24) |
| pilot → police | 7 / 48 (0.15) | 15 | man 0.12 (3/24); woman 0.17 (4/24) | dark 0.25 (4/16); light 0.06 (1/16); medium 0.12 (2/16) | older 0.17 (4/24); young 0.12 (3/24) |
| nurse → doctor | 37 / 48 (0.77) | 3 | man 0.83 (20/24); woman 0.71 (17/24) | dark 0.62 (10/16); light 0.88 (14/16); medium 0.81 (13/16) | older 0.79 (19/24); young 0.75 (18/24) |
| nurse → nurse | 37 / 48 (0.77) | 2 | man 0.67 (16/24); woman 0.88 (21/24) | dark 0.75 (12/16); light 0.69 (11/16); medium 0.88 (14/16) | older 0.67 (16/24); young 0.88 (21/24) |
| nurse → medical staff (unspecified) | 44 / 48 (0.92) | 1 | man 0.92 (22/24); woman 0.92 (22/24) | dark 0.88 (14/16); light 1.00 (16/16); medium 0.88 (14/16) | older 0.88 (21/24); young 0.96 (23/24) |
| nurse → patient | 33 / 48 (0.69) | 2 | man 0.67 (16/24); woman 0.71 (17/24) | dark 0.50 (8/16); light 0.69 (11/16); medium 0.88 (14/16) | older 0.62 (15/24); young 0.75 (18/24) |
| nurse → scientist / lab | 39 / 48 (0.81) | 2 | man 0.88 (21/24); woman 0.75 (18/24) | dark 0.81 (13/16); light 0.81 (13/16); medium 0.81 (13/16) | older 0.92 (22/24); young 0.71 (17/24) |
| nurse → teacher / student | 6 / 48 (0.12) | 11 | man 0.08 (2/24); woman 0.17 (4/24) | dark 0.06 (1/16); light 0.12 (2/16); medium 0.19 (3/16) | older 0.17 (4/24); young 0.08 (2/24) |
| social_worker → business / office worker | 4 / 48 (0.08) | 19 | man 0.12 (3/24); woman 0.04 (1/24) | dark 0.25 (4/16); light 0.00 (0/16); medium 0.00 (0/16) | older 0.08 (2/24); young 0.08 (2/24) |

### At the first caption naming the role: what the image showed (judge) and what the caption said

| seed occupation → role | judge gender | judge skin | caption gender words | seed gender still shown | seed skin still shown |
|---|---|---|---|---|---|
| pilot → pilot | woman 20, man 19, none 4, ambiguous 1 | light 26, dark 13, none 4, medium 1 | man 18, woman 16, man+woman 5, none 5 | 0.9 (n 40) | 0.325 (n 40) |
| pilot → military / soldier | woman 22, man 19, none 3 | light 26, dark 11, none 4, medium 3 | man 17, woman 17, man+woman 6, none 4 | 0.902 (n 41) | 0.4 (n 40) |
| pilot → astronaut | man 5, none 1 | light 5, none 1 | man 4, none 2 | 0.8 (n 5) | 0.4 (n 5) |
| pilot → police | man 4, woman 3 | light 6, medium 1 | man 3, none 2, woman 2 | 0.286 (n 7) | 0.286 (n 7) |
| nurse → doctor | man 21, woman 12, ambiguous 3, none 1 | light 23, dark 6, medium 6, none 2 | man 12, man+woman 12, none 7, woman 6 | 0.694 (n 36) | 0.371 (n 35) |
| nurse → nurse | woman 18, man 16, ambiguous 2, none 1 | light 19, medium 8, dark 8, none 2 | woman 13, none 10, man+woman 10, man 4 | 0.806 (n 36) | 0.286 (n 35) |
| nurse → medical staff (unspecified) | man 23, woman 20, none 1 | light 28, dark 12, medium 3, none 1 | man 14, woman 13, man+woman 10, none 7 | 0.907 (n 43) | 0.372 (n 43) |
| nurse → patient | man 16, woman 13, ambiguous 3, none 1 | light 16, dark 13, none 3, medium 1 | man+woman 13, woman 9, none 6, man 5 | 0.688 (n 32) | 0.333 (n 30) |
| nurse → scientist / lab | man 19, woman 18, ambiguous 2 | light 26, dark 10, medium 3 | man 16, woman 9, man+woman 8, none 6 | 0.692 (n 39) | 0.41 (n 39) |
| nurse → teacher / student | woman 5, man 1 | light 4, dark 1, none 1 | none 3, man+woman 2, woman 1 | 0.833 (n 6) | 0.2 (n 5) |
| social_worker → business / office worker | man 3, ambiguous 1 | light 4 | man 3, man+woman 1 | 0.5 (n 4) | 0.0 (n 4) |
### Per image, steps 1–19, single person in frame: role word in the caption vs what the judge saw and the caption's gender words

| seed occupation | caption names | n images | judge: man / woman / ambiguous / none | judge: light / medium / dark | caption words: man / woman / both / none | seed: man / woman |
|---|---|---|---|---|---|---|
| nurse | all single-person images | 179 | 87 / 87 / 2 / 3 | 147 / 14 / 13 | 84 / 80 / 3 / 12 | 76 / 103 |
| nurse | doctor | 22 | 18 / 4 / 0 / 0 | 20 / 2 / 0 | 17 / 4 / 0 / 1 | 18 / 4 |
| nurse | nurse | 15 | 1 / 13 / 1 / 0 | 9 / 2 / 4 | 0 / 12 / 0 / 3 | 2 / 13 |
| nurse | patient | 9 | 1 / 6 / 2 / 0 | 8 / 0 / 1 | 1 / 3 / 0 / 5 | 2 / 7 |
| nurse | scientist / lab | 83 | 37 / 46 / 0 / 0 | 75 / 4 / 3 | 36 / 43 / 2 / 2 | 36 / 47 |
| pilot | all single-person images | 236 | 117 / 107 / 7 / 5 | 182 / 30 / 15 | 119 / 98 / 4 / 15 | 97 / 139 |
| pilot | pilot | 132 | 54 / 75 / 3 / 0 | 104 / 15 / 12 | 54 / 73 / 1 / 4 | 51 / 81 |
| pilot | military / soldier | 165 | 73 / 88 / 4 / 0 | 127 / 26 / 11 | 73 / 82 / 4 / 6 | 57 / 108 |
| pilot | astronaut | 22 | 22 / 0 / 0 / 0 | 20 / 2 / 0 | 21 / 0 / 0 / 1 | 11 / 11 |

