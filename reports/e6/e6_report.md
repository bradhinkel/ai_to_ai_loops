# E6 pilot readouts

## e6_photo  (192 trajectories, horizon 19; judge coverage 100%, faces 100%)

Seed attribute realised in the step-0 image (judge = seed): gender 0.99 (n 192), age 1.0 (n 192), skin 0.677 (n 192). Survival below is relative to what step 0 showed.

### Attribute survival (share of trajectories with the step-0 value still present; competing dropout)

| attribute | group | n | kept @5 | kept @10 | kept @end | lost by end | dropout by end |
|---|---|---|---|---|---|---|---|
| gender | set=occupation | 144 | 0.4931 | 0.2431 | 0.1042 | 0.7639 | 0.1319 |
| gender | set=portrait | 48 | 0.8333 | 0.625 | 0.25 | 0.7292 | 0.0208 |
| gender | occupation=nurse | 48 | 0.2708 | 0.1042 | 0.0208 | 0.8958 | 0.0833 |
| gender | occupation=pilot | 48 | 0.3958 | 0.1667 | 0.0208 | 0.75 | 0.2292 |
| gender | occupation=portrait | 48 | 0.8333 | 0.625 | 0.25 | 0.7292 | 0.0208 |
| gender | occupation=social_worker | 48 | 0.8125 | 0.4583 | 0.2708 | 0.6458 | 0.0833 |
| gender | skin=dark | 64 | 0.5156 | 0.2656 | 0.1406 | 0.8125 | 0.0469 |
| gender | skin=light | 64 | 0.5625 | 0.3906 | 0.1562 | 0.7188 | 0.125 |
| gender | skin=medium | 64 | 0.6563 | 0.3594 | 0.125 | 0.7344 | 0.1406 |
| gender | gender=man | 96 | 0.6562 | 0.4375 | 0.1979 | 0.625 | 0.1771 |
| gender | gender=woman | 96 | 0.5 | 0.2396 | 0.0833 | 0.8854 | 0.0312 |
| age | set=occupation | 144 | 0.2292 | 0.0764 | 0.0139 | 0.8958 | 0.0903 |
| age | set=portrait | 48 | 0.5417 | 0.2083 | 0.0625 | 0.8958 | 0.0417 |
| age | occupation=nurse | 48 | 0.2083 | 0.0417 | 0.0 | 0.9375 | 0.0625 |
| age | occupation=pilot | 48 | 0.2083 | 0.0417 | 0.0 | 0.8542 | 0.1458 |
| age | occupation=portrait | 48 | 0.5417 | 0.2083 | 0.0625 | 0.8958 | 0.0417 |
| age | occupation=social_worker | 48 | 0.2708 | 0.1458 | 0.0417 | 0.8958 | 0.0625 |
| age | skin=dark | 64 | 0.25 | 0.0938 | 0.0312 | 0.8906 | 0.0781 |
| age | skin=light | 64 | 0.2969 | 0.1094 | 0.0312 | 0.875 | 0.0938 |
| age | skin=medium | 64 | 0.375 | 0.125 | 0.0156 | 0.9219 | 0.0625 |
| age | gender=man | 96 | 0.3229 | 0.1146 | 0.0208 | 0.8646 | 0.1146 |
| age | gender=woman | 96 | 0.2917 | 0.1042 | 0.0313 | 0.9271 | 0.0417 |
| skin | set=occupation | 144 | 0.0556 | 0.0347 | 0.0139 | 0.9028 | 0.0833 |
| skin | set=portrait | 48 | 0.125 | 0.0833 | 0.0417 | 0.9583 | 0.0 |
| skin | occupation=nurse | 48 | 0.0625 | 0.0417 | 0.0208 | 0.9375 | 0.0417 |
| skin | occupation=pilot | 48 | 0.1042 | 0.0625 | 0.0208 | 0.7708 | 0.2083 |
| skin | occupation=portrait | 48 | 0.125 | 0.0833 | 0.0417 | 0.9583 | 0.0 |
| skin | occupation=social_worker | 48 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| skin | skin=dark | 64 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| skin | skin=light | 64 | 0.1875 | 0.1094 | 0.0625 | 0.7969 | 0.1406 |
| skin | skin=medium | 64 | 0.0312 | 0.0312 | 0.0 | 0.9531 | 0.0469 |
| skin | gender=man | 96 | 0.0625 | 0.0625 | 0.0417 | 0.875 | 0.0833 |
| skin | gender=woman | 96 | 0.0833 | 0.0312 | 0.0 | 0.9583 | 0.0417 |

### Loss hazard per window (first losses / at-risk trajectory-steps)

