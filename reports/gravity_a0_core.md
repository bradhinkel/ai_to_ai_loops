# Attractor gravity: a0_core

States: archive/a0_core_centroids.npz. Fixed radius 0.2 (DINOv2 cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.71. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 28 | 1761 | 226 | 198 | 0.112 | 8.9 | 6 | 0.0278 | 185 | 46 | 0.192 | 0.28 |
| 0 | gothic cathedral nave | 11 | 574 | 30 | 19 | 0.033 | 30.2 | 23 | 0.0032 | 19 | 43 | 0.085 | 0.11 |
| 2 | luxury canopy bedroom | 8 | 364 | 70 | 62 | 0.170 | 5.9 | 4 | 0.0073 | 51 | 43 | 0.040 | 0.08 |
| 6 | Victorian house with garden | 5 | 158 | 36 | 31 | 0.196 | 5.1 | 4 | 0.0037 | 27 | 13 | 0.017 | 0.05 |
| 5 | castle on water | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 3 | old-town street / village (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 48 | | | | | | | | | | 0.666 | 0.48 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 301 | 0.017 |
| [0.40, 0.60) | 688 | 0.073 |
| [0.60, 0.80) | 894 | 0.087 |
| [0.80, 1.00) | 649 | 0.173 |
| [1.00, 1.25) | 325 | 0.200 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 142 | 0.134 |
| 20-40 | 499 | 0.098 |
| 40-60 | 647 | 0.117 |
| 60-80 | 740 | 0.103 |
| 80-99 | 829 | 0.109 |
