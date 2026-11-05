# E3-S7B: 100-seed Mistral and Qwen cells against predictions.md "E3-S7B" (2026-11-03)

Pooled Haiku reference: ('e3_1_haiku_100', 'e3_1_haiku_100b'), anonymised, k 396, 51 shared wells. Atlas rules as E3-S. Exclusion rule applied before the atlas.

## e3_1_mistral_100: 100 of 100 trajectories kept (0 degenerate)

**M1 (same level as Haiku): fails** — anon rate 0.0178 (88 of 4950; band 0.003–0.012), shared wells 35, max multiplicity 4, W-hat 56, raw shared 4; no-wells clause False, D-like clause False.
**M2 (different themes): holds** — 0 trajectories dwell in a Haiku well (wells []), median late distance to the nearest Haiku shared well 0.457 (≥ 0.35), inside any Haiku persistent cluster late 0.000; judge max share difference vs Haiku None (fields ≥ 0.15: None).
**M3 (Claude's alternative)** — rate in 0.01–0.03: True; W-hat ≤ 100: True; excluded 0; half-life None.
**M4 (cross-model seed trace vs Haiku A): holds** — same-seed pairs sharing a joint well 0 of 100 (≤ 2), late-distance gap -0.023 (< 0.02).

