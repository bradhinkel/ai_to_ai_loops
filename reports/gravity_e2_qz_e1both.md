# Attractor gravity: e2_qz (dinov2)

States: archive/e1_both_centroids.npz (dinov2). Fixed radius 0.2 (dinov2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.96. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | attractor 4 | 2 | 357 | 71 | 70 | 0.196 | 5.1 | 3 | 0.0074 | 51 | 22 | 0.037 | 0.02 |
| 5 | attractor 5 | 0 | 38 | 15 | 15 | 0.395 | 2.5 | 1 | 0.0015 | 6 | 9 | 0.004 | 0.00 |
| 2 | attractor 2 | 1 | 32 | 9 | 8 | 0.250 | 4.0 | 2 | 0.0009 | 4 | 18 | 0.004 | 0.01 |
| 3 | attractor 3 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 6 | attractor 6 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | attractor 7 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 1 | attractor 1 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 0 | attractor 0 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 97 | | | | | | | | | | 0.956 | 0.97 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 0 | - |
| [0.40, 0.60) | 6 | 0.000 |
| [0.60, 0.80) | 104 | 0.125 |
| [0.80, 1.00) | 200 | 0.225 |
| [1.00, 1.25) | 117 | 0.299 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 36 | 0.167 |
| 20-40 | 63 | 0.270 |
| 40-60 | 160 | 0.181 |
| 60-80 | 91 | 0.264 |
| 80-99 | 77 | 0.221 |
