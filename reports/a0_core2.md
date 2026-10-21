# A0-core-2 replication report — same pair, same seeds, new generator seed (SPEC2 §3), 2026-10-21

A0-core rerun with `sdxl_base_seed` 20261020 instead of 20261017 and nothing else changed (SDXL + llava:latest 7B, Hintze's 100 seeds and instruction, T = 0.9, 100 × 100 steps, pod config `configs/a0_core2_runpod96.yaml`, code 2de993d). Every SDXL draw and every LLaVA sample differs from A0-core, so the comparison is the run-to-run noise of one pair. Prediction recorded in `predictions.md` on 2026-10-20.

**Outcome: complete, no data loss, no restarts. A0 replicates.** Knee, plateau, Vendi, the attractor census, the time spent in attractors, the hazards of the big basins, the caption statistics, the palette persistence and the face-dropout curve all land within sampling noise of A0-core. The one miss in Claude's prediction is the seed-memory half-life (6 steps in DINOv2 against the predicted 3–5). The useful product is the noise floor below: it says which E1 differences are model effects and which are not, and it shows that one E1 metric (share of endpoints inside A0's p95 radii) is too noisy to carry a verdict on its own.

## Prediction vs result

| criterion as written (Claude) | result | verdict |
|---|---|---|
| cathedral, palatial salon, canopy bedroom, Victorian house each ≥ 3 persistent visits in both runs | atlas persistent visits A0-core / A0-core-2: gold salon 80 / 87, white salon 58 / 69, cathedral 20 / 14, bedroom 30 / 21. Victorian house is a gravity state, not an atlas cluster: 36 / 12 entries, longest visits 13 / 10 steps, so a handful of ≥ 5-step visits in each run | **passes** (Victorian house is the weakest and shrinks by 3×) |
| endpoint share of each within ± 8 endpoints of A0-core | salon 28 → 26, cathedral 11 → 8, bedroom 8 → 5, Victorian 5 → 2 | **passes** |
| knee k 6–10 | 8 (per-run script) and 10 (pooled comparison) in DINOv2; 8 in MiniLM | **passes** (upper edge in the pooled fit) |
| Vendi within 20% of 31.8 | 34.8 (+9%) | **passes** |
| 30–45% of steps in persistent attractors | 37% (A0-core 39% in the same six-cell atlas) | **passes** |
| seed-memory half-life 3–5 steps | 6 steps in DINOv2, 4 in MiniLM (A0-core 4 / 3); identification at step 10 is 0.33 vs 0.20 | **fails in DINOv2**: this run holds its seeds a little longer |
| Brad: expects replication | see above | **holds** |

## Metrics side by side

| | A0-core | A0-core-2 | A0-photo (for scale) |
|---|---|---|---|
| knee k DINOv2 / MiniLM (per-run) | 7 / 7 | 8 / 8 | 8 / 8 |
| Vendi (DINOv2, step 99) | 31.8 | 34.8 | 43.9 |
| plateau step (step drift) | 16 | 20 | 11 |
| mean step drift, last 20 steps | 0.164 | 0.162 | 0.170 |
| share of endpoints inside A0-core p95 radii | 0.92 (in-sample) | **0.62** | 0.48 |
| endpoints in a named A0 state (gravity, R 0.20) | 52 | 41 | 22 |
| steps in any persistent attractor (six-cell atlas) | 39% | 37% | 26% |
| persistent visits per trajectory / median dwell | 2.53 / 9 | 2.56 / 9 | 1.55 / 9 |
| salon hazard / capture per step | 0.112 / 0.028 | 0.109 / 0.028 | 0.218 / 0.022 |
| cathedral hazard / capture per step | 0.033 / 0.0032 | 0.022 / 0.0021 | 0.040 / 0.0038 |
| bedroom hazard; Victorian hazard | 0.170; 0.196 | 0.200; 0.256 | — |
| exit rate by step window 20–40 / 40–60 / 60–80 / 80–99 | flat ≈ 0.10 | 0.11 / 0.08 / 0.12 / 0.10 | 0.12 / 0.17 / 0.14 / 0.14 |
| P(palette kept \| subject jump) | 0.52 | 0.55 | 0.61 |
| caption words median; style share 76–99; people share 76–99 | 131; 87%; 22% | 131; 87%; 24% | 106; 53%; 36% |
| faces at step 99 / faces at step 0 | 16 / 58 | 12 / 61 | 16 / 58 |
| median s per trajectory-step (SDXL / LLaVA) | 2.5 (1.8 / 0.7) | 3.6 (1.9 / 1.7) | 3.3 (1.85 / 1.5) |

