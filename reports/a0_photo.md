# A0-photo report — SDXL + LLaVA with the photographic caption instruction (SPEC2 §3), 2026-10-20/21

A0-core with one change: the first sentence of the caption instruction, "Describe this image in vivid, artistic terms." → "Describe this image as a realistic photograph, in plain, precise terms." Everything else verbatim (same 100 Hintze seeds, same step-0 images, T = 0.9, 100 × 100 steps, pod config `configs/a0_photo_runpod96.yaml`, code a46934e). This is the baseline for E6. Predictions were recorded in `predictions.md` on 2026-10-20 before the run.

**Outcome: complete, no data loss, no restarts.** Convergence is the same as A0-core (plateau 11–15, knee 8); the attractor *set* is broader and more mundane (Vendi 43.9 vs 31.8; half the endpoints outside A0-core's radii); the gold-and-blue salon basin halves, the cathedral is untouched, and three new persistent attractors appear that no other cell has: a fitted kitchen, a supermarket produce aisle, and sepia "vintage photograph" portraits of Native Americans in headdress. Caption register moves toward photography but LLaVA's "vivid/ethereal" vocabulary does not go away. People leave the images at the same rate as in A0-core even though the photo captions keep mentioning them longer.

## Predictions vs results

| prediction (who) | criterion as written | result | verdict |
|---|---|---|---|
| Convergence unchanged (Claude) | plateau by step 25; knee k 6–10 | plateau 11 (A0-core 16 by the same script; 15 / 15 in the joint comparison); knee 8 DINOv2 / 8 MiniLM (A0-core 8 / 7) | **passes** |
| Vendi within 20% of A0-core's 31.8 (Claude) | 25.4–38.2 | **43.9** (+38%) | **fails** — more diverse endpoints, not fewer |
| Attractor set shifts toward architecture, street and landscape photography (Claude) | qualitative | shifts toward *interiors and retail stock photography*: fitted kitchens (23 persistent visits, 5 endpoints), supermarket produce aisles (9 / 3), offices, product grids, aerial stadium; also vintage-photo Native American portraits (7 / 3). Street and landscape endpoints are no more common than in A0-core | **partly** (direction "stock" right, subjects wrong) |
| Salon basin shrinks below half its A0 size (Claude) | endpoints and steps inside | endpoints 28 → 10; steps inside 1761 → 871 (0.49×); hazard 0.112 → 0.218 /step (residence halves, 8.9 → 4.6 steps) | **passes** |
| Cathedral persists (Claude) | still a persistent attractor | 11 → 12 endpoints, 574 → 580 steps inside, hazard 0.033 → 0.040; longest visit 48 steps | **passes** |
| Style vocabulary falls from ~55% to under 25% of captions; photographic vocabulary rises (Claude) | shares in the caption audit | style share 53% → 28% at step 0 and 87% → 53% at steps 76–99 (falls by 40%, not to < 25%); photo share 46% → 71% (A0 vs photo, all windows) | **fails on the threshold**, direction right |
| People drain out at a similar rate to A0 (caption mentions halve by ~step 25) (Claude) | caption people share | captions: 73% → 35% by steps 26–50 in both runs; but A0-core keeps falling to 22% while A0-photo stays at 36% through step 99. Face detector (YuNet, 12 sampled steps, all 100 trajectories): identical curves — 58 → 16 faces at step 99 in both; of the 58 trajectories with a face at step 0, 9 (A0) vs 10 (photo) still have one at step 99 | **passes on images**; captions keep naming people longer than the images keep them |
| Converges at least as hard as A0, toward stock-photography attractors (Brad) | — | same knee/plateau, but *less* time in persistent attractors (30% of steps vs 37%; 46% of endpoints vs 51%; 1.83 vs 2.43 persistent visits per trajectory) and 85% of steps free of any named A0 attractor vs 67%. The new attractors are stock-photo subjects | **half**: stock yes, harder no |

## Metrics

| | A0-core | A0-photo |
|---|---|---|
| knee k DINOv2 / MiniLM | 8 / 7 | 8 / 8 |
| Vendi (DINOv2, step-99) | 31.8 | 43.9 |
| plateau step (step drift) | 16 | 11 |
| mean step drift, last 20 steps | 0.164 | 0.170 |
| share of endpoints inside A0-core p95 radii | 0.92 | 0.48 |
| endpoints inside a named A0-core attractor at step 99 (gravity, R 0.20; the rest are free) | 52 | 22 |
| steps in any persistent attractor (5-cell atlas) | 37% | 30% |
| persistent visits per trajectory / median dwell | 2.43 / 9 | 1.83 / 9 |
| P(palette kept \| subject jump) (chance ≈ 0.30) | 0.52 | 0.61 |
| caption words (median) / clip fired | 131 / 99.6% | 106 / 95.1% |
| style share, steps 76–99 / photo share | 87% / 46% | 53% / 71% |
| captions mentioning people, steps 76–99 | 22% | 36% |
| faces detected at step 99 (of 100) | 16 | 16 |
| median s per trajectory-step (SDXL / LLaVA) | 2.5 (1.78 / 0.75) | 3.3 (1.85 / 1.49) |

Joint k-means over the 200 pooled endpoints (k = 8): six shared clusters, one A0-core-only (9 endpoints), one A0-photo-only (8 kitchens). Figures: `reports/a0_photo_vs_a0/` (drift curves in both spaces, elbow, joint-cluster sheet, endpoint sheets), `reports/a0_photo/` (per-run drift, elbow, trajectories strip, endpoint contact sheet).

## Attractors (five-cell persistent atlas, `reports/persistent_atlas_photo.md`)

Joint k = 40 over all 49,500 intermediate steps of A0-core, A0-photo, E1-cap, E1-gen, E1-both; fixed radius 0.20, dwell ≥ 5. Names carried from the four-cell atlas by centroid match; three new ones named by eye (`archive/persistent_atlas_photo_names.json`).

| attractor | A0-core visits / traj / endpoints | A0-photo visits / traj / endpoints | note |
|---|---|---|---|
| gold-and-blue palatial salon | 52 / 32 / 7 | 83 / 26 / 17 | the gold salon family (two clusters) together: A0-core 151 visits, 26 endpoints; A0-photo 98 visits, 19 endpoints |
| white-and-gold salon / ballroom | 99 / 37 / 19 | 15 / 13 / 2 | the white salon nearly disappears under the photo instruction |
| gothic cathedral nave | 20 / 11 / 11 | 22 / 12 / 12 | unchanged; present in every SDXL and LLaVA cell |
| modern fitted kitchen (stock) | 2 / 1 / 1 | 23 / 7 / 5 | **A0-photo only** |
| supermarket produce aisle | 1 / 1 / 0 | 9 / 4 / 3 | **A0-photo only** (E1-gen touches it twice) |
| Native American portraits in feather headdress (vintage photo) | 1 / 1 / 0 | 7 / 3 / 3 | **A0-photo only**; sepia "old photograph" register |
| luxury canopy bedroom | 26 / 15 / 7 | 0 / 0 / 0 | gone |
| lighthouse in a storm | 7 / 2 / 1 | 9 / 2 / 1 | unchanged |
| ballerinas and dancers | 7 / 2 / 1 | 5 / 1 / 1 | unchanged |

Reading: the instruction removes the *painterly* interiors (white salon, canopy bedroom) and adds *stock-photo* interiors; the gold salon and the cathedral, which SDXL renders photographically anyway, survive. The endpoint sheet (`reports/a0_photo_vs_a0/endpoints_a0_photo.jpg`) shows the rest of the spread: product grids, offices, a stadium from the air, Santorini, warehouse workers, a dog montage, lunar craters.

Gravity against A0-core's eight named states (`reports/gravity_a0_photo.md`): salon hazard doubles (0.112 → 0.218 /step) while capture is unchanged (0.028 → 0.022 /step), so the salon is entered as often but held half as long; the cathedral's hazard and capture are the same as in A0-core (0.040 vs 0.033; 0.0038 vs 0.0032). Depth dependence holds (exit rate 0.026 at d/R < 0.4, 0.27 at the rim).

## Captions (`reports/caption_audit.md`)

LLaVA still ignores the 50-word limit (median 106 words vs 131; 97.5% over the limit; CLIP clip fires on 95% of prompts). The style vocabulary does not vanish: "vibrant", "serene", "ethereal" still appear in 53% of late captions (87% in A0-core), and 71% of captions use photographic vocabulary (46% in A0-core). Male-gendered words outnumber female ones about 2:1 in both runs from step 0 on.

## Palette (`reports/palette_persistence.md`)

Palette is kept across a subject jump more often under the photo instruction (0.61 vs 0.52, chance 0.29); tinted-mono dwells cover 34% of steps (26% in A0-core) and the longest vivid dwell is 79 steps. The grayscale/sepia register that the vintage-photo portraits live in is part of this.

## People and faces (first look for E6; `analysis/cache/{a0_core,a0_photo}/faces.jsonl`)

YuNet face detector + CelebAMask skin parser on steps 0, 1, 2, 3, 5, 10, 15, 20, 30, 50, 75, 99 of all 100 trajectories in both runs (1,200 images each; identical step-0 images, 58 with a detected face).

| step | A0-core faces / 100 | of the 58 step-0 faces | A0-photo faces / 100 | of the 58 | skin L* mean (sd), A0-core | A0-photo |
|---|---|---|---|---|---|---|
| 0 | 58 | 58 | 58 | 58 | 53.9 (14.0) | 53.9 (14.0) |
| 5 | 38 | 30 | 52 | 41 | 46.9 (14.3) | 44.6 (14.7) |
| 10 | 35 | 25 | 43 | 31 | 48.0 (18.4) | 45.3 (16.6) |
| 20 | 25 | 18 | 30 | 24 | 39.7 (19.0) | 49.2 (17.2) |
| 50 | 19 | 12 | 17 | 11 | 44.2 (20.3) | 41.1 (15.9) |
| 99 | 16 | 9 | 16 | 10 | 47.1 (17.6) | 47.6 (19.9) |

Faces survive a little longer in the first 20 steps under the photo instruction and end at the same place: about one in six images has a face at step 99, and five in six of the seed faces are gone. Mean skin lightness of the faces that remain falls from L* 54 to the low-to-mid 40s in both runs by step 20 and stays there; with 15–30 faces per step this is suggestive, not a result, and it is confounded by *which* trajectories keep faces (the headdress portraits and the sepia register). E6's seeded design is what resolves it. No E6 prediction is touched by this table.

## Throughput, cost, deviations

Pod RTX PRO 6000: 3.3 s per trajectory-step median (SDXL 1.85 s, LLaVA 1.49 s under the photo instruction vs 0.75 s under Hintze's; LLaVA writes longer and slower here), 9.97 h wall (18:12–04:10 UTC), ≈ $25. One pass, no resume events, no tracebacks, no empty captions or refusals. No new deviations: the instruction change is the arm's definition (SPEC2 §3), everything else is A0-core's configuration and pins.

## What this means for E6

The photo instruction does not create a stronger funnel; it widens the landscape and shifts it to stock photography, and it does not stop people from draining out of the loop. As the E6 baseline it is adequate: the vocabulary is photographic enough for the attribute coder, and attribute loss will not be masked by a global collapse into one painterly basin. One caution for E6: LLaVA under this instruction keeps describing people in captions after the generator has dropped them (36% vs 16% of images at step 99), which is the omission-vs-override split in reverse (caption keeps it, image loses it) and the E6 report already separates those.
