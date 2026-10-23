# E2-QZ gate report — Chinese caption instruction (SPEC2 §4 E2), 2026-10-23

Run `runs/e2_qz`: Hunyuan-DiT v1.2 + Qwen2.5-VL 7B with the caption instruction in Simplified Chinese (70-character budget, D15), Hintze's 100 English seeds, 100 trajectories × 100 steps, T = 0.9, Hunyuan's bilingual CLIP-77 clip with the character rule. Control: E1-both (same models, English instruction, same seeds; step 0 is identical). Predictions: `predictions.md` "E2-QZ" (recorded 2026-10-20, before any E2 run). Comparison: `reports/e2_qz_vs_e1_both/`, `reports/e2_qz_vs_a0/`. Atlas: `reports/persistent_atlas_e2.md` (five cells, DINOv2). Gravity: `reports/gravity_e2_qz*.md`. Captions: `reports/caption_audit_e2_qz.md`. Culture judge: `reports/culture_judge_e2_qz.md`. Strips and face sheets: `reports/e2_qz/`.

**Gate: the run is complete and clean (10,000 images and records, one start, no restart, 12.4 h at 4.5 s/trajectory-step, about $31). Convergence and register survive translation; the cultural content does not. The loop still converges at the same rate to the same mirror-water sunset register, and half of its persistent visits land in E1-both's attractors. But the people in it become East Asian within one to five steps, and three attractors absent under English captions appear: a pagoda by a misty lake, an arched stone bridge under a full moon, and a lone boat on a misty lake. Brad's hypothesis (different language, different attractors, culturally Chinese) holds in direction; Claude's thresholds for how small the shift would be fail.**

## Verdicts

| prediction | criterion as written | result | verdict |
|---|---|---|---|
| 1 convergence unchanged | DINOv2 plateau by 25; knee k 6–10; Vendi within 25% of 39.2 | plateau 19; knee k 12 by the rule but 6 / 9 / 12 / 14 across kmax 15–40, subsample median 10 [8, 13], identical to E1-both's 10 [8, 13] (`elbow_table.md`); Vendi 35.6 (9% below) | **passes**: the rule's knee is above the band, the bootstrap knee is inside it and indistinguishable from the control |
| 2 register survives | ≥ half of E2-QZ persistent visits in E1-both's top attractors; sunset / mirror-water / silhouette family dominates the step-99 sheet | 68 of 130 persistent visits (52%) in E1-both's top five (dancer in a swirling gown 34, lone tree in a mirror lake 13, sunset lake 12, ballerinas 9, raised-arms figure 0); step-99 sheet is still mostly mirror water at sunset or moonrise | **passes, narrowly on the visit share** |
| 3 some new attractors | ≥ 1 persistent attractor with ≥ 5 trajectories that no E1 cell has; ≥ 1 E1-both attractor drops below 3 visits | pagoda lake: 17 visits / 7 trajectories in E2-QZ, but E1-cap has 4 visits / 3 trajectories (present at the ≥ 3 rule); moon bridge: 12 visits but only 4 trajectories. E1-both's raised-arms figure (8 → 0), rainbow tunnel (3 → 0), gold corridor (3 → 0), bathroom (4 → 0) all drop out | **half: the drop-outs hold; the new-attractor clause fails on the letter (one trajectory short, or three E1-cap visits)**. Brad's "some different attractors" holds in both directions |
| 4 Chinese content a minority | persistent visits to East Asian motifs at most triple E1-both's; < 15 trajectories at step 99; > 30 supports Brad | persistent visits to pagoda + bridge: 29 vs 1 (plus 27 vs 3 for the misty-lake boat); step-99 trajectories: 19 by the judge's setting call, 26 with any East Asian motif, 28 by eye without the boats, 38 with them | **fails**. Under 30 on every instrument except Claude's eye count with the boat family; the direction is Brad's |
| 5 captions | ≥ 99% Chinese; median 45–60 characters; clip < 5%; people persist and gendered words skew female | 100% Chinese; median 40 characters (p90 54); clip 0.2–1.0%; people fall (captions naming a person 0.59 → 0.22, E1-both 0.53 at the end); female : male 260 : 31 in the last window | **half: language, clip and the female skew hold; length is under the band and people do not persist** |