| attribute | group | steps | losses | at risk | hazard |
|---|---|---|---|---|---|
| gender | set=occupation | 1-5 | 65 | 567 | 0.1146 |
| gender | set=occupation | 6-10 | 31 | 261 | 0.1188 |
| gender | set=occupation | 11-20 | 14 | 207 | 0.0676 |
| gender | set=portrait | 1-5 | 8 | 223 | 0.0359 |
| gender | set=portrait | 6-10 | 10 | 182 | 0.0549 |
| gender | set=portrait | 11-20 | 17 | 190 | 0.0895 |
| gender | occupation=nurse | 1-5 | 32 | 170 | 0.1882 |
| gender | occupation=nurse | 6-10 | 7 | 40 | 0.175 |
| gender | occupation=nurse | 11-20 | 4 | 20 | 0.2 |
| gender | occupation=pilot | 1-5 | 24 | 175 | 0.1371 |
| gender | occupation=pilot | 6-10 | 9 | 61 | 0.1475 |
| gender | occupation=pilot | 11-20 | 3 | 34 | 0.0882 |
| gender | occupation=portrait | 1-5 | 8 | 223 | 0.0359 |
| gender | occupation=portrait | 6-10 | 10 | 182 | 0.0549 |
| gender | occupation=portrait | 11-20 | 17 | 190 | 0.0895 |
| gender | occupation=social_worker | 1-5 | 9 | 222 | 0.0405 |
| gender | occupation=social_worker | 6-10 | 15 | 160 | 0.0938 |
| gender | occupation=social_worker | 11-20 | 7 | 153 | 0.0458 |
| age | set=occupation | 1-5 | 104 | 430 | 0.2419 |
| age | set=occupation | 6-10 | 20 | 107 | 0.1869 |
| age | set=occupation | 11-20 | 5 | 46 | 0.1087 |
| age | set=portrait | 1-5 | 22 | 204 | 0.1078 |
| age | set=portrait | 6-10 | 15 | 87 | 0.1724 |
| age | set=portrait | 11-20 | 6 | 56 | 0.1071 |
| age | occupation=nurse | 1-5 | 36 | 136 | 0.2647 |
| age | occupation=nurse | 6-10 | 8 | 23 | 0.3478 |
| age | occupation=nurse | 11-20 | 1 | 6 | 0.1667 |
| age | occupation=pilot | 1-5 | 33 | 137 | 0.2409 |
| age | occupation=pilot | 6-10 | 7 | 31 | 0.2258 |
| age | occupation=pilot | 11-20 | 1 | 11 | 0.0909 |
| age | occupation=portrait | 1-5 | 22 | 204 | 0.1078 |
| age | occupation=portrait | 6-10 | 15 | 87 | 0.1724 |
| age | occupation=portrait | 11-20 | 6 | 56 | 0.1071 |
| age | occupation=social_worker | 1-5 | 35 | 157 | 0.2229 |
| age | occupation=social_worker | 6-10 | 5 | 53 | 0.0943 |
| age | occupation=social_worker | 11-20 | 3 | 29 | 0.1034 |
| skin | set=occupation | 1-5 | 127 | 247 | 0.5142 |
| skin | set=occupation | 6-10 | 2 | 36 | 0.0556 |
| skin | set=occupation | 11-20 | 1 | 34 | 0.0294 |
| skin | set=portrait | 1-5 | 42 | 85 | 0.4941 |
| skin | set=portrait | 6-10 | 2 | 26 | 0.0769 |
| skin | set=portrait | 11-20 | 2 | 25 | 0.08 |
| skin | occupation=nurse | 1-5 | 43 | 86 | 0.5 |
| skin | occupation=nurse | 6-10 | 1 | 15 | 0.0667 |
| skin | occupation=nurse | 11-20 | 1 | 15 | 0.0667 |
| skin | occupation=pilot | 1-5 | 36 | 99 | 0.3636 |
| skin | occupation=pilot | 6-10 | 1 | 21 | 0.0476 |
| skin | occupation=pilot | 11-20 | 0 | 19 | 0.0 |
| skin | occupation=portrait | 1-5 | 42 | 85 | 0.4941 |
| skin | occupation=portrait | 6-10 | 2 | 26 | 0.0769 |
| skin | occupation=portrait | 11-20 | 2 | 25 | 0.08 |
| skin | occupation=social_worker | 1-5 | 48 | 62 | 0.7742 |
| skin | occupation=social_worker | 6-10 | 0 | 0 | None |
| skin | occupation=social_worker | 11-20 | 0 | 0 | None |

### Changes: 942 attribute losses from a kept state

- toward the occupation's prior: 0.362 (n 320)
- recovered within 3 steps: 0.502 (n 942)
- mechanism (caption that made the image): omission 823, override 82, caption change 37
- toward lighter skin or male presentation, by occupation: pilot 0.473 (n 129), nurse 0.362 (n 312), social_worker 0.403 (n 243)

### All three seeded attributes still present (joint survival; competing dropout)

