# Attractor gravity: e1_cap (dinov2)

States: k-means k=8 on e1_cap step-99 dinov2. Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.74. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | attractor 5 | 8 | 640 | 109 | 101 | 0.158 | 6.3 | 4 | 0.0118 | 80 | 28 | 0.066 | 0.08 |
| 2 | attractor 2 | 12 | 471 | 40 | 28 | 0.059 | 16.8 | 9 | 0.0042 | 22 | 41 | 0.064 | 0.12 |
| 4 | attractor 4 | 9 | 392 | 23 | 14 | 0.036 | 28.0 | 22 | 0.0024 | 14 | 39 | 0.060 | 0.09 |
| 3 | attractor 3 | 8 | 396 | 30 | 22 | 0.056 | 18.0 | 15 | 0.0032 | 21 | 39 | 0.051 | 0.08 |
| 7 | attractor 7 | 9 | 338 | 84 | 75 | 0.222 | 4.5 | 2 | 0.0088 | 63 | 13 | 0.036 | 0.09 |
| 0 | attractor 0 | 5 | 287 | 70 | 65 | 0.226 | 4.4 | 2 | 0.0073 | 55 | 22 | 0.029 | 0.05 |
| 1 | attractor 1 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 6 | attractor 6 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 49 | | | | | | | | | | 0.695 | 0.49 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 372 | 0.016 |
| [0.40, 0.60) | 668 | 0.024 |
| [0.60, 0.80) | 633 | 0.112 |
| [0.80, 1.00) | 554 | 0.240 |
| [1.00, 1.25) | 297 | 0.266 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 113 | 0.195 |
| 20-40 | 390 | 0.159 |
| 40-60 | 527 | 0.146 |
| 60-80 | 730 | 0.104 |
| 80-99 | 764 | 0.089 |
