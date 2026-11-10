# E5 runbook — D&D bias injection (revised 2026-11-06, Brad's decisions of the same day)

SPEC2 §4 E5 as amended here. Question: can a model's prior be pushed on purpose so that the image loop's attractors move to match?
Brad's expectation: with a D&D-tuned captioner and/or generator, the loop has D&D-like attractors. Everything below is laptop or
API work except the two training jobs and the four loop cells, which need a 48 GB pod.

## 0. Decisions (Brad, 2026-11-06)

- Base captioner: **Qwen2.5-VL-7B-Instruct** (same model family as E1-cap's untuned captioner and as the E3 text Qwen).
- Training data: the dndcollect sets in `~/Image-search/sets/` — `captions_train_{a,b,c,d}.jsonl` (12,002 D&D images
  with Sonnet 5.5 captions, 140 words median, grounded: the captioner saw no metadata) and `captions_test.jsonl` (1,000 held out).
  No further captioning (train_e–g stay uncaptioned).
- Untuned control: **E1-cap already is it** (SDXL + qwen2.5vl:7b Q4_K_M through Ollama, 100 seeds × 100 steps, `reports/e1.md`):
  10 persistent attractors, 38 % of steps inside them, 0.53 of endpoints inside A0's p95 radii, captions 37 words median,
  fantasy-lexicon share of late captions 0.051 (A0-core 0.019). No new control cell unless the tuned captioner has to be served
  through a different backend (step 4).
- Split: train on train_a–c (9,000), validate on train_d (3,000, early stopping), report fidelity on test (1,000) only once.
- The generator half is trained from the same pairs (an SDXL LoRA), not downloaded: both halves of the 2×2 then come from one
  dataset. Experiment 1 = captioner LoRA; Experiment 2 = generator LoRA; Experiment 3 = the loop cells.

## 1. The 2×2 (unchanged) plus dose-response

| | captioner: untuned Qwen2.5-VL | captioner: D&D LoRA |
|---|---|---|
| generator: SDXL | **E1-cap** (exists) | E5-cap |
| generator: SDXL + D&D LoRA | E5-gen | E5-both |

Dose-response pilot first on the generator side (LoRA scale 0 / 0.25 / 0.5 / 1.0, 20 seeds × 100 steps each) to find the scale where
the attractors flip; the captioner adapter at partial strength if the serving path allows it. Instruction verbatim ("vivid, artistic",
50 words); Hintze's 100 seeds; T 0.9; CLIP-77 clip as in E1 (D13).

## 2. Pre-pod work (laptop + API; nothing here bills a GPU)

1. **Prediction** — `predictions.md` "E5" block confirmed by Brad (draft written 2026-11-06). Nothing runs before that.
2. **Packaging** — `scripts/e5_pack.py`: read the four captioned sets + test, resize each original to 1024 px on the long edge
   (Lanczos, RGB, JPEG q90, as the caption stage sent them to Sonnet), write `data/e5/images/<sha>.jpg` and
   `data/e5/{train,val,test}.jsonl` (sha, file, caption, category, aspect). ≈ 4 GB instead of 16 GB of originals. Record the
   dndcollect commit and the sha list in `data/e5/MANIFEST.json`.
3. **Fidelity judge** — `analysis/e5_fidelity.py`: SigLIP image–text similarity (never CLIP, rule 4) of a caption against its image,
   plus a Haiku judge that scores a caption for (a) grounded elements present, (b) elements not in the image, (c) fantasy
   vocabulary. Run on the test set captions (Sonnet's, the ceiling) and on E1-cap's untuned Qwen captions of the same 1,000 images
   (the floor for D&D voice, the reference for grounding).
4. **Serving path decision, settled by a laptop smoke** — the loop's captioner backend is Ollama. Preferred: merge the LoRA into the
   bf16 weights, convert with llama.cpp (`convert_hf_to_gguf.py` + the Qwen2.5-VL mmproj) to GGUF Q4_K_M, `ollama create` a
   pinned local model, and log its digest; E1-cap then stays the control with the same backend and quantisation. Smoke the
   conversion on the laptop with the untuned weights (CPU, 17 GB download) before any training. Fallback if the conversion fails:
   a transformers + PEFT captioner backend in `src/captioners/` and a bf16 untuned control cell on the pod (≈ $5).
5. **Training script** — `scripts/e5_train_captioner.py`: transformers + PEFT LoRA (r 16, alpha 32, all linear layers of the LLM,
   vision tower frozen), images at 1024 px long edge, bf16, gradient checkpointing, batch 8 with accumulation, 2 epochs,
   lr 1e-4 cosine, eval on val each 500 steps, keep the best 3 adapters. Laptop smoke with Qwen2-VL-2B-Instruct in 4-bit on 50
   examples: train → adapter → caption 5 test images → fidelity script runs end to end.
6. **Generator script** — `scripts/e5_train_sdxl_lora.py` (diffusers SDXL LoRA, rank 32, 1024 px buckets by aspect, the
   Sonnet captions as prompts clipped to 77 CLIP tokens, 1 epoch over 12k pairs ≈ 6–8 h on an L40). Laptop smoke at 512 px on
   20 pairs with a tiny rank.
7. **Pod setup** — `scripts/runpod_setup_e5.sh`: packages (peft, bitsandbytes, accelerate, llama.cpp build), model downloads
   with pinned revisions, data rsync, and a `df` check against the volume before anything writes. Add to `.env` the new
   `RUNPOD_SSH`. Pod: RTX A6000 or L40 (either), 100 GB volume at /workspace, 30 GB container disk.
8. **DEVIATIONS** — D20: captioner family for E5 is Qwen2.5-VL (as E1), tuned by LoRA on dndcollect pairs; serving quantisation
   recorded; the generator LoRA's training data recorded.

## 3. On the pod (one experiment at a time, pull and verify each result on the laptop before the next)

| experiment | job | GPU time (L40) | disk peak | output pulled to laptop |
|---|---|---|---|---|
| 1 | captioner LoRA, 2 epochs over 9k, val on 3k | 3–5 h | ≈ 70 GB | adapter(s), training log, val curves |
| 1b | merge + GGUF Q4_K_M + fidelity on test (1,000) | 1 h | +20 GB | GGUF, fidelity table vs Sonnet and E1-cap |
| 2 | SDXL LoRA, 1 epoch over 12k at 1024 px | 6–8 h | +10 GB | LoRA safetensors, sample grid at scales 0.25/0.5/1.0 |
| 3a | dose-response pilot E5-gen × 4 scales, 20 seeds | 4 × 0.5 h | +3 GB | runs, pulled |
| 3b | E5-cap, E5-gen, E5-both at 100 seeds | 3 × 7 h | +12 GB | runs, pulled; remove mirrors after verification |

Cost at $0.82/h: ≈ $35–45 all in. Readout as SPEC2 §E5 (which cell's endpoints look like E5-both; whether the D&D cells
converge to a few fantasy clichés), measured as in E1 (`analysis/e1_compare.py` pattern: persistent attractors, share inside
E1-cap's p95 radii, endpoints in named E1-cap attractors, Vendi, memory half-life) plus the fantasy-lexicon share of captions and a
Haiku theme judge over endpoint images.