Decision rule as written: prediction 2 holds but prediction 4 does not stay under 15 trajectories, so "language alone does not move the attractor set much" is not supported. The language-vs-provenance question stays open (see "Reading").

## Metrics (DINOv2 unless stated)

| metric | E1-both (English) | E2-QZ (Chinese) |
|---|---|---|
| knee k, pooled step-99 (rule; subsample median [5%, 95%]) | 8 (10 [8, 13]) | 12 (10 [8, 13]) |
| Vendi, step 99 | 39.2 | 35.6 |
| plateau step (`e1_report`) | 25 | 19 |
| mean step-to-step drift, last 20 | 0.205 | 0.228 |
| endpoints inside E1-both's own p95 cluster radii | 0.94 | 0.79 |
| endpoints inside A0 p95 radii | 0.78 | 0.85 |
| steps inside any A0 attractor at R 0.20 (`gravity_e2_qz.md`) | 1% | 0% |
| steps inside any E1-both attractor at R 0.20 (`gravity_e2_qz_e1both.md`) | 11% | 4% |
| persistent visits per trajectory (five-cell atlas) | 1.08 | 1.30 |
| share of steps in persistent clusters | 0.18 | 0.20 |
| seed half-life (steps) | 5 | 4 |
| caption length, median | 34 words | 40 characters |
| CLIP-77 clip fired | 1% | 0.5% |
| captions naming a person, steps 76–99 | 0.53 | 0.22 |
| images with a person, step 99 (judge) | 53 | 29 |

MiniLM is an English sentence model; its numbers for E2-QZ (knee 9, Vendi 6.3, seed half-life 1) are in the tables but say nothing about Chinese captions and are not interpreted.

## Attractors (five-cell persistent atlas, R 0.20, dwell ≥ 5; persistent visits / trajectories with one / endpoints)

| attractor | A0-core | E1-cap (Qwen + SDXL) | E1-both | **E2-QZ** |
|---|---|---|---|---|
| dancer in a swirling gown | 0 | 0 | 14 / 8 / 2 | **34 / 19 / 3** |
| lone boat on a misty lake | 1 / 1 / 0 | 8 / 3 / 2 | 3 / 2 / 1 | **27 / 12 / 8** |
| pagoda by a misty lake | 0 | 4 / 3 / 0 | 1 / 1 / 1 | **17 / 7 / 3** |
| lone tree in a mirror lake | 0 | 22 / 10 / 4 | 18 / 11 / 3 | **13 / 8 / 4** |
| sunset lake with forest reflection | 0 | 0 | 14 / 6 / 3 | **12 / 11 / 4** |
| arched stone bridge under a full moon | 2 / 2 / 0 | 2 / 1 / 1 | 0 | **12 / 4 / 2** |
| ballerinas and dancers | 6 / 2 / 1 | 0 | 30 / 16 / 7 | **9 / 7 / 0** |
| figure with raised arms in a light burst | 0 | 0 | 8 / 5 / 1 | 0 |
| luxury bathroom | 3 / 3 / 0 | 22 / 9 / 8 | 4 / 2 / 2 | 0 |
| rainbow / neon tunnel | 0 | 0 | 3 / 1 / 0 | 0 |
| gothic cathedral nave | 20 / 11 / 11 | 15 / 7 / 2 | 2 / 1 / 0 | 0 |
| white-and-gold salon | 115 / 40 / 25 | 47 / 23 / 7 | 0 | 0 |

