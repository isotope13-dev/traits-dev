def decode(source, destination, key, command_key):
    command = b'\xae\xa9\xb2\xb8\xb0\xb0\xef\xee'
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        while byte := src.read(1):
            decoded = ord(byte) ^ key
            dst.write(bytes([decoded]))
    return bytes([b ^ command_key for b in command]).decode() + ', CalculateSum'