Joint k-means over the 300 pooled endpoints of A0-core, A0-core-2 and A0-photo (k = 8): all eight clusters are shared between the two A0 runs, with per-cluster counts 34/34, 11/10, 5/5, 6/5, 23/30, 9/6, 1/2, 11/8. The only cluster that is not shared is A0-photo's kitchens. Figures: `reports/a0_core2_vs_a0/`, `reports/a0_core2/`.

## The noise floor (what a one-pair rerun moves)

From the six-cell atlas (`reports/persistent_atlas_rep.md`; joint k = 40 over 59,400 steps; radius 0.20, dwell ≥ 5):

- Big attractors move by about ± 10 persistent visits and ± 5 trajectories: gold salon 80 → 87, white salon 58 → 69, bedroom 30 → 21, cathedral 20 → 14.
- Small ones come and go: an unnamed LLaVA cluster 16 → 7, gnarled tree 0 → 6, East Asian garden 5 → 0, desert dunes 6 → 2. So "present in one cell and absent in the other" is noise when the larger count is under about 10 visits.
- Share of steps in persistent attractors moves by 2 points (39 → 37%), persistent visits per trajectory by 0.03, Vendi by 3, knee by 1, salon hazard by 3% relative, cathedral hazard by a third (20 vs 30 entries), the small basins' hazards by 30%.
- Endpoints inside the named A0 states: 52 → 41. **Share inside A0-core's p95 radii: 0.92 → 0.62.** The 0.92 is in-sample (the radii were fitted on A0-core's own endpoints), so 0.62 is what an identical pair scores on this metric. That matters for E1 below.

Against this floor the E1 results stand or sharpen:

- Hunyuan cells have 0 salon visits against 80–87 in the A0 runs, and E1-cap's salons (44 white, 6 gold) are far below both A0 runs; E1-cap's mirror-lake, banquet-hall and bathroom attractors (24, 27, 22 visits) have 0–3 in either A0 run. These are model effects by any reading of the floor.
- The cathedral (20 / 14 / 21 / 15 / 24 visits across A0-core, A0-core-2, A0-photo, E1-cap, E1-gen) is the same size in every cell that has it; its absence in E1-both (2) is real.
- Time in persistent attractors: A0 39 / 37%, E1-cap 36%, E1-gen 15%, E1-both 12%. The SDXL cells sit inside the A0 noise band; the Hunyuan cells are far outside it. This is the cleanest statement of the generator rule.
- The "share inside A0 p95 radii" column in `reports/e1.md` (E1-cap 0.53, E1-gen 0.37, E1-both 0.78) should be read against 0.62 for a same-pair rerun, not against 0.92. E1-cap is then at the noise floor, E1-gen below it, and E1-both above it (it is a loose landscape cluster, as the E1 report already says). The H3 verdict in E1 rests on the atlas and gravity evidence, which survives; this one column does not discriminate, and a note to that effect is appended to `reports/e1.md`.
- Hazard consistency (Brad's hypothesis in E1): a same-pair rerun keeps every hazard within 1.5× (salon 1.03×, cathedral 1.5×, bedroom 1.2×, Victorian 1.3×). E1's cross-pair ratios were mostly outside 2×, so the E1 "not supported" verdicts were not noise.

## Other readouts

- **Hintze comparison.** Knee 8 in MiniLM caption space (Hintze's T = 0.9 data 8 under the same rule, `reports/elbow_table.md`); the bootstrap spread row for A0-core-2 is in that table.
- **Memory curve** (`reports/memory_curve.md`): the second run holds seeds longer in the first ten steps (identification 0.60 / 0.51 / 0.33 at steps 3 / 5 / 10 vs 0.51 / 0.41 / 0.20) and is identical from step 50 on. One run of each is not enough to say whether that is the generator seed or chance; the E1 cells all sit in the A0-core band, so the claim "seed half-life 3–5 steps" should be loosened to "about 3–6 steps" in the write-up, not in the prediction file.
- **Faces** (YuNet on 12 sampled steps): 61 step-0 faces (different step-0 renders), 24 at step 20, 12 at step 99; A0-core 58 → 25 → 16. Same curve within a few faces.
- **Captions and palette** replicate to the percentage point (tables in `reports/caption_audit.md` and `reports/palette_persistence.md`).

## Throughput, cost, deviations

Pod RTX PRO 6000: 3.6 s per trajectory-step median, 10.1 h wall (04:15–14:24 UTC), ≈ $25. LLaVA took 1.7 s per trajectory against 0.7 s in A0-core with the same Ollama 0.40.6, the same model digest and the same parallelism; SDXL time was unchanged. The difference is the machine (A0-core ran on an earlier pod on 2026-10-18), not the code, and it has no effect on outputs. No resume events, tracebacks, refusals or empty captions. No new deviations.
