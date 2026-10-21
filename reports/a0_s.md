# A0-S gate report — SDXL + Claude Sonnet as captioner (SPEC §5; SPEC2 §4 E1 second new captioner), 2026-10-21

A0-core with the captioner swapped for `claude-sonnet-5-5` over the Messages API and nothing else changed: SDXL base, Hintze's 100 seeds and caption instruction verbatim, 100 trajectories × 100 steps, pod config `configs/a0_s_runpod96.yaml`, code 97a4595, SDXL base seed 20261017 (so step 0 is identical to A0-core). D16: the API offers no temperature control for this model, so captions are sampled at the model's default rather than T = 0.9; every record carries `temperature_applied: false`. Predictions: `predictions.md` "A0-S" (Brad 2026-10-16: H1 holds, H2 fails; Claude 2026-10-20, six numbered predictions, confirmed by Brad).

**Outcome: complete, 10,000 captions, 0 refusals, 0 empty responses, 0 retries, no restarts.** The loop converges like every other cell (prediction 1 passes), the caption-space attractor set is entirely Sonnet's own (prediction 3 passes), and the image-space attractors are SDXL's (prediction 2 passes on the count). Three things were not predicted: (a) Sonnet does not create image attractors of its own; it lands in the attractors Qwen found in E1-cap (misty gnarled tree, mirror lake, pink banquet hall), which LLaVA never reached (prediction 4 fails); (b) Sonnet drops people faster than LLaVA, not slower, and its gendered vocabulary ends 8:1 female (prediction 5 fails); (c) the whole run drifts into a purple-magenta palette, the strongest colour attractor of any cell (hue census below). Brad's H1 holds and his H2 fails as he expected.

## Prediction vs result

