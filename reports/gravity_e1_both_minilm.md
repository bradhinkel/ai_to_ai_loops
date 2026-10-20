# Attractor gravity: e1_both (minilm)

States: k-means k=7 on e1_both step-99 minilm. Fixed radius 0.15 (minilm cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.92. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | attractor 4 | 6 | 416 | 158 | 152 | 0.365 | 2.7 | 1 | 0.0167 | 119 | 28 | 0.043 | 0.06 |
| 2 | attractor 2 | 5 | 198 | 60 | 56 | 0.283 | 3.5 | 3 | 0.0062 | 47 | 13 | 0.021 | 0.05 |
| 5 | attractor 5 | 7 | 158 | 33 | 26 | 0.165 | 6.1 | 4 | 0.0034 | 22 | 16 | 0.020 | 0.07 |
| 1 | attractor 1 | 1 | 19 | 14 | 13 | 0.684 | 1.5 | 1 | 0.0014 | 5 | 3 | 0.002 | 0.01 |
| 3 | attractor 3 | 2 | 13 | 12 | 10 | 0.769 | 1.3 | 1 | 0.0012 | 3 | 3 | 0.002 | 0.02 |
| 6 | attractor 6 | 0 | 9 | 5 | 5 | 0.556 | 1.8 | 2 | 0.0005 | 1 | 3 | 0.001 | 0.00 |
| 0 | attractor 0 | 0 | 3 | 3 | 3 | 1.000 | 1.0 | 1 | 0.0003 | 0 | 1 | 0.000 | 0.00 |
| - | free | 79 | | | | | | | | | | 0.910 | 0.79 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 43 | 0.116 |
| [0.60, 0.80) | 180 | 0.222 |
| [0.80, 1.00) | 402 | 0.368 |
| [1.00, 1.25) | 191 | 0.377 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 21 | 0.476 |
| 20-40 | 93 | 0.430 |
| 40-60 | 174 | 0.328 |
| 60-80 | 259 | 0.313 |
| 80-99 | 269 | 0.286 |
