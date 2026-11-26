import json, urllib.request
def tx_input(h):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_getTransactionByHash","params":[h]}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://ethereum.publicnode.com", body, {"content-type":"application/json"})))
    return bytes.fromhex(r["result"]["input"][2:]).decode(errors="replace")
print(tx_input("0x00"))
