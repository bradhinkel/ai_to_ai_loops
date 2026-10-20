# E1-both core (Hunyuan-DiT v1.2 + Qwen2.5-VL 7B, both NEW) — cell report, 2026-10-20

Run `runs/e1_both` (100 trajectories × 100 steps, T = 0.9, CLIP-77 clip enabled, pod RTX PRO 6000; manifest commit 1814b74). Predictions: `predictions.md` "E1 model factorial" (recorded 2026-10-18, confirmed by Brad before any E1 run). This is one cell; H3 and the E1 gate wait for E1-cap core (running).

## Verdict against the predictions

| prediction | criterion | E1-both | result |
|---|---|---|---|
| H1 convergence | DINOv2 step-drift plateau by ~step 25; pooled elbow k < 20 | plateau 25 (`e1_report`; 12 by the `a0_report` rule); knee k = 8 DINOv2, 7 MiniLM | **passes** |
| H2 attractors differ | < half of E1-both endpoints inside A0 cluster radii; joint clustering shows E1-both-only clusters | 0.78 inside A0 p95 radii, but 75 of those 78 are inside A0's loose "catch-all landscapes" cluster (radius 0.79) and 3 inside "people and art (loose)" (0.59); 1 endpoint inside a named A0 attractor (bedroom), 0 in cathedral, salon, Victorian house or castle. Joint clustering: one cluster is 82% E1-both (mirror-lake trees, 27 endpoints), one is 70% E1-both (dancers, 16) | **fails as written, on the loose-cluster artefact; passes on every tight reading** (see note) |
| H3 captioner dominates | E1-cap overlap with A0 lower than E1-gen's | needs E1-cap core | pending |
| Interaction | E1-both differs from both single swaps | E1-both shares its mirror-lake cluster with the E1-cap pilot (Qwen) and its tunnel/light cluster with E1-gen (Hunyuan), plus an own dancers cluster | partial: both parents visible, plus one own basin |
| Side prediction (Claude) | Qwen obeys 50 words; clip rarely fires in Qwen cells | median 34–40 words; clip fired on 0.9% of prompts (97–99% under LLaVA) | **passes** |

Note on H2: the "share inside A0 radii" metric uses each A0 cluster's p95 member radius. A0's catch-all landscapes cluster has radius 0.79 in DINOv2 cosine, four times the fixed 0.20 attractor radius, and E1-both's sunset-lake endpoints land inside it. The same metric gave E1-gen 0.37 because E1-gen's endpoints are tunnels, canyons and interiors rather than landscapes. Under the fixed 0.20 radius (`gravity_e1_both.md`, A0 probes) 1 of 100 E1-both endpoints is inside any A0 attractor. The prediction's threshold was written for this metric and is reported as failed; the reading that the attractor set differs from A0 is supported by every other measure. No prediction text was edited.

## Metrics vs the other cells

| run | knee k DINOv2 / MiniLM | Vendi (DINOv2) | plateau step | share inside A0 radii (p95) | endpoints in a named A0 attractor (R 0.20) | mean step drift, last 20 | caption words, median | CLIP-77 clip fired |
|---|---|---|---|---|---|---|---|---|
| A0-core (SDXL + LLaVA) | 8 / 7 | 31.8 | 15 | 0.92 | 48 | 0.164 | 126 | 99% |
| E1-gen (Hunyuan + LLaVA) | 8 / 11 | 58.9 | 22 | 0.37 | 18 | 0.174 | 112 | 97% (113 → 62 words) |
| E1-cap pilot (SDXL + Qwen, n = 20) | 10 / 9 | (n = 20) | 20 | 0.45 | — | — | 36 | 3.8% |
| **E1-both (Hunyuan + Qwen)** | **8 / 7** | **39.2** | **25** | **0.78** | **1** | **0.188** | **34** | **0.9%** |

E1-both's endpoint diversity (Vendi 39) sits between A0 (32) and E1-gen (59): the Qwen captioner pulls the Hunyuan loop back toward a concentrated endpoint set. The drift curves are the same shape as A0 and E1-gen (`e1_both_vs_a0/drift_dinov2.png`); E1-both's last-20 drift is the highest of the three, consistent with wide, shallow basins (below).

## Motifs (step-99 k-means, k = 8, DINOv2; `reports/e1_both/sheet_step99.jpg`, `e1_both_vs_a0/endpoints_e1_both.jpg`)

Nearly every endpoint is a sunset or twilight scene in purple, orange and pink, with a mirror-flat water surface and a symmetric reflection.

- Lone tree on an islet in a mirror lake, often cherry-pink (21). The signature E1-both basin; shared with the E1-cap pilot's "lavender trees" cluster (6 of the pilot's 20 endpoints fall in the same joint cluster), not with E1-gen.
- Groups of silhouettes facing each other or the sun across water (18, loose): hooded figures, astronauts, couples, swans, deer.
- Dancers and figures with raised arms in a burst of light (16): ballerinas, tutus, fairies, yoga lines. Mostly E1-both's own (16 of the joint cluster's 23).
- Meditating silhouettes, lotus position, reflected (12). The "Sukhasana" figures Brad noted at step 61.
- Light bursts, vortices and swirls, a figure at the centre (11). Shared with E1-gen's tunnel/light cluster (the Hunyuan side).
- Moonlit lake or forest, deer, orbs (11).
- Palm trees at sunset, tropical sofas (6).
- Gold corridors and grand interiors (5), including E1-both's single cathedral (traj 18).

Chinese-flavoured content is present but minor: multi-tier pagodas by water (traj 53, 92, 93), a Fuji-and-pagoda, cherry trees. Nothing Chinese-specific became a basin on its own under English captions (relevant to E2, SPEC2 §4).

