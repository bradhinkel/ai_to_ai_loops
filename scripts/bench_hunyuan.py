"""Throughput of Hunyuan-DiT on the current GPU: seconds per image by batch size and step count (no run data written).
    .venv/bin/python scripts/bench_hunyuan.py [--batches 4,8,16,32] [--steps 50,25]
"""
import argparse, time, torch, json
from src.generators.hunyuan import HunyuanGenerator

ap = argparse.ArgumentParser(); ap.add_argument("--batches", default="4,8,16,32"); ap.add_argument("--steps", default="50,25"); a = ap.parse_args()
prompt = "A grand palatial interior with gold and blue walls, crystal chandeliers and an ornate painted ceiling, warm light"
out = []
for steps in [int(s) for s in a.steps.split(",")]:
    g = HunyuanGenerator({"model": "Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers", "revision": "5e96094e0ad19e7f475de8711f03634ca0ccc40c", "dtype": "float16",
                          "resize_to": 512, "batch": 32, "num_inference_steps": steps, "guidance_scale": None, "cpu_offload": False})
    g.load(); g.generate_batch([prompt] * 2, [1, 2])   # warm-up
    print("attn processor:", type(g.pipe.transformer.blocks[0].attn1.processor).__name__, flush=True)
    for b in [int(x) for x in a.batches.split(",")]:
        torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats(); t0 = time.time()
        try:
            g.generate_batch([prompt] * b, list(range(b)))
            dt = time.time() - t0; r = {"steps": steps, "batch": b, "s_per_image": round(dt / b, 2), "batch_s": round(dt, 1), "peak_alloc_gb": round(torch.cuda.max_memory_allocated() / 1e9, 1)}
        except torch.cuda.OutOfMemoryError:
            r = {"steps": steps, "batch": b, "oom": True}; torch.cuda.empty_cache()
        print(json.dumps(r), flush=True); out.append(r)
    g.release(); del g; torch.cuda.empty_cache()
print("RESULT", json.dumps(out))
