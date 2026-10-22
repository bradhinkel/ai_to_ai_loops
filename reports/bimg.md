# B-img pilot gate report — image-archive rejection on the A0 pair, with arm A control (SPEC2 §5, B-img pilot design), 2026-10-22

SDXL + `llava:latest` 7B, Hintze's instruction verbatim, T = 0.9, 20 trajectories (Hintze seeds 0–19) × 100 steps. Each step the captioner writes K = 4 captions of the current image and all four are rendered. **B-img** (`runs/bimg`, `configs/bimg_runpod96.yaml`, code d15271e): candidates within r = 0.078 (SigLIP cosine; the window-matched equivalent of DINOv2 0.20, `reports/siglip_calibration.md`, D17) of any archive entry are rejected, one survivor is picked at random; no survivor → resample the four captions up to twice more, then advance the most distant candidate and log the step as trapped. The archive takes every image whose last five steps stayed within 0.078 of their mean, after a five-step burn-in. **Arm A** (`runs/arm_a`): the same four candidates, one picked at random, no archive, same seeds. Evaluation is DINOv2 (images) and MiniLM (captions); SigLIP steered and is never graded.

**Outcome: both runs complete (4,000 selections, 16,000 candidate images, 0 errors). Rejection against the archive did not break convergence.** The share of trajectory-steps spent inside persistent attractors fell from 44–46% to 33%, not below 15%; endpoint diversity equals A0 at the same sample size; the trajectories ended where SDXL + LLaVA always end (salons, cathedrals, castles, villages). What the rejection did do is shorten every stay and raise every escape hazard two- to three-fold, so B-img trajectories tour the A0 attractor family instead of settling in one member of it. The archive still grew by one entry per 2.6 trajectory-steps: the loop kept finding states that pass the persistence test, almost all of them adjacent to states already archived. The limit is the scale of the rule, not the sampler: the four candidate renders differ from each other by about 1.7 rejection radii on average, but the rejection radius is sized to a five-step persistence window while the attractor family is many radii across, so discarding the points already visited leaves the trajectory inside the family.

## Prediction vs result

| prediction (Claude, 2026-10-20) | result | verdict |
|---|---|---|
| 1. share of trajectory-steps in persistent attractors falls from A0's 39% to under 15%; persistent visits per trajectory from 2.8 to under 1.0; arm A changes neither by more than a quarter | four-cell DINOv2 atlas (A0-core, A0-core-2, B-img, arm A; R 0.20, dwell ≥ 5): steps inside 44% / 41% / **33%** / 46%; visits per trajectory 2.79 / 2.60 / **2.60** / 2.45; median dwell 8 / 9 / **7** / 10 | **fails** on both B-img numbers; the arm A clause holds |
| 2. step-99 Vendi above 50 (A0 32); step-to-step drift at steps 50–99 above A0's | Vendi at n = 20: B-img 12.7, arm A 13.8; A0-core's 20-trajectory subsamples give 12.5 [9.5, 15.7] (A0-core-2 13.1). Drift, last 20 steps, DINOv2: B-img 0.297, A0 0.254, arm A 0.236; MiniLM 0.167 vs 0.164 vs 0.170 | **fails** on Vendi; drift up 17% over A0 and 26% over arm A in image space, flat in caption space |
| 3. trapped steps under 5% in the first 25 steps, over 20% in the last 25 | 1.2% / 2.4% / 1.8% / **5.6%** by quarter (6, 12, 9, 27 of 500) | first clause **passes**, second **fails** |
| 4. ≥ 2 clusters with ≥ 3 persistent visits that A0 never visits; trajectories orbit the archive boundary (median distance to the nearest entry between r and 2r in the last 25 steps) | one: cluster 22, a glass-walled modern living room (3 visits in B-img; 0 in A0-core, 1 in A0-core-2, 1 in arm A). Chosen candidate's SigLIP distance to the nearest archive entry, steps 76–99: median 0.093 = 1.2 r, 10th percentile 0.079 = r. In DINOv2 the median distance to the nearest archived image is 0.19 and 52% of late steps lie within R 0.20 of one | new clusters **fails** (one, not two); orbit **passes** |
| 5. escapes are stylistic variants of the same motifs rather than new subjects; style vocabulary stays above 80% | style share, steps 76–99: B-img 90%, A0 87%, arm A 82%. The strips show the hops: salon → cathedral → castle → salon, trains → station nave → salon, produce aisle → umbrellas → beach → salon | **passes** |
| Brad: the known basins can be escaped "but new attractors form"; the dynamic archive forces perpetual drift | escapes: yes, hazards up 2–3× and dwell cut (below). New attractors: 736 states passed the persistence test and entered the archive (39% of eligible trajectory-steps), but they are variants of the old family; one cluster is absent from A0-core. Perpetual drift: no; 60% of endpoints sit inside a persistent attractor (A0 61%) | **half holds**: escape and re-settling, not drift |

