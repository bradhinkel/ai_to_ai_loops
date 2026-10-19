#!/bin/bash
# On the pod: run several core cells back to back, each after the previous one finished cleanly.
#   nohup bash scripts/runpod_queue.sh configs/e1_gen_runpod96.yaml configs/e1_both_runpod96.yaml ... > logs/queue.out 2>&1 &
# Waits first for any running runner and for a queued benchmark (logs/bench_hunyuan.log without BENCH_EXIT) to finish.
set -uo pipefail
source /workspace/env.sh; cd /workspace/ai_to_ai_loops
state() { python3 -c "import json;print(json.load(open('runs/$1/progress.json'))['state'])" 2>/dev/null || echo missing; }
runner_alive() { pgrep -f "python -m src[.]runner" > /dev/null; }
for CFG in "$@"; do
  NAME=$(.venv/bin/python -c "from src.config import load_config; print(load_config('$CFG')['run_name'])")
  while runner_alive; do sleep 60; done
  if [ -f logs/bench_hunyuan.log ]; then while ! grep -q BENCH_EXIT logs/bench_hunyuan.log; do sleep 60; done; fi
  echo "$(date -u +%FT%TZ) launching $NAME ($CFG)"
  CFG=$CFG OLLAMA_PAR=8 bash scripts/runpod_launch.sh core || { echo "launch failed for $NAME"; exit 1; }
  sleep 120
  while runner_alive; do sleep 120; done
  S=$(state "$NAME"); echo "$(date -u +%FT%TZ) $NAME ended with state $S"
  [ "$S" = "finished" ] || { echo "stopping the queue: $NAME state $S"; exit 1; }
done
echo "$(date -u +%FT%TZ) QUEUE_DONE"
