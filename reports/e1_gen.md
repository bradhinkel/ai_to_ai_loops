# E1-gen core (Hunyuan-DiT v1.2 generator + LLaVA captioner): cell report

Run `runs/e1_gen`, 100 trajectories x 100 steps, T = 0.9, Hunyuan at 25 steps with torch.compile (D12 amendment), CLIP-77 clip of every prompt (D13). Pod RTX Pro 6000 96 GB, commit 1814b74. Finished 2026-10-19 22:08 UTC. Predictions: `predictions.md` E1 section (written 2026-10-18, confirmed by Brad before any E1 run).

## Verdict against the written E1 thresholds

| prediction | threshold | E1-gen | result |
|---|---|---|---|
| H1 convergence | DINOv2 step-to-step drift plateau by about step 25; pooled elbow k < 20 on final images | plateau step 22; knee k = 8 (DINOv2), 11 (MiniLM) | **passes as written** |
| H3 point estimate for this cell | E1-gen keeps most of A0's motifs: over half of endpoints inside A0 cluster radii | 37 of 100 inside A0 radii | **fails** |
| H2 / H3 proper | need E1-both and E1-cap cores | pending | - |

The H1 pass needs a caveat. The drift curves of E1-gen and A0-core are almost identical (plateau about 0.25 cosine per step from step 20 on), and the knee rule gives the same k, but the endpoint population is far less concentrated: Vendi 58.9 vs 31.8, silhouette prefers about 40 clusters, and at a fixed 0.20 DINOv2 radius 82 of 100 endpoints sit in no attractor at all (A0: 48). Per-trajectory dynamics are the same; what changed is that far fewer trajectories end in a shared basin. "Converges" on the written thresholds, "collapses onto few attractors" much less than A0.

## Metrics vs A0-core (and the E1-cap pilot)

| run | n | knee k DINOv2 / MiniLM | Vendi (DINOv2) | plateau step | share inside A0 radii | mean step drift, last 20 | caption words, median | CLIP-77 clip fired |
|---|---|---|---|---|---|---|---|---|
| A0-core (SDXL + LLaVA) | 100 | 8 / 7 | 31.8 | 15-16 | 0.92 | 0.164 | 127 | implicit (SDXL truncates) |
| E1-cap pilot (SDXL + Qwen) | 20 | 10 / 9 | 11.8 | 14-20 | 0.45 | 0.203 | 36 | 3.8% |
| **E1-gen (Hunyuan + LLaVA)** | 100 | 8 / 11 | 58.9 | 22 | 0.37 | 0.174 | 112 | 97.1% (113 -> 62 words) |

Figures: `reports/e1_gen/` (contact_endpoints.jpg, drift_step.png, drift_cumulative.png, elbow.png, trajectories.jpg), `reports/e1_gen_vs_a0/` (drift_dinov2.png, drift_minilm.png, joint_clusters.jpg, endpoints_*.jpg, summary.md), `reports/elbow_table.md`.

## Endpoint motifs (k = 8 on DINOv2, see contact sheet)

- Gothic cathedral (14): naves and Notre-Dame-style facades. Shared with A0, where the nave was the tightest basin.
- Rainbow / neon tunnel with silhouetted walkers (4 at step 99 inside 0.30 of the cluster centroid; 9 in the k-means group with neon corridors and stained glass). New: no A0 step ever comes within 0.41 of it.
- White humanoid robots (7), soccer / sports figures (10), red sandstone canyons (4), eagles and birds (4), 3D product shots on white (bananas, strawberry, pizza, vases, jars).
- About 40 singletons: Capitol, carousel, clownfish in a boat, Kremlin, pink alien, sunflowers, jet fighters, Eiffel towers, lighthouses.
- Absent: A0's gold-and-blue salon (0 endpoints, visited transiently by 5 trajectories), canopy bedroom (1), Victorian house (0).

## Gravity (analysis/gravity.py)

Caption space (MiniLM, radius 0.15) is the fair comparison between A0 and E1-gen because both use LLaVA; in DINOv2 at a fixed radius Hunyuan's cathedrals spread 0.1-0.6 from A0's centroid (facades vs naves, different rendering), so the image-space hazard mostly measures rendering variety.

| shared attractor (A0 archive centroid, MiniLM) | A0-core: endpoints / hazard per step / KM median residence | E1-gen: endpoints / hazard / KM median | hazard ratio |
|---|---|---|---|
| gothic cathedral | 11 / 0.027 / 25 steps | 13 / 0.054 / 15 steps | 2.0 |
| gold-and-blue salon | 34 / 0.018 / 44 steps | 0 / 0.107 / 3 steps | 5.9 |
| canopy bedroom | 9 / 0.045 / 14 steps | 2 / 0.043 / 12 steps | 1.0 |
| Victorian house | 4 / 0.179 / 5 steps | 0 / - | - |

First reading of the 2026-10-19 hypothesis note (Brad: hazard tracks the attractor; Claude: tracks the captioner): on this same-captioner pair, the cathedral and the bedroom keep their depth within a factor of 2 across the generator swap, which is consistent with both claims; the salon loses its depth entirely under Hunyuan, which fits neither cleanly and says the salon was an SDXL-specific basin. Full test after E1-both and E1-cap.

Rainbow tunnel (E1-gen's own cluster centroid, DINOv2 radius 0.30): 13 trajectories visited, 4 were inside at step 99, 9 left. Occupancy rose from 1 at step 10 to a peak of 6 at steps 50-65 and was 5 at step 75 (Brad's observation), then 3-4. Steps inside 348, so escape hazard about 0.026 per step and mean residence about 39 steps; the four longest visits that still ended in departure lasted 46, 59, 40 and 18 steps (trajectories 0, 15, 77, 67). Deep by A0 standards, comparable to the cathedral, but with low capture (about 0.001 per step).

E1-gen as a whole (own attractors, DINOv2 0.20): hazards 0.08-0.30 per step and 90% of all steps in no attractor, versus A0's 71%. The pooled exit rate again rises with distance from the centroid (0.03 at the core to 0.32 at the rim).

## Transient visits (analysis/transient_visits.py)

- A0 attractors inside E1-gen's 10,000 steps: cathedral visited by 15 trajectories, 2 stayed (at A0's tight radius); salon visited by 5, 1 stayed; bedroom 1/1; Victorian house never (nearest 0.26).
- E1-gen attractors inside A0-core's steps: the rainbow tunnel was never approached (1 trajectory within its loose k-means radius, nearest 0.41); canyons visited transiently by 3 A0 trajectories (nearest 0.08), none stayed; robots 1 transient visit; the cathedral group 17 visited / 11 stayed.

## Run quality

- 10,000 records, 0 empty captions, 0 refusals, 0 length cutoffs. LLaVA wrote a median 112 words; the CLIP-77 clip rewrote 97.1% of prompts to a median 62 words before Hunyuan, so Hunyuan's mT5 encoder only ever saw the clipped prompt (by design, SPEC2 §4).
- Throughput: median 5.1 s per trajectory-step (Hunyuan 3.6 s, LLaVA 1.5 s), 14.8 h wall including the restart; about $37 at the pod rate.
- Crash/resume: the pod container restarted at 21:00 UTC (RunPod network outage) after step 92; relaunched 21:03, resumed by file presence from step 93 (events.jsonl holds both start events; step 93 took 13 min for the recompile). Four transient Ollama errors earlier in the day were retried successfully.
