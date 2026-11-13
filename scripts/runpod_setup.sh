#!/bin/bash
# One-time setup of a RunPod pod for A0-core (run ON THE POD as root, from any directory):
#   bash /workspace/ai_to_ai_loops/scripts/runpod_setup.sh
# Assumes the repo was rsynced to /workspace/ai_to_ai_loops by scripts/runpod_sync.sh push (from the laptop).
# Everything large lives under /workspace (the network volume): repo + runs/, Ollama models, HF cache, uv cache.
set -euo pipefail
W=/workspace; REPO=$W/ai_to_ai_loops
export HF_HOME=$W/hf OLLAMA_MODELS=$W/ollama UV_CACHE_DIR=$W/uv-cache
LLAVA_DIGEST=8dd30f6b0cb1          # llava:latest as pinned in DEVIATIONS D2
MODELS=${MODELS:-a0}               # a0 = SDXL base + llava:latest; fast = SDXL-Turbo + Moondream 2 only (D21, no Ollama)
echo "== host"; nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader; df -h $W | tail -1
DRV=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1 | cut -d. -f1)
if [ "$DRV" -lt 570 ]; then echo "!! driver $DRV < 570: cannot run the cu128 wheels pinned in requirements.txt. Pick a pod/template with CUDA 12.8 (driver >= 570)."; exit 1; fi

echo "== apt"; export DEBIAN_FRONTEND=noninteractive; apt-get update -qq && apt-get install -y -qq rsync tmux netcat-openbsd curl git zstd > /dev/null
echo "== uv"; command -v uv > /dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null); export PATH=$HOME/.local/bin:$PATH
echo "== python venv (same pins as the laptop)"
cd $REPO
[ -d .venv ] || uv venv .venv --python 3.11 > /dev/null
uv pip install --python .venv/bin/python --extra-index-url https://download.pytorch.org/whl/cu128 --index-strategy unsafe-best-match -r requirements.txt 2>&1 | tail -2
.venv/bin/python -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0),torch.cuda.get_device_capability(0))"

if [ "$MODELS" = fast ]; then
echo "== fast pair weights -> $HF_HOME (pinned revisions, D21)"
mkdir -p $W/logs
.venv/bin/python - <<'PY2'
from huggingface_hub import snapshot_download
print("sdxl-turbo", snapshot_download("stabilityai/sdxl-turbo", revision="71153311d3dbb46851df1931d3ca6e939de83304",
      allow_patterns=["*.json", "*.txt", "*/*.fp16.safetensors"]))
print("moondream2", snapshot_download("vikhyatk/moondream2", revision="2025-06-21"))
PY2
else
echo "== ollama"
command -v ollama > /dev/null || (curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1)
mkdir -p $OLLAMA_MODELS $W/logs
if ! curl -s localhost:11434/api/version > /dev/null; then
  OLLAMA_NUM_PARALLEL=${OLLAMA_PAR:-4} OLLAMA_CONTEXT_LENGTH=${OLLAMA_CTX:-8192} OLLAMA_KEEP_ALIVE=30m OLLAMA_MODELS=$OLLAMA_MODELS nohup ollama serve > $W/logs/ollama.out 2>&1 &
  for i in $(seq 1 30); do curl -s localhost:11434/api/version > /dev/null && break; sleep 1; done
fi
curl -s localhost:11434/api/version; echo
ollama pull llava:latest 2>&1 | tail -1
GOT=$(curl -s localhost:11434/api/tags | python3 -c "import json,sys; print([m['digest'][:12] for m in json.load(sys.stdin)['models'] if m['name']=='llava:latest'][0])")
if [ "$GOT" != "$LLAVA_DIGEST" ]; then echo "!! llava:latest digest $GOT != pinned $LLAVA_DIGEST. The tag moved; do NOT run. Report to Brad."; exit 1; fi
echo "llava:latest digest $GOT OK"

echo "== SDXL weights -> $HF_HOME"
.venv/bin/python - <<'PY'
import os
from diffusers import StableDiffusionXLPipeline
p = StableDiffusionXLPipeline.download("stabilityai/stable-diffusion-xl-base-1.0", variant="fp16", torch_dtype=None)
print("sdxl snapshot", p)
PY
fi
mkdir -p $REPO/runs $REPO/logs
cat > $W/env.sh <<ENV
export HF_HOME=$W/hf OLLAMA_MODELS=$W/ollama UV_CACHE_DIR=$W/uv-cache PATH=\$HOME/.local/bin:\$PATH
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
ENV
echo "== done. Next: source /workspace/env.sh; cd $REPO; bash scripts/runpod_launch.sh smoke   (then: bash scripts/runpod_launch.sh core)"
