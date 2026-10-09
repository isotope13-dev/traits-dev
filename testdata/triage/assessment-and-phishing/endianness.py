def cyclic_offset(token):
    return bytes.fromhex(token[2:])[::-1]
