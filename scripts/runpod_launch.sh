#!/bin/bash
# On the pod: start Ollama if needed, then the runner in the background, plus the web UI on 127.0.0.1:8787.
#   CFG=configs/<cfg>.yaml bash scripts/runpod_launch.sh smoke   -> <run_name>_smoke: 16 traj x 3 steps with the config's batch/parallel settings
#   CFG=configs/<cfg>.yaml bash scripts/runpod_launch.sh pilot   -> <run_name>_pilot: 20 traj x 100 steps
#   CFG=configs/<cfg>.yaml bash scripts/runpod_launch.sh core    -> <run_name>: the config as written (100 traj x 100 steps)
#   COUNT=20 CFG=configs/<cfg>.yaml bash scripts/runpod_launch.sh part -> <run_name> itself, first COUNT trajectories only (the A0-1000 pilot runs in the real directory)
# CFG defaults to configs/a0_core_runpod.yaml (48 GB). The 96 GB configs (a0_core_runpod96, e1_*_runpod96) expect OLLAMA_PAR=8.
set -euo pipefail
source /workspace/env.sh; cd /workspace/ai_to_ai_loops
CFG=${CFG:-configs/a0_core_runpod.yaml}
NAME=$(.venv/bin/python -c "from src.config import load_config; print(load_config('$CFG')['run_name'])")
if ! curl -s localhost:11434/api/version > /dev/null; then
  OLLAMA_NUM_PARALLEL=${OLLAMA_PAR:-4} OLLAMA_KEEP_ALIVE=30m nohup ollama serve > /workspace/logs/ollama.out 2>&1 &
  for i in $(seq 1 30); do curl -s localhost:11434/api/version > /dev/null && break; sleep 1; done
fi
case "${1:-}" in
  smoke) RUN=${NAME}_smoke; ARGS="--run-name $RUN --steps 3 --count 16" ;;
  pilot) RUN=${NAME}_pilot; ARGS="--run-name $RUN --count 20" ;;
  core)  RUN=$NAME; ARGS="" ;;
  part)  RUN=$NAME; ARGS="--count ${COUNT:?set COUNT}" ;;
  *) echo "usage: CFG=configs/<cfg>.yaml $0 smoke|pilot|core|part"; exit 1 ;;
esac
if pgrep -f "src.runner" > /dev/null; then echo "a runner is already running:"; pgrep -af src.runner; exit 1; fi
nohup .venv/bin/python -m src.runner $CFG $ARGS > logs/$RUN.out 2>&1 &
echo $! > logs/$RUN.pid; echo "runner pid $(cat logs/$RUN.pid), config $CFG, log logs/$RUN.log"
pgrep -f "uvicorn src.web.app" > /dev/null || (nohup .venv/bin/uvicorn src.web.app:app --host 127.0.0.1 --port 8787 > logs/web.out 2>&1 & echo "web UI on pod port 8787 (ssh -L 8787:127.0.0.1:8787 ...)")