| group | n | kept @5 | kept @10 | kept @end | lost by end | dropout by end |
|---|---|---|---|---|---|---|
| set=occupation | 144 | 0.0069 | 0.0 | 0.0 | 0.9792 | 0.0208 |
| set=portrait | 48 | 0.0833 | 0.0417 | 0.0 | 1.0 | 0.0 |
| occupation seeds: counter-stereotypical | 97 | 0.0103 | 0.0 | 0.0 | 1.0 | 0.0 |
| occupation seeds: stereotypical | 47 | 0.0 | 0.0 | 0.0 | 0.9362 | 0.0638 |
| occupation=pilot | 48 | 0.0 | 0.0 | 0.0 | 0.9375 | 0.0625 |
| occupation=nurse | 48 | 0.0208 | 0.0 | 0.0 | 1.0 | 0.0 |
| occupation=social_worker | 48 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |

### First-loss hazard and recovery by seed stereotypicality (whole horizon; Wilson 95% CI)

| attribute | seed vs prior | n traj | first losses | at-risk steps | hazard [CI] | lost by end | recovered within 3 [CI] |
|---|---|---|---|---|---|---|---|
| gender | counter | 73 | 59 | 542 | 0.1089 [0.0853, 0.1379] | 0.808 | 0.356 (n 59) [0.246, 0.4834] |
| gender | stereo | 71 | 51 | 493 | 0.1034 [0.0796, 0.1335] | 0.718 | 0.667 (n 51) [0.5297, 0.7803] |
| gender | **ratio counter / stereo** | | | | **1.05** | | |
| skin | counter | 53 | 52 | 71 | 0.7324 [0.6195, 0.8215] | 0.981 | 0.173 (n 52) [0.0938, 0.2973] |
| skin | stereo | 43 | 33 | 130 | 0.2538 [0.1868, 0.335] | 0.767 | 0.121 (n 33) [0.0482, 0.2733] |
| skin | **ratio counter / stereo** | | | | **2.89** | | |

### All losses by seed stereotypicality

| attribute | seed vs prior | losses | toward prior | recovered within 3 | omission / override / caption change |
|---|---|---|---|---|---|
| gender | counter | 95 | 0.758 | 0.442 | 70 / 18 / 7 |
| gender | stereo | 110 | 0.0 | 0.582 | 73 / 37 / 0 |
| skin | counter | 73 | 0.603 | 0.247 | 73 / 0 / 0 |
| skin | stereo | 42 | 0.0 | 0.143 | 41 / 0 / 1 |

### Single person in head-and-shoulders framing

| set | step | n | share |
|---|---|---|---|
| occupation | 0 | 144 | 0.0 |
| occupation | 5 | 144 | 0.0 |
| occupation | 10 | 144 | 0.0 |
| occupation | 19 | 144 | 0.0 |
| portrait | 0 | 48 | 0.833 |
| portrait | 5 | 47 | 0.213 |
| portrait | 10 | 48 | 0.083 |
| portrait | 19 | 48 | 0.0 |

### Skin L* by occupation and step (chromatic images with a detected face)

| group | step | n | L* mean | L* std | mean dL* vs own step 0 | share within 10 of step 0 |
|---|---|---|---|---|---|---|
| nurse | 0 | 46 | 32.9 | 11.5 | 0.0 | 1.0 |
| nurse | 5 | 39 | 47.8 | 13.6 | 16.2 | 0.237 |
| nurse | 10 | 31 | 51.7 | 14.6 | 20.8 | 0.167 |
| nurse | 19 | 25 | 52.3 | 11.9 | 20.5 | 0.217 |
| pilot | 0 | 48 | 40.0 | 14.9 | 0.0 | 1.0 |
| pilot | 5 | 18 | 49.5 | 15.0 | 4.6 | 0.333 |
| pilot | 10 | 18 | 46.7 | 16.4 | 5.1 | 0.444 |
| pilot | 19 | 13 | 45.4 | 15.7 | 8.3 | 0.308 |
| portrait | 0 | 40 | 46.7 | 16.2 | 0.0 | 1.0 |
| portrait | 5 | 43 | 51.7 | 12.4 | 4.3 | 0.429 |
| portrait | 10 | 35 | 53.3 | 14.6 | 3.8 | 0.387 |
| portrait | 19 | 40 | 52.5 | 14.5 | 3.3 | 0.394 |
| social_worker | 0 | 47 | 35.7 | 9.5 | 0.0 | 1.0 |
| social_worker | 5 | 34 | 58.5 | 15.8 | 22.6 | 0.182 |
| social_worker | 10 | 30 | 56.3 | 14.1 | 18.8 | 0.333 |
| social_worker | 19 | 18 | 51.9 | 13.4 | 16.8 | 0.222 |

### Portrait loss per step