## Metrics side by side

| | A0-core (n 100) | A0-core-2 (n 100) | arm A (n 20) | B-img (n 20) |
|---|---|---|---|---|
| steps in any persistent attractor (four-cell atlas) | 44% | 41% | 46% | **33%** |
| endpoints inside one / persistent visits per trajectory / median dwell | 61% / 2.79 / 8 | 58% / 2.60 / 9 | 55% / 2.45 / 10 | 60% / 2.60 / **7** |
| steps free of every named A0 state (gravity, A0-core centroids, R 0.20) | — | — | 0.73 | **0.84** |
| Vendi, DINOv2 step 99 (20-trajectory subsample median for the n = 100 runs) | 31.8 (12.5) | 34.8 (13.1) | 13.8 | 12.7 |
| step drift, last 20 steps, DINOv2 / MiniLM | 0.254 / 0.164 | — | 0.236 / 0.170 | **0.297** / 0.167 |
| self-novelty: median DINOv2 distance from a step to the nearest earlier image of any trajectory, steps 76–99 | 0.120 | 0.121 | 0.131 | **0.173** |
| plateau step (DINOv2) | 15 | 20 | 32 | 35 |
| share of endpoints inside A0-core p95 radii (same-pair floor 0.62) | 0.92 | 0.62 | 0.75 | 0.80 |
| seed half-life, DINOv2 / MiniLM (steps) | 4 / 3 | 6 / 4 | 7 / 9 | 5 / 6 |
| caption words median; people share steps 76–99 | 131; 22% | 131; 24% | 119; 23% | 128; 15% |
| knee k DINOv2 / MiniLM | 8 / 7 | 10 / 8 | 10 / 8 | 10 / 10 (n = 20: not meaningful) |
| s per trajectory-step (wall) | 2.5 | 3.6 | 14.1 | 19.4 |

Elbow table rows (`reports/elbow_table.md`, rebuilt; at n = 20 the rule runs k = 2..19 and the knee sits where it always does): B-img captions **7** [6, 8], images **8** [7, 9]; arm A captions **8** [6, 8], images **9** [8, 10]; A0-core 7 / 8.

## What the archive did to the attractors

Persistent visits / trajectories with one / endpoints / mean dwell / escape hazard per step, four-cell atlas (`reports/persistent_atlas_bimg.md`). A0-core numbers are for 100 trajectories; divide by five for the 20-trajectory expectation.

