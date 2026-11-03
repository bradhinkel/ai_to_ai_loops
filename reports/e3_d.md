# E3-D gate: the one-sentence theme bottleneck (Haiku 2026-11-02, Mistral 2026-11-03)

Prediction D1: `predictions.md` "E3 follow-ups" (written 2026-11-01, before the E3-C cells ran). Metrics: `reports/e3/d_haiku.md` and `d_mistral.md` (joint atlas with the model's 50-word cell, the gate's procedure), `d_haiku_alone.md` and `d_mistral_alone.md` (the D cell's own atlas and pair sharing), the matching `.json` and `.png`; cluster sheets `reports/e3/sw_cluster_e3_d_<model>_*.md` (joint) and `sw_cluster_e3_d_<model>_alone_*.md`. Script: `analysis/e3s_report.py --d1`. Loop: story → *"State the theme of this story in one sentence of 25 words or fewer. Do not mention any character's name or any place name."* → story (expand unchanged); seeds 0–19 × 100; step 0 copied from e3_1_haiku.

## Verdict (Haiku)

**D1 fails as written, 2 of 4 clauses, and the direction it predicted is the strongest effect seen in any text cell.** Holds: seed half-life 1 (≤ 10; the 50-word cell's is 11) and median nearest other-trajectory distance 0.208 (≤ 0.30; was 0.342). Fails: raw story clusters shared by ≥ 2 trajectories 0 (≥ 3), and theme-sentence Vendi at step 99 6.8 against a threshold of 6.6 (half of the 50-word summaries' 13.1). The two failures have one cause, described below, and the anonymised atlas shows what the raw one cannot: 7 shared wells visited by 2 to 5 trajectories each, 35 sharing pairs of 190 (rate 0.18, thirty times the 50-word cell's 0.006 at n = 100), an implied well count of about 5, and 18% of late steps within 0.15 of another trajectory's step with names kept (32% without). Abstraction does what width did not.

| measure | 50-word cell | 20-word cell | one-sentence theme (D) |
|---|---|---|---|
| seed half-life | 11 | 5 | 1 |
| own seed identified at step 10 / 50 | 0.60 / 0.45 | 0.55 / 0.20 | 0.15 / 0.10 |
| nn-other, raw / anonymised | 0.342 / 0.262 | 0.338 / 0.266 | 0.208 / 0.170 |
| late steps within 0.15 of another trajectory, raw / anon | 0.000 / 0.004 | 0.000 / 0.004 | 0.177 / 0.316 |
| shared clusters, own atlas k 40, raw / anon (sharing pairs of 190) | 0 / 0 (0 / 0) | 0 / 2 (0 / 2) | 0 / 7 (0 / 35) |
| story Vendi at 99 / bottleneck-text Vendi at 99 | 9.5 / 13.1 | 9.6 / 14.6 | 6.9 / 6.8 |
| words at 99 | 502 | 488 | 456 |
| bottleneck text, median words (share within limit) | 50 (0.55) | 20 (0.64) | 19 (0.99) |
| top-10 lead-name cover 50–99 (top name) | 0.54 (Maya 200) | 0.44 (Nora 77) | 0.53 (Daniel 131) |
| hopeful endings 50–99 (judge) | 0.73 | 0.73 | 0.80 |
| modal (age × conflict × ending) tuple 50–99, share | young_adult × internal × hopeful, 0.16 | unclear × social × hopeful, 0.11 | middle_aged × interpersonal × hopeful, 0.28 |

### Why the raw atlas is empty: D has no memory, so it has no dwell

The persistent-visit rule (a trajectory inside a 0.15-radius cluster for ≥ 5 consecutive steps) assumes the loop carries the story from step to step. The 50-word loop does: each trajectory visits about 2 clusters in 100 steps with a median dwell of 4–5 steps. The theme loop does not: each trajectory visits about 12 clusters with a median dwell of 1 (raw) or 2 (anonymised), and two-thirds of raw steps are outside every cluster. A 25-word moral with no names re-rolls the plot every step (seed half-life 1 means even the previous story barely survives), so consecutive stories are different plots on the same moral, with different lead names (Daniel, Maya, Ruth, Thomas, Marcus), and the raw embeddings hop between neighbouring centroids. Anonymising removes the name hop and the dwell appears. The Vendi clause misses by 0.2 for the same reason: the theme sentences are near-paraphrases of about five morals, and MiniLM counts paraphrases as partly distinct.

What D converges to is therefore a **stationary distribution**, not a set of wells with gravity. In the image loops and in the 50-word text loop a trajectory falls into a well and stays; in D every trajectory draws each step from the same small menu. Both are "the model's defaults under minimal constraint", but only the first is an attractor in Hintze's sense.

### The menu (anonymised joint atlas, `sw_cluster_e3_d_haiku_anon.md`)

- **Grief is eased by small kindnesses from a community** (8 trajectories, 14 persistent visits).
- **Estranged siblings reconcile through shared grief; pride gives way to humility and honesty** (7 trajectories; a second pride-and-reconciliation well with 5, a third with 3).
- Kindness ripples outward through strangers (3); a shared crisis dissolves old grudges between neighbours (3); grief softens through family rituals and shared memory (3).

Every step-99 theme sentence of the 20 trajectories is one of these. The judge's schema shows the same concentration from the other side (post-hoc, all 2,000 stories): the modal tuple middle_aged × interpersonal × hopeful covers 0.28 of late stories against 0.16 in the 50-word cell, the first tuple concentration seen in any text cell; interpersonal conflict 0.58 (was 0.26), home interior 0.58 (was 0.28), a sibling as the second character 0.53, a death present in 0.68, a reconciliation in 0.61, hopeful endings 0.80 (was 0.73), woman leads 0.75. This is the moral layer under the object-level wells of the 100-seed cell: the shoebox of letters, the ledger and the unfinished melody are all instances of "estrangement healed through grief and humility" or "a community's kindness".

## Verdict (Mistral)

**D1's Mistral clause fails on the raw-shared count and holds on the other three, and the picture is the Haiku one with a narrower menu.** Holds: seed half-life 2 (was 22), median nearest other-trajectory distance 0.223 (was 0.330), theme-sentence Vendi at step 99 5.5 against a threshold of 6.1 (half of the 50-word summaries' 12.2). Fails: raw story clusters shared by ≥ 2 trajectories 0 (≥ 2). Own anonymised atlas: 8 shared wells, 39 sharing pairs of 190 (rate 0.21; the 50-word Mistral cell has 1 pair), one well visited by 6 of the 20 trajectories, implied well count about 5; 11% of late steps within 0.15 of another trajectory's step with names kept, 36% without. In the joint atlas 4 of the D wells are also visited by the 50-word Mistral cell, so Mistral's theme menu and its 50-word wells (Meadowgrove, the artist who revives the town) are the same places seen at two depths.

| measure | Mistral 50-word | Mistral theme (D) | Haiku 50-word | Haiku theme (D) |
|---|---|---|---|---|
| seed half-life | 22 | 2 | 11 | 1 |
| own seed identified at step 10 / 50 | 0.85 / 0.30 | 0.30 / 0.05 | 0.60 / 0.45 | 0.15 / 0.10 |
| nn-other, raw / anonymised | 0.330 / 0.220 | 0.223 / 0.171 | 0.342 / 0.262 | 0.208 / 0.170 |
| late steps within 0.15 of another trajectory, raw / anon | 0.000 / 0.019 | 0.111 / 0.361 | 0.000 / 0.004 | 0.177 / 0.316 |
| shared clusters, own atlas k 40, raw / anon (sharing pairs of 190) | 0 / 1 (0 / 1) | 0 / 8 (0 / 39) | 0 / 0 (0 / 0) | 0 / 7 (0 / 35) |
| largest number of trajectories in one anonymised well | 2 | 6 | 1 | 5 |
| story Vendi at 99 / bottleneck-text Vendi at 99 | 9.1 / 12.2 | 7.3 / 5.5 | 9.5 / 13.1 | 6.9 / 6.8 |
| words at 99 | 388 | 419 | 502 | 456 |
| bottleneck text, median words (share within limit) | 58 (0.24) | 24 (0.56) | 50 (0.55) | 19 (0.99) |
| clusters visited per trajectory / median dwell, raw | 2 / 15 | 7 / 1 | 2 / 4 | 12 / 1 |
| free steps (outside every cluster), raw | 0.15 | 0.74 | 0.28 | 0.66 |
| modal (age × conflict × ending) tuple 50–99, share | unclear × social × hopeful, 0.33 | same, 0.42 | young_adult × internal × hopeful, 0.16 | middle_aged × interpersonal × hopeful, 0.28 |
| effective tuples 50–99 | 4.6 | 4.2 | 15.3 | 7.8 |

The dwell diagnosis is the same: the 50-word Mistral loop visits 2 clusters per trajectory with a median dwell of 15 steps; the theme loop visits 7 with a median dwell of 1 and three-quarters of raw steps outside every cluster. Mistral keeps slightly more than Haiku across the bottleneck (half-life 2, not 1; anonymised dwell ≥ 5 in 18% of visits against 14%), which shows in the sheets as long anonymised stays (one trajectory inside the tyranny well for 60 of 100 steps), but the loop is still a stationary draw, not a descent. Mistral also ignores the 25-word limit more often (44% over, median 24, up to 36 words) and writes "Theme:" as a title line in some steps.

### The Mistral menu (`sw_cluster_e3_d_mistral_alone_anon.md`)

- **The transformative power of art and community revives a decaying town** (five of the eight wells are paraphrases of this one moral: 6, 6, 5, 5 and 4 trajectories; the "Brushstrokes of Revival / Hope / Renewal" stories, Meadowgrove, Elderglen, Harmonyville).
- The healing power of music rebuilds a shattered city (4); unity and rebellion overcome tyranny and the people rebuild their city (3 + 2); a wasteland village is restored by survivors (3, joint atlas).

Fourteen of the twenty step-99 theme sentences are the first moral; the rest are resilience-and-unity variants of it. The judge sees the same thing from the schema side: an artist or craftsperson lead in 0.50 of late stories (0.26 in the 50-word cell), a small-town setting 0.63 (0.28), social-or-community conflict 0.59 (0.39), hopeful endings 0.98, no interpersonal conflict and no sibling in either Mistral cell, death present 0.07. Where Haiku's menu is domestic (grief, estranged siblings, a kitchen table), Mistral's is civic (a town, a mural, a festival). The two models' default morals do not overlap at all.

| judge field, steps 50–99 | Mistral 50-word | Mistral D | Haiku 50-word | Haiku D |
|---|---|---|---|---|
| interpersonal conflict | 0.00 | 0.00 | 0.26 | 0.58 |
| social or community conflict | 0.39 | 0.59 | 0.15 | 0.11 |
| internal conflict | 0.03 | 0.01 | 0.52 | 0.28 |
| setting home interior | 0.01 | 0.01 | 0.28 | 0.58 |
| setting small town or rural | 0.28 | 0.63 | 0.27 | 0.21 |
| setting city | 0.39 | 0.24 | 0.11 | 0.08 |
| sibling as second character | 0.00 | 0.00 | 0.02 | 0.53 |
| lead is an artist or craftsperson | 0.26 | 0.50 | 0.10 | 0.01 |
| death present | 0.10 | 0.07 | 0.43 | 0.68 |
| reconciliation present | 0.05 | 0.12 | 0.26 | 0.61 |
| nature central | 0.39 | 0.29 | 0.23 | 0.14 |
| hopeful ending | 0.88 | 0.98 | 0.73 | 0.80 |
| woman lead | 0.34 | 0.47 | 0.70 | 0.75 |

## Decision for Brad: should the one-sentence loop become the core text-loop model?

Recommendation, unchanged by the Mistral half: **no as the core, yes as the second instrument.** The reasons:

- D is the cheapest and clearest probe of a model's theme menu: five wells visible at 20 seeds, $1.30 and 45 minutes per model on the API or 7 laptop-hours for a 7B model, against 100 seeds and no visible wells in the raw 50-word atlas. On both models it gave the same kind of answer (a short menu of morals, no memory) and a different menu, which is what a per-model probe should do. For mapping the default morals of Haiku, Sonnet, Mistral and Qwen side by side it is the right tool, and anonymised embedding should be its standard measurement.
- But D removes the loop. With a half-life of 1 there is no gravity, no escape and no memory curve to measure; the paper's claim that text loops follow Hintze's model at a different scale rests on the 50-word loop, where the seed decays over tens of steps, trajectories dwell in object-level wells, and the wells obey the birthday law. D's menu is what the loop falls toward; the 50-word cells show the falling.
- The two together are the paper: the 50-word 100-seed cell gives the wells and the law; D gives the menu those wells belong to. Keep the 50-word loop as the Hintze-faithful arm for the second Haiku sample and the Mistral and Qwen 100-seed cells, and run D (20 seeds) on each of those models as well, which adds about $1.30 or 45 laptop-minutes per model.

## Runs

| run | trajectories × steps | wall | s per trajectory-step | cost | notes |
|---|---|---|---|---|---|
| e3_d_haiku | 20 × 100 | 41 min | 1.1 | $1.10 | no crash or resume; 0 empty, 0 refusals (the D19 dialogue flag fired as usual, not used); 99% of theme sentences within 25 words |
| e3_d_mistral | 20 × 100 | 6 h 59 min (laptop, Ollama, parallel 2) | 12.2 | $0 | no crash or resume; 4 refusal flags, all D19 dialogue false positives; 44% of theme sentences over 25 words (median 24, max 36) |

Smokes `e3_d_haiku_smoke` (2 × 3) and `e3_d_mistral_smoke` (2 × 2) passed. Theme judge (Haiku, post-hoc): e3_d_haiku 2,000 stories ≈ $0.9; e3_d_mistral 2,000 stories 22 min, $0.96, 2 malformed responses retried, 0 missing. Judge records archived under `reports/e3/judge/e3_d_<model>.theme_judge.jsonl.gz`.

Deviation from the prediction text: none in procedure. The anonymised atlas and the dwell diagnostics are post-hoc and labelled as such; D1's verdict stands on the raw clauses as written.
