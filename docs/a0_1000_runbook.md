# A0-1000 runbook: A0-core continued to 1,000 steps (prediction in predictions.md, 2026-11-10; D20)

Pilot = trajectories 0–19 to step 999 on a RunPod 48 GB card (RTX A6000). The other 80 trajectories run in the same directory only after
the pilot gate and Brad's go-ahead. Costs are Brad's estimate at $0.59/h (A6000); a pod that mounts the existing network volume has to be
in the volume's data centre, where the price may differ.

| | trajectory-steps | wall at 6–10 s per trajectory-step | pod cost | disk on the laptop |
|---|---|---|---|---|
| pilot (20 × 900) | 18,000 | 30–50 h | about $20–30 | 7 GB |
| remaining 80 | 72,000 | 5–8 days | about $70–120 | 29 GB |

The per-trajectory-step rate is a guess (A0-core did 2.5 s on an RTX PRO 6000; the A6000 is roughly a third as fast, and 20 trajectories
batch less well than 100). The smoke measures it before anything is committed.

## 1. Laptop, before the pod (done 2026-11-10 unless noted)
1. `scripts/seed_continuation.py --target a0_1000 --count 100` → `runs/a0_1000/` holds A0-core's steps 0–99 for all 100 trajectories
   (4 GB; the pilot uses the first 20, the rest are ready for the full run).
2. Laptop smoke of the continuation mechanics: `seed_continuation.py --target a0_1000_lsmoke --count 2`, then
   `.venv/bin/python -m src.runner configs/a0_1000.yaml --run-name a0_1000_lsmoke --count 2 --steps 102` and check that the log says the run
   resumes at step 100 and that step_100/101 records cite `caption_of_step_099` as the prompt source.
3. Commit and push.

## 2. Pod
1. RunPod: a pod with an RTX A6000 (or L40 / 6000 Ada), CUDA 12.8 template (driver ≥ 570), **the existing network volume mounted at /workspace**
   (it holds the venv, SDXL and llava:latest). Put the SSH line in `.env` as `RUNPOD_SSH="root@HOST -p PORT"`.
2. `scripts/runpod_sync.sh push` (code and configs), then on the pod `bash scripts/runpod_setup.sh` (idempotent: checks the driver, the venv and
   the llava digest 8dd30f6b0cb1; refuses if the tag moved).
3. **Volume space.** On the pod: `du -sh /workspace/ai_to_ai_loops/runs/* ; df -h /workspace`. The mirrors of runs already pulled and verified on
   the laptop (arm_a, bimg, e2_qz, e6_photo, e6_track, e1_*) can go: check each against the laptop copy's byte count first
   (`du -sb runs/<run>` both sides), then `rm -rf` the pod mirror. Need ≥ 15 GB free before the pilot starts; the offload loop keeps it there.
4. `scripts/runpod_sync.sh push-run a0_1000 99` → the pod gets steps 0–99 records and the step-99 image for all 100 trajectories (about 100 MB).
5. Smoke on the pod: `COUNT=2 CFG=configs/a0_1000_runpod.yaml OLLAMA_PAR=8 bash scripts/runpod_launch.sh part` with `--steps` **not** overridden is
   the real run on 2 trajectories, so instead run the standard GPU smoke `CFG=configs/a0_1000_runpod.yaml OLLAMA_PAR=8 bash scripts/runpod_launch.sh smoke`
   (`a0_1000_smoke`, 16 seeds × 3 steps from the seeds: tests models, batch 16 and 8 slots on the 48 GB card) and read s per trajectory-step.
6. Pilot: `COUNT=20 CFG=configs/a0_1000_runpod.yaml OLLAMA_PAR=8 bash scripts/runpod_launch.sh part`. The log should open with
   "run a0_1000: 20 trajectories x 1000 steps" and the first generated step should be 100.
7. On the laptop, the offload loop: `nohup scripts/runpod_pull_loop.sh a0_1000 1200 --offload > logs/runpod_pull_loop_a0_1000.out 2>&1 &`.
   It pulls every 20 min, verifies each new image's sha256 against its gen record, deletes the verified images from the pod (keeping the newest 3
   per trajectory and every record), and stops itself when progress.json says the run ended. `logs/offload_a0_1000.json` is its ledger.
8. Check in with `scripts/runpod_sync.sh status`; expect a pod restart or two over a multi-day run (the runner resumes; relaunch step 6 and the
   loop keeps going).

## 3. Pilot gate (reports/a0_1000_pilot.md)
- `analysis/embed.py a0_1000 --spaces dinov2,minilm` (incremental; run it on the laptop copy).
- `analysis/gravity.py a0_1000 --archive archive/a0_core_centroids.npz --labels <A0 labels>` for the whole run and `--window 100:200` … `--window 900:1000`.
- Endpoint sheet: `analysis/endpoint_sheets.py --run a0_1000 --grid 5x4 --step 999 ...`; step-999 k-means vs A0-core step-99 centroids (`attractor_atlas.py`).
- Grade P1–P5 against predictions.md; throughput, cost, crash/resume log, offload ledger summary; degenerate-trajectory check (length_cutoff flags,
  caption word counts, image variance).
- Brad decides on the remaining 80 (`CFG=configs/a0_1000_runpod.yaml OLLAMA_PAR=8 bash scripts/runpod_launch.sh core`; trajectories 0–19 are
  skipped as complete).
