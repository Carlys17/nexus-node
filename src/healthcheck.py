"""Long-running RPC poller for the Nexus prover. Alerts via Telegram on stall."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, urllib.request

def rpc(rpc_addr, method, params=None):
    body = json.dumps({"jsonrpc":"1.0","id":"hc","method":method,"params":params or []}).encode()
    req = urllib.request.Request(f"http://{rpc_addr}", data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def send_tg(bot, chat, text):
    url = f"https://api.telegram.org/bot{bot}/sendMessage"
    body = json.dumps({"chat_id":chat,"text":text,"parse_mode":"Markdown"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}), timeout=10).read()
    except Exception as e:
        print(f"tg: {e}", file=sys.stderr)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rpc", default=os.getenv("NEXUS_RPC","127.0.0.1:7333"))
    p.add_argument("--interval", type=int, default=60)
    p.add_argument("--tg-bot", default=os.getenv("TG_BOT"))
    p.add_argument("--tg-chat", default=os.getenv("TG_CHAT"))
    args = p.parse_args()

    last = None
    fails = 0
    while True:
        try:
            h = rpc(args.rpc, "getblockcount").get("result", 0)
            p_ = rpc(args.rpc, "getconnectioncount").get("result", 0)
            print(f"[{time.strftime('%H:%M:%S')}] height={h} peers={p_}")
            if last == h and p_ == 0:
                msg = f"⚠️ Nexus stalled: h={h} peers=0"
                print(msg)
                if args.tg_bot: send_tg(args.tg_bot, args.tg_chat, msg)
            last = h
            fails = 0
        except Exception as e:
            print(f"err: {e}")
            fails += 1
            if fails >= 3 and args.tg_bot:
                send_tg(args.tg_bot, args.tg_chat, f"❌ Nexus RPC down 3x: {e}")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
