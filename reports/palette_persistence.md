# Palette persistence vs subject change

Palette class from pixels only; subject jump = DINOv2 step distance > 0.35. Dwell = >= 5 consecutive steps in one palette class. 'kept' = same class as the previous step. Strips: `reports/palette_persistence/<run>_<class>.jpg` (longest dwells that contain a subject jump; yellow = step, red bar under a step = subject jump).

## a0_core

P(palette kept | subject jump) = **0.52**, P(kept | no jump) = 0.60, chance = 0.30. Share of steps inside a palette dwell of >= 5: 40%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 8% | 258 | 0.57 | 39 | 25 | 23 |
| tinted-mono | 26% | 689 | 0.51 | 99 | 60 | 17 |
| rainbow | 1% | 23 | 0.13 | 1 | 1 | 6 |
| vivid | 42% | 729 | 0.66 | 263 | 149 | 49 |
| high-contrast | 0% | 0 | - | 0 | 0 | 0 |
| neutral | 23% | 485 | 0.33 | 44 | 26 | 13 |

## a0_core2

P(palette kept | subject jump) = **0.55**, P(kept | no jump) = 0.60, chance = 0.30. Share of steps inside a palette dwell of >= 5: 42%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 9% | 286 | 0.56 | 39 | 33 | 24 |
| tinted-mono | 27% | 666 | 0.52 | 109 | 69 | 25 |
| rainbow | 1% | 13 | 0.15 | 0 | 0 | 0 |
| vivid | 42% | 719 | 0.71 | 282 | 151 | 39 |
| high-contrast | 0% | 1 | 0.00 | 0 | 0 | 0 |
| neutral | 21% | 429 | 0.33 | 39 | 19 | 12 |

## a0_photo

P(palette kept | subject jump) = **0.61**, P(kept | no jump) = 0.64, chance = 0.29. Share of steps inside a palette dwell of >= 5: 48%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 10% | 275 | 0.55 | 48 | 34 | 17 |
| tinted-mono | 34% | 719 | 0.64 | 180 | 105 | 26 |
| rainbow | 1% | 14 | 0.07 | 0 | 0 | 0 |
| vivid | 36% | 579 | 0.76 | 212 | 127 | 79 |
| high-contrast | 0% | 3 | 0.00 | 0 | 0 | 0 |
| neutral | 18% | 325 | 0.37 | 42 | 19 | 10 |

## e1_cap

P(palette kept | subject jump) = **0.65**, P(kept | no jump) = 0.70, chance = 0.35. Share of steps inside a palette dwell of >= 5: 58%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 8% | 91 | 0.68 | 42 | 18 | 43 |
| tinted-mono | 25% | 347 | 0.54 | 134 | 47 | 29 |
| rainbow | 1% | 10 | 0.20 | 0 | 0 | 0 |
| vivid | 50% | 703 | 0.80 | 295 | 162 | 99 |
| high-contrast | 0% | 1 | 0.00 | 0 | 0 | 0 |
| neutral | 16% | 230 | 0.34 | 28 | 14 | 10 |

## e1_gen

P(palette kept | subject jump) = **0.60**, P(kept | no jump) = 0.63, chance = 0.45. Share of steps inside a palette dwell of >= 5: 51%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 4% | 92 | 0.49 | 12 | 8 | 14 |
| tinted-mono | 11% | 242 | 0.33 | 20 | 6 | 8 |
| rainbow | 7% | 174 | 0.21 | 3 | 1 | 6 |
| vivid | 65% | 1460 | 0.79 | 415 | 290 | 72 |
| high-contrast | 5% | 122 | 0.18 | 3 | 2 | 7 |
| neutral | 9% | 179 | 0.20 | 7 | 3 | 7 |

## e1_both

P(palette kept | subject jump) = **0.78**, P(kept | no jump) = 0.81, chance = 0.71. Share of steps inside a palette dwell of >= 5: 76%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 0% | 5 | 0.20 | 0 | 0 | 0 |
| tinted-mono | 5% | 56 | 0.29 | 10 | 3 | 10 |
| rainbow | 4% | 50 | 0.18 | 3 | 0 | 10 |
| vivid | 84% | 988 | 0.89 | 403 | 241 | 98 |
| high-contrast | 2% | 22 | 0.23 | 1 | 0 | 5 |
| neutral | 5% | 66 | 0.18 | 4 | 0 | 7 |

## a0_s

P(palette kept | subject jump) = **0.72**, P(kept | no jump) = 0.75, chance = 0.36. Share of steps inside a palette dwell of >= 5: 64%.

| class | share of steps | subject jumps from it | palette kept across the jump | dwells >= 5 | dwells containing a jump | longest dwell |
|---|---|---|---|---|---|---|
| grayscale | 6% | 72 | 0.89 | 24 | 16 | 89 |
| tinted-mono | 22% | 228 | 0.63 | 118 | 40 | 71 |
| rainbow | 0% | 1 | 0.00 | 1 | 0 | 10 |
| vivid | 52% | 359 | 0.87 | 241 | 101 | 98 |
| high-contrast | 0% | 1 | 0.00 | 0 | 0 | 0 |
| neutral | 19% | 134 | 0.36 | 54 | 8 | 16 |

