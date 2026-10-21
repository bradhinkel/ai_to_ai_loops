# Attractor gravity: a0_s (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.89. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | gothic cathedral nave | 10 | 720 | 93 | 83 | 0.115 | 8.7 | 6 | 0.0101 | 75 | 33 | 0.081 | 0.10 |
| 1 | gold-and-blue palatial salon | 4 | 355 | 73 | 69 | 0.194 | 5.1 | 3 | 0.0076 | 55 | 22 | 0.038 | 0.04 |
| 2 | luxury canopy bedroom | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 6 | Victorian house with garden | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 86 | | | | | | | | | | 0.881 | 0.86 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 113 | 0.027 |
| [0.40, 0.60) | 243 | 0.037 |
| [0.60, 0.80) | 287 | 0.146 |
| [0.80, 1.00) | 296 | 0.203 |
| [1.00, 1.25) | 136 | 0.279 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 61 | 0.148 |
| 20-40 | 161 | 0.137 |
| 40-60 | 274 | 0.131 |
| 60-80 | 313 | 0.160 |
| 80-99 | 266 | 0.132 |
