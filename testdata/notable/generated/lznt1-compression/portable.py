import lznt1

def encode(payload):
    return lznt1.compress(payload)
