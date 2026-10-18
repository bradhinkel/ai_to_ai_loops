#!/bin/bash
# On the pod: start Ollama if needed, then the runner in the background, plus the web UI on 127.0.0.1:8787.
#   bash scripts/runpod_launch.sh smoke   -> a0_smoke_runpod: 16 traj x 3 steps with the core's batch/parallel settings
#   bash scripts/runpod_launch.sh core    -> a0_core (100 traj x 100 steps)
# CFG picks the config (default configs/a0_core_runpod.yaml for 48 GB; CFG=configs/a0_core_runpod96.yaml OLLAMA_PAR=8 for the 96 GB card).
set -euo pipefail
source /workspace/env.sh; cd /workspace/ai_to_ai_loops
CFG=${CFG:-configs/a0_core_runpod.yaml}
if ! curl -s localhost:11434/api/version > /dev/null; then
  OLLAMA_NUM_PARALLEL=${OLLAMA_PAR:-4} OLLAMA_KEEP_ALIVE=30m nohup ollama serve > /workspace/logs/ollama.out 2>&1 &
  for i in $(seq 1 30); do curl -s localhost:11434/api/version > /dev/null && break; sleep 1; done
fi
case "${1:-}" in
  smoke) ARGS="--run-name a0_smoke_runpod --steps 3 --count 16"; RUN=a0_smoke_runpod ;;
  core)  ARGS=""; RUN=a0_core ;;
  *) echo "usage: $0 smoke|core"; exit 1 ;;
esac
if pgrep -f "src.runner" > /dev/null; then echo "a runner is already running:"; pgrep -af src.runner; exit 1; fi
nohup .venv/bin/python -m src.runner $CFG $ARGS > logs/$RUN.out 2>&1 &
echo $! > logs/$RUN.pid; echo "runner pid $(cat logs/$RUN.pid), log logs/$RUN.log"
pgrep -f "uvicorn src.web.app" > /dev/null || (nohup .venv/bin/uvicorn src.web.app:app --host 127.0.0.1 --port 8787 > logs/web.out 2>&1 & echo "web UI on pod port 8787 (ssh -L 8787:127.0.0.1:8787 ...)")
