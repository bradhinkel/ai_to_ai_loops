# E3-S and E3-W gate: Haiku compress–expand on 100 seeds, and with a 20-word summary (2026-11-02)

Predictions: `predictions.md` "E3 scale and bottleneck width" (commit 96e15d6, clarified in 3faa37f before any result). Metrics and verdicts: `reports/e3/scale_width.md`, `scale_width.json`, `scale_width.png`; shared-cluster sheets `reports/e3/sw_cluster_*.md`. Script: `analysis/e3s_report.py`.

## Verdict

**Speculation 1 (text attractors exist but are more numerous than the image ones): holds.** S1 holds at its thresholds, S4 holds, S2 fails on one clause (half-life), S3 fails on one clause (within-0.15 share). At 100 trajectories the anonymised story atlas has 13 clusters shared by two or more trajectories, 30 sharing pairs of 4,950, and two wells visited by four trajectories each; the raw atlas (names kept) has 5 shared clusters where the 20-trajectory cell had 0. The sharing-pair count grows with the number of pairs, not the number of trajectories (per-pair rate 0.006 from n = 20 to n = 100), which is the fixed-well law. The implied well count is about 165 anonymised and about 1,000 raw: far more wells than the image loops' handful, each holding few trajectories.

**Speculation 2 (the 50-word summary is what holds a trajectory on its path): holds for the seed, fails for convergence.** W1 holds 3 of 8 clauses, W2 fails on one clause, W3 is monotone so far, W4 fails. Narrowing the summary to 20 words halves the seed half-life (11 to 5) and the own-seed trace at step 50 (0.45 to 0.20), but the freed trajectories do not move toward one another: nearest other-trajectory distance is unchanged (0.342 to 0.338), no raw cluster is shared, name cover falls (0.54 to 0.44), the summaries are more diverse (Vendi 13.1 to 14.6) and the conflict-type distribution flattens. Losing the seed faster does not produce convergence. The 30-word cell stays held.

## Cells

| cell | n | half-life | own seed at 10 / 50 / 99 | nn-other raw / anon | within 0.15 raw / anon | Vendi story / summary at 99 | words at 99 | summary words (≤ 20 / ≤ 50) | top-10 cover | top names 50–99 |
|---|---|---|---|---|---|---|---|---|---|---|
| e3_1_haiku (50 words, gate) | 20 | 11 | 0.60 / 0.45 / 0.20 | 0.342 / 0.262 | 0.000 / 0.004 | 9.5 / 13.1 | 502 | 50 (0.00 / 0.55) | 0.54 | Maya 200, Nora 55, Daniel 52, Priya 43, Mara 39 |
| e3_1_haiku_100 (E3-S) | 100 | 12 (1-in-100 task) | 0.57 / 0.29 / 0.13 | 0.314 / 0.243 | 0.002 / 0.013 | 21.6 / 37.9 | 512 | 48 (0.00 / 0.64) | 0.39 | Maya 412, Ruth 362, Mara 190, Tomas 178, Marcus 151 |
| e3_1w20_haiku (E3-W) | 20 | 5 | 0.55 / 0.20 / 0.15 | 0.338 / 0.266 | 0.000 / 0.004 | 9.6 / 14.6 | 488 | 20 (0.64 / 1.00) | 0.44 | Nora 77, Walt 57, Maya 48, Walter 48, Gerald 46 |

Half-lives at n = 100 are compared on 20-trajectory subsamples (median 26, IQR 17–30) and on the fresh sample of seeds 0–19 (18).

## E3-S: pair sharing at n = 100 (k 198, radius 0.15, hysteresis 1.25, dwell ≥ 5, ≥ 3 visits)

| atlas | persistent | shared (≥ 2 traj) | sharing pairs / pairs | per-pair rate | largest well (trajectories) | W-hat | steps inside |
|---|---|---|---|---|---|---|---|
| raw | 54 | 5 | 5 / 4,950 | 0.0010 | 2 | ≈ 990 | 0.25 |
| anonymised | 46 | 13 | 30 / 4,950 | 0.0061 | 4 | ≈ 165 | 0.24 |

Sharing pairs vs n (mean over 10 random subsamples, k scaled to 40 per 2,000 trajectory-steps):

| n | pairs | raw sharing pairs | anonymised sharing pairs | anonymised per-pair rate |
|---|---|---|---|---|
| 10 | 45 | 0.0 | 0.1 | 0.002 |
| 20 | 190 | 0.6 | 1.1 | 0.006 |
| 40 | 780 | 1.7 | 4.6 | 0.006 |
| 60 | 1,770 | 3.5 | 12.0 | 0.007 |
| 80 | 3,160 | 4.8 | 17.7 | 0.006 |
| 100 | 4,950 | 5.0 | 30.0 | 0.006 |