| attractor | A0-core | A0-core-2 | arm A | B-img |
|---|---|---|---|---|
| white-and-gold salon / ballroom | 72 / 36 / 12 / 10 / 0.16 | 65 / 29 / 12 / 10 / 0.15 | 6 / 4 / 1 / 9 / 0.20 | 4 / 4 / 2 / 6 / **0.36** |
| gold-and-blue palatial salon | 58 / 32 / 13 / 12 / 0.13 | 66 / 38 / 13 / 13 / 0.11 | 4 / 3 / 1 / 17 / 0.09 | 10 / 6 / 4 / 7 / **0.24** |
| luxury canopy bedroom | 31 / 16 / 8 / 12 / 0.12 | 20 / 11 / 6 / 10 / 0.17 | 4 / 2 / 1 / 9 / 0.14 | 3 / 2 / 0 / 5 / **0.33** |
| gothic cathedral nave (cluster 7) | 14 / 9 / 6 / 20 / 0.05 | 8 / 7 / 2 / 31 / 0.03 | 6 / 5 / 2 / 30 / 0.03 | 6 / 4 / 1 / 7 / **0.18** |
| gothic cathedral nave (cluster 4) | 9 / 9 / 5 / 32 / 0.03 | 9 / 8 / 8 / 34 / 0.00 | 5 / 4 / 3 / 34 / 0.01 | 2 / 2 / 0 / 12 / **0.17** |
| stained-glass saints | 1 / 1 / 0 / 7 / 0.46 | 4 / 3 / 0 / 7 / 0.23 | 0 | 4 / 3 / 0 / 8 / 0.32 |
| glass-walled modern living room (cluster 22) | 0 | 1 / 1 / 0 / 6 / 0.44 | 1 / 1 / 0 / 10 / 0.26 | 3 / 1 / 0 / 6 / 0.33 |

Reading: the white salon loses two thirds of its expected visits (14 → 4) and the bedroom half; the gold salon and the cathedral keep their visit counts but lose their dwell (cathedral 20–34 steps → 7–12). Hazards of the shared attractors rise from 0.03–0.16 to 0.17–0.36 per step. The rejection makes the basins shallow; it does not remove them, and the trajectories move on to the next one.

## The mechanism, from the selection records

| steps | rejected per step (mean) | steps needing a resample | trapped | chosen candidate's SigLIP distance to the nearest archive entry, median (p10) | archive size at window end |
|---|---|---|---|---|---|
| 1–25 | 0.52 | 22 / 500 | 6 (1.2%) | 0.171 (0.087) | 136 |
| 26–50 | 0.93 | 41 / 500 | 12 (2.4%) | 0.122 (0.083) | 328 |
| 51–75 | 1.28 | 67 / 500 | 9 (1.8%) | 0.108 (0.080) | 521 |
| 76–99 | 1.80 | 96 / 480 | 27 (5.6%) | 0.093 (0.079) | 730 |

- The archive grew linearly, about 7.6 entries per step across 20 trajectories: 736 of the 1,900 eligible trajectory-steps (39%) passed the five-step persistence test in SigLIP, the same order as the 33–46% of steps the DINOv2 atlas calls persistent. Trajectory 12 alone contributed 70 entries.
- Rejections rose with the archive (0.5 → 1.8 of 4 per step) and the chosen image drifted toward the boundary (median distance 2.2 r → 1.2 r). The trajectories orbit the archive at arm's length, as predicted, but they orbit it from inside the same motif family.
- Trapped steps concentrate in a few trajectories: 16 (17 trapped steps, a cathedral nave), 18 (7), 15 (6), 9 and 11 (5 each). Twelve rounds of captioning could not get these images out of their basin.
- Candidate spread (SigLIP, all four round-0 renders of every step, `reports/bimg/candidate_spread_siglip.json`): the four candidates are not duplicates. Mean pairwise distance 0.146 → 0.126 by quarter in B-img (0.138 → 0.108 in arm A), i.e. 1.6–1.9 r; the median widest pair 0.19 → 0.17; all four within one radius of each other on only 2% of steps; some pair more than 2 r apart on 58–67%. So the rule almost always had a candidate that survived. The trapped-step sheet shows the exception: in the deep basins (cathedral nave, salon, canopy bedroom) the four renders collapse onto the same image at 0.03–0.08 from the archive, and twelve captions cannot leave.
- Why survival is not escape: in DINOv2, 52% of the late steps lie within R 0.20 of an archived image although every chosen candidate was by construction more than r from every archive entry in SigLIP. The archive is a cloud of 730 points inside a family whose A0 clusters have p95 radii of 0.11–0.79 in DINOv2; the trajectory threads between the archived points at a spacing of about one radius and keeps passing the persistence test on new points of the same family.
- Sanity: the chosen candidate index is uniform (522 / 481 / 473 / 504 over k = 0..3); 98% of prompts exceeded CLIP's 77 tokens, as in A0.