| set | step | n | person | single person | head-and-shoulders | face detected | median face area | B&W or sepia |
|---|---|---|---|---|---|---|---|---|
| occupation | 0 | 144 | 1.0 | 0.785 | 0.0 | 1.0 | 0.0361 | 0.035 |
| occupation | 1 | 144 | 1.0 | 0.562 | 0.0 | 0.944 | 0.0239 | 0.181 |
| occupation | 2 | 144 | 0.993 | 0.521 | 0.014 | 0.917 | 0.0188 | 0.208 |
| occupation | 3 | 144 | 0.972 | 0.424 | 0.021 | 0.868 | 0.017 | 0.181 |
| occupation | 4 | 144 | 0.924 | 0.326 | 0.028 | 0.868 | 0.0136 | 0.208 |
| occupation | 5 | 144 | 0.917 | 0.285 | 0.042 | 0.84 | 0.0097 | 0.208 |
| occupation | 6 | 144 | 0.882 | 0.243 | 0.035 | 0.806 | 0.0113 | 0.16 |
| occupation | 7 | 144 | 0.875 | 0.25 | 0.049 | 0.743 | 0.0089 | 0.188 |
| occupation | 8 | 144 | 0.819 | 0.222 | 0.028 | 0.729 | 0.0088 | 0.146 |
| occupation | 9 | 144 | 0.819 | 0.208 | 0.062 | 0.681 | 0.0084 | 0.132 |
| occupation | 10 | 144 | 0.806 | 0.222 | 0.076 | 0.681 | 0.0078 | 0.167 |
| occupation | 11 | 144 | 0.792 | 0.188 | 0.049 | 0.674 | 0.006 | 0.167 |
| occupation | 12 | 144 | 0.785 | 0.174 | 0.062 | 0.653 | 0.0083 | 0.201 |
| occupation | 13 | 144 | 0.736 | 0.153 | 0.076 | 0.597 | 0.0078 | 0.188 |
| occupation | 14 | 144 | 0.708 | 0.153 | 0.062 | 0.597 | 0.0057 | 0.132 |
| occupation | 15 | 144 | 0.688 | 0.146 | 0.062 | 0.583 | 0.0061 | 0.132 |
| occupation | 16 | 144 | 0.667 | 0.153 | 0.104 | 0.569 | 0.0072 | 0.181 |
| occupation | 17 | 144 | 0.681 | 0.188 | 0.056 | 0.528 | 0.006 | 0.153 |
| occupation | 18 | 144 | 0.646 | 0.16 | 0.076 | 0.507 | 0.0066 | 0.167 |
| occupation | 19 | 144 | 0.639 | 0.146 | 0.076 | 0.514 | 0.0067 | 0.16 |
| portrait | 0 | 48 | 1.0 | 0.979 | 0.854 | 1.0 | 0.1937 | 0.229 |
| portrait | 1 | 48 | 1.0 | 0.688 | 0.5 | 1.0 | 0.1213 | 0.271 |
| portrait | 2 | 48 | 1.0 | 0.562 | 0.542 | 1.0 | 0.084 | 0.229 |
| portrait | 3 | 48 | 1.0 | 0.542 | 0.479 | 1.0 | 0.0746 | 0.229 |
| portrait | 4 | 48 | 1.0 | 0.625 | 0.458 | 1.0 | 0.0506 | 0.208 |
| portrait | 5 | 47 | 1.0 | 0.532 | 0.468 | 1.0 | 0.0261 | 0.17 |
| portrait | 6 | 48 | 1.0 | 0.479 | 0.396 | 1.0 | 0.0153 | 0.229 |
| portrait | 7 | 48 | 0.979 | 0.396 | 0.417 | 0.979 | 0.0215 | 0.292 |
| portrait | 8 | 48 | 1.0 | 0.396 | 0.396 | 0.958 | 0.0183 | 0.312 |
| portrait | 9 | 48 | 0.979 | 0.292 | 0.396 | 0.917 | 0.0207 | 0.292 |
| portrait | 10 | 48 | 0.979 | 0.333 | 0.417 | 0.938 | 0.0185 | 0.292 |
| portrait | 11 | 48 | 0.979 | 0.312 | 0.375 | 0.938 | 0.01 | 0.312 |
| portrait | 12 | 48 | 0.979 | 0.271 | 0.375 | 0.938 | 0.014 | 0.271 |
| portrait | 13 | 48 | 0.979 | 0.229 | 0.333 | 0.958 | 0.0092 | 0.25 |
| portrait | 14 | 48 | 0.958 | 0.229 | 0.354 | 0.917 | 0.0127 | 0.229 |
| portrait | 15 | 48 | 0.938 | 0.229 | 0.333 | 0.938 | 0.0134 | 0.208 |
| portrait | 16 | 48 | 0.938 | 0.229 | 0.333 | 0.917 | 0.0147 | 0.229 |
| portrait | 17 | 48 | 0.917 | 0.146 | 0.354 | 0.917 | 0.0135 | 0.208 |
| portrait | 18 | 48 | 0.917 | 0.167 | 0.271 | 0.938 | 0.0102 | 0.229 |
| portrait | 19 | 48 | 0.917 | 0.167 | 0.271 | 0.896 | 0.008 | 0.146 |

## e6_track  (192 trajectories, horizon 19; judge coverage 100%, faces 100%)

