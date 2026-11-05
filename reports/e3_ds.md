# E3-DS gate: Sonnet theme-bottleneck cell (2026-11-05)

Prediction: predictions.md "E3-DS" (written 2026-11-05 before the run). Cell `e3_d_sonnet`: the E3-D loop (one-sentence theme ≤ 25 words,
no names) on claude-sonnet-5-5, Hintze seeds 0–19 × 100 steps, step 0 copied from `e3_1_sonnet`. Run 08:57–10:07 PST, 71 min, 41 s per step
(2.1 s per trajectory-step at parallel 8), no crash or resume. Cost: run $25.69, Haiku theme judge $0.90, Haiku moral judge $0.21
(plus $0.16 for the same judge on `e3_d_haiku`, run for comparison) = $27.0. Measurement files: `reports/e3/ds.{md,json}`
(`analysis/e3ds_report.py`), `reports/e3/d_sonnet.*` and `d_sonnet_alone.*` (`analysis/e3s_report.py --d1`), sheets
`reports/e3/sw_cluster_e3_d_sonnet{,_alone}_{raw,anon}.md`, hand read `reports/e3/ds_handread.md` (recorded before the moral-judge shares),
judge archives `reports/e3/judge/e3_d_sonnet.{theme,moral}_judge.jsonl.gz` and `e3_d_haiku.moral_judge.jsonl.gz`.

## Verdict

**DS1 holds, DS2 fails on two of six clauses, DS3 fails on two of four, DS4 fails.** Brad's within-family claim is the one that held, and
it held by a wide margin: the Haiku moral judge places 0.82 of Sonnet's late theme-loop stories on one of Haiku D's five morals (needs
≥ 0.5; Haiku's own 50-word stories fit at 0.53), four of the five morals are each above 0.10, and the hand read made before the judge shares
put three of Sonnet's top five morals in Haiku's five. The clauses that failed are about degree, not kind: Sonnet spreads its stories more
evenly over the menu than Haiku does (top moral 0.40 against Haiku's 0.52, five single-trajectory morals; pair-sharing rate 0.068
against 0.184, W-hat 14.6 against 5.4), and its judge shape is domestic but a step less so (hopeful 0.72, family secondary 0.34). My DS4 addition failed as the hand read expected: the morals Sonnet has
that Haiku lacks are "accepting help is not weakness" and "unseen care needs no recognition", not confession.

| clause | needs | Sonnet D | Haiku D | Mistral D | verdict |
|---|---|---|---|---|---|
| DS1 judge fit to Haiku's five morals (late stories) | ≥ 0.50 | **0.82** | 0.89 (own menu) | ≈ 0 by construction (civic) | holds |
| DS1 morals above 0.10 | ≥ 2 | 4 (H3 0.40, H1 0.17, H5 0.15, H2 0.11; H4 0.00) | | | holds |
| DS1 hand-read top-five overlap | ≥ 2 | 3 (S1↔H3, S2↔H1/H5, S4↔H2) | | | holds |
| DS2 seed half-life | ≤ 3 | 1 | 1 | 2 | holds |
| DS2 raw median dwell | 1 | 1 | 1 | 1 | holds |
| DS2 clusters per trajectory (raw) | 7–12 | **6** | 12 | 7 | fails |
| DS2 free steps (raw) | ≥ 0.6 | 0.75 | 0.66 | 0.74 | holds |
| DS2 anonymised shared wells (k 40) | ≥ 5 | 5 | 7 | 8 | holds |
| DS2 pair-sharing rate (anon) | 0.10–0.30 | **0.068** (13 of 190; W-hat 14.6) | 0.184 (W-hat 5.4) | 0.205 (W-hat 4.9) | fails |
| DS3 interpersonal + internal conflict | ≥ 0.6 | 0.71 | 0.85 | 0.01 | holds |
| DS3 home interior + small town | ≥ 0.5 | 0.54 | 0.67 | 0.62 | holds |
| DS3 hopeful ending | ≥ 0.8 | **0.72** | 0.80 | 0.98 | fails |
| DS3 family secondary character | ≥ 0.4 | **0.34** | 0.71 | 0.07 | fails |
| DS4 confession rule on late sentences | ≥ 0.15 | 0.13 | 0.24 | 0.00 | fails |
| DS4 confession share among "none" stories | ≥ 0.5 | 0.27 | | | fails |

D1 from the E3 follow-ups, graded for completeness by `e3s_report.py --d1`: fails 2 of 4 as for Haiku D (raw shared 0 vs ≥ 2; half-life 1 holds;
nn-other 0.227 holds; theme Vendi 7.5 vs ≤ 7.0 fails by half a unit).

## What the Sonnet menu is

Haiku's five morals, with Sonnet's weights. The judge's shares over 1,000 late stories: kindness ripples outward through strangers and
returns to the giver (H3) 0.40; grief eased by small kindnesses from a community (H1) 0.17; grief softened by family ritual and shared
memory (H5) 0.15; estranged relatives reconciled when pride gives way to humility and honesty (H2) 0.11; a shared crisis dissolves old
grudges between neighbours (H4) 0.00; none of the five 0.17. The "none" stories are not scattered: trajectory 8 (an unseen keeper whose
reward is the uneventful day) accounts for 50 of 175, trajectory 7 (science combined with inherited local knowledge, then working with
nature) 37, trajectory 3 (accepting help is belonging) 25, trajectory 1 (honest self-disclosure renews a long marriage) 18, trajectory 16
(restitution and confession that ask nothing) 18. So the Sonnet additions are three single-trajectory morals plus the apology-that-asks-nothing
variant of H2, and H4 is the one Haiku moral Sonnet never reaches.

The judge is Haiku scoring Sonnet against Haiku's menu, so a high fit could in principle be the judge's own bias. Two checks against that:
Mistral D's late sentences match the confession rule and the grief words at 0.00 and ≈ 0 (its menu is civic and the same judge would have
nothing to assign), and the hand read, made from the Sonnet sentences alone before the judge shares, reached the same three-of-five overlap.