Random 20-trajectory subsamples (50 draws, k 40): median shared clusters 0 raw (IQR 0–0.75) and 1 anonymised (IQR 0.25–1); mean sharing pairs 0.34 raw, 1.38 anonymised. The 20-trajectory gate cell (0 raw, 1 anonymised in the joint gate atlas) is an ordinary draw from this distribution: nothing about the 20-seed cells was unlucky; 20 trajectories cannot see wells at this density.

- **S1 holds, at the thresholds.** Anonymised sharing pairs 30 (band 25–150), shared clusters 13 (≥ 10), largest well 4 (≥ 4), raw shared 5 (≥ 5). Subsamples reproduce the 20-trajectory cell (median 0 raw / 1 anonymised; predicted 0 / 0–2).
- **S2 fails on two clauses (half-life, modal tuple).** Fresh sample of seeds 0–19: half-life 18 (band 8–15; the first sample gave 11), top-10 cover 0.47 (band 0.45–0.65), Maya the top name again, 494 words (band 480–520), modal tuple young_adult × interpersonal × hopeful (0.10) against the first sample's young_adult × internal × hopeful (0.16); over all 100 seeds the modal tuple is young_adult × internal × hopeful again (0.09), in a near tie with its age-unclear twin. The modal tuple at a 10–16% share is not a stable statistic of a 20-trajectory sample; the field margins (woman, hopeful, death) are. Two samples of the same 20 seeds give half-lives 11 and 18: the half-life has roughly ± 5 of sampling variance, which the earlier model comparisons (Sonnet 45, Qwen 14, LLaVA 22, Mistral 22, Haiku 11) should be read against.
- **S3 fails on the within-0.15 clause.** Nearest other-trajectory distance 0.314 (band 0.26–0.32), but the share of late steps within 0.15 of another trajectory is 0.002 (band 0.01–0.05). The density shows at the atlas radius through dwell, not as a mass of steps under 0.15. The continuum condition (nn-other ≥ 0.33 and raw shared < 5) is not met.
- **S4 holds.** Same-seed trajectories of the two runs are closer at steps 50–99 than different-seed pairs (0.426 vs 0.492, gap 0.065; anonymised gap 0.028): the seed's trace outlives the embedding half-life by a factor of several. 1 of 20 same-seed pairs shares a persistent cluster in the joint atlas (predicted 0 or 1).

### What the shared wells are

The anonymised sheet (`reports/e3/sw_cluster_e3_1_haiku_100_anon.md`) reads as Brad's multidimensional attractors, each a conjunction of object, relation and resolution rather than an archetype:

- **A woman finds a shoebox of unopened or unsent letters from an estranged relative, and a reconciliation follows** (two wells of 4 trajectories each: trajectories 24, 30, 57, 80 and 24, 52, 57, 95; also 2 of the 5 raw wells). Counts of letters are always specific: thirty, forty-one, forty-three, 112, 211.
- **A late relative's ledger (of kindnesses or of debts) and a town that rallies** (two wells of 3: 16, 22, 71 and 71, 84, 93; a third of 3, with an embezzlement confession, 8, 20, 72).
- A sibling or parent returns to the family farm or cabin after an estrangement and repairs something with them (4, 61); a laid-off man hides it from his family for weeks in a library (63, 94); an unfinished melody or songbook of the dead relative, finished at the piano (12, 79); a footbridge the late father built, rebuilt (27, 91); a laptop dies before a deadline (5, 37); a grieving woman hears voices of the dead she must not answer (18, 97).

Under Haiku the wells are object-driven: a box of letters, a ledger, a map, a songbook, a bridge. The lead is a woman named Maya or Ruth about two-thirds of the time, the setting a home or a small town, the ending hopeful. The gate's Mistral well (the Amelia-and-Serenity town revival) is the same kind of thing.

## E3-W: 20-word summary (joint atlas with e3_1_haiku, k 40)

| atlas | width persistent (shared, pairs) | base persistent (shared, pairs) | clusters visited by both cells |
|---|---|---|---|
| raw | 8 (0, 0) | 12 (0, 0) | 5 |
| anonymised | 17 (2, 2) | 17 (1, 1) | 7 |

