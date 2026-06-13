#!/usr/bin/env bash
set -euo pipefail
if command -v systemctl >/dev/null && systemctl list-unit-files | grep -q nexus.service; then
  systemctl disable --now nexus || true
  rm -f /etc/systemd/system/nexus.service
  systemctl daemon-reload
fi
screen -S nexus-node -X quit 2>/dev/null || true
rm -rf /root/.nexus
rm -f /usr/local/bin/nexus-node
echo "nexus-node removed"
