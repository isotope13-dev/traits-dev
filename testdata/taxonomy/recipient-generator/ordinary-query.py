import json
import os
import urllib.request

rpc = os.environ['ETHEREUM_RPC_URL']
wallet = os.environ['RESOLVER_WALLET']
request = urllib.request.Request(rpc, data=json.dumps({
    'jsonrpc': '2.0', 'id': 1, 'method': 'eth_getBlockByNumber',
    'params': ['latest', True]
}).encode(), headers={'Content-Type': 'application/json'})
block = json.loads(urllib.request.urlopen(request).read())['result']
for tx in reversed(block['transactions']):
    if tx['from'].lower() != wallet.lower():
        continue
    if tx['value'] != '0x0' or tx['input'] != '0x':
        continue
    print(tx['to'])
