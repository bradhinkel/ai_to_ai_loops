# E3 follow-ups A–C gate report (SPEC2 §4 E3 follow-ups, 2026-11-01); D held

Three follow-ups to the E3 gate (`reports/e3.md`, 2026-10-29: no shared attractors across trajectories in any text cell). Predictions: `predictions.md` "E3 follow-ups (2026-11-01)", written before any of these ran. A = anonymised re-embedding of the six existing cells; B = theme-layer coding of the same 12,000 stories by a judge outside the loop; C = new cells, the rewrite loop with an absolute length ("length about 500 words") under claude-haiku-5-5, and the two new models. Haiku's two C cells are finished and reported here; the Mistral cells and Qwen E3-2b are still running on the laptop (ETA 2026-11-02 morning) and get a section of their own when they land. D (the theme-bottleneck loop) has a prediction and no run; it waits for Brad.

**Gate: A1 fails as written, B1–B6 fail, B7 holds, C1 and C2 hold for Haiku, C4 fails on its theme clause. The three results agree on one picture. Names and places are about two-thirds of what keeps trajectories apart in MiniLM space, and once they are removed one or two plot-level clusters shared by two or three trajectories appear in every compress–expand cell, none under the matched null. But the theme layer does not collapse: the effective number of (age × conflict × ending) tuples does not fall under Sonnet and falls only mildly under the 7B models, no theme-sentence cluster is shared at the gate's radius, and each trajectory's theme stays traceable to its own seed for as long as its story does (theme-space half-life 40 / 11 / 18 steps for Sonnet / Qwen / LLaVA against 45 / 14 / 22 in story space). What is strong is the marginal grain, the model's default values field by field: a woman lead in 63–77% of late stories under the Claude models, a hopeful ending in 64–93% everywhere, present day, internal or community conflict, and under Sonnet's compress–expand loop a death in the story rising from 29% of early steps to 51% of late ones. Haiku adds the size axis: shorter seed memory (half-life 11 vs Sonnet's 45), a narrower name pool (top-10 cover 0.54 vs 0.40, "Maya" leading 200 of ~1,000 late stories), the field defaults sharper still (internal conflict 71%, home interior 44%), and a rewrite loop that is nearly the identity (631 verbatim copies in 1,980 steps; Sonnet made 2).**

## A. Anonymised re-embedding (`reports/e3/anon.md`, `anon_clusters.md`; `analysis/e3_anon.py`)

Names and places (the gate's per-cell name filter) replaced by "X"; MiniLM re-embedding; the gate's atlas procedure on original, anonymised and a null column where the same token budget of random non-name content words is replaced instead.

| cell | text | nn-other orig → anon / null | names-specific fall | shared persistent (≥ 2 traj) anon / null |
|---|---|---|---|---|
| e3_1_sonnet | summaries | 0.520 → 0.383 / 0.449 | 0.066 | 1 / 0 (estranged sisters reconcile after a funeral; a widow and a grieving child) |
| e3_1_sonnet | stories | 0.381 → 0.293 / 0.350 | 0.057 | 0 / 0 |
| e3_1_qwen | summaries | 0.450 → 0.328 / 0.403 | 0.075 | 2 / 0 (an elder revitalises a square or forest; wartime family letters found in an attic) |
| e3_1_qwen | stories | 0.369 → 0.264 / 0.341 | 0.077 | 0 / 0 |
| e3_1_llava | summaries | 0.440 → 0.313 / 0.408 | 0.095 | 1 / 0 (a small-town musical duo finds success) |
| e3_1_llava | stories | 0.409 → 0.305 / 0.374 | 0.069 | 1 / 0 (the same duo) |

A1 as written (fall ≥ 0.10, or any shared attractor in an E3-1 cell → names were the barrier): the largest total fall is 0.137 and the largest names-specific fall 0.096, and shared attractors appear in every E3-1 cell after anonymising, so **A1 fails as written**: names were a large part of the barrier. The clusters are the multidimensional conjunctions Brad predicted (a relationship, an event, a place type, a life stage), but weak: 1–2 per cell, 2–3 trajectories each, and the share of late steps within 0.15 of another trajectory stays ≤ 0.05 (captions: 0.36–0.51). Rewrite cells gain no shared cluster. Random-replacement null: fall 0.03–0.07, no shared cluster anywhere.

## B. Theme-layer coding (`reports/e3/theme.md`, `theme.json`, `theme_curves.png`, `codebook.md`, `handcode_sample.md`; `analysis/theme_judge.py`, `analysis/e3_theme_report.py`)

Judge claude-haiku-5-5 (effort low, default sampling, D16) read each of the 12,000 stories alone, with no seed, step or model, and filled the fixed schema (11 categorical fields, a free role, a one-sentence theme with no names). Second judge claude-sonnet-5-5 on a stratified 287; a Haiku repeat on the same 287 (post-hoc) for test-retest. Nothing the judge writes is fed back into any loop. Cost: Haiku $5.2 (18.6 M in / 6.6 M out tokens, 2.0 h at 16 concurrent calls), Sonnet $1.5, Haiku repeat $0.1. Malformed answers 34 of 12,000 (27 in one Sonnet E3-2 trajectory where the judge invented a secondary_character value), excluded.

| prediction | result | numbers |
|---|---|---|
| B1 collapse in E3-1 (eff. tuples late / early ≤ 0.5; modal late ≥ 0.25) | **fails** | ratio 1.17 Sonnet (shuffle null 1.11), 0.84 Qwen (null 1.10), 0.91 LLaVA (null 1.11); modal late 0.07 / 0.26 / 0.24 |
| B2 ≥ 2 shared theme attractors Sonnet, ≥ 1 Qwen, multidimensional | **fails** | 0 shared theme-sentence clusters in every cell; nn-other in theme space 0.40–0.57, none within 0.15 |
| B3 attractors belong to the model (modal tuples differ; JS across > within) | **fails** | Sonnet's modal tuple differs from both 7B models, but Qwen and LLaVA share one (unclear / none_or_unclear / hopeful) and their JS across (0.08) is below their within-model JS (0.15, 0.19) |
| B4 Sonnet place entropy ±20%; setting_time present ≥ 80% at 1–10 | **half** | place entropy +3% (holds); present_day 0.81 Sonnet E3-1, 0.75 E3-2, 0.53 Qwen, 0.65 LLaVA (fails) |
| B5 rewrite cells do not move (JS early–late ≤ 0.05; ≥ 90% hold step-1 tuple at 99) | **fails** | JS 0.061 / 0.073 / 0.147; hold 0.65 / 0.55 / 0.15 |
| B6 own step-0 tuple ≤ 0.5 by step 25; Sonnet > 0.2 at 99 | **fails** on the Sonnet clause | half-step 1 / 1 / 2; Sonnet 0.00 at 99 |
| B7 reliability (≥ 6 of 10 fields κ ≥ 0.6; gender, death ≥ 0.8; pronoun heuristic ≥ 0.85) | **holds** | 8 of 10 (setting_time 0.42, nature_central 0.58 below); lead_gender 0.90, death 0.85; heuristic 0.89 |

What the fields say. The per-field late-window modes (`theme.md`, second table) are the grain: woman 0.63 (Sonnet E3-1), 0.71 (E3-2), 0.68 (Qwen E3-1), 0.46 (LLaVA); hopeful 0.64–0.93; present_day where coded; internal conflict under Sonnet (0.43), social_or_community under Qwen (0.39); parent_or_grandparent the modal secondary character under Sonnet E3-1; death present rising 0.29 → 0.51 under Sonnet E3-1 and only there. These are the defaults the loop exposes, and they are model-level; they are not points the trajectories move toward together, because the effective number of tuples never falls and no two trajectories share a theme cluster.

Post-hoc checks (added after the verdicts were read; labelled so in `theme.md`):
- *lead_age is the weak field.* Haiku codes 'unclear' 0.60 of the subsample, Sonnet 0.38 (κ 0.62), so the predicted tuple is dominated by 'unclear' in the 7B cells. Tuple B (gender × conflict × ending; κ 0.90 / 0.79 / 0.63) tells the same story: ratio 1.25 Sonnet (null 1.05), 0.78 Qwen (null 1.06), 1.08 LLaVA; modal 0.15 / 0.27 / 0.11.
- *Judge noise is not the reason the tuples move.* Haiku test-retest on 287 stories: κ 0.78–0.94 by field (lead_age 0.86, conflict 0.88, ending 0.88). So the step-1 drop in own-tuple hold (0.65 of trajectories keep their coded age across the first compress–expand) is real: the categorical fields are labile from the first step while the gist is sticky.
- *The gist is the seed's.* Seed identification by theme sentence (own step-0 theme nearest among the 20): half-life 40 (Sonnet), 11 (Qwen), 18 (LLaVA), still at 0.41 / 0.15 / 0.35 at step 99; rewrite cells never fall below 0.95. The codebook draft (k-means k 20 over 240 theme sentences) groups by seed across models, not by model: the harbour-and-fog seed, the online-persona seed and the grieving-boy seed each form their own cluster with members from all three models at steps 1–95. A codebook built this way would be a seed list. The closed-codebook pass is therefore not run; the next useful codebook would come from late-window sentences only, or from the D loop.

Hand-coding: `reports/e3/handcode_sample.md` holds 48 stories for Brad with the schema; the judge's answers are in `analysis/cache/e3_handcode_key.json`, not in the sample.

## C. Absolute-length rewrite and the new models (`reports/e3/c.md`, `c.json`, `c_curves.png`, `c_cluster_NN.md`; `analysis/e3c_report.py`)

Haiku cells finished 2026-11-01 (e3_1_haiku 46 min, 1.4 s per trajectory-step at 8 concurrent calls, $1.29; e3_2b_haiku 21 min, 0.6 s, $1.24; no crash, no resume; smokes `e3_1_haiku_smoke`, `e3_1_mistral_smoke` kept). Haiku rejects `temperature` like Sonnet (D16). Mistral E3-1 on the laptop runs at 16 s per trajectory-step (~9 h), then E3-2b Mistral and E3-2b Qwen.

| cell | half-life | own seed at 10 / 50 / 99 | dist from step 1 at 99 | persistent (shared) | nn-other | self-share 50–99 | words at 99 median (min–max) | copies | top-10 cover |
|---|---|---|---|---|---|---|---|---|---|
| e3_1_haiku | 11 | 0.60 / 0.45 / 0.20 | 0.487 | 8 (0) | 0.342 | 0.66 | 502 (399–576) | 0 | 0.54 (Maya 200, Nora 55, Daniel 52) |
| e3_2b_haiku | > 99 | 1.0 / 1.0 / 1.0 | 0.093 | 0 (0) | 0.451 | 1.00 | 556 (447–625) | **631** | 0.59 |
| e3_1_sonnet (gate) | 45 | 0.90 / 0.45 / 0.35 | 0.448 | 0 (0) | 0.381 | 0.49 | 558 | 0 | 0.40 |
| e3_2_sonnet (gate) | > 99 | | 0.274 | 0 (0) | 0.468 | 0.88 | 533 | 2 | 0.56 |

| prediction | result | numbers |
|---|---|---|
| C1 absolute target removes the length drift (Haiku 450–550 at 99) | **holds** E3-1, **misses** E3-2b by 6 words | 502; 556 (length ratio 1.14, creeping up, not down) |
| C2 rewrite results reproduce (half-life > 99; distance at 99 below E3-1; no shared attractor; self-share ≥ 0.85) | **holds** | > 99; 0.093 vs 0.487; 0; 1.00 |
| C4 size axis (half-life ≤ 30; top-10 cover ≥ 0.5; 500 words; modal tuple = Sonnet's on ≥ 2 of 3 fields) | **holds** on size, **fails** on the tuple | 11; 0.54; 502 / 556; modal unclear / internal / hopeful vs Sonnet's young_adult / interpersonal / hopeful (1 of 3); tuple B woman / internal / hopeful (0.45) vs Sonnet's woman / interpersonal / hopeful (2 of 3) |

The rewrite loop under Haiku is a copy machine with the shrinkage gone: step-to-step drift 0.01 (Sonnet E3-2 0.05–0.07), one third of all steps byte-identical to the previous one, concentrated in trajectories (91, 92, 75, 74, 70 copies of 99 in five of them), length drifting up to 556. The absolute target did what it was for under Haiku; whether it does under the 7B models is the Mistral and Qwen question. Haiku E3-1 has eight persistent attractors, every one a single trajectory's well (a general store in Harlow Creek, a violinist freezing on stage, a county finance worker finding shell vendors), 27% of steps inside, nn-other 0.342: slightly closer across trajectories than Sonnet (0.381) or Qwen (0.369), still far above the caption cells. Haiku's late fields are sharper than Sonnet's: woman 0.77, internal conflict 0.71, home_interior 0.44, parent_or_grandparent 0.30, death present 0.59. Haiku's summaries run over 50 words 45% of the time (Sonnet 14%).

C3 (Mistral) and the Qwen and Mistral parts of C1–C2 are open until the laptop queue finishes.

## Deviations and notes
- D16 applies to Haiku (temperature rejected; `temperature_applied: false` in every record). The Haiku configs carry the Ollama `digest_prefix`/`host` keys from the template; the backend is `anthropic` and they are unused.
- `story_meta.flags.refusal` fires on dialogue as in D19 (368 in e3_1_haiku, 100 in e3_2b_haiku; all calls `end_turn`); not used.
- E3-C is reported by a new script rather than by `e3_report.py`, whose cells and verdicts are hard-coded to the six gate cells; the atlas in `c.md` is a joint k-means over the C cells only, so cluster counts are not pooled with the gate's.
- Post-hoc analyses (tuple B, test-retest, theme-space memory) are labelled as such in `theme.md` and here; no prediction was edited.

## What this means for D
The question D asks, whether destroying the specifics every step (theme sentence as the bottleneck) produces the cross-seed convergence the 50-word summary did not, is sharper after A–C: names were most of the barrier (A), the theme layer does not converge on its own (B), and the seed's gist survives a 50-word summary for 11–40 steps (B post-hoc). D1 as written (≥ 3 shared attractors under Haiku, half-life ≤ 10, nn-other ≤ 0.30) is the direct test, and the judge's theme sentences from B are a free preview of its input distribution. Held for Brad's call.
