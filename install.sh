#!/usr/bin/env bash
# install.sh — install the Nexus prover node and configure it.
set -euo pipefail
REPO="${NEXUS_REPO:-nexus-network/nexus-node}"
VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep -m1 '"tag_name"' | cut -d'"' -f4)
VERSION="${VERSION#v}"
ARCH=$(uname -m)
case "$ARCH" in x86_64) BIN=amd64 ;; aarch64) BIN=arm64 ;; *) echo "bad arch $ARCH"; exit 1 ;; esac

URL="https://github.com/${REPO}/releases/download/v${VERSION}/nexus-node-${VERSION}-linux-${BIN}.tar.gz"
echo "==> installing nexus-node v${VERSION} (${BIN})"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
curl -fsSL "$URL" -o "$TMP/nexus.tgz"
tar -xzf "$TMP/nexus.tgz" -C "$TMP"
install -m 0755 "$TMP/nexus-node" /usr/local/bin/nexus-node

mkdir -p /root/.nexus
[[ -f /root/.nexus/config.toml ]] || cp config.toml.example /root/.nexus/config.toml

if [[ ! -f /root/.nexus/prover.key ]]; then
  echo "==> generating prover key"
  /usr/local/bin/nexus-node key gen --out /root/.nexus/prover.key
fi

if command -v systemctl >/dev/null && systemctl --no-pager status >/dev/null 2>&1; then
  cp nexus.service /etc/systemd/system/nexus.service
  systemctl daemon-reload
  systemctl enable --now nexus
  echo "==> service installed: nexus (systemd)"
else
  echo "==> no systemd; use ./start.sh"
fi

nexus-node --version
