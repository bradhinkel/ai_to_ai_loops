# Attractor gravity: e1_cap_pilot

States: k-means k=10 on e1_cap_pilot step-99 DINOv2. Fixed radius 0.2 (DINOv2 cosine), exit at 1.25x radius (hysteresis). 20 trajectories x 100 steps; free share of all steps 0.81. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).

| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attractor 0 | 4 | 158 | 19 | 15 | 0.095 | 10.5 | 9 | 0.0104 | 15 | 33 | 0.094 | 0.20 |
| 1 | attractor 1 | 5 | 110 | 22 | 17 | 0.155 | 6.5 | 6 | 0.0118 | 16 | 17 | 0.067 | 0.25 |
| 8 | attractor 8 | 1 | 15 | 1 | 0 | 0.000 | - | - | 0.0005 | 0 | 0 | 0.022 | 0.05 |
| 3 | attractor 3 | 2 | 37 | 12 | 10 | 0.270 | 3.7 | 2 | 0.0062 | 10 | 13 | 0.021 | 0.10 |
| 5 | attractor 5 | 2 | 17 | 4 | 2 | 0.118 | 8.5 | 2 | 0.0020 | 2 | 2 | 0.015 | 0.10 |
| 6 | attractor 6 | 1 | 22 | 5 | 4 | 0.182 | 5.5 | 6 | 0.0026 | 2 | 8 | 0.013 | 0.05 |
| 9 | attractor 9 | 1 | 9 | 7 | 6 | 0.667 | 1.5 | 1 | 0.0036 | 5 | 3 | 0.005 | 0.05 |
| 7 | attractor 7 | 1 | 4 | 3 | 2 | 0.500 | 2.0 | 2 | 0.0015 | 2 | 2 | 0.003 | 0.05 |
| 4 | attractor 4 | 1 | 0 | 1 | 0 | - | - | - | 0.0005 | 0 | 0 | 0.001 | 0.05 |
| 2 | attractor 2 | 0 | 0 | 0 | 0 | - | - | - | 0.0000 | 0 | 0 | 0.000 | 0.00 |
| - | free | 2 | | | | | | | | | | 0.759 | 0.10 |

Exit rate by depth inside the basin (distance / radius, pooled over attractors):

| d/R | n steps | exit rate |
|---|---|---|
| [0.00, 0.40) | 7 | 0.286 |
| [0.40, 0.60) | 86 | 0.093 |
| [0.60, 0.80) | 124 | 0.081 |
| [0.80, 1.00) | 103 | 0.223 |
| [1.00, 1.25) | 52 | 0.250 |

Exit rate by step window (pooled; a stationary loop is flat):

| steps | n inside | exit rate |
|---|---|---|
| 0-20 | 14 | 0.286 |
| 20-40 | 45 | 0.244 |
| 40-60 | 68 | 0.118 |
| 60-80 | 92 | 0.152 |
| 80-99 | 153 | 0.124 |
