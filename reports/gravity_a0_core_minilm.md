# Attractor gravity: a0_core (minilm)

States: archive/a0_core_centroids.npz (minilm). Fixed radius 0.15 (minilm cosine), exit at 1.25x radius (hysteresis). 100 trajectories x 100 steps; free share of all steps 0.63. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gold-and-blue palatial salon | 34 | 2354 | 76 | 42 | 0.018 | 56.0 | 44 | 0.0101 | 36 | 75 | 0.346 | 0.34 |
| 0 | gothic cathedral nave | 11 | 585 | 27 | 16 | 0.027 | 36.6 | 25 | 0.0029 | 15 | 44 | 0.077 | 0.11 |
| 2 | luxury canopy bedroom | 9 | 381 | 26 | 17 | 0.045 | 22.4 | 14 | 0.0027 | 9 | 25 | 0.052 | 0.09 |
| 6 | Victorian house with garden | 4 | 168 | 34 | 30 | 0.179 | 5.6 | 5 | 0.0035 | 25 | 13 | 0.015 | 0.04 |
| 3 | old-town street / village (loose) | 4 | 175 | 55 | 51 | 0.291 | 3.4 | 3 | 0.0057 | 39 | 11 | 0.015 | 0.04 |
| 5 | castle on water | 1 | 9 | 4 | 3 | 0.333 | 3.0 | 1 | 0.0004 | 2 | 7 | 0.001 | 0.01 |
| 7 | people and art (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| 4 | catch-all landscapes (loose) | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 37 | | | | | | | | | | 0.494 | 0.37 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 181 | 0.011 |
| [0.40, 0.60) | 1265 | 0.012 |
| [0.60, 0.80) | 1184 | 0.023 |
| [0.80, 1.00) | 702 | 0.095 |
| [1.00, 1.25) | 340 | 0.141 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 232 | 0.060 |
| 20-40 | 622 | 0.043 |
| 40-60 | 838 | 0.042 |
| 60-80 | 933 | 0.041 |
| 80-99 | 1047 | 0.043 |
