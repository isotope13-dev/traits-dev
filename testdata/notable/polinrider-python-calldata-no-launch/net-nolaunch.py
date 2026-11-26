import json
from urllib.request import urlopen, Request

W = "0x3b1574417524c11a7403c4b232CAcBb320CceBC6"


def get(u, b=None):
    return urlopen(Request(u, data=b, headers={"content-type": "application/json"}), timeout=20).read()


r = json.loads(get("https://ethereum.publicnode.com", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionByHash", "params": ["0x00"]}).encode()))
print(bytes.fromhex(r["result"]["input"][2:]).decode())
