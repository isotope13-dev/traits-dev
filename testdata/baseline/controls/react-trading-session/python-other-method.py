def build(contract, args):
    return contract.encode_abi("balanceOf", args=args)