- **W1 fails (3 of 8 clauses).** Hold: half-life 5 (≤ 7), anonymised shared 2 (≥ 2), words 488 (480–520). Fail: nn-other 0.338 (≤ 0.30), within-0.15 0.000 (≥ 0.02), raw shared 0 (≥ 1), cover 0.44 (≥ 0.60), summary Vendi 14.6 vs 13.1 (predicted lower). The direction-if-wrong condition (half-life ≥ 9, nn-other ≥ 0.33, 0 shared) is not met either: the width is a lever on seed memory and on nothing else. The two anonymised shared wells are the letters-from-an-estranged-parent plot (14, 18) and music at a family funeral (12, 19).
- **W2 fails on one clause.** Median summary exactly 20 words (band 20–28) and no empties or refusals, but 64% of summaries are at or under 20 words (band 30–60%). Haiku keeps the 20-word limit better than it kept the 50-word one (55%).
- **W3 monotone so far.** Half-life 11 → 5 and nn-other 0.342 → 0.338 with width 50 → 20; raw shared 0 stays below D1's ≥ 3. The 30-word cell is held: with no convergence at 20 words there is nothing for 30 to sit between.
- **W4 fails.** Modal late tuple unclear × social_or_community × hopeful (0.11) vs the 50-word cell's young_adult × internal × hopeful (0.16): the lead's age becomes unreadable to the judge (unclear 0.32 → 0.45) and the conflict distribution flattens (internal 0.52 → 0.35, social_or_community 0.15 → 0.26, external_physical 0.06 → 0.15). The woman share (0.70) and the hopeful share (0.73) are identical in the two cells to two decimals. Width changes which plots appear, toward community and physical-danger plots, and does not concentrate them.

## Theme layer (Haiku judge, steps 50–99)

| cell | stories judged | modal tuple (share) | lead age unclear | conflict internal / interpersonal / social / external | woman | hopeful |
|---|---|---|---|---|---|---|
| e3_1_haiku | 1,995 | young_adult × internal × hopeful (0.16) | 0.32 | 0.52 / 0.26 / 0.15 / 0.06 | 0.70 | 0.73 |
| e3_1w20_haiku | 1,999 | unclear × social_or_community × hopeful (0.11) | 0.45 | 0.35 / 0.24 / 0.26 / 0.15 | 0.70 | 0.73 |
| e3_1_haiku_100 | 9,983 | young_adult × internal × hopeful (0.09; unclear × internal × hopeful 0.09) | 0.37 | 0.46 / 0.24 / 0.18 / 0.12 | 0.67 | 0.70 |
| e3_1_haiku_100, seeds 0–19 only | 1,983 | young_adult × interpersonal × hopeful (0.10) | | | 0.78 | 0.70 |

No tuple collapse at n = 100 either: effective number of (age × conflict × ending) tuples 32.6 at steps 1–10 and 34.4 at 50–99 (ratio 1.06; the gate's Sonnet ratio was 1.17 against a shuffle null of 1.11). The field-level drifts are the gate's, now on 100 seeds: death present 0.31 → 0.53 (Sonnet's gate cell went 0.29 → 0.51), home interior 0.15 → 0.30, bittersweet endings 0.13 → 0.24, institution settings 0.23 → 0.12; woman 0.65 → 0.67 and hopeful 0.73 → 0.70 are flat. The model's grain is in the fields and the objects, not in a collapsing tuple.

## Runs

| run | trajectories × steps | wall time | s per trajectory-step | parallel | 429 retries | cost | judge cost |
|---|---|---|---|---|---|---|---|
| e3_1_haiku_100 | 100 × 100 | 2 h 21 min | 0.8 | 12 | 40 | $6.55 | $4.72 (10,000 stories, 17 malformed answers) |
| e3_1w20_haiku | 20 × 100 | 42 min | 1.3 | 8 | 2 | $1.18 | $0.93 (1 malformed answer of 2,000) |

Both runs finished without a crash or a resume; no refusals or empty stories. Smokes: `e3_1_haiku_100_smoke` (100 × 2), `e3_1w20_haiku_smoke` (2 × 3). Config key added: `summary_word_limit` (the over-limit flag follows it; default 50, so earlier runs are unchanged). Step 0 of the 20-word cell is copied from e3_1_haiku (same model, same expand instruction; the runner checks both); step 0 of the 100-seed cell is fresh. Judge outputs are archived gzipped under `reports/e3/judge/`.

Deviations from the prediction text: none in procedure. k for the 100-trajectory atlas is 198 (40 per 2,000 trajectory-steps, rounded), stated as "k 200" in the prediction.

## Reading

Three results fit together. The wells are there and they obey the birthday arithmetic, so the 20-seed cells were not wrong, only small. The wells are many and narrow (about 165 after names are removed, about 1,000 with names), which is why no cell showed them with 20 trajectories and why "shallow" is the wrong word: a trajectory that enters the letters-in-a-shoebox well stays 20 to 70 steps. And the bottleneck's width governs how fast the seed is forgotten but not where the story goes afterwards: the freed trajectory falls into one of the many wells, not into a shared one. The remaining lever on the number of wells is abstraction (E3-D: a one-sentence theme with no names), which removes the objects and names that define Haiku's wells; whether the wells merge when the objects go is the next question. The other open question is whether the wells belong to the model: a 100-seed cell under a second model (Mistral on the laptop at no API cost, about 1.5 days; or Sonnet at about $30) would show whether the shoebox of letters is Haiku's or everyone's.

Nothing further has been started.
