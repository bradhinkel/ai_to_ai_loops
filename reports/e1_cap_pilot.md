# E1-cap pilot (SDXL + Qwen2.5-VL 7B, CLIP-77 clip): 20 trajectories × 100 steps

Run `e1_cap_pilot`, RunPod RTX Pro 6000, `configs/e1_cap_runpod96.yaml` (batch 16, 8 caption slots), 2026-10-19 05:13–06:50 pod time, one process, no restarts, 2,000 of 2,000 records, pulled to the laptop. Figures: `reports/e1_cap_pilot/` (a0_report) and `reports/e1_cap_pilot_vs_a0/` (e1_report against the A0-core archive). Not a SPEC gate; a pre-check for the core and the first look at H3.

**Verdict: the loop runs cleanly and converges; the core goes ahead (queued third behind the two Hunyuan cells).**

| | E1-cap pilot (n = 20) | A0-core (n = 100) | A0-pilot (n = 20) |
|---|---|---|---|
| Plateau step (MiniLM caption drift) | 14 | 16 | 26 |
| Last-20 mean step drift | 0.203 | 0.164 | – |
| Knee k, MiniLM / DINOv2 (kmax 19 at n = 20) | 9 / 10 | 7 / 8 | 8 / 8 |
| Subsample knee range, MiniLM / DINOv2 | 7–9 / 8–10 | 6–10 / 5–9 | 6–8 / 7–9 |
| Vendi (DINOv2 endpoints) | 11.8 | 31.8 | – |
| Share of endpoints inside A0 cluster radii (DINOv2) | **0.45** | 0.92 (its own radii) | – |
| Throughput per trajectory-step | 2.8 s (SDXL 1.9, Qwen 0.9) | 2.5 s | – |

## Captions and the clip (the side prediction)
- 37.4 words mean, 36 median, max 92; 179 of 1,980 captions (9%) over 50 words. Qwen largely obeys the instruction; LLaVA in A0-core averaged 139.
- The CLIP-77 clip fired on **75 of 1,980 prompts (3.8%)** versus 98.3% in A0-core. Median prompt 50 CLIP tokens, p90 68. The side prediction (clip rarely fires in the Qwen cells) holds.
- 0 empty, 0 refusals, 0 length cut-offs, 0 retries.

## Endpoints (`contact_endpoints.jpg`, MiniLM k = 10)
Pastel, soft-light images throughout. The largest basin (6 of 20) is new: bare silhouetted trees on small islands mirrored in still water under a lavender sunset. Palatial interiors survive in a Qwen form: gilded ballrooms with set tables (2) and luxury bathrooms in emerald, pink or gold marble (4). Singletons: hooded figure in a misty forest, mossy forest staircase, moss cottage with pink door, cherry-blossom pond with swans (2), ballerinas in a pink ballroom, bride in a stained-glass cathedral, pagoda with Mount Fuji.

Against the A0-core archive the joint k-means (k = 8, 120 endpoints) puts 9 of the 20 pilot endpoints in A0-dominated clusters (mostly the palatial-interior cluster), 7 in two shared clusters and 5 in a cluster unique to the pilot (the lavender trees), with 45% inside A0's per-cluster radii. At n = 20 these are directions, not estimates: H3 predicted "under a third" of E1-cap endpoints inside A0 radii, and the pilot sits above that, with the interiors family persisting across captioners while the dominant new motif is Qwen's own. The core (n = 100) decides.

## Notes
- D11 applies (pod numerics). Captioner digest 5ced39dfa4ba, Ollama 0.40.6, context 32,768 per slot. Code commit 1814b74 at launch (GIT_COMMIT), config sha in the manifest.
- The a0_report field `share_prompts_clip_truncated` reads SDXL's own tokenizer flag, which is always false once the explicit clip runs; the clip share above comes from the step records' `clipped` field.