Three readings of the table:
- **The Hunyuan + Qwen register is intact.** The dancer, the mirror-lake tree and the sunset lake are E2-QZ's second to fifth attractors, and the dancer in a swirling gown is its strongest basin (34 visits, more than double E1-both's). Nothing of SDXL's (salon, cathedral, bedroom) appears, as in every Hunyuan cell.
- **The Chinese attractors were already latent in the Qwen cells.** The misty-lake boat (8 visits) and the pagoda (4) exist in E1-cap, where Qwen writes English for SDXL; the moon bridge has two A0 visits as a Japanese garden bridge. Under Chinese captions they become basins: 56 persistent visits across the three, against 4 in E1-both.
- **People leave.** The raised-arms figure, the bathroom and the tunnel drop out, and the dancers fall from 30 to 9 visits. The judge finds a person in 29 step-99 images against E1-both's 53, and a visible face in 3 against 7.

Joint k-means on the 200 pooled endpoints (`e2_qz_vs_e1_both/joint_clusters.jpg`, k = 8): two clusters are E2-QZ's own, pagodas and lanterns on misty water (13 E2-QZ endpoints vs 3 E1-both) and lone boats on a moonlit lake (10 vs 2). The dancers cluster is 6 vs 13 and the meditating-silhouettes cluster 6 vs 22. Gravity on E2-QZ's own step-99 clusters (`gravity_e2_qz_own.md`): basins are as shallow as E1-both's (escape hazard 0.20–0.39 per step, Kaplan–Meier median residence 3 steps, 12% of steps inside).

## Brad's observation: faces turn East Asian within five steps

Logged during the run at step 5 (2026-10-22), before any analysis; not covered by any prediction, so it is reported as an unpredicted finding. Two instruments:

**Culture judge** (`analysis/culture_judge.py`, Claude Sonnet 5.5, image only, prompt `culture_v1`, 800 images: steps 0, 5, 20, 99 of both cells; about $4; added after the run, not pre-registered):

| step | cell | person | face | setting judged East Asian | any East Asian motif |
|---|---|---|---|---|---|
| 0 | both | 78 | 48–52 | 0 | 0 |
| 5 | E1-both | 74 | 28 | 2 | 3 |
| 5 | **E2-QZ** | 66 | 29 | **9** | **12** |
| 20 | E1-both | 68 | 7 | 1 | 5 |
| 20 | **E2-QZ** | 53 | 7 | **12** | **15** |
| 99 | E1-both | 53 | 7 | 4 | 17 (14 of them cherry blossom at the mirror-lake tree) |
| 99 | **E2-QZ** | 29 | 3 | **19** | **26** (curved tiled roofs 10, ink-wash style 10, temples 6, pagodas 4, lanterns 4, East Asian dress 4) |

The judge declined to code the faces. Its `primary_apparent_east_asian` field is "yes" on 0 of 800 images and "ambiguous" on most visible faces, with notes such as "I did not infer ethnicity from facial features, so the field is coded ambiguous" (traj 85, step 5). That column is a refusal, not a measurement, and is not used.

**Eye count** (Claude, from `reports/e2_qz/faces_zoom_1..4.jpg`: the 29 trajectories with a visible face at step 5 in E2-QZ, steps 0–5 of both cells side by side; provisional until Brad checks the sheets):

| | E2-QZ | E1-both |
|---|---|---|
| an East Asian face at some step 1–5 | **15 of 29** | 0 of 29 |
| face stays non-East-Asian through step 5 | 5 (all blonde seeds: 5, 31, 37, 47, 88) | 20 |
| no usable face / stylised | 9 | 9 |

The switch is immediate: the lecturer of trajectory 85 is East Asian at step 1, the hard-hat engineer of 13 and the police officers of 19 and 56 at step 1, the farmer of 21 wears a conical hat by step 5, the praying child of 55 and the nurse of 75 switch at step 2. It happens at the first Chinese prompt, before the caption has changed anything but its language: Hunyuan renders "一位女子" as a Chinese woman where it rendered "a woman" as a white one. Blonde seeds are the exception: the caption names the hair colour and the generator keeps it. By step 20 almost no face is left in either cell (7 and 7), so the face effect is a burn-in phenomenon that is then overwritten by the pair's usual person drop-out, which is faster under Chinese captions.

