# Attractor gravity: e1_both (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 1.00. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | gothic cathedral nave | 0 | 4 | 2 | 2 | 0.500 | 2.0 | 1 | 0.0002 | 1 | 3 | 0.000 | 0.00 |
| 2 | luxury canopy bedroom | 1 | 2 | 2 | 1 | 0.500 | 2.0 | 2 | 0.0002 | 1 | 2 | 0.000 | 0.01 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 6 | Victorian house with garden | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 1 | gold-and-blue palatial salon | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 99 | | | | | | | | | | 0.999 | 0.99 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 0 | - |
| [0.60, 0.80) | 0 | - |
| [0.80, 1.00) | 3 | 0.333 |
| [1.00, 1.25) | 3 | 0.667 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 0 | - |
| 20-40 | 0 | - |
| 40-60 | 0 | - |
| 60-80 | 0 | - |
| 80-99 | 6 | 0.500 |
