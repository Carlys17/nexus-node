"""Build the on-chain Prover registration transaction.

Calls the registry contract's `register(moniker, feeAddr, sig)` function.
The sig is produced by signing the message:
    keccak256("nexus-register:" + proverAddress + ":" + moniker)
with the prover private key.

Outputs the calldata + sender + nonce; ready to be signed and broadcast.
"""
from __future__ import annotations
import argparse, json, os
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import keccak

REGISTRY = "0x4F5A77e7B1F4e2A0b5Cd3aA88B1b9F0E1c33C0a2"
ABI = ["function register(string moniker, address feeAddr, bytes sig)"]
CHAIN_ID = 11155111  # testnet

def register_tx(pk: str, moniker: str, fee_addr: str, nonce: int) -> dict:
    acct = Account.from_key(pk)
    msg_text = f"nexus-register:{acct.address}:{moniker}"
    digest = keccak(text=msg_text)
    # EIP-191 personal sign
    sig = Account.sign_message(encode_defunct(primitive=digest), pk).signature.hex()
    # Build calldata using web3 (no full dep needed for encoding here, just provide the args).
    from web3 import Web3
    w3 = Web3()
    contract = w3.eth.contract(address=REGISTRY, abi=ABI)
    tx = contract.functions.register(moniker, fee_addr, bytes.fromhex(sig[2:])).build_transaction({
        "from": acct.address,
        "nonce": nonce,
        "chainId": CHAIN_ID,
        "gas": 200_000,
        "gasPrice": w3.to_wei("20", "gwei"),
    })
    signed = Account.sign_transaction(tx, pk)
    return {"raw": signed.rawTransaction.hex(), "hash": signed.hash.hex(), "from": acct.address}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pk", default=os.getenv("NEXUS_PROVER_PK"))
    p.add_argument("--moniker", default="carlys-prover")
    p.add_argument("--fee-addr", default=os.getenv("NEXUS_FEE_ADDR", ""))
    p.add_argument("--nonce", type=int, required=True)
    args = p.parse_args()
    if not args.pk: raise SystemExit("--pk or NEXUS_PROVER_PK required")
    if not args.fee_addr: args.fee_addr = Account.from_key(args.pk).address
    out = register_tx(args.pk, args.moniker, args.fee_addr, args.nonce)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