What vanished relative to A0: the gold-and-blue salon (0 endpoints; 34 in A0, 1 in E1-gen, 2 in the E1-cap pilot), the Victorian house and the old-town street. The bedroom/bathroom basin survives in every cell (4 here). The cathedral, which survived the generator swap unchanged (11 A0, 12 E1-gen), nearly disappears under Qwen (1 here, 1 in the E1-cap pilot). So the cathedral tracks the captioner and the salon tracks the SDXL + LLaVA pair.

## Gravity (`reports/gravity_e1_both_own.md`, `gravity_e1_both_minilm.md`; fixed radius 0.20 DINOv2 / 0.15 MiniLM, hysteresis 1.25×)

| basin (DINOv2, own k = 8) | endpoints at R 0.20 | steps inside | hazard /step | KM median residence | capture /step | re-entries |
|---|---|---|---|---|---|---|
| dancers / raised arms in light | 8 | 639 | 0.097 | 5 | 0.0075 | 50 |
| lone tree, mirror lake | 5 | 144 | 0.236 | 3 | 0.0040 | 28 |
| light bursts / vortices | 2 | 106 | 0.217 | 2 | 0.0026 | 15 |
| moonlit lake | 2 | 92 | 0.239 | 4 | 0.0024 | 16 |
| meditators | 2 | 45 | 0.356 | 3 | 0.0018 | 9 |
| free | 78 | | | | | |

Compared with A0's cathedral (hazard 0.033, KM median 23) and salon (0.112, capture 0.028), E1-both's basins are shallow and wide: at the 0.20 radius 78 of 100 endpoints are "free" even though the step-99 sheet is visibly homogeneous. The family (sunset, mirror water, silhouette) is tight in style and loose in DINOv2 content, so trajectories wander between neighbouring variants (tree ↔ meditator ↔ dancers) with per-step hazards of 0.1–0.36 and many re-entries. Hazard by depth has the usual gradient (0.06–0.09 near the centre, 0.16 at the rim, 0.29 in the hysteresis band) and is flat over steps 20–99, so the picture is stationary. In caption space (MiniLM) the basins are shallower still (hazard 0.17–0.37), the opposite of A0, where the salon was deepest in caption space.

Hazard-hypothesis test (predictions note of 2026-10-19): the nothing-shared pair A0 / E1-both has no attractor with enough steps on both sides to compare (cathedral: 4 E1-both steps; salon, Victorian house: 0). The same-captioner pair E1-cap / E1-both and the same-generator pair E1-gen / E1-both are tested once E1-cap core is in. The one basin shared by E1-gen and E1-both (light bursts / tunnels) is loose in both and not comparable at R 0.20.

## Transient visits

- A0 attractors in E1-both (`visits_a0_core_in_e1_both`): cathedral visited by 1 trajectory (1 step, step 86), salon 1 (2 steps), bedroom 3 (1 stayed), Victorian house and castle never. The A0 attractors are essentially not on E1-both's map.
- E1-both basins in A0 (`visits_e1_both_in_a0_core`): the mirror-lake tree basin was visited transiently by 27 A0 trajectories (2 stayed; longest dwell 26 steps) and the loose silhouette-group basin by 34 (1 stayed). So SDXL + LLaVA passes through sunset-lake scenes but does not settle in them.
- E1-both basins in E1-gen (`visits_e1_both_in_e1_gen`): the vortex/light basin visited by 35 E1-gen trajectories (3 stayed), mirror-lake trees 29 (4 stayed), dancers 8 (2 stayed, nearest 0.14). Hunyuan + LLaVA reaches these places and mostly leaves.

## Captions (`reports/caption_audit.md`)

- Qwen writes a median 34 words after step 0 (A0's LLaVA 126), 439 of 10,000 captions over 50 words, 0 empty, 0 refusals. The clip fired on 0.9% of prompts, so Hunyuan saw whole captions; mT5 never truncated.
- Style vocabulary rises from 61% of step-0 captions to 94–96% from step 6 on, the highest of any run; photographic vocabulary falls from 11% to 0–1%.
- People stay in the loop: 66% of step-0 captions mention a person, still 53% at steps 76–99 (A0: 73% → 22%). Gendered words go from 32 : 44 male : female at step 0 to 6 : 353 at steps 26–50 and 22 : 318 at the end. The E1-cap pilot shows the same female skew under Qwen with SDXL (0 : 45 at steps 11–25); A0 runs about 2 : 1 male; E1-gen (LLaVA on Hunyuan) is near 1 : 1.2. The loop's gender prior therefore follows the captioner first and the generator second. This is a caption-level count, not an image measure, and feeds the E6 design.

## Run quality

- 10,000 records, no crash, no resume; 15.0 h wall (22:09 → 10:27 UTC) incl. the 13-min compile. Median 4.4 s per trajectory-step (Hunyuan 3.6, Qwen 0.8 with 8 Ollama slots), VRAM 90–92 GB (runner 28 GB + Ollama 64 GB). Cost about $37.
- Pinned: Hunyuan-DiT v1.2 snapshot 5e96094e, 25 steps + torch.compile (D12 amendment), 512 px resized; `qwen2.5vl:7b` digest 5ced39dfa4ba (D14); DINOv2 `facebook/dinov2-base` f9e44c81, MiniLM 1110a243. CLIP steered only (rule 4).
- Figures: `reports/e1_both/` (a0_report set + sheets at steps 10, 50, 99), `reports/e1_both_vs_a0/` (drift, elbow, joint clusters k = 8, endpoint sheets), gravity and visits reports named above; elbow table updated in `reports/elbow_table.md` (E1-both knee 8 DINOv2 / 7 MiniLM, subsample 10 [8, 13] / 8 [6, 11]).
