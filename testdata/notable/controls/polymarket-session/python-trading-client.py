def sell(client, contract):
    order = client.create_market_order({"side": "SELL", "amount": 2})
    client.post_order(order)
    return contract.encode_abi("safeBatchTransferFrom", ["owner", "recipient", [1], [2], b""])
