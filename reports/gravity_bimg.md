# Attractor gravity: bimg (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 20 trajectories x 100 steps; free share of all steps 0.84. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | attractor 1 | 6 | 170 | 49 | 43 | 0.253 | 4.0 | 3 | 0.0271 | 40 | 10 | 0.096 | 0.30 |
| 0 | attractor 0 | 1 | 78 | 13 | 12 | 0.154 | 6.5 | 7 | 0.0068 | 9 | 16 | 0.042 | 0.05 |
| 6 | attractor 6 | 0 | 37 | 13 | 13 | 0.351 | 2.8 | 1 | 0.0067 | 9 | 10 | 0.019 | 0.00 |
| 2 | attractor 2 | 0 | 20 | 8 | 8 | 0.400 | 2.5 | 2 | 0.0041 | 5 | 7 | 0.010 | 0.00 |
| 3 | attractor 3 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | attractor 4 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | attractor 5 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | attractor 7 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 13 | | | | | | | | | | 0.832 | 0.65 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 19 | 0.053 |
| [0.40, 0.60) | 50 | 0.200 |
| [0.60, 0.80) | 91 | 0.198 |
| [0.80, 1.00) | 93 | 0.258 |
| [1.00, 1.25) | 52 | 0.442 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 22 | 0.136 |
| 20-40 | 39 | 0.256 |
| 40-60 | 70 | 0.243 |
| 60-80 | 79 | 0.278 |
| 80-99 | 95 | 0.253 |
