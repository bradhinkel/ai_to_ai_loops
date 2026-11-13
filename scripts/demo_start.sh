#!/bin/bash
# Start a live demo grid on the laptop: scripts/demo_start.sh <side 3|4|5> [through_step=49]
#   - builds runs/demo_base once (fast_100 trajectories 0-19 copied through step 49; trajectories 20-24 run fresh to step 49),
#   - stops any demo runner still alive (control.json "stopped", then SIGTERM after 90 s),
#   - seeds a fresh runs/demo_<side>x<side>_<stamp> from demo_base and starts the runner on side^2 chains (two-pass, steps to 1999).
# Prints the run name. runs/ stays append-only: every demo is a new directory.
set -euo pipefail
cd "$(dirname "$0")/.."
SIDE=${1:?grid side 3, 4 or 5}; THROUGH=${2:-49}; N=$((SIDE * SIDE)); PY=.venv/bin/python
mkdir -p logs
alive() { [ -f "logs/$1.pid" ] && kill -0 "$(cat "logs/$1.pid")" 2>/dev/null; }
for p in logs/demo_*.pid; do
  [ -e "$p" ] || continue; r=$(basename "$p" .pid)
  if alive "$r"; then
    echo "stopping $r" >&2
    printf '{"state": "stopped", "set_at": "%s"}' "$(date +%FT%T)" > "runs/$r/control.json.tmp" && mv "runs/$r/control.json.tmp" "runs/$r/control.json"
    for i in $(seq 1 90); do alive "$r" || break; sleep 1; done
    alive "$r" && kill "$(cat "$p")" && sleep 3
  fi
done
if [ ! -f runs/demo_base/BASE_READY ]; then
  echo "building runs/demo_base (one-time, ~6 min)" >&2
  [ -d runs/demo_base/traj_000 ] || $PY scripts/seed_continuation.py --source fast_100 --target demo_base --through "$THROUGH" --first 0 --count 20 >&2
  $PY -m src.runner configs/demo_fast.yaml --run-name demo_base --count 25 --steps $((THROUGH + 1)) >> logs/demo_base.out 2>&1
  date -Is > runs/demo_base/BASE_READY
fi
RUN=demo_${SIDE}x${SIDE}_$(date +%Y%m%d_%H%M%S)
$PY scripts/seed_continuation.py --source demo_base --target "$RUN" --through "$THROUGH" --first 0 --count "$N" >&2
nohup $PY -m src.runner configs/demo_fast.yaml --run-name "$RUN" --count "$N" > "logs/$RUN.out" 2>&1 < /dev/null &
echo $! > "logs/$RUN.pid"; echo "$RUN"
