# Nexus Network Node Setup Guide

Complete guide for setting up and running a Nexus Network prover node.

## Overview

Nexus Network is a verifiable computing network that generates and verifies zero-knowledge proofs at scale. By running a node, you contribute to the network's proving capacity and earn rewards.

## System Requirements

### Minimum Requirements
- **CPU**: 4 cores (8 threads recommended)
- **RAM**: 8 GB (16 GB recommended)
- **Storage**: 50 GB SSD
- **Network**: Stable internet connection (10 Mbps+)
- **OS**: Ubuntu 20.04/22.04 LTS, Debian 11/12

### Recommended for Production
- **CPU**: 8+ cores (AMD Ryzen or Intel Xeon)
- **RAM**: 32 GB DDR4
- **Storage**: 100 GB NVMe SSD
- **Network**: 100 Mbps+ with static IP
- **GPU**: Optional (for accelerated proving)

## Installation

### Step 1: System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y curl wget git build-essential pkg-config libssl-dev

# Install Rust (required for building from source)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Step 2: Install Nexus CLI

```bash
# Download and install Nexus CLI
curl -sSL https://cli.nexus.xyz/ | sh

# Or download specific version
wget https://github.com/nexus-xyz/nexus-cli/releases/latest/download/nexus-cli-linux-x64
chmod +x nexus-cli-linux-x64
sudo mv nexus-cli-linux-x64 /usr/local/bin/nexus-cli

# Verify installation
nexus-cli --version
```

### Step 3: Configure Node

```bash
# Create configuration directory
mkdir -p ~/.nexus

# Initialize configuration
nexus-cli config init

# Edit configuration
cat > ~/.nexus/config.json << 'EOF'
{
  "network": "testnet",
  "node": {
    "name": "your-node-name",
    "region": "auto",
    "parallel_jobs": 4
  },
  "proving": {
    "enabled": true,
    "max_concurrent_proofs": 2,
    "memory_limit": "8GB"
  },
  "rewards": {
    "address": "YOUR_ETHEREUM_ADDRESS"
  }
}
EOF
```

### Step 4: Start Node

```bash
# Start node in foreground (for testing)
nexus-cli start

# Or start as systemd service
sudo tee /etc/systemd/system/nexus.service > /dev/null << 'EOF'
[Unit]
Description=Nexus Network Node
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME
ExecStart=/usr/local/bin/nexus-cli start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable nexus
sudo systemctl start nexus
```

### Step 5: Verify Node Status

```bash
# Check node status
nexus-cli status

# View logs
sudo journalctl -u nexus -f

# Check connected peers
nexus-cli peers list
```

## Troubleshooting

### Issue: Node fails to start

**Symptoms**: `nexus-cli start` returns error immediately

**Solutions**:
1. Check configuration file syntax:
   ```bash
   cat ~/.nexus/config.json | python3 -m json.tool
   ```

2. Verify port availability:
   ```bash
   netstat -tlnp | grep -E '8080|30303'
   ```

3. Check disk space:
   ```bash
   df -h
   ```

### Issue: Low proof generation rate

**Symptoms**: Node running but few proofs generated

**Solutions**:
1. Increase parallel jobs in config:
   ```json
   "parallel_jobs": 8
   ```

2. Check CPU usage:
   ```bash
   htop
   ```

3. Verify network latency:
   ```bash
   ping api.nexus.xyz
   ```

### Issue: Connection timeout

**Symptoms**: Node disconnects frequently

**Solutions**:
1. Check firewall rules:
   ```bash
   sudo ufw allow 30303/tcp
   sudo ufw allow 30303/udp
   ```

2. Use static IP or DDNS
3. Configure router port forwarding

## FAQ

**Q: How much can I earn?**
A: Rewards depend on network demand, your node's proving capacity, and stake. Check the Nexus dashboard for current rates.

**Q: Can I run multiple nodes?**
A: Yes, but each node needs unique configuration and sufficient resources.

**Q: Is GPU required?**
A: No, but GPU acceleration can significantly improve proof generation speed.

**Q: How do I update the node?**
A: ```bash
nexus-cli stop
nexus-cli update
nexus-cli start
```

## Resources

- [Official Documentation](https://docs.nexus.xyz)
- [Nexus Explorer](https://explorer.nexus.xyz)
- [Discord Community](https://discord.gg/nexus)
- [GitHub Repository](https://github.com/nexus-xyz)

## License

MIT License - See LICENSE file
