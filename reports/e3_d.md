# E3-D gate: the one-sentence theme bottleneck (Haiku done 2026-11-02; Mistral running)

Prediction D1: `predictions.md` "E3 follow-ups" (written 2026-11-01, before the E3-C cells ran). Metrics: `reports/e3/d_haiku.md` (joint atlas with the 50-word cell, the gate's procedure), `reports/e3/d_haiku_alone.md` (the D cell's own atlas and pair sharing), `d_haiku.json`, `d_haiku_alone.json`, `d_haiku.png`; cluster sheets `reports/e3/sw_cluster_e3_d_haiku_*.md` (joint) and `sw_cluster_e3_d_haiku_alone_*.md`. Script: `analysis/e3s_report.py --d1`. Loop: story → *"State the theme of this story in one sentence of 25 words or fewer. Do not mention any character's name or any place name."* → story (expand unchanged); seeds 0–19 × 100; step 0 copied from e3_1_haiku.

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

## Decision for Brad: should the one-sentence loop become the core text-loop model?

Recommendation: **no as the core, yes as the second instrument.** The reasons:

- D is the cheapest and clearest probe of a model's theme menu: five wells visible at 20 seeds, $1.30 and 45 minutes per model, against 100 seeds and no visible wells in the raw 50-word atlas. For mapping the default morals of Haiku, Sonnet, Mistral and Qwen side by side it is the right tool, and anonymised embedding should be its standard measurement.
- But D removes the loop. With a half-life of 1 there is no gravity, no escape and no memory curve to measure; the paper's claim that text loops follow Hintze's model at a different scale rests on the 50-word loop, where the seed decays over tens of steps, trajectories dwell in object-level wells, and the wells obey the birthday law. D's menu is what the loop falls toward; the 50-word cells show the falling.
- The two together are the paper: the 50-word 100-seed cell gives the wells and the law; D gives the menu those wells belong to. Keep the 50-word loop as the Hintze-faithful arm for the second Haiku sample and the Mistral and Qwen 100-seed cells, and run D (20 seeds) on each of those models as well, which adds about $1.30 or 45 laptop-minutes per model.

## Runs

| run | trajectories × steps | wall | s per trajectory-step | cost | notes |
|---|---|---|---|---|---|
| e3_d_haiku | 20 × 100 | 41 min | 1.1 | $1.10 | no crash or resume; 0 empty, 0 refusals (the D19 dialogue flag fired as usual, not used); 99% of theme sentences within 25 words |
| e3_d_mistral | 20 × 100 | running (laptop, ≈ 7.5 h) | | $0 | D1's Mistral clause (≥ 2 shared) graded when it finishes |

Smokes `e3_d_haiku_smoke` (2 × 3) and `e3_d_mistral_smoke` (2 × 2) passed. Theme judge on e3_d_haiku: 2,000 stories, Haiku, ≈ $0.9 (post-hoc row in `reports/e3/d_haiku.md`).

Deviation from the prediction text: none in procedure. The anonymised atlas and the dwell diagnostics are post-hoc and labelled as such; D1's verdict stands on the raw clauses as written.
