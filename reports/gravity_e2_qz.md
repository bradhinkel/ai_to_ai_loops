# Attractor gravity: e2_qz (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 1.00. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | attractor 1 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 3 | attractor 3 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | attractor 4 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | attractor 5 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 6 | attractor 6 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | attractor 7 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 2 | attractor 2 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 0 | attractor 0 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 100 | | | | | | | | | | 1.000 | 1.00 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 0 | - |
| [0.60, 0.80) | 0 | - |
| [0.80, 1.00) | 0 | - |
| [1.00, 1.25) | 0 | - |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 0 | - |
| 20-40 | 0 | - |
| 40-60 | 0 | - |
| 60-80 | 0 | - |
| 80-99 | 0 | - |
