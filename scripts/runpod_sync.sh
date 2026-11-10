#!/bin/bash
# From the laptop. Needs RUNPOD_SSH="root@HOST -p PORT" (the 'SSH over exposed TCP' line from the pod's Connect dialog)
# in a git-ignored .env at the repo root, and the key ~/.ssh/claude_runpod registered in RunPod > Settings > SSH Public Keys.
#   scripts/runpod_sync.sh push    code + configs + hintze_osf + requirements to /workspace/ai_to_ai_loops (never runs/)
#   scripts/runpod_sync.sh pull    runs/ and logs/ from the pod into this repo (append-only: no --delete, never overwrites a newer local file)
#   scripts/runpod_sync.sh ssh     open a shell (with the web UI forwarded to http://127.0.0.1:8788)
#   scripts/runpod_sync.sh status  one-line progress of the running job
#   scripts/runpod_sync.sh push-run <run> [png_from]   runs/<run>/ to the pod (seeded continuation, D20); images below step png_from are left out
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; source .env; set +a
: "${RUNPOD_SSH:?set RUNPOD_SSH in .env, e.g. RUNPOD_SSH=\"root@1.2.3.4 -p 12345\"}"
HOST=${RUNPOD_SSH%% *}; PORT=${RUNPOD_SSH##*-p }
SSH="ssh -i $HOME/.ssh/claude_runpod -o StrictHostKeyChecking=accept-new -p $PORT"
case "${1:-}" in
  push) git rev-parse HEAD > GIT_COMMIT; git status --porcelain | grep -q . && echo "(working tree has uncommitted changes; GIT_COMMIT records HEAD)"
        rsync -az --no-o --no-g -e "$SSH" --exclude .venv --exclude runs --exclude logs --exclude data --exclude Resources --exclude .git --exclude __pycache__ --exclude .env \
          ./ "$HOST:/workspace/ai_to_ai_loops/" && echo pushed ;;
  pull) mkdir -p runs logs
        rsync -az --no-o --no-g --update -e "$SSH" "$HOST:/workspace/ai_to_ai_loops/runs/" runs/ && rsync -az --no-o --no-g --update -e "$SSH" "$HOST:/workspace/ai_to_ai_loops/logs/" logs/runpod/ && echo pulled && du -sh runs/a0_core 2>/dev/null ;;
  push-run) RUN=${2:?run name}; EX=(); for s in $(seq 0 $(( ${3:-0} - 1 ))); do EX+=(--exclude "step_$(printf %03d $s).png"); done
        rsync -az --no-o --no-g --ignore-existing -e "$SSH" "${EX[@]}" "runs/$RUN/" "$HOST:/workspace/ai_to_ai_loops/runs/$RUN/" && echo "pushed runs/$RUN (images from step ${3:-0}; existing pod files untouched)" ;;
  ssh)  $SSH -L 8788:127.0.0.1:8787 "$HOST" ;;
  status) $SSH "$HOST" 'cd /workspace/ai_to_ai_loops && python3 -c "import json,glob,os;f=max(glob.glob(\"runs/*/progress.json\"),key=os.path.getmtime);p=json.load(open(f));print(f,p[\"state\"],\"step\",p[\"step\"],p[\"completed_steps\"],\"/\",p[\"total_steps\"],\"s/traj-step\",p.get(\"s_per_traj_step\"),\"eta h\",p.get(\"eta_hours\"),p[\"updated\"])" 2>/dev/null || ls -t logs/*.log | head -1 | xargs tail -2' ;;
  *) echo "usage: $0 push|pull|push-run <run> [png_from]|ssh|status"; exit 1 ;;
esac
