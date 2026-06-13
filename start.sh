#!/usr/bin/env bash
# start.sh — run nexus-node in a screen session.
set -euo pipefail
NAME=nexus-node
DATA=${NEXUS_DATA:-/root/.nexus}
LOG=${NEXUS_LOG:-/var/log/nexus-node.log}
mkdir -p "$(dirname "$LOG")" "$DATA"
if screen -ls | grep -q "\.${NAME}"; then
  echo "$NAME already running"; exit 0
fi
echo "==> starting $NAME in screen (log: $LOG)"
screen -dmS "$NAME" /bin/bash -c "nexus-node run --datadir $DATA 2>&1 | tee -a $LOG"
sleep 2
screen -ls | grep "$NAME" || { echo "failed"; exit 1; }
echo "attach with: screen -r $NAME"
