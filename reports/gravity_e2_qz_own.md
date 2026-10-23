# Attractor gravity: e2_qz (dinov2)

States: k-means k=12 on e2_qz step-99 dinov2. Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.88. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | attractor 2 | 8 | 248 | 57 | 49 | 0.198 | 5.1 | 3 | 0.0059 | 42 | 20 | 0.029 | 0.08 |
| 11 | attractor 11 | 3 | 264 | 66 | 63 | 0.239 | 4.2 | 3 | 0.0068 | 47 | 25 | 0.028 | 0.03 |
| 1 | attractor 1 | 3 | 191 | 44 | 41 | 0.215 | 4.7 | 3 | 0.0045 | 35 | 34 | 0.020 | 0.03 |
| 5 | attractor 5 | 5 | 171 | 43 | 38 | 0.222 | 4.5 | 3 | 0.0044 | 28 | 20 | 0.020 | 0.05 |
| 4 | attractor 4 | 4 | 125 | 53 | 49 | 0.392 | 2.6 | 2 | 0.0054 | 32 | 10 | 0.014 | 0.04 |
| 6 | attractor 6 | 5 | 94 | 34 | 29 | 0.309 | 3.2 | 3 | 0.0035 | 19 | 8 | 0.011 | 0.05 |
| 8 | attractor 8 | 2 | 88 | 21 | 19 | 0.216 | 4.6 | 3 | 0.0021 | 16 | 18 | 0.010 | 0.02 |
| 0 | attractor 0 | 2 | 8 | 6 | 4 | 0.500 | 2.0 | 2 | 0.0006 | 2 | 4 | 0.001 | 0.02 |
| 7 | attractor 7 | 0 | 4 | 4 | 4 | 1.000 | 1.0 | 1 | 0.0004 | 0 | 1 | 0.000 | 0.00 |
| 10 | attractor 10 | 1 | 1 | 2 | 1 | 1.000 | 1.0 | 1 | 0.0002 | 0 | 1 | 0.000 | 0.01 |
| 3 | attractor 3 | 1 | 0 | 1 | 0 | - | - | - | 0.0001 | 0 | 0 | 0.000 | 0.01 |
| 9 | attractor 9 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 66 | | | | | | | | | | 0.867 | 0.66 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 33 | 0.091 |
| [0.60, 0.80) | 204 | 0.172 |
| [0.80, 1.00) | 568 | 0.252 |
| [1.00, 1.25) | 389 | 0.298 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 67 | 0.239 |
| 20-40 | 209 | 0.215 |
| 40-60 | 257 | 0.280 |
| 60-80 | 290 | 0.303 |
| 80-99 | 371 | 0.205 |
