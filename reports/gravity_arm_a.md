# Attractor gravity: arm_a (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 20 trajectories x 100 steps; free share of all steps 0.73. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attractor 0 | 5 | 342 | 12 | 7 | 0.020 | 48.9 | 43 | 0.0073 | 7 | 78 | 0.257 | 0.25 |
| 1 | attractor 1 | 2 | 152 | 15 | 13 | 0.086 | 11.7 | 10 | 0.0082 | 11 | 52 | 0.080 | 0.10 |
| 2 | attractor 2 | 1 | 37 | 8 | 7 | 0.189 | 5.3 | 3 | 0.0041 | 6 | 10 | 0.020 | 0.05 |
| 6 | attractor 6 | 1 | 7 | 6 | 5 | 0.714 | 1.4 | 1 | 0.0030 | 4 | 2 | 0.004 | 0.05 |
| 5 | attractor 5 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | attractor 7 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | attractor 4 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 3 | attractor 3 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 11 | | | | | | | | | | 0.639 | 0.55 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 156 | 0.019 |
| [0.40, 0.60) | 155 | 0.032 |
| [0.60, 0.80) | 108 | 0.083 |
| [0.80, 1.00) | 78 | 0.115 |
| [1.00, 1.25) | 41 | 0.146 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 24 | 0.083 |
| 20-40 | 96 | 0.052 |
| 40-60 | 129 | 0.023 |
| 60-80 | 132 | 0.076 |
| 80-99 | 157 | 0.076 |
