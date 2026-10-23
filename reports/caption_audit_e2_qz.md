# Caption audit (Chinese-aware): e2_qz, e1_both

Length = characters for Chinese captions (CJK share >= 0.5), words for English. Chinese term lists are substrings (people excludes 无人/迷人/动人/他们 etc.); English lists are words. East Asian motif vocabulary: architecture (pagoda, pavilion, temple, courtyard garden, curved eaves, ...), nature (Fuji, cherry blossom, bamboo, lotus, koi, crane, dragon), dress/art (hanfu, qipao, kimono, ink wash, calligraphy, lantern, zen, monk). Male/female = total gendered-term counts in the window. Clip = CLIP-77 clip fired (character rule for CJK).

## e2_qz (10000 records)

| steps | n | length median / p90 | in Chinese | clip | over limit | empty / refusal / cutoff | people | male : female | style | EA any | EA arch | EA nature | EA dress/art |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 46 / 63 | 1.000 | 0.000 | 0.040 | 0.000 / 0.000 / 0.000 | 0.59 | 26 : 31 | 0.50 | 0.010 | 0.000 | 0.010 | 0.000 |
| 1-5 | 500 | 43 / 58 | 1.000 | 0.010 | 0.018 | 0.000 / 0.000 / 0.000 | 0.54 | 56 : 137 | 0.59 | 0.062 | 0.020 | 0.022 | 0.028 |
| 6-10 | 500 | 42 / 56 | 1.000 | 0.004 | 0.010 | 0.000 / 0.000 / 0.000 | 0.44 | 9 : 122 | 0.63 | 0.070 | 0.024 | 0.022 | 0.042 |
| 11-25 | 1500 | 40 / 54 | 1.000 | 0.004 | 0.009 | 0.000 / 0.000 / 0.000 | 0.40 | 35 : 346 | 0.70 | 0.099 | 0.023 | 0.037 | 0.058 |
| 26-50 | 2500 | 40 / 54 | 1.000 | 0.007 | 0.011 | 0.000 / 0.000 / 0.000 | 0.34 | 27 : 441 | 0.72 | 0.085 | 0.027 | 0.018 | 0.048 |
| 51-75 | 2500 | 40 / 54 | 1.000 | 0.002 | 0.007 | 0.000 / 0.000 / 0.000 | 0.24 | 46 : 306 | 0.77 | 0.111 | 0.031 | 0.042 | 0.051 |
| 76-99 | 2400 | 40 / 54 | 1.000 | 0.005 | 0.012 | 0.000 / 0.000 / 0.000 | 0.22 | 31 : 260 | 0.79 | 0.167 | 0.062 | 0.075 | 0.056 |

Trajectories whose step-99 caption carries an East Asian motif term: 16 / 100; with one anywhere in steps 50-99: 55.

## e1_both (10000 records)

| steps | n | length median / p90 | in Chinese | clip | over limit | empty / refusal / cutoff | people | male : female | style | EA any | EA arch | EA nature | EA dress/art |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 40 / 51 | 0.000 | 0.000 | 0.120 | 0.000 / 0.000 / 0.000 | 0.67 | 32 : 44 | 0.70 | 0.000 | 0.000 | 0.000 | 0.000 |
| 1-5 | 500 | 37 / 49 | 0.004 | 0.030 | 0.086 | 0.000 / 0.000 / 0.000 | 0.64 | 59 : 117 | 0.87 | 0.036 | 0.012 | 0.014 | 0.016 |
| 6-10 | 500 | 34 / 47 | 0.002 | 0.016 | 0.060 | 0.000 / 0.000 / 0.000 | 0.63 | 34 : 84 | 0.96 | 0.036 | 0.014 | 0.022 | 0.008 |
| 11-25 | 1500 | 34 / 46 | 0.000 | 0.007 | 0.044 | 0.000 / 0.000 / 0.000 | 0.63 | 10 : 228 | 0.96 | 0.068 | 0.017 | 0.032 | 0.032 |
| 26-50 | 2500 | 35 / 46 | 0.001 | 0.015 | 0.044 | 0.000 / 0.000 / 0.000 | 0.61 | 6 : 353 | 0.98 | 0.052 | 0.018 | 0.031 | 0.006 |
| 51-75 | 2500 | 34 / 46 | 0.002 | 0.012 | 0.034 | 0.000 / 0.000 / 0.000 | 0.56 | 4 : 297 | 0.98 | 0.091 | 0.025 | 0.059 | 0.014 |
| 76-99 | 2400 | 34 / 46 | 0.001 | 0.011 | 0.039 | 0.000 / 0.000 / 0.000 | 0.53 | 22 : 318 | 0.98 | 0.115 | 0.027 | 0.090 | 0.004 |

Trajectories whose step-99 caption carries an East Asian motif term: 12 / 100; with one anywhere in steps 50-99: 32.
