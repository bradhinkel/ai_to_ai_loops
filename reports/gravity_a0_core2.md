# Attractor gravity: a0_core2 (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.73. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 26 | 1827 | 226 | 200 | 0.109 | 9.1 | 6 | 0.0280 | 186 | 47 | 0.197 | 0.26 |
| 0 | gothic cathedral nave | 8 | 538 | 20 | 12 | 0.022 | 44.8 | 29 | 0.0021 | 10 | 86 | 0.084 | 0.08 |
| 2 | luxury canopy bedroom | 5 | 205 | 46 | 41 | 0.200 | 5.0 | 3 | 0.0047 | 32 | 14 | 0.022 | 0.05 |
| 6 | Victorian house with garden | 2 | 39 | 12 | 10 | 0.256 | 3.9 | 3 | 0.0012 | 9 | 10 | 0.004 | 0.02 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 59 | | | | | | | | | | 0.692 | 0.59 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 284 | 0.014 |
| [0.40, 0.60) | 695 | 0.063 |
| [0.60, 0.80) | 772 | 0.095 |
| [0.80, 1.00) | 579 | 0.154 |
| [1.00, 1.25) | 279 | 0.190 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 149 | 0.081 |
| 20-40 | 359 | 0.109 |
| 40-60 | 591 | 0.081 |
| 60-80 | 711 | 0.120 |
| 80-99 | 799 | 0.099 |
