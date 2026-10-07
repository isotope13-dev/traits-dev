def decode(data, key):
    output = bytearray(len(data))
    for i in range(len(data)):
        output[i] = data[i] ^ key[i % len(key)]
    return output


stream = open("payload.bin")
print("".join(chr(value) for value in decode(b"ciphertext", b"secret")
             if 32 <= value <= 126))
