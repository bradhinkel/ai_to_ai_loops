# Attractor gravity: a0_photo (dinov2)

States: archive/a0_core_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.85. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 10 | 871 | 200 | 190 | 0.218 | 4.6 | 4 | 0.0222 | 173 | 16 | 0.090 | 0.10 |
| 0 | gothic cathedral nave | 12 | 580 | 35 | 23 | 0.040 | 25.2 | 24 | 0.0038 | 23 | 48 | 0.086 | 0.12 |
| 6 | Victorian house with garden | 0 | 7 | 2 | 2 | 0.286 | 3.5 | 2 | 0.0002 | 0 | 5 | 0.001 | 0.00 |
| 2 | luxury canopy bedroom | 0 | 5 | 2 | 2 | 0.400 | 2.5 | 2 | 0.0002 | 1 | 3 | 0.001 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 78 | | | | | | | | | | 0.823 | 0.78 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 230 | 0.026 |
| [0.40, 0.60) | 344 | 0.105 |
| [0.60, 0.80) | 372 | 0.137 |
| [0.80, 1.00) | 322 | 0.224 |
| [1.00, 1.25) | 195 | 0.267 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 64 | 0.219 |
| 20-40 | 252 | 0.123 |
| 40-60 | 350 | 0.169 |
| 60-80 | 374 | 0.142 |
| 80-99 | 423 | 0.142 |
