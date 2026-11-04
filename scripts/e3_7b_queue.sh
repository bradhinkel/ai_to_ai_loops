#!/usr/bin/env bash
# E3-S7B laptop queue: Mistral 100-seed cell, then Qwen. Each runner is resumable; if the laptop reboots, rerun this script and both resume.
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python -m src.text_runner configs/e3_1_mistral_100.yaml > logs/e3_1_mistral_100.out 2>&1
.venv/bin/python -m src.text_runner configs/e3_1_qwen_100.yaml > logs/e3_1_qwen_100.out 2>&1
echo "QUEUE_DONE $(date)" >> logs/e3_7b_queue.out
