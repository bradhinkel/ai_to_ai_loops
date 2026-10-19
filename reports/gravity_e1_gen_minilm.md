# Attractor gravity: e1_gen (minilm)

States: k-means k=11 on e1_gen step-99 minilm. Fixed radius 0.15 (minilm cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.87. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attractor 0 | 13 | 647 | 56 | 43 | 0.066 | 15.0 | 10 | 0.0061 | 38 | 52 | 0.083 | 0.13 |
| 10 | attractor 10 | 4 | 190 | 19 | 15 | 0.079 | 12.7 | 11 | 0.0020 | 11 | 30 | 0.024 | 0.04 |
| 9 | attractor 9 | 3 | 123 | 20 | 17 | 0.138 | 7.2 | 7 | 0.0020 | 17 | 14 | 0.014 | 0.03 |
| 4 | attractor 4 | 4 | 98 | 36 | 33 | 0.337 | 3.0 | 2 | 0.0037 | 31 | 11 | 0.011 | 0.04 |
| 7 | attractor 7 | 4 | 87 | 27 | 24 | 0.276 | 3.6 | 2 | 0.0028 | 24 | 15 | 0.010 | 0.04 |
| 2 | attractor 2 | 0 | 46 | 11 | 11 | 0.239 | 4.2 | 2 | 0.0011 | 5 | 18 | 0.005 | 0.00 |
| 3 | attractor 3 | 2 | 26 | 22 | 20 | 0.769 | 1.3 | 1 | 0.0022 | 12 | 4 | 0.003 | 0.02 |
| 8 | attractor 8 | 0 | 25 | 12 | 12 | 0.480 | 2.1 | 1 | 0.0012 | 8 | 7 | 0.002 | 0.00 |
| 5 | attractor 5 | 2 | 12 | 11 | 9 | 0.750 | 1.3 | 1 | 0.0011 | 2 | 2 | 0.002 | 0.02 |
| 6 | attractor 6 | 2 | 0 | 2 | 0 | - | - | - | 0.0002 | 0 | 0 | 0.000 | 0.02 |
| 1 | attractor 1 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 66 | | | | | | | | | | 0.847 | 0.66 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 63 | 0.032 |
| [0.40, 0.60) | 338 | 0.036 |
| [0.60, 0.80) | 284 | 0.081 |
| [0.80, 1.00) | 369 | 0.249 |
| [1.00, 1.25) | 200 | 0.275 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 67 | 0.284 |
| 20-40 | 205 | 0.171 |
| 40-60 | 281 | 0.135 |
| 60-80 | 316 | 0.158 |
| 80-99 | 385 | 0.109 |