Seed attribute realised in the step-0 image (judge = seed): gender 0.99 (n 192), age 1.0 (n 192), skin 0.677 (n 192). Survival below is relative to what step 0 showed.

### Attribute survival (share of trajectories with the step-0 value still present; competing dropout)

| attribute | group | n | kept @5 | kept @10 | kept @end | lost by end | dropout by end |
|---|---|---|---|---|---|---|---|
| gender | set=occupation | 144 | 0.6042 | 0.3472 | 0.1319 | 0.8056 | 0.0625 |
| gender | set=portrait | 48 | 0.8333 | 0.5417 | 0.3125 | 0.6875 | 0.0 |
| gender | occupation=nurse | 48 | 0.4792 | 0.2292 | 0.0625 | 0.875 | 0.0625 |
| gender | occupation=pilot | 48 | 0.625 | 0.375 | 0.1042 | 0.7917 | 0.1042 |
| gender | occupation=portrait | 48 | 0.8333 | 0.5417 | 0.3125 | 0.6875 | 0.0 |
| gender | occupation=social_worker | 48 | 0.7083 | 0.4375 | 0.2292 | 0.75 | 0.0208 |
| gender | skin=dark | 64 | 0.6719 | 0.3906 | 0.1094 | 0.8594 | 0.0312 |
| gender | skin=light | 64 | 0.6875 | 0.3906 | 0.2344 | 0.7031 | 0.0625 |
| gender | skin=medium | 64 | 0.625 | 0.4062 | 0.1875 | 0.7656 | 0.0469 |
| gender | gender=man | 96 | 0.7188 | 0.4792 | 0.2396 | 0.6979 | 0.0625 |
| gender | gender=woman | 96 | 0.6042 | 0.3125 | 0.1146 | 0.8542 | 0.0312 |
| age | set=occupation | 144 | 0.3611 | 0.1181 | 0.0208 | 0.9375 | 0.0417 |
| age | set=portrait | 48 | 0.6875 | 0.4583 | 0.2292 | 0.7708 | 0.0 |
| age | occupation=nurse | 48 | 0.2708 | 0.1042 | 0.0 | 0.9375 | 0.0625 |
| age | occupation=pilot | 48 | 0.2708 | 0.1042 | 0.0417 | 0.9375 | 0.0208 |
| age | occupation=portrait | 48 | 0.6875 | 0.4583 | 0.2292 | 0.7708 | 0.0 |
| age | occupation=social_worker | 48 | 0.5417 | 0.1458 | 0.0208 | 0.9375 | 0.0417 |
| age | skin=dark | 64 | 0.4062 | 0.1562 | 0.0625 | 0.9219 | 0.0156 |
| age | skin=light | 64 | 0.5 | 0.2188 | 0.0938 | 0.8594 | 0.0469 |
| age | skin=medium | 64 | 0.4219 | 0.2344 | 0.0625 | 0.9062 | 0.0312 |
| age | gender=man | 96 | 0.4792 | 0.2396 | 0.1042 | 0.8646 | 0.0312 |
| age | gender=woman | 96 | 0.4063 | 0.1667 | 0.0417 | 0.9271 | 0.0312 |
| skin | set=occupation | 144 | 0.1111 | 0.0694 | 0.0347 | 0.9236 | 0.0417 |
| skin | set=portrait | 48 | 0.1042 | 0.0833 | 0.0625 | 0.9375 | 0.0 |
| skin | occupation=nurse | 48 | 0.125 | 0.0833 | 0.0208 | 0.9375 | 0.0417 |
| skin | occupation=pilot | 48 | 0.1875 | 0.125 | 0.0833 | 0.8542 | 0.0625 |
| skin | occupation=portrait | 48 | 0.1042 | 0.0833 | 0.0625 | 0.9375 | 0.0 |
| skin | occupation=social_worker | 48 | 0.0208 | 0.0 | 0.0 | 0.9792 | 0.0208 |
| skin | skin=dark | 64 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| skin | skin=light | 64 | 0.2656 | 0.1719 | 0.1094 | 0.8125 | 0.0781 |
| skin | skin=medium | 64 | 0.0625 | 0.0469 | 0.0156 | 0.9688 | 0.0156 |
| skin | gender=man | 96 | 0.1458 | 0.0938 | 0.0625 | 0.9062 | 0.0312 |
| skin | gender=woman | 96 | 0.0729 | 0.0521 | 0.0208 | 0.9479 | 0.0313 |

### Loss hazard per window (first losses / at-risk trajectory-steps)

