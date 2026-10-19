#!/bin/bash
# E1 models on a pod already set up by scripts/runpod_setup.sh (run ON THE POD): Qwen2.5-VL 7B via Ollama (digest-pinned)
# and Hunyuan-DiT v1.2 (HF snapshot-pinned). Needs ~15 GB of free disk; frees the uv cache first if short.
set -euo pipefail
source /workspace/env.sh; cd /workspace/ai_to_ai_loops
QWEN_DIGEST=5ced39dfa4ba                                   # qwen2.5vl:7b as pinned in DEVIATIONS D14
HY_REV=5e96094e0ad19e7f475de8711f03634ca0ccc40c             # Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers (D12)
free_gb() { df -BG /workspace | tail -1 | awk '{print $4+0}'; }
echo "== disk: $(free_gb) GB free"
if [ "$(free_gb)" -lt 22 ]; then echo "clearing the uv cache"; uv cache clean > /dev/null 2>&1 || true; rm -rf /root/.cache/pip; echo "now $(free_gb) GB free"; fi
if [ "$(free_gb)" -lt 16 ]; then echo "!! less than 16 GB free; the Hunyuan download (14.4 GB) will not fit. Report to Brad."; exit 1; fi
curl -s localhost:11434/api/version > /dev/null || { echo "ollama is not running; run scripts/runpod_launch.sh first or start it"; exit 1; }
echo "== qwen2.5vl:7b"; ollama pull qwen2.5vl:7b 2>&1 | tail -1
GOT=$(curl -s localhost:11434/api/tags | python3 -c "import json,sys; print([m['digest'][:12] for m in json.load(sys.stdin)['models'] if m['name']=='qwen2.5vl:7b'][0])")
if [ "$GOT" != "$QWEN_DIGEST" ]; then echo "!! qwen2.5vl:7b digest $GOT != pinned $QWEN_DIGEST. The tag moved; do NOT run. Report to Brad."; exit 1; fi
echo "qwen2.5vl:7b digest $GOT OK"
echo "== Hunyuan-DiT -> $HF_HOME"
.venv/bin/python - <<PY
from huggingface_hub import snapshot_download
p = snapshot_download("Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers", revision="$HY_REV", allow_patterns=["*.json","*.txt","*.model","*.safetensors","*.py","*.md"])
print("hunyuan snapshot", p)
PY
echo "== done: $(free_gb) GB free. Smoke: CFG=configs/e1_both_runpod96.yaml OLLAMA_PAR=8 bash scripts/runpod_launch.sh smoke"
