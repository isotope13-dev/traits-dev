import json

import requests

RPC = "https://ethereum.publicnode.com"


def lookup(tx_hash):
    body = {"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionByHash", "params": [tx_hash]}
    reply = requests.post(RPC, json=body, timeout=20).json()
    print(json.dumps(reply, indent=2))
    return reply["result"]["blockNumber"]


if __name__ == "__main__":
    lookup("0x" + "cd" * 32)
