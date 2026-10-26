from pathlib import Path


def decode(data, key):
    output = bytearray(len(data))
    for i in range(len(data)):
        output[i] = data[i] ^ key[i % len(key)]
    return output


encrypted = Path("payload.bin").read_bytes()
decoded = decode(encrypted, b"secret")
print("".join(chr(value) for value in decoded if 32 <= value <= 126))
