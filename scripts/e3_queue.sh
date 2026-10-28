#!/usr/bin/env bash
# Run E3 text-loop cells one after another on the laptop (SPEC2 §4 E3). Each cell starts only if the previous one exited with
# progress.json state "finished"; otherwise the queue stops and says so. Resume-safe: re-running the queue skips finished cells
# and resumes a partial one (the runner resumes by file presence).
#   nohup scripts/e3_queue.sh configs/e3_1_qwen.yaml configs/e3_2_qwen.yaml ... > logs/e3_queue.out 2>&1 &
set -u
cd "$(dirname "$0")/.."
state() { python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('state','?'))" "$1" 2>/dev/null || echo none; }
for cfg in "$@"; do
  run=$(basename "$cfg" .yaml)
  if [ "$(state runs/$run/progress.json)" = finished ]; then echo "$(date -Is) $run already finished; skipping"; continue; fi
  echo "$(date -Is) START $run"
  .venv/bin/python -m src.text_runner "$cfg" >> "logs/$run.out" 2>&1
  st=$(state runs/$run/progress.json)
  echo "$(date -Is) END $run state=$st"
  if [ "$st" != finished ]; then echo "$(date -Is) QUEUE STOPPED: $run did not finish (state=$st); fix and re-run the same command"; exit 1; fi
done
echo "$(date -Is) QUEUE_DONE"
