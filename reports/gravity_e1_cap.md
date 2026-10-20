# Attractor gravity: e1_cap (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.90. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 8 | 602 | 102 | 94 | 0.156 | 6.4 | 3 | 0.0110 | 73 | 44 | 0.066 | 0.08 |
| 0 | gothic cathedral nave | 2 | 273 | 32 | 30 | 0.110 | 9.1 | 4 | 0.0033 | 24 | 36 | 0.029 | 0.02 |
| 2 | luxury canopy bedroom | 0 | 50 | 14 | 14 | 0.280 | 3.6 | 2 | 0.0014 | 8 | 9 | 0.005 | 0.00 |
| 6 | Victorian house with garden | 0 | 20 | 2 | 2 | 0.100 | 10.0 | 1 | 0.0002 | 0 | 19 | 0.002 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 90 | | | | | | | | | | 0.898 | 0.90 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 55 | 0.091 |
| [0.40, 0.60) | 161 | 0.087 |
| [0.60, 0.80) | 292 | 0.086 |
| [0.80, 1.00) | 307 | 0.208 |
| [1.00, 1.25) | 130 | 0.246 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 81 | 0.173 |
| 20-40 | 204 | 0.152 |
| 40-60 | 226 | 0.164 |
| 60-80 | 256 | 0.141 |
| 80-99 | 178 | 0.124 |
