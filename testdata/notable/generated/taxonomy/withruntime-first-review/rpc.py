def request(contract):
    return {'jsonrpc': '2.0', 'method': 'eth_call',
            'params': [{'to': contract, 'data': '0x12345678'}, 'latest']}