## Captions (`caption_audit_e2_qz.md`)

Every caption is Chinese (CJK share ≥ 0.5 on 10,000 of 10,000); none empty, refused or cut off; 1% over the 70-character limit; the clip fired on 0.5% of prompts (character rule). Median length 40 characters, below the predicted 45–60, p90 54. The style vocabulary (梦幻, 宁静, 壮丽, 光影 ...) rises from 50% of captions at step 0 to 79% at the end, the same drift to the "vivid, artistic" register as every cell. East Asian motif terms appear in 1% of step-0 captions and 17% of the last window (E1-both's English list: 0% → 13%, mostly cherry blossom); 55 of 100 trajectories carry one somewhere in steps 50–99 (E1-both 37). Captions naming a person fall from 59% to 22% while E1-both holds 53%; gendered terms end 260 female : 31 male (E1-both 318 : 22), so the female skew is the Qwen prior in either language.

## Reading

Language changed the content prior, not the dynamics. Convergence (plateau 19, Vendi 36, half-life 4) and the register (mirror water, sunset, dancer) are the Hunyuan + Qwen pair's and survive translation, which is what Claude predicted. What Claude got wrong is the size of the content shift: the people become Chinese at the first Chinese prompt, Chinese landscape motifs that were latent in the Qwen cells (a boat in mist, a pagoda, a moon bridge) become persistent basins, and about a quarter to a third of the endpoints are recognisably Chinese scenes against a handful under English captions. Brad's hypothesis holds in direction; his > 30 threshold is reached only on the broadest count (the boat family included).

Where the shift comes from is not settled by this cell. E2-QZ vs E1-both isolates the language within one captioner and one generator, and the step-1 face switch says the generator's text encoder, conditioned on Chinese, carries most of it: the captioner only translated. Whether a Chinese-writing captioner adds its own cultural prior on top needs the other row of the E2 table (a non-Chinese captioner writing Chinese for Hunyuan, SPEC2 §4). Prediction 4's decision rule therefore does not retire that row; it is Brad's call whether the question is worth the run.

Two further things to record. The person drop-out is faster under Chinese captions (person in the step-99 image 29 vs 53), which matters for E6 if a Chinese arm is ever added. And the anime register appears: the judge's notes call 4 of the step-5 E2-QZ images anime-style and none of E1-both's.

## Run log and deviations

- Launched 2026-10-22 17:16 UTC by the queue waiter after arm A; finished 05:40 UTC 2026-10-23; one start, no restart, no crash, no `.tmp` files; manifest commit d15271e; 4.5 s/trajectory-step on the RTX PRO 6000 (E1-both 4.4).
- Analysis additions, all rebuildable from `runs/`: `analysis/caption_audit_zh.py` (character-rule audit with fixed Chinese and English term lists), `analysis/culture_judge.py` (post-hoc judge, not pre-registered), `analysis/pair_strips.py` (side-by-side strips for shared seeds). The atlas names for the five-cell atlas live in `archive/persistent_atlas_e2_names.json`; the E1 names file was restored after the atlas run rewrote it (its git-ignored centroid file now reflects the five-cell run, which only affects name carrying by nearest centroid).
- The face count is Claude's by eye and provisional. The judge's refusal to code apparent ethnicity is recorded verbatim above; no second judge was tried.
- MiniLM metrics for E2-QZ are not interpretable (English model) and are excluded from every verdict.

Figures: `e2_qz_vs_e1_both/{drift_dinov2.png, elbow.png, joint_clusters.jpg, endpoints_e2_qz.jpg, endpoints_e1_both.jpg}`, `persistent_atlas_e2/cluster_*.jpg`, `e2_qz/strips_people.jpg` (eight people seeds, steps 0–99, both cells), `e2_qz/faces_zoom_1..4.jpg`.

CLIP is used for steering only and does not appear in any number above.
