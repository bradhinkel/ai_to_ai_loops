# A0-core gate report

Run `a0_core`: 100 trajectories (all Hintze seeds) × 100 steps, T = 0.9, on a RunPod RTX Pro 6000 96 GB (single-pass, 16 prompts per SDXL call, 8 Ollama slots; `configs/a0_core_runpod96.yaml`).
Started 2026-10-18 18:55, finished 2026-10-19 02:05 pod time, one process, no restarts. 10,000 of 10,000 records; copied to the laptop and verified byte-identical by combined SHA-256.
Figures and `summary.json` are in `reports/a0_core/`, rebuilt with `analysis/a0_report.py a0_core`, `analysis/build_archive.py a0_core`, `analysis/elbow_check.py a0_core`.

## Gate (SPEC §4.3): 2 of 3 criteria pass as written; the third fails as written but matches Hintze's own data under the same measurement. Brad's call.

| Criterion | Result | Verdict |
|---|---|---|
| Pooled elbow k in about 10–16 | MiniLM caption endpoints: knee k = 7 (the a0_report rule, k = 2..25). DINOv2 image endpoints: knee 8. Silhouette maxima: MiniLM 4, DINOv2 11. **Hintze's own 99 T = 0.9 endpoint captions, same MiniLM and same rule: knee 8, silhouette 8.** | fails as written; matches the reference |
| Motifs match Hintze's categories | 67 of 100 endpoints are palatial interiors (34 + 9 luxury bedrooms), gothic cathedrals (11) or village streets and houses (13). Lighthouse, urban night scene and castle also present. | pass |
| Step-to-step drift plateaus within ~25 steps | plateau at step 16 (pilot: 26). Starts at 0.26 like Hintze's, settles at 0.164 vs his ~0.19. | pass |

**On the elbow criterion.** The 10–16 range came from Hintze's 12 pooled clusters, which he found on 700 trajectories across seven temperatures. A single temperature with 100 trajectories gives fewer clusters under any knee rule, and the inertia curve has no sharp knee (`elbow_check.png`): the knee moves from 7 to 14 as the k range widens from 25 to 40 on our captions, and from 8 to 9 on Hintze's. The like-for-like comparison is our 100 endpoints against his 100 T = 0.9 endpoints, and those agree (7 vs 8 on captions; DINOv2 silhouette 11 sits inside the written range). I recommend reading the criterion as "matches Hintze's T = 0.9 data under the same rule" and recording that recalibration in SPEC2 §3; the prediction in `predictions.md` (10–16, point estimate 12) stays as written with a dated note.

## Attractors (`archive_clusters.jpg`, DINOv2 k = 8 by knee; `contact_endpoints.jpg`, MiniLM k = 7)
| DINOv2 cluster | n | r95 | What it is | Hintze motif? |
|---|---|---|---|---|
| 1 | 34 | 0.32 | palatial interior: gold and blue salon, chandeliers, ornate ceiling | yes (palatial interiors) |
| 0 | 11 | 0.11 | gothic cathedral nave, stained glass | yes (cathedrals) |
| 2 | 9 | 0.33 | luxury bedroom, canopy bed, soft light | yes (interiors variant) |
| 3 | 8 | 0.71 | old-town cobblestone street, village at dusk, London bus in rain | yes (village / urban night) |
| 6 | 5 | 0.19 | Victorian house with garden | near (houses) |
| 5 | 4 | 0.46 | fairy-tale castle on water, coastal town | yes (castle) |
| 4 | 24 | 0.79 | catch-all landscapes and scenes: tropical road at sunset, lighthouse in storm, mountains, nebula, sphinx, birch forest, mosaic guitar | lighthouse yes; rest mixed |
| 7 | 5 | 0.59 | people and art: soccer players, ballerina, geisha print, obelisk | no |

Cluster 0 (cathedrals) is the tightest basin (r95 0.11); the interiors basin is the largest. Pooled r95 radius 0.747 is inflated by the two loose clusters (4, 7); E1's overlap test should use per-cluster radii, which `archive/a0_core_centroids.npz` stores, and treat cluster 4 as "no attractor".

## Drift (MiniLM, caption k vs k−1): `drift_step.png`, `drift_cumulative.png`
Mean drift 0.26 → 0.225 → 0.228 → 0.21 → 0.21 over the first five steps, last-20 mean 0.164. Hintze's T = 0.9 curve from the figshare captions starts at the same 0.26 and sits about 0.03 higher throughout. Individual trajectories keep spiking above 0.4 late in the run, as his do. The DINOv2 image-space drift (`analysis/cache/a0_core/dinov2.npz`) is the primary space from SPEC2 on; the E1 report will plot it alongside.

## Throughput and GPU
| | Per trajectory-step | Notes |
|---|---|---|
| SDXL 1024px, 25 steps, batch 16 | 1.78 s (median) | 1.64 s per image inside the batch; peak 12.3 GB allocated |
| LLaVA 7B caption, 8 slots | 0.75 s (median) | 4.1 s per request, 8 in flight |
| Total | **2.5 s** (mean 2.58) | 250 s per lockstep step; 7.1 h wall; about $18 of pod time |

GPU log (`logs/runpod/gpu.csv`, 2,579 samples): mean 70 °C, max 85 °C, mean 440 W (598 W while generating), max 53.7 GB used.

## Captions and flags
- 10,000 captions, 0 empty, 0 refusals, 0 retries. Mean 139 words, median 127 (Hintze's: 89). 9,969 exceed 50 words.
- 98.3% of prompts from step 1 on were cut by CLIP at 77 tokens, which is the only truncation in the loop (as in Hintze's data, 85%).
- One runaway: trajectory 84, step 12, LLaVA repeated itself until the pod's 32,768-token context filled (22,199 words, 392 s, `done_reason = length`). CLIP read its first 77 tokens; the next caption was a normal 166 words. On the laptop's 4,096-token context the same event would have stopped at about 3,000 words. This is the only `length_cutoff` flag and the only slow step (step 12: 6.3 s per trajectory-step).

## Deviations and provenance
- D11 applies: batch 16 and 8 parallel captions change floating-point numerics only, but seeded CUDA `randn` differs between GPU models, so these trajectories are different draws from the same distribution as the laptop's, not the same draws (as Hintze's unseeded runs were).
- The manifest's `git_commit` is empty: the pod had no `.git`, and the `GIT_COMMIT` fallback was added after launch. The code was commit `d845c4f` plus the uncommitted `scripts/runpod_pull_loop.sh`; `config_sha256` in the manifest matches `configs/a0_core_runpod96.yaml`.
- Ollama 0.40.6 on the pod (laptop 0.40.5), context 32,768 per slot (D9, D11). Captioner digest 8dd30f6b0cb1 as pinned.
- Crash/resume log: no crash, no restart, one `start` event. The resume path was exercised in the pilot's kill test.

## Outputs for SPEC2 §3 and E1
- `archive/a0_core_centroids.npz`: 8 cluster centroids in DINOv2, CLIP-image, CLIP-text and MiniLM space, members, per-cluster r95 (CLIP for steering only). `archive/a0_core_labels.json`: members and the three nearest captions per cluster.
- `analysis/cache/a0_core/`: DINOv2, MiniLM and CLIP embeddings of all 10,000 steps (rebuildable).
- `reports/a0_core/elbow_check.{png,json}`: knee and silhouette curves for our captions, our images and Hintze's captions.
