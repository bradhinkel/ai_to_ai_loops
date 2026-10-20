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

## e1_cap  (10000 records; empty 0, refusals 0, length cutoffs 0, over 50 words 1072)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 41 | 0.0% |  | 49% | 0.85 | 12% | 67% | 32 : 32 | 0.0% |
| 1-5 | 500 | 37 | 4.2% | 64 -> 59 | 74% | 1.52 | 7% | 52% | 61 : 97 | 0.0% |
| 6-10 | 500 | 37 | 3.0% | 59 -> 55 | 84% | 1.93 | 6% | 46% | 30 : 90 | 0.0% |
| 11-25 | 1500 | 37 | 3.0% | 63 -> 56 | 86% | 2.10 | 7% | 34% | 54 : 298 | 0.0% |
| 26-50 | 2500 | 37 | 4.0% | 62 -> 57 | 85% | 2.08 | 5% | 27% | 15 : 257 | 0.0% |
| 51-75 | 2500 | 37 | 3.7% | 61 -> 56 | 89% | 2.23 | 4% | 20% | 6 : 61 | 0.0% |
| 76-99 | 2400 | 36 | 4.1% | 61 -> 57 | 87% | 2.21 | 3% | 14% | 0 : 39 | 0.0% |

## e1_gen  (10000 records; empty 0, refusals 0, length cutoffs 0, over 50 words 9902)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 107 | 0.0% |  | 59% | 1.11 | 48% | 79% | 161 : 114 | 0.0% |
| 1-5 | 500 | 114 | 97.0% | 115 -> 62 | 73% | 1.53 | 37% | 68% | 522 : 514 | 0.0% |
| 6-10 | 500 | 112 | 98.4% | 114 -> 62 | 80% | 1.85 | 34% | 60% | 272 : 277 | 0.0% |
| 11-25 | 1500 | 111 | 98.2% | 112 -> 62 | 82% | 1.92 | 28% | 51% | 664 : 556 | 0.0% |
| 26-50 | 2500 | 112 | 98.1% | 113 -> 62 | 86% | 2.25 | 30% | 45% | 493 : 644 | 0.0% |
| 51-75 | 2500 | 112 | 98.3% | 112 -> 62 | 86% | 2.16 | 26% | 41% | 340 : 539 | 0.0% |
| 76-99 | 2400 | 112 | 97.9% | 112 -> 62 | 87% | 2.11 | 24% | 42% | 440 : 541 | 0.0% |

## e1_both  (10000 records; empty 0, refusals 0, length cutoffs 0, over 50 words 439)

| steps | n | caption words (median) | clip fired | clip words before -> after | style share | style words / caption | photo share | people share | male : female words | mT5 truncated |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100 | 40 | 0.0% |  | 61% | 1.18 | 11% | 66% | 32 : 44 | 0.0% |
| 1-5 | 500 | 37 | 3.0% | 60 -> 57 | 82% | 1.93 | 8% | 64% | 58 : 117 | 0.0% |
| 6-10 | 500 | 34 | 1.6% | 55 -> 54 | 94% | 2.54 | 3% | 64% | 34 : 84 | 0.0% |
| 11-25 | 1500 | 34 | 0.7% | 40 -> 39 | 94% | 2.54 | 2% | 63% | 10 : 228 | 0.0% |
| 26-50 | 2500 | 35 | 1.5% | 60 -> 56 | 96% | 2.63 | 1% | 61% | 6 : 353 | 0.0% |
| 51-75 | 2500 | 34 | 1.2% | 32 -> 31 | 95% | 2.58 | 1% | 56% | 4 : 298 | 0.0% |
| 76-99 | 2400 | 34 | 1.1% | 59 -> 54 | 95% | 2.57 | 0% | 53% | 22 : 318 | 0.0% |
