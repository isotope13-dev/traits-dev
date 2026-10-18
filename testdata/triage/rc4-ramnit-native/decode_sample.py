#!/usr/bin/env python3
"""Reproduce the sample-specific static extractions. Does not execute or fetch.

The transform constants belong to this analysis, not to stng or detection
rules. Detection rules intentionally do not require these keys or this URL.
"""
import argparse
import base64
import hashlib
from pathlib import Path
import struct


def rc4(data, key):
    state = list(range(256))
    j = 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) & 255
        state[i], state[j] = state[j], state[i]
    i = j = 0
    output = bytearray()
    for byte in data:
        i = (i + 1) & 255
        j = (j + state[i]) & 255
        state[i], state[j] = state[j], state[i]
        output.append(byte ^ state[(state[i] + state[j]) & 255])
    return bytes(output)


def extract(sample, output):
    data = sample.read_bytes()
    expected = '5afebd696654a9060cbce22c25516db9c4e85b5e0faa0818d2ea3dbfdef377d5'
    assert hashlib.sha256(data).hexdigest() == expected, 'Different sample'
    encoded = data[0x1e30:].split(b'\0', 1)[0]
    transformed = bytes(((byte + 0x7a) & 255) ^ 0x59
                        for byte in base64.b64decode(encoded))
    url = rc4(transformed, b'Getong538').rstrip(b'\0').decode('ascii')
    print('Decoded URL:', url)
    key_size = struct.unpack_from('<I', data, 0x2734)[0]
    key = data[0x2738:0x2738 + key_size][1:][::-1]
    size = struct.unpack_from('<I', data, 0x296e)[0]
    encrypted = data[0x2973:0x2973 + size]
    payload = bytes(byte ^ key[i % len(key)] for i, byte in enumerate(encrypted))
    assert hashlib.sha256(payload).hexdigest() == 'd7ec3fcd80b3961e5bab97015c91c843803bb915c13a4a35dfb5e9bdf556c6d3'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'overlay-payload.exe').write_bytes(payload)
    # The inner host is UPX-packed and has an appended parasite. Repair a
    # separate copy for UPX; retain the unmodified extracted member above.
    repaired = bytearray(payload[:0x14800])
    pe_offset = struct.unpack_from('<I', repaired, 0x3c)[0]
    sections = pe_offset + 24 + struct.unpack_from('<H', repaired, pe_offset + 20)[0]
    struct.pack_into('<I', repaired, sections + 2 * 40 + 16, 0x7200)
    (output / 'payload-upx-repaired.exe').write_bytes(repaired)
    print('Extracted payload SHA-256:', hashlib.sha256(payload).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    extract(args.sample, args.out)