| attribute | group | steps | losses | at risk | hazard |
|---|---|---|---|---|---|
| gender | set=occupation | 1-5 | 54 | 619 | 0.0872 |
| gender | set=occupation | 6-10 | 35 | 355 | 0.0986 |
| gender | set=occupation | 11-20 | 27 | 295 | 0.0915 |
| gender | set=portrait | 1-5 | 8 | 222 | 0.036 |
| gender | set=portrait | 6-10 | 14 | 164 | 0.0854 |
| gender | set=portrait | 11-20 | 11 | 190 | 0.0579 |
| gender | occupation=nurse | 1-5 | 24 | 188 | 0.1277 |
| gender | occupation=nurse | 6-10 | 12 | 89 | 0.1348 |
| gender | occupation=nurse | 11-20 | 6 | 55 | 0.1091 |
| gender | occupation=pilot | 1-5 | 17 | 206 | 0.0825 |
| gender | occupation=pilot | 6-10 | 10 | 130 | 0.0769 |
| gender | occupation=pilot | 11-20 | 11 | 92 | 0.1196 |
| gender | occupation=portrait | 1-5 | 8 | 222 | 0.036 |
| gender | occupation=portrait | 6-10 | 14 | 164 | 0.0854 |
| gender | occupation=portrait | 11-20 | 11 | 190 | 0.0579 |
| gender | occupation=social_worker | 1-5 | 13 | 225 | 0.0578 |
| gender | occupation=social_worker | 6-10 | 13 | 136 | 0.0956 |
| gender | occupation=social_worker | 11-20 | 10 | 148 | 0.0676 |
| age | set=occupation | 1-5 | 88 | 517 | 0.1702 |
| age | set=occupation | 6-10 | 35 | 180 | 0.1944 |
| age | set=occupation | 11-20 | 12 | 80 | 0.15 |
| age | set=portrait | 1-5 | 15 | 224 | 0.067 |
| age | set=portrait | 6-10 | 11 | 136 | 0.0809 |
| age | set=portrait | 11-20 | 11 | 136 | 0.0809 |
| age | occupation=nurse | 1-5 | 34 | 167 | 0.2036 |
| age | occupation=nurse | 6-10 | 8 | 56 | 0.1429 |
| age | occupation=nurse | 11-20 | 3 | 22 | 0.1364 |
| age | occupation=pilot | 1-5 | 34 | 155 | 0.2194 |
| age | occupation=pilot | 6-10 | 8 | 44 | 0.1818 |
| age | occupation=pilot | 11-20 | 3 | 28 | 0.1071 |
| age | occupation=portrait | 1-5 | 15 | 224 | 0.067 |
| age | occupation=portrait | 6-10 | 11 | 136 | 0.0809 |
| age | occupation=portrait | 11-20 | 11 | 136 | 0.0809 |
| age | occupation=social_worker | 1-5 | 20 | 195 | 0.1026 |
| age | occupation=social_worker | 6-10 | 19 | 80 | 0.2375 |
| age | occupation=social_worker | 11-20 | 6 | 30 | 0.2 |
| skin | set=occupation | 1-5 | 125 | 283 | 0.4417 |
| skin | set=occupation | 6-10 | 5 | 65 | 0.0769 |
| skin | set=occupation | 11-20 | 3 | 69 | 0.0435 |
| skin | set=portrait | 1-5 | 43 | 91 | 0.4725 |
| skin | set=portrait | 6-10 | 1 | 22 | 0.0455 |
| skin | set=portrait | 11-20 | 1 | 35 | 0.0286 |
| skin | occupation=nurse | 1-5 | 41 | 97 | 0.4227 |
| skin | occupation=nurse | 6-10 | 2 | 23 | 0.087 |
| skin | occupation=nurse | 11-20 | 2 | 23 | 0.087 |
| skin | occupation=pilot | 1-5 | 38 | 106 | 0.3585 |
| skin | occupation=pilot | 6-10 | 2 | 40 | 0.05 |
| skin | occupation=pilot | 11-20 | 1 | 46 | 0.0217 |
| skin | occupation=portrait | 1-5 | 43 | 91 | 0.4725 |
| skin | occupation=portrait | 6-10 | 1 | 22 | 0.0455 |
| skin | occupation=portrait | 11-20 | 1 | 35 | 0.0286 |
| skin | occupation=social_worker | 1-5 | 46 | 80 | 0.575 |
| skin | occupation=social_worker | 6-10 | 1 | 2 | 0.5 |
| skin | occupation=social_worker | 11-20 | 0 | 0 | None |

### Changes: 1063 attribute losses from a kept state

- toward the occupation's prior: 0.414 (n 403)
- recovered within 3 steps: 0.492 (n 1063)
- mechanism (caption that made the image): omission 570, override 295, caption change 198
- toward lighter skin or male presentation, by occupation: pilot 0.366 (n 246), nurse 0.397 (n 315), social_worker 0.42 (n 269)

### All three seeded attributes still present (joint survival; competing dropout)

