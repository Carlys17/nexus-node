#!/usr/bin/env bash
set -euo pipefail
if screen -ls | grep -q '\.nexus-node'; then
  screen -S nexus-node -X quit
  echo "stopped"
else
  echo "not running"
fi
