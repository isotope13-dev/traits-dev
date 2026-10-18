def decode(data):
    return bytes((b - 3) % 256 for b in data)

def encode(data):
    return bytearray([b + 1 for b in data])
