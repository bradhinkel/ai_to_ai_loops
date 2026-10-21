# SigLIP radius calibration on a0_core (D17)

DINOv2 gravity radius 0.2; 100 trajectories, 9900 consecutive-step pairs, 9500 5-step windows ending at step >= 5.

| matching | share under DINOv2 0.20 | SigLIP radius with the same share | Spearman (DINOv2 vs SigLIP distance) |
|---|---|---|---|
| consecutive pairs | 0.372 | 0.0823 | 0.535 |
| 5-step windows (archive condition) | 0.592 | 0.0777 | 0.600 |

Persistence decisions (window max distance <= radius) agree in 73.5% of windows: both 4359, DINOv2 only 1261, SigLIP only 1261.

SigLIP consecutive-pair distance quantiles: q10 0.054, q25 0.070, q50 0.096, q75 0.134, q90 0.179
DINOv2 consecutive-pair distance quantiles: q10 0.115, q25 0.165, q50 0.237, q75 0.333, q90 0.448

Decision: radius_archive = radius_reject = 0.078 (window matching), rounded in the config and recorded in DEVIATIONS D17.
