# Attractor gravity: e1_both (dinov2)

States: k-means k=8 on e1_both step-99 dinov2. Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.89. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | attractor 4 | 8 | 639 | 69 | 62 | 0.097 | 10.3 | 5 | 0.0075 | 50 | 42 | 0.071 | 0.08 |
| 2 | attractor 2 | 5 | 144 | 39 | 34 | 0.236 | 4.2 | 3 | 0.0040 | 28 | 16 | 0.016 | 0.05 |
| 1 | attractor 1 | 2 | 106 | 25 | 23 | 0.217 | 4.6 | 2 | 0.0026 | 15 | 36 | 0.012 | 0.02 |
| 5 | attractor 5 | 2 | 92 | 24 | 22 | 0.239 | 4.2 | 4 | 0.0024 | 16 | 12 | 0.010 | 0.02 |
| 3 | attractor 3 | 2 | 45 | 18 | 16 | 0.356 | 2.8 | 3 | 0.0018 | 9 | 7 | 0.005 | 0.02 |
| 0 | attractor 0 | 2 | 12 | 6 | 4 | 0.333 | 3.0 | 2 | 0.0006 | 4 | 6 | 0.002 | 0.02 |
| 6 | attractor 6 | 1 | 5 | 5 | 4 | 0.800 | 1.2 | 1 | 0.0005 | 2 | 2 | 0.001 | 0.01 |
| 7 | attractor 7 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 78 | | | | | | | | | | 0.883 | 0.78 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 35 | 0.086 |
| [0.60, 0.80) | 274 | 0.055 |
| [0.80, 1.00) | 497 | 0.159 |
| [1.00, 1.25) | 237 | 0.287 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 27 | 0.333 |
| 20-40 | 170 | 0.141 |
| 40-60 | 243 | 0.189 |
| 60-80 | 287 | 0.136 |
| 80-99 | 316 | 0.149 |
