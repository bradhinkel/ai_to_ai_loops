# Attractor gravity: e1_cap (minilm)

States: k-means k=6 on e1_cap step-99 minilm. Fixed radius 0.15 (minilm cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.81. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attractor 0 | 17 | 871 | 212 | 195 | 0.224 | 4.5 | 2 | 0.0235 | 177 | 23 | 0.093 | 0.17 |
| 3 | attractor 3 | 8 | 353 | 40 | 32 | 0.091 | 11.0 | 9 | 0.0042 | 31 | 46 | 0.043 | 0.08 |
| 5 | attractor 5 | 9 | 325 | 66 | 57 | 0.175 | 5.7 | 4 | 0.0069 | 56 | 18 | 0.037 | 0.09 |
| 4 | attractor 4 | 9 | 231 | 73 | 64 | 0.277 | 3.6 | 2 | 0.0075 | 59 | 25 | 0.026 | 0.09 |
| 1 | attractor 1 | 3 | 116 | 56 | 53 | 0.457 | 2.2 | 2 | 0.0057 | 44 | 7 | 0.012 | 0.03 |
| 2 | attractor 2 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 54 | | | | | | | | | | 0.788 | 0.54 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 3 | 0.000 |
| [0.40, 0.60) | 155 | 0.090 |
| [0.60, 0.80) | 510 | 0.118 |
| [0.80, 1.00) | 785 | 0.251 |
| [1.00, 1.25) | 443 | 0.293 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 96 | 0.271 |
| 20-40 | 243 | 0.300 |
| 40-60 | 371 | 0.270 |
| 60-80 | 561 | 0.182 |
| 80-99 | 625 | 0.160 |
