def build(contract, args):
    return contract.encode_abi("safeBatchTransferFrom", args=args)