| group | n | kept @5 | kept @10 | kept @end | lost by end | dropout by end |
|---|---|---|---|---|---|---|
| set=occupation | 144 | 0.0347 | 0.0208 | 0.0 | 0.9722 | 0.0278 |
| set=portrait | 48 | 0.0625 | 0.0417 | 0.0208 | 0.9792 | 0.0 |
| occupation seeds: counter-stereotypical | 97 | 0.0412 | 0.0206 | 0.0 | 0.9691 | 0.0309 |
| occupation seeds: stereotypical | 47 | 0.0213 | 0.0213 | 0.0 | 0.9787 | 0.0213 |
| occupation=pilot | 48 | 0.0208 | 0.0208 | 0.0 | 0.9792 | 0.0208 |
| occupation=nurse | 48 | 0.0625 | 0.0417 | 0.0 | 0.9583 | 0.0417 |
| occupation=social_worker | 48 | 0.0208 | 0.0 | 0.0 | 0.9792 | 0.0208 |

### First-loss hazard and recovery by seed stereotypicality (whole horizon; Wilson 95% CI)

| attribute | seed vs prior | n traj | first losses | at-risk steps | hazard [CI] | lost by end | recovered within 3 [CI] |
|---|---|---|---|---|---|---|---|
| gender | counter | 73 | 59 | 630 | 0.0937 [0.0733, 0.1189] | 0.808 | 0.542 (n 59) [0.4166, 0.663] |
| gender | stereo | 71 | 57 | 639 | 0.0892 [0.0695, 0.1138] | 0.803 | 0.667 (n 57) [0.5372, 0.7751] |
| gender | **ratio counter / stereo** | | | | **1.05** | | |
| skin | counter | 53 | 53 | 83 | 0.6386 [0.5312, 0.7337] | 1.0 | 0.208 (n 53) [0.12, 0.3346] |
| skin | stereo | 43 | 35 | 191 | 0.1832 [0.1348, 0.2442] | 0.814 | 0.314 (n 35) [0.1855, 0.4798] |
| skin | **ratio counter / stereo** | | | | **3.49** | | |

### All losses by seed stereotypicality

| attribute | seed vs prior | losses | toward prior | recovered within 3 | omission / override / caption change |
|---|---|---|---|---|---|
| gender | counter | 114 | 0.816 | 0.474 | 51 / 58 / 5 |
| gender | stereo | 124 | 0.0 | 0.581 | 51 / 70 / 3 |
| skin | counter | 113 | 0.655 | 0.283 | 49 / 12 / 52 |
| skin | stereo | 52 | 0.0 | 0.288 | 30 / 8 / 14 |

### Single person in head-and-shoulders framing

| set | step | n | share |
|---|---|---|---|
| occupation | 0 | 144 | 0.0 |
| occupation | 5 | 144 | 0.014 |
| occupation | 10 | 144 | 0.021 |
| occupation | 19 | 144 | 0.007 |
| portrait | 0 | 48 | 0.833 |
| portrait | 5 | 48 | 0.229 |
| portrait | 10 | 48 | 0.125 |
| portrait | 19 | 48 | 0.042 |

### Skin L* by occupation and step (chromatic images with a detected face)

| group | step | n | L* mean | L* std | mean dL* vs own step 0 | share within 10 of step 0 |
|---|---|---|---|---|---|---|
| nurse | 0 | 46 | 32.9 | 11.5 | 0.0 | 1.0 |
| nurse | 5 | 38 | 53.7 | 10.6 | 19.6 | 0.167 |
| nurse | 10 | 44 | 49.2 | 13.4 | 16.0 | 0.286 |
| nurse | 19 | 38 | 48.5 | 14.6 | 15.9 | 0.278 |
| pilot | 0 | 48 | 40.0 | 14.9 | 0.0 | 1.0 |
| pilot | 5 | 38 | 57.2 | 11.5 | 18.2 | 0.342 |
| pilot | 10 | 28 | 55.6 | 13.2 | 16.6 | 0.25 |
| pilot | 19 | 32 | 55.2 | 10.1 | 16.0 | 0.281 |
| portrait | 0 | 40 | 46.7 | 16.2 | 0.0 | 1.0 |
| portrait | 5 | 41 | 57.3 | 13.0 | 11.5 | 0.471 |
| portrait | 10 | 41 | 55.2 | 13.1 | 9.2 | 0.294 |
| portrait | 19 | 43 | 57.6 | 10.7 | 9.4 | 0.371 |
| social_worker | 0 | 47 | 35.7 | 9.5 | 0.0 | 1.0 |
| social_worker | 5 | 38 | 54.8 | 12.0 | 18.0 | 0.237 |
| social_worker | 10 | 35 | 54.8 | 13.5 | 18.4 | 0.206 |
| social_worker | 19 | 28 | 57.7 | 13.7 | 20.6 | 0.185 |

### Portrait loss per step

