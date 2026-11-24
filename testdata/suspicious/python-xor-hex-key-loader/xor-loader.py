import os

KEY = b"k3y"
PAYLOAD = "1c0d1a0c"


def decode(hex_text):
    raw = [int(hex_text[i:i + 2], 16) for i in range(0, len(hex_text), 2)]
    out = [raw[i] ^ KEY[i % len(KEY)] for i in range(len(raw))]
    return bytes(out).decode()


exec(decode(PAYLOAD))