Figures: `reports/bimg/strips_bimg.jpg` and `strips_arm_a.jpg` (every tenth step of all 20 trajectories), `reports/bimg/trapped_steps.jpg` (ten trapped steps: the previous image, the advanced image, the four round-0 candidates with their archive distances), `reports/bimg_vs_a0/` (drift curves, endpoint sheets, joint clusters), `reports/persistent_atlas_bimg/cluster_*.jpg`, `reports/gravity_bimg.md`, `reports/gravity_arm_a.md`, `reports/memory_curve.md`, `reports/caption_audit_bimg.md`.

## Arm A

Four captions with a random pick is A0 with a different caption sample: 46% of steps in persistent attractors, 2.45 visits per trajectory, dwell 10, hazards within A0's range, Vendi at the A0 subsample median. The cost of sampling alone changes nothing; every B-img difference above is the rejection's.

## Run log, throughput, cost

| run | started (UTC) | finished | wall | s per trajectory-step | restarts |
|---|---|---|---|---|---|
| B-img | 2026-10-21 21:45 | 2026-10-22 08:33 | 10.8 h | 19.4 (4 SDXL renders 1.6 s each; 4 LLaVA captions ≈ 34 s per trajectory with 8 slots) | none |
| arm A | 2026-10-22 08:33 | 17:12 | 8.6 h incl. 46 min down | 14.1 | one: disk-quota crash at step 89 |

The network volume (100 GB) hit its quota at 15:37 UTC while arm A wrote step 89 (`OSError: [Errno 122] Disk quota exceeded` on the progress file); the queue script died with the runner. Atomic writes left no partial records; the runner resumed at step 89 by file presence after Brad approved deleting the pod mirrors of seven runs already verified on the laptop (`STATUS.md`, 2026-10-22). Two zero-byte `.tmp` files from the crash were pulled into `runs/arm_a/` before the cleanup and are left in place (append-only). Pod cost at ~$2.5/h: about $48 for the pair against the ~$25 estimate; the estimate missed that captioning four candidates per step, not rendering them, sets the pace.

Deviation of the analysis, not the pipeline: `analysis/caption_audit.py` read the Part 1 `caption` field, which is null in K-candidate records; it now uses `common.caption_used` (the caption that produced the next image), the same rule `embed.py` already applied.

## What this says, and the next step

1. **The attractors are not a property of a single image state.** Forbidding the loop to stay within 0.078 of any state it has settled in cuts dwell and raises hazard, but the trajectories go to the next salon, cathedral or castle. The pull is the composed map's prior, as SPEC2 §1 says, and an image archive only removes points from it.
2. **The radius has to match the basin, not the window.** The candidates differed by 1.7 r on average and still landed in the family, because r was calibrated to what counts as persistence over five steps and the basins are several r across. A rule that pushes away from the archived *cluster* (reject by distance to the archive's running centroids at the cluster's own radius, or a repulsion term that grows with the number of archived neighbours) acts at the right scale; point rejection does not. Where the sampler does collapse, in the deep basins that produced the trapped steps, no radius helps and the candidates have to be diversified before rendering (caption-stage rejection, larger K, or a higher candidate temperature), which is also the cheaper arm to run.
3. **At 20 trajectories the diversity readouts (Vendi, knee) cannot show a gain of less than about 30%.** The dwell and hazard readouts can, and they did.

Gate: the pilot ran to completion with no data loss; prediction 5 and the orbit clause hold, predictions 1–3 fail, 4 half. B-img as designed is not an anti-convergence arm. Recommendation: do not scale B-img to 100 trajectories; the next Part 2 pilot should be the caption-stage variant with a diversity check on the candidates before the archive rule is applied.
