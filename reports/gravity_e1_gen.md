# Attractor gravity: e1_gen

States: archive/a0_core_centroids.npz. Fixed radius 0.2 (DINOv2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.99. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | gothic cathedral nave | 3 | 71 | 51 | 48 | 0.676 | 1.5 | 1 | 0.0052 | 36 | 4 | 0.008 | 0.03 |
| 2 | luxury canopy bedroom | 1 | 54 | 13 | 12 | 0.222 | 4.5 | 2 | 0.0013 | 12 | 11 | 0.006 | 0.01 |
| 1 | gold-and-blue palatial salon | 0 | 10 | 7 | 7 | 0.700 | 1.4 | 1 | 0.0007 | 4 | 2 | 0.001 | 0.00 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 6 | Victorian house with garden | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 96 | | | | | | | | | | 0.985 | 0.96 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 6 | 0.333 |
| [0.60, 0.80) | 28 | 0.464 |
| [0.80, 1.00) | 61 | 0.557 |
| [1.00, 1.25) | 40 | 0.450 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 11 | 0.455 |
| 20-40 | 29 | 0.552 |
| 40-60 | 18 | 0.722 |
| 60-80 | 28 | 0.429 |
| 80-99 | 49 | 0.429 |
