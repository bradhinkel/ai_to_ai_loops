# Caption audit

Counted from the step records only. Word lists are fixed in `analysis/caption_audit.py` (style = Hintze's 'vivid, artistic' register; photo = photographic / everyday-scene vocabulary; people = any person word incl. pronouns). Shares are the fraction of captions in the step window containing at least one list word; clip columns are median words of the clipped prompts before and after the CLIP-77 cut.

## a0_core  (10000 records; empty 0, refusals 0, length cutoffs 1, over 50 words 9969)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 116 | 0.0% |  | 53% | 0.83 | 46% | 73% | 101 : 87 | 0.0% |
| 1-5 | 500 | 121 | 97.0% |  | 67% | 1.37 | 46% | 69% | 514 : 283 | 0.0% |
| 6-10 | 500 | 117 | 99.0% |  | 75% | 1.60 | 42% | 55% | 359 : 189 | 0.0% |
| 11-25 | 1500 | 124 | 98.9% |  | 82% | 1.98 | 43% | 48% | 791 : 521 | 0.0% |
| 26-50 | 2500 | 126 | 99.4% |  | 86% | 2.24 | 44% | 36% | 803 : 417 | 0.0% |
| 51-75 | 2500 | 130 | 99.5% |  | 85% | 2.20 | 46% | 25% | 556 : 254 | 0.0% |
| 76-99 | 2400 | 131 | 99.6% |  | 87% | 2.39 | 46% | 22% | 298 : 183 | 0.0% |

## a0_core2  (10000 records; empty 0, refusals 0, length cutoffs 0, over 50 words 9955)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 115 | 0.0% |  | 65% | 1.08 | 44% | 78% | 100 : 69 | 0.0% |
| 1-5 | 500 | 118 | 98.6% |  | 66% | 1.30 | 47% | 67% | 522 : 267 | 0.0% |
| 6-10 | 500 | 119 | 99.2% |  | 73% | 1.61 | 40% | 57% | 393 : 236 | 0.0% |
| 11-25 | 1500 | 122 | 98.9% |  | 80% | 1.95 | 43% | 43% | 643 : 425 | 0.0% |
| 26-50 | 2500 | 125 | 98.9% |  | 82% | 2.03 | 43% | 38% | 764 : 598 | 0.0% |
| 51-75 | 2500 | 129 | 99.2% |  | 85% | 2.20 | 44% | 32% | 479 : 273 | 0.0% |
| 76-99 | 2400 | 131 | 99.5% |  | 87% | 2.32 | 45% | 24% | 292 : 114 | 0.0% |

## bimg  (2000 records; empty 0, refusals 0, length cutoffs 0, over 50 words 1992)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 103 | 0.0% |  | 40% | 1.05 | 35% | 80% | 25 : 2 | 0.0% |
| 1-5 | 100 | 116 | 98.0% |  | 70% | 1.51 | 49% | 66% | 113 : 16 | 0.0% |
| 6-10 | 100 | 125 | 97.0% |  | 86% | 1.94 | 37% | 40% | 65 : 0 | 0.0% |
| 11-25 | 300 | 125 | 98.0% |  | 76% | 1.67 | 39% | 32% | 172 : 2 | 0.0% |
| 26-50 | 500 | 126 | 99.8% |  | 90% | 2.25 | 36% | 27% | 78 : 43 | 0.0% |
| 51-75 | 500 | 132 | 99.4% |  | 85% | 2.28 | 41% | 20% | 34 : 28 | 0.0% |
| 76-99 | 480 | 128 | 99.8% |  | 90% | 2.58 | 37% | 15% | 18 : 3 | 0.0% |

## arm_a  (2000 records; empty 0, refusals 0, length cutoffs 0, over 50 words 1992)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 116 | 0.0% |  | 70% | 1.75 | 50% | 75% | 27 : 2 | 0.0% |
| 1-5 | 100 | 112 | 100.0% |  | 65% | 1.14 | 40% | 56% | 95 : 6 | 0.0% |
| 6-10 | 100 | 112 | 99.0% |  | 76% | 1.48 | 46% | 46% | 66 : 0 | 0.0% |
| 11-25 | 300 | 118 | 99.7% |  | 82% | 1.77 | 43% | 26% | 57 : 0 | 0.0% |
| 26-50 | 500 | 122 | 98.4% |  | 85% | 1.91 | 40% | 19% | 74 : 0 | 0.0% |
| 51-75 | 500 | 120 | 99.2% |  | 86% | 2.12 | 39% | 24% | 91 : 13 | 0.0% |
| 76-99 | 480 | 119 | 99.6% |  | 82% | 1.92 | 36% | 23% | 83 : 2 | 0.0% |