| set | step | n | person | single person | head-and-shoulders | face detected | median face area | B&W or sepia |
|---|---|---|---|---|---|---|---|---|
| occupation | 0 | 144 | 1.0 | 0.778 | 0.0 | 1.0 | 0.0361 | 0.035 |
| occupation | 1 | 144 | 0.993 | 0.611 | 0.0 | 0.951 | 0.0308 | 0.125 |
| occupation | 2 | 144 | 0.986 | 0.479 | 0.042 | 0.965 | 0.0283 | 0.139 |
| occupation | 3 | 144 | 0.986 | 0.375 | 0.104 | 0.958 | 0.0266 | 0.181 |
| occupation | 4 | 144 | 0.972 | 0.354 | 0.139 | 0.931 | 0.0172 | 0.264 |
| occupation | 5 | 144 | 0.965 | 0.299 | 0.188 | 0.931 | 0.0153 | 0.271 |
| occupation | 6 | 144 | 0.958 | 0.292 | 0.208 | 0.944 | 0.014 | 0.271 |
| occupation | 7 | 144 | 0.972 | 0.257 | 0.208 | 0.931 | 0.0093 | 0.299 |
| occupation | 8 | 144 | 0.951 | 0.25 | 0.188 | 0.931 | 0.0131 | 0.319 |
| occupation | 9 | 144 | 0.951 | 0.229 | 0.222 | 0.924 | 0.014 | 0.354 |
| occupation | 10 | 144 | 0.958 | 0.181 | 0.16 | 0.924 | 0.0122 | 0.306 |
| occupation | 11 | 144 | 0.965 | 0.201 | 0.194 | 0.944 | 0.0111 | 0.361 |
| occupation | 12 | 144 | 0.965 | 0.188 | 0.194 | 0.931 | 0.0101 | 0.312 |
| occupation | 13 | 144 | 0.944 | 0.188 | 0.208 | 0.924 | 0.0115 | 0.319 |
| occupation | 14 | 144 | 0.938 | 0.194 | 0.208 | 0.917 | 0.0102 | 0.319 |
| occupation | 15 | 144 | 0.917 | 0.146 | 0.208 | 0.889 | 0.009 | 0.319 |
| occupation | 16 | 144 | 0.917 | 0.153 | 0.236 | 0.868 | 0.0085 | 0.347 |
| occupation | 17 | 144 | 0.944 | 0.146 | 0.201 | 0.875 | 0.0088 | 0.354 |
| occupation | 18 | 144 | 0.896 | 0.139 | 0.188 | 0.847 | 0.008 | 0.361 |
| occupation | 19 | 144 | 0.91 | 0.16 | 0.181 | 0.847 | 0.0089 | 0.368 |
| portrait | 0 | 48 | 1.0 | 0.979 | 0.854 | 1.0 | 0.1937 | 0.229 |
| portrait | 1 | 48 | 1.0 | 0.771 | 0.604 | 1.0 | 0.1425 | 0.167 |
| portrait | 2 | 48 | 1.0 | 0.75 | 0.604 | 1.0 | 0.1595 | 0.146 |
| portrait | 3 | 48 | 1.0 | 0.562 | 0.625 | 1.0 | 0.1381 | 0.125 |
| portrait | 4 | 48 | 1.0 | 0.479 | 0.604 | 0.979 | 0.0939 | 0.167 |
| portrait | 5 | 48 | 1.0 | 0.438 | 0.604 | 0.979 | 0.0654 | 0.25 |
| portrait | 6 | 48 | 1.0 | 0.417 | 0.5 | 0.979 | 0.0309 | 0.25 |
| portrait | 7 | 48 | 1.0 | 0.396 | 0.562 | 0.979 | 0.0269 | 0.229 |
| portrait | 8 | 48 | 1.0 | 0.354 | 0.5 | 0.979 | 0.0304 | 0.25 |
| portrait | 9 | 48 | 1.0 | 0.354 | 0.521 | 0.979 | 0.0289 | 0.229 |
| portrait | 10 | 48 | 1.0 | 0.375 | 0.521 | 0.979 | 0.0231 | 0.229 |
| portrait | 11 | 48 | 1.0 | 0.396 | 0.521 | 0.979 | 0.0255 | 0.25 |
| portrait | 12 | 48 | 1.0 | 0.354 | 0.458 | 0.979 | 0.0193 | 0.333 |
| portrait | 13 | 48 | 1.0 | 0.333 | 0.521 | 0.979 | 0.0154 | 0.354 |
| portrait | 14 | 48 | 1.0 | 0.312 | 0.438 | 1.0 | 0.0148 | 0.375 |
| portrait | 15 | 48 | 1.0 | 0.25 | 0.417 | 1.0 | 0.0132 | 0.375 |
| portrait | 16 | 48 | 1.0 | 0.208 | 0.417 | 1.0 | 0.0138 | 0.354 |
| portrait | 17 | 48 | 1.0 | 0.229 | 0.396 | 1.0 | 0.0146 | 0.375 |
| portrait | 18 | 48 | 1.0 | 0.229 | 0.354 | 1.0 | 0.009 | 0.417 |
| portrait | 19 | 48 | 1.0 | 0.229 | 0.271 | 1.0 | 0.0102 | 0.417 |

