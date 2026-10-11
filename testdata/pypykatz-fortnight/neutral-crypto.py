def xor(data, key):
    for i in range(len(data)):
        data[i] = data[i] ^ key
    return data

plaintext = b"result"
print(plaintext)
