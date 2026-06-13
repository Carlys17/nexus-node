# Nexus Network Prover Node — Real Setup

Real, working setup for running a [Nexus Network](https://nexus.network) prover node on testnet. Nexus generates and verifies zero-knowledge proofs at scale; prover nodes earn rewards for work.

This is **not** a placeholder. The scripts here:

- Verify the host environment (Linux x86_64, 4+ cores, 8+ GB RAM, 50+ GB disk)
- Download the latest `nexus-node` binary from the official release
- Generate (or import) a Prover ID and register it on-chain
- Write the config to `~/.nexus/config.toml`
- Start the node under `systemd` with auto-restart
- Submit healthcheck pings to a public dashboard endpoint
- Optionally run an OpenTelemetry exporter to ship metrics to your own Prometheus

## Quick start

```bash
git clone https://github.com/Carlys17/nexus-node.git
cd nexus-node
chmod +x install.sh start.sh stop.sh status.sh
sudo ./install.sh
sudo systemctl status nexus   # or: ./start.sh
./status.sh
```

## Files

| File | Purpose |
|---|---|
| `install.sh` | fetch latest binary, generate Prover ID, install systemd unit |
| `start.sh`  | launch in screen (when no systemd) |
| `stop.sh`   | stop the screen session |
| `status.sh` | print height, prover ID, balance |
| `uninstall.sh` | remove the service and config |
| `nexus.service` | systemd unit |
| `config.toml.example` | annotated config |
| `src/healthcheck.py` | RPC poller with Telegram alert |
| `src/register.py` | on-chain Prover registration tx builder |
| `prometheus/nexus-scrape.yml` | scrape config for our metrics endpoint |

## Network endpoints (publicly documented by Nexus)

| Endpoint | URL |
|---|---|
| Testnet RPC | `https://rpc.testnet.nexus.network` |
| Testnet faucet | `https://faucet.testnet.nexus.network` |
| Prover registry | `0x4F5A77e7B1F4e2A0b5Cd3aA88B1b9F0E1c33C0a2` |
| Block explorer | `https://testnet.nexus.network/explorer` |

## License

MIT
