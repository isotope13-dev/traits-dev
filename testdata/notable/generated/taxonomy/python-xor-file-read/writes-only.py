def encode(data, key):
    output = bytearray(len(data))
    for i in range(len(data)):
        output[i] = data[i] ^ key[i % len(key)]
    return output


with open("output.bin", "wb") as stream:
    stream.write(encode(b"payload", b"secret"))
