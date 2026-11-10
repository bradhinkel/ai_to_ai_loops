#!/bin/bash
# Laptop side: pull one run from the pod every INTERVAL seconds (default 20 min) until its progress.json says it ended.
#   nohup scripts/runpod_pull_loop.sh <run> [interval_s] [--offload] > logs/runpod_pull_loop_<run>.out 2>&1 &
# With --offload every pull also deletes the images already verified on the laptop from the pod (scripts/runpod_offload.py), which
# a long run needs because the network volume is 100 GB. Without it, this is a plain append-only pull of runs/ and logs/.
cd "$(dirname "$0")/.."
RUN=${1:?run name}; INTERVAL=${2:-1200}; OFFLOAD=""; [ "${3:-}" = "--offload" ] && OFFLOAD=1
while true; do
  date +%FT%T
  if [ -n "$OFFLOAD" ]; then .venv/bin/python scripts/runpod_offload.py "$RUN" || echo "offload failed"; else scripts/runpod_sync.sh pull || echo "pull failed"; fi
  if [ -f "runs/$RUN/progress.json" ] && grep -qE '"state": "(finished|crashed|stopped)"' "runs/$RUN/progress.json"; then echo "run ended; final pull done"; break; fi
  sleep "$INTERVAL"
done
