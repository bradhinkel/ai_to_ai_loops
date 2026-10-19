# Hunyuan-DiT v1.2 throughput on the RunPod RTX Pro 6000 (2026-10-19, `scripts/bench_hunyuan.py`)

fp16, 1024×1024, guidance 5.0, DDPM, one fixed prompt, seconds per image inside the batch (wall time of the batch / batch size), after a warm-up call. Attention processor: `HunyuanAttnProcessor2_0` (SDPA).

| Steps | Batch | s / image | Peak alloc GB |
|---|---|---|---|
| 50 | 4 | 10.64 | 11.0 |
| 50 | 8 | 11.19 | 14.2 |
| 50 | 16 | 11.26 | 20.7 |
| 50 | 32 | 11.46 | 33.6 |
| 25 | 4 | 5.41 | 11.0 |
| 25 | 8 | 5.67 | 14.2 |
| 25 | 16 | 6.29 | 20.7 |
| 25 | 32 | 5.81 | 33.6 |
| 25 | 16, `torch.compile(mode="max-autotune-no-cudagraphs")` | **2.89** | – |

Batch size does not matter (the GPU is compute-bound from batch 4). Halving the steps halves the time. Compiling the transformer gave a further 2.2× at 25 steps; the autotuner logged many "No valid triton configs ... out of resource" candidates, which are rejected kernel configurations, not errors, and the compile took about 2 min. The smoke run `e1_both_smoke` (50 steps, batch 16, uncompiled) measured 11.6 s per image in the real loop, consistent with the table.
