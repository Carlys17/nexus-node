#!/usr/bin/env bash
# status.sh — print node status.
set -euo pipefail
DATA=${NEXUS_DATA:-/root/.nexus}
RPC=${NEXUS_RPC:-127.0.0.1:7333}
echo "height : $(nexus-node rpc --rpc=$RPC getblockcount 2>/dev/null || echo n/a)"
echo "peers  : $(nexus-node rpc --rpc=$RPC getconnectioncount 2>/dev/null || echo n/a)"
echo "balance: $(nexus-node rpc --rpc=$RPC getbalance 2>/dev/null || echo n/a)"
echo "prover : $(cat $DATA/prover.key.pub 2>/dev/null || echo n/a)"
