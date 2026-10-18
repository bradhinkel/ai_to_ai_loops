#!/bin/bash
# Laptop side: pull runs/ and logs/ from the pod every 20 min while a_core runs (the pod has no persistent volume).
#   nohup scripts/runpod_pull_loop.sh > logs/runpod_pull_loop.out 2>&1 &
cd "$(dirname "$0")/.."
while true; do
  date +%FT%T; scripts/runpod_sync.sh pull || echo "pull failed"
  if [ -f runs/a0_core/progress.json ] && grep -qE '"state": "(finished|crashed|stopped)"' runs/a0_core/progress.json; then echo "run ended; final pull done"; break; fi
  sleep 1200
done
