#!/usr/bin/env bash
# Run the FAST-100 pilot, then the FAST-X crossed cell, on the laptop (2026-11-12). Each runner resumes idempotently if restarted.
cd "$(dirname "$0")/.." || exit 1
for c in configs/fast_100.yaml configs/fast_x_llava.yaml; do
  echo "$(date -Is) start $c"; .venv/bin/python -m src.runner "$c" >> "logs/$(basename "$c" .yaml).out" 2>&1; echo "$(date -Is) exit $? $c"
done