## Where Sonnet's theme loop differs: a wider, flatter menu, not a stickier one

Both theme loops re-roll the plot every step (half-life 1, raw median dwell 1) and both hold the moral per trajectory. The same Haiku
moral judge on Haiku D's own late stories (run for this comparison, $0.16) fits its own five morals at 0.89, with H2 (estranged relatives
reconciled through humility) at 0.52 and rising from 0.41 in steps 50–74 to 0.63 in 75–99; the median Haiku trajectory has 0.79 of its late
stories on one moral, 16 of 20 trajectories ≥ 0.6 and 10 ≥ 0.8 (five trajectories at 50 of 50). Sonnet: median 0.69, 12 of 20 ≥ 0.6, 7 ≥ 0.8
(trajectories 4, 8 and 15 at 50 of 50). So the E3-D gate's phrase "no memory" needs the qualifier it now gets: the theme loop has no plot
memory and a strong moral memory; the dwell of 1 is at the embedding level, where a new plot with new names moves the story each step.

That is what sets Sonnet's lower pair-sharing rate: not stickiness (Haiku is the stickier of the two) but a flatter menu. Haiku parks
half its trajectories on one moral, so many pairs meet in that well; Sonnet's top moral carries 0.40 and five morals are held by one
trajectory each (unseen care, science with local knowledge, accepting help, honest self-disclosure, restitution), which cannot form a shared
well in a cell of 20. The anonymised atlas shows the spread as long stays in five different wells (trajectory 6 inside one grief well for
37 of 100 steps, trajectory 5 for 32) and 6 clusters per trajectory against Haiku's 12. The Sonnet menu is also not quite stationary: H3's
share rises from 0.33 in steps 50–74 to 0.47 in 75–99 while H1 falls from 0.22 to 0.12, so "kindness ripples and returns" is a slow
attractor within the menu, as it was the largest D-menu family in the 50-word Haiku cells; in Haiku D the slow attractor is H2.

For Brad's scale speculation this is one data point in the predicted direction, at the theme layer and at n 20: W-hat Mistral 4.9 <
Haiku 5.4 < Sonnet 14.6, and with the stickiness alternative ruled out the higher W-hat is a wider menu. The 50-word layer at 100 seeds is
where the speculation is stated and it is still unmeasured for Sonnet.

## Judge shape

Sonnet D is domestic in kind and less so in degree than Haiku D: conflict internal 0.53 + interpersonal 0.18 (Haiku interpersonal 0.58 +
internal 0.28), setting home interior 0.42 + city 0.28 (Haiku home 0.58), secondary character stranger 0.31 + friend 0.22 + sibling 0.14
(Haiku sibling 0.53), lead a woman 0.82, older adult the modal age, death present 0.60, reconciliation 0.26 (Haiku 0.61), hopeful 0.72.
Nothing of Mistral D's shape (social conflict 0.15 vs 0.59; artist lead 0.02 vs 0.50). The kindness-ripples moral, with its strangers and
its city, is what pulls the family-and-home shares under the DS3 thresholds; the thresholds were set from Haiku D's sibling-heavy
reconciliation menu, and Sonnet's version of the same menu weights the stranger moral higher.

## Decision rule and what this gate changes

The decision rule in the prediction keys on DS1 and DS3 together. DS1 holds and DS3 fails on degree, so the exhibit for the credit requests
should say exactly that: Claude models share a domestic moral menu across scale (0.82 of Sonnet's theme-loop stories land on Haiku's five
morals; the 7B models' menus are civic and share none of them), with Sonnet weighting the stranger-kindness moral higher and holding a
moral longer per trajectory; the ask is the 100-seed cells on Sonnet, Opus and Fable to measure W-hat against scale at the 50-word layer,
where the gravity and the birthday law live. Measurement notes for later cells: (1) the per-trajectory moral concentration (share of late
stories on the trajectory's modal moral) is the memory measure for D cells and goes next to the dwell diagnostic, which only sees plots;
(2) a D cell's pair-sharing rate measures how evenly the menu is used, so W-hat is the comparable number across models; (3) the story refusal flag fired on 425 of 2,000 Sonnet stories,
all dialogue containing "I'm sorry" or "I can't" (DEVIATIONS D19), none a refusal.

## Runs

| run | model | trajectories × steps | wall | s per trajectory-step | crash / resume | cost |
|---|---|---|---|---|---|---|
| e3_d_sonnet | claude-sonnet-5-5, effort low, default sampling (temperature rejected, D16) | 20 × 100 | 71 min | 2.1 | none | $25.69 |