| prediction (Claude, 2026-10-20) | result | verdict |
|---|---|---|
| 1. convergence as in every cell: plateau by 25, knee 6–10, seed half-life 3–5 | plateau 12 (per-run drift) / 23 (comparison fit); knee 9 in DINOv2 and 9 in MiniLM; half-life 4 steps in both spaces | **passes** |
| 2. generator rule: ≥ 6 of A0's 11 persistent image attractors present (salons, cathedral, bedroom, bathroom among them); 30–45% of steps in persistent attractors | 7 of A0's 12 atlas attractors present (≥ 3 persistent visits): both salons, cathedral, bathroom, desert dunes and two small unnamed ones. **Canopy bedroom absent** (A0 30 visits, A0-S 0). 29% of steps in persistent attractors | **passes on the count; bedroom missing; share one point under the band** |
| 3. captioner rule in caption space: < 4 of A0's 12 caption attractors survive; ≥ 5 of A0-S's own | 0 of A0's 11 survive; A0-S has 5 of its own plus 1 shared with Qwen | **passes** |
| 4. Sonnet-specific content: ≥ 2 persistent image attractors absent from all four E1 cells; Vendi 28–40 | 0: every A0-S attractor with ≥ 3 visits is present in at least one other cell (5 of the 12 are Qwen's from E1-cap). Vendi 36.4 | **fails** on the attractors, Vendi inside the band |
| 5. people: captions naming a person stay above 30% through step 99; gendered words nearer 1:1 than LLaVA (2:1 male) or Qwen (female) | people share 64% → 17% in steps 76–99 (LLaVA 22%); male : female words 45 : 38 at step 0 → 64 : 518 in steps 76–99 | **fails** on both |
| 6. D16 caveat: flag if shared basins are deeper (median hazard < half of A0's) | shared attractors' hazards A0 → A0-S: white salon 0.148 → 0.178, gold salon 0.155 → 0.268, cathedral 0.022 → 0.068, bathroom 0.25 → 0.11, dunes 0.07 → 0.03; median ratio 1.2 (shallower) | **caveat not triggered** |
| Brad: H1 converges to a small attractor set | yes | **holds** |
| Brad: H2 same attractors as LLaVA's — expected to fail | caption space: none shared. Image space: the SDXL motifs (salons, cathedral) persist but the set shifts toward Qwen's | **fails as predicted** |

## Metrics side by side

| | A0-core | A0-core-2 | E1-cap (Qwen + SDXL) | A0-S (Sonnet + SDXL) |
|---|---|---|---|---|
| knee k DINOv2 / MiniLM (per-run) | 7 / 7 | 8 / 8 | 8 / 7 | 9 / 9 |
| Vendi (DINOv2, step 99) | 31.8 | 34.8 | 36.3 | 36.4 |
| plateau step (per-run step drift) | 16 | 20 | — | 12 |
| mean step drift, last 20 steps | 0.164 | 0.162 | — | 0.155 |
| share of endpoints inside A0-core p95 radii (same-pair floor 0.62) | 0.92 | 0.62 | 0.53 | 0.50 |
| endpoints in a named A0 state (gravity, R 0.20) | 52 | 41 | — | 14 |
| steps in any persistent attractor, seven-cell DINOv2 atlas | 39% | 36% | 39% | 29% |
| persistent visits per trajectory / median dwell | 2.45 / 9 | 2.41 / 9 | 2.13 / 11 | 1.59 / 10 |
| steps in any persistent caption attractor (MiniLM, five English cells) | 47% | — | 27% | 31% |
| seed half-life DINOv2 / MiniLM (steps) | 4 / 3 | 6 / 4 | 3 / 3 | 4 / 4 |
| P(palette class kept \| subject jump) (chance) | 0.52 (0.30) | 0.55 (0.30) | 0.65 (0.35) | **0.72** (0.36) |
| caption words median; over the 50-word limit | 131; 99.7% | 131; 99.6% | 37; 10.7% | **46; 0.5%** |
| style share / people share, steps 76–99 | 87% / 22% | 87% / 24% | 87% / 14% | 91% / 17% |
| male : female words, steps 76–99 | 298 : 183 | — | 0 : 39 | 64 : 518 |
| images with a face, step 0 → 1 → 20 → 99 | 58 → 57 → 25 → 16 | 61 → 56 → 24 → 12 | — | 58 → **42** → 19 → **10** |
| s per trajectory-step (SDXL / captioner) | 2.5 (1.8 / 0.7) | 3.6 (1.9 / 1.7) | — | 2.7 (1.9 / 0.9) |

Figures: `reports/a0_s/` (drift, elbow, step-99 contact sheet at k = 9, trajectories strip), `reports/a0_s_vs_a0/` (joint clusters, endpoint sheets, drift against A0-core), `reports/persistent_atlas_s/` (seven-cell atlas sheets), `reports/persistent_atlas_minilm_s/` (caption-space atlas), `reports/gravity_a0_s.md`.

## Where Sonnet's loop goes (image space, DINOv2 seven-cell atlas, R 0.20, dwell ≥ 5)

Persistent visits per cell (A0-core / A0-core-2 / A0-photo / E1-cap / E1-gen / E1-both / **A0-S**):

| attractor | A0 | A0-2 | A0-photo | E1-cap | E1-gen | E1-both | **A0-S** | reading |
|---|---|---|---|---|---|---|---|---|
| white-and-gold salon / ballroom | 73 | 80 | 8 | 44 | 0 | 0 | **25** | SDXL motif, kept |
| gold-and-blue palatial salon | 65 | 75 | 77 | 5 | 0 | 0 | **5** | SDXL motif, nearly gone (as under Qwen) |
| gothic cathedral nave | 20 | 13 | 23 | 14 | 23 | 2 | **38** | strongest A0-S attractor; rendered violet |
| luxury canopy bedroom | 30 | 21 | 0 | 5 | 5 | 0 | **0** | gone |
| gnarled old tree in mist | 0 | 3 | 0 | 19 | 0 | 0 | **24** | Qwen's motif, now Sonnet's too |
| lone tree in a mirror lake | 0 | 0 | 0 | 27 | 0 | 8 | **14** | Qwen's motif |
| pink-and-gold banquet hall | 0 | 3 | 1 | 29 | 0 | 0 | **13** | Qwen's motif |
| mossy tree / cypress swamp | 0 | 2 | 0 | 7 | 0 | 1 | **11** | Qwen's motif |
| canoe on a still lake at dusk | 1 | 3 | 0 | 8 | 0 | 4 | **9** | Qwen's motif |
| luxury bathroom; desert dunes | 3; 6 | 0; 2 | 0; 0 | 22; 13 | 0; 1 | 4; 1 | **4; 5** | shared |

Of A0-S's 159 persistent visits, 77 are in attractors shared by A0 and E1-cap (the SDXL motifs), 71 are in attractors that E1-cap has and A0 does not (Qwen's motifs), and 8 are in attractors A0 has and E1-cap does not (LLaVA's). No attractor at this resolution belongs to Sonnet alone. The joint endpoint clustering against A0-core says the same thing with different boundaries: three clusters unique to A0-S (misty trees 16 endpoints, pink banquet halls 9, lavender fields and violet desert sunsets 13), two A0-only (bedrooms 9 → 0; Victorian houses, geisha and vintage cars 10 → 2), five shared.

**A hypothesis, not a claim.** LLaVA writes 130-word captions that SDXL's 77-token window cuts mid-sentence; Qwen (37 words) and Sonnet (46) write captions that fit, so SDXL sees a complete description ending in the mood sentence. If the attractor set follows the prompt's length and shape rather than the captioner's identity, the two short captioners should share attractors, which is what the table shows. E4 (caption length) is the test: LLaVA with a hard 50-word limit should move toward the Qwen/Sonnet set. Recorded here for E4's prediction; nothing in this run can separate the two readings.

**Gravity of A0's named states** (`reports/gravity_a0_s.md`): cathedral 10 endpoints and 720 steps inside (A0 11 and 574), but with a hazard of 0.115 against 0.033, so Sonnet visits the cathedral more and stays a third as long; gold salon 4 endpoints (A0 28); bedroom and Victorian house 0; 86 of 100 endpoints outside every A0 state (A0 48, A0-core-2 59). Exit rate by step window is flat (0.13–0.16), so the loop is stationary from step 20 on.

## Caption space (MiniLM, R 0.15, five English cells)

None of A0's 11 persistent caption attractors receives a persistent visit from A0-S. A0-S has five of its own (named in `archive/persistent_atlas_minilm_s_names.json`): the violet-lit Gothic cathedral (28 visits, mean dwell 27 steps, hazard 0.03, the deepest basin in the run), the blush-pink rococo salon (26), the gilded baroque ballroom in golden light (27), the terracotta courtyard with ferns and arched doors (41 visits, 14 trajectories), and the twilight lake or cottage in lavender haze (27); plus the gnarled tree over still water in sepia mist (20), which it shares with Qwen. 31% of A0-S steps are inside a persistent caption attractor (A0 47%, E1-cap 27%). The captioner rule stands with a third captioner: the words belong to the captioner, the pictures to the generator, and the pair decides which of the generator's motifs are reached.

## Captions, people, palette

- **Compliance.** Median 46 words in every step window, maximum 53; 51 captions (0.5%) over 50 words by the runner's count; all 10,000 responses `end_turn`, one attempt each. 23 prompts of 9,900 exceeded SDXL's 77 tokens and were cut by its tokenizer, as in Hintze's own setup (no explicit clip in this cell). Style vocabulary 67% → 91%; photographic vocabulary 7% → 2% (LLaVA 46%).
- **People.** Captions naming a person: 64% at step 0 → 50% (steps 1–5) → 17% (76–99). LLaVA: 73% → 69% → 22%. Images with a detected face (YuNet, 12 sampled steps): 58 → 42 after one step → 10 at step 99; LLaVA 58 → 57 → 16. Sonnet drops figures in the first step, not gradually: it describes "a solitary figure" or none where LLaVA lists "a man in a suit". Gendered words run 45 : 38 male : female at step 0 and 64 : 518 by the last quarter; the surviving people are the red-haired women in green gowns of the Pre-Raphaelite cluster and silhouetted women by twilight lakes.
- **Palette.** P(palette class kept across a subject jump) 0.72 against 0.52–0.55 in the A0 runs and 0.65 under Qwen; 64% of steps sit in palette dwells of ≥ 5 steps (A0 40%). Grayscale, once entered, is kept across 89% of subject jumps (A0 57%): the sepia-mist trees and the black-and-white swamps are a palette attractor that outlives the subject. The hue census from pixels (`reports/hue_share.md`) is in the next section.

## Hue census (pixels only; `reports/hue_share.md`)

Share of saturated pixels in the purple-magenta band (255–335°) and share of images whose largest hue band is purple-magenta, by step:

| run | step 0 | 1 | 5 | 20 | 50 | 99 | images dominant purple at 99 |
|---|---|---|---|---|---|---|---|
| A0-core | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 | 0.02 | 0.03 |
| A0-core-2 | 0.01 | 0.01 | 0.02 | 0.01 | 0.01 | 0.02 | 0.03 |
| A0-photo | 0.01 | 0.01 | 0.00 | 0.01 | 0.01 | 0.00 | 0.00 |
| E1-cap (Qwen) | 0.01 | 0.01 | 0.03 | 0.05 | 0.10 | 0.10 | 0.13 |
| **A0-S (Sonnet)** | 0.01 | 0.02 | 0.05 | 0.11 | 0.16 | 0.24 | 0.30 |

Step 0 is the same 100 SDXL renders in every SDXL cell (1% purple). Under LLaVA the purple share never exceeds 2.4%; under Qwen it climbs to 10%; under Sonnet it reaches 24% of all saturated pixels by step 99, and 30 of 100 final images are purple-dominant. Sonnet's captions carry the colour words that LLaVA's do not: in steps 50–99, "violet" appears in 41% of Sonnet's captions, "lavender" in 27%, "twilight" in 24%, "amethyst" in 13%, "blush" in 15% and "magenta" in 10%, against 0% for each in LLaVA's and 1–4% in Qwen's (Qwen says "purple" and "pink", 15% and 26%). SDXL renders the word, and the next caption names the colour again. This is the colour-attractor Brad asked about after A0-photo, now with a captioner that produces it: the palette is the captioner's, the subject is the generator's. Saturated-pixel share also rises from 33% to 66% (A0 55%).

## Hintze comparison, elbow table

Knee 9 in MiniLM caption space against 8 in Hintze's T = 0.9 data under the same rule, 7–8 in the A0 runs and 7 in E1-cap; the bootstrap interval is in `reports/elbow_table.md`. ELBOW_LINE

## Throughput, cost, deviations

Pod RTX PRO 6000: 6.6 h wall (14:28–21:02 UTC), 2.7 s per trajectory-step (SDXL 1.9 s, Sonnet 0.9 s per trajectory at 8 concurrent calls; 2.2 s median per call), ≈ $16 of pod time. API: 4.23 M input tokens (images) and 1.19 M output tokens over 10,000 calls; at Sonnet's list price ($3 / $15 per million) that is about $31, to be checked against the Console. No 429s or 5xx retries were needed. No resume events, tracebacks, refusals or empty captions. Deviations: D16 (no temperature control) applies; no new ones. With the pod's A0-size cost now ≈ $25, A0-S cost about the same as an A0 run plus the API bill.

## What this changes

1. **The E1 captioner rule holds for a third captioner** and the generator rule holds with a qualification: SDXL's motifs persist, but which of them a loop reaches, and how long it stays, is set by the captioner. The canopy bedroom needs LLaVA; the misty tree needs a short captioner.
2. **For E6:** a frontier captioner follows the instruction but is not neutral on people. Sonnet removed figures faster than LLaVA and feminised the survivors. The E6 Claude cell (SPEC2 §11) is worth running for exactly this reason; the result will not be "Claude preserves attributes because it obeys".
3. **For E4:** the Qwen–Sonnet overlap gives E4 a sharp prediction to write before it runs.
4. **A0-S vs A0 is not a same-temperature comparison** (D16). The shared basins are shallower, not deeper, so the missing temperature control did not make Sonnet's loop stickier; it may have made it less so.
