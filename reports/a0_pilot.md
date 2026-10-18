# A0-pilot gate report

Run `a0_pilot`: 20 trajectories (Hintze seeds 0–19) × 100 steps, T = 0.9, two-pass lockstep on the RTX 5070 laptop.
Started 2026-10-17 15:17, finished 2026-10-18 01:29 in one process, no restarts. Config `configs/a0_pilot.yaml`, commit `9787c32`.
Figures and `summary.json` are in `reports/a0_pilot/`, rebuilt with `.venv/bin/python analysis/a0_report.py a0_pilot`.

## Gate (SPEC §4.2): PASS
| Criterion | Result |
|---|---|
| Pipeline runs end to end | 2,000 of 2,000 step records written; 0 warnings or errors in `logs/a0_pilot.log`; no orphan or temp files |
| Resume after a forced kill | Verified on `a0_killtest` (2 traj × 4 steps): SIGKILL during the SDXL pass of step 1 and during the LLaVA pass of step 2, restarted with the same command each time; both trajectories completed, prompt chain intact, no orphans (`logs/a0_killtest_driver.log`) |

The pilot itself never crashed, so its resume path was not exercised during the pilot; the kill test is the evidence.

## Throughput (measured)
| | Median per trajectory-step | Notes |
|---|---|---|
| SDXL 1024px, 25 steps, cpu offload | 14.8 s | peak 5.5 GB allocated |
| LLaVA 7B caption | 3.5 s | 60 to 70 tok/s; includes amortised load |
| Total | **18.3 s** | 6.1 min per lockstep step of 20 trajectories |

Wall time 10.2 h. **A0-core (100 × 100) projects to about 51 h** at this rate (SPEC §4.2 said 25 to 40 h). GPU health over 3,669 samples: max 81 °C (median 74), max 128 W, max 6.1 GB VRAM. No reboot.

## Drift (MiniLM, caption k vs k-1): `drift_step.png`, `drift_cumulative.png`
- Mean step-to-step distance starts at 0.26 (Hintze's T = 0.9 mean from the figshare captions also starts at 0.26) and plateaus at step 26 by the report's criterion (10-step rolling mean within 10% of the final level); SPEC §4.3 asks for about 25.
- Plateau level is 0.165 for us against about 0.19 for Hintze: our loop settles slightly harder. Individual trajectories keep spiking (a few jumps above 0.4 late in the run), as his do.

## Endpoints: `contact_endpoints.jpg`, `trajectories.jpg`
k-means on the 20 final captions (k = 10 for the sheet; the elbow on 20 points is not meaningful, A0-core answers that):
| Motif | Trajectories | Hintze motif? |
|---|---|---|
| Palatial interior (chandeliers, gilt, blue drapes) | 0, 2, 5, 6, 11, 13 | yes |
| Gothic cathedral nave / stained glass | 3, 4, 9, 17, 19 | yes |
| European village at dusk, cobblestones | 1, 7 | close to "urban night scene" |
| Lighthouse in a storm | 18 | yes |
| Castle on a cliff; lakeside boat; thatched cottage garden; Grand Canyon aerial; skull with roses; mosaic tile wall | 8; 14; 10; 15; 16; 12 | singletons |

13 of 20 endpoints sit in Hintze's named motifs after 100 steps from unrelated seeds (hospital bed, soldiers, supermarket, tomato seller, ...). The trajectory sheet shows the familiar path: the seed scene is lost by step 5 to 10, and the image is an interior or a cathedral by step 50 to 75. Three endpoints (8, 14, 18) are diptychs that LLaVA describes as "two views", which SDXL then keeps reproducing.

## Captions
- Mean 134 words, median 124, none under 50 except 4 of 2,000; no empty responses, no refusals, no length cut-offs.
- 98.4% of prompts exceed CLIP's 77 tokens, so SDXL saw about the first 69 words each time, as in Hintze's data (85% truncated there).
- Our captions are longer than Hintze's (his mean 89 words). Same instruction, same model tag and quantisation, so the likely causes are the Ollama version (ours 0.40.5, his unrecorded) and its default context (4,096 here). Because CLIP cuts the prompt anyway, the generator sees similar input; the difference matters only for caption-space analyses, and is flagged for A0-core.

## Deviations and incidents
No new deviations; D1 to D10 in `DEVIATIONS.md` apply. No crashes, pauses or manual interventions during the run.

## Recommendation
Gate passed. A0-core is ready to launch with `configs/a0_core.yaml` (100 trajectories, ~51 h). Waiting for Brad's go-ahead (CLAUDE.md rule 2).
