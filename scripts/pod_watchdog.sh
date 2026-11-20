#!/bin/bash
# Pod side: keeps a seeded run and the T1 caption arm going through runner crashes and container restarts (ESC-C: a volume I/O
# error 2026-11-16 and a container restart 2026-11-17 each left the pod idle until someone looked).
#   setsid nohup bash scripts/pod_watchdog.sh > /dev/null 2>&1 &          (log: /workspace/logs/watchdog.log)
# Boot: /pre_start.sh (run by the image's /start.sh on every container start) launches this same line, so it survives restarts.
# Every 5 min:
#   run not finished, no runner process   -> resume it (CFG via scripts/runpod_launch.sh core; the runner resumes idempotently from
#                                            the last complete step and fills in a partial step), after copying logs/<run>.out aside
#   run not finished, runner alive but progress.json older than 45 min -> log a warning only (never kills a live runner)
#   run finished, T1 not finished, nothing T1 running -> start /workspace/queue_t1.sh (which starts Ollama if needed and resumes T1)
#   both finished -> exit. THEN=none (T1-cont pod, 2026-11-20): no T1 step; exit as soon as the run is finished.
#   AUTOSTOP_MIN=N (with THEN=none): N minutes after the run finishes (time for the laptop's last pull), stop this pod through the REST v2
#   pod action (runpodctl 1.14 rejects the key) with the pod-scoped RUNPOD_API_KEY from the container environment (stop, not terminate: the volume disk and the data stay)
# At most MAX_RESTARTS automatic restarts in total (counted in the log), so a broken volume cannot loop forever. One instance only (flock).
cd /workspace/ai_to_ai_loops || exit 1
source /workspace/env.sh
RUN=${RUN:-esc_c}; CFG=${CFG:-configs/esc_c_runpod.yaml}; MAX_RESTARTS=${MAX_RESTARTS:-6}; STALE=${STALE:-2700}; EVERY=${EVERY:-300}; THEN=${THEN:-t1}; AUTOSTOP_MIN=${AUTOSTOP_MIN:-}
LOG=/workspace/logs/watchdog.log; mkdir -p /workspace/logs; exec >> "$LOG" 2>&1
log() { echo "$(date -u +%FT%T) $*"; }
exec 9> /workspace/.watchdog.lock; flock -n 9 || { log "another watchdog holds the lock; exiting"; exit 0; }
state() { python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['state'])" "$1" 2>/dev/null || echo none; }
restarts() { grep -c " RESTART " "$LOG"; }
log "watchdog start pid $$ run $RUN cfg $CFG then $THEN (restarts so far $(restarts) of $MAX_RESTARTS)"
while true; do
  s=$(state runs/$RUN/progress.json)
  if [ "$s" != finished ]; then
    if ! pgrep -f "python -m src[.]runner" > /dev/null; then
      if [ "$(restarts)" -ge "$MAX_RESTARTS" ]; then log "runner down (state $s); restart limit reached, not restarting"
      else
        log " RESTART runner (state $s, no runner process)"
        cp -p logs/$RUN.out logs/$RUN.before_restart_$(date -u +%m%d%H%M).out 2>/dev/null
        CFG=$CFG OLLAMA_PAR=8 bash scripts/runpod_launch.sh core 9>&- 2>&1 | tail -2
      fi
    else
      age=$(( $(date +%s) - $(stat -c %Y runs/$RUN/progress.json 2>/dev/null || date +%s) ))
      [ "$age" -gt "$STALE" ] && log "WARNING runner alive but runs/$RUN/progress.json is ${age}s old (not touched)"
    fi
  else
    if [ "$THEN" = none ]; then
      if [ -n "$AUTOSTOP_MIN" ]; then
        log "$RUN finished; stopping the pod in $AUTOSTOP_MIN min"; sleep $(( AUTOSTOP_MIN * 60 ))
        eval "$(tr '\0' '\n' < /proc/1/environ | grep -E '^RUNPOD_(API_KEY|POD_ID)=' | sed 's/^/export /')"
        log "AUTOSTOP stop pod $RUNPOD_POD_ID"
        curl -s -X POST -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" -d '{"action":"stop"}' \
          "https://api.runpod.io/v2/pods/$RUNPOD_POD_ID/action" | head -c 300; echo
      fi
      log "$RUN finished; watchdog exits"; exit 0
    fi
    t=$(state runs/t1_caption/progress.json)
    if [ "$t" = finished ]; then log "$RUN and t1_caption finished; watchdog exits"; exit 0; fi
    if ! pgrep -f "queue_t1[.]sh|src[.]t1_caption" > /dev/null; then
      if [ "$(restarts)" -ge "$MAX_RESTARTS" ]; then log "t1_caption down (state $t); restart limit reached, not restarting"
      else log " RESTART t1 (t1 state $t)"; setsid nohup /workspace/queue_t1.sh >> logs/queue_t1.out 2>&1 < /dev/null 9>&- & fi
    fi
  fi
  sleep "$EVERY"
done
