#!/usr/bin/env python3
"""Build deterministic PNGs containing shell text; never execute the payload.

Uses only the Python standard library. Optional --stegano-cli adds fixtures
from the real stegano-lsb CLI, with byte-for-byte reveal checks.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import zlib

WIDTH = HEIGHT = 128
DEFAULT_PAYLOAD = b"#!/bin/sh\nprintf '%s\\n' 'PNG steganography fixture'\nid\nuname -a\n"


def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))


def write_png(path, pixels):
    rows = b''.join(b'\0' + pixels[y * WIDTH * 3:(y + 1) * WIDTH * 3] for y in range(HEIGHT))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'
                     + chunk(b'IHDR', struct.pack('>IIBBBBB', WIDTH, HEIGHT, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(rows, 9)) + chunk(b'IEND', b''))


def read_pixels(path):
    """Read this builder's RGB8, filter-zero files back from compressed PNG."""
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    offset = 8
    compressed = b''
    while offset < len(data):
        size = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        body = data[offset + 8:offset + 8 + size]
        assert zlib.crc32(kind + body) == struct.unpack('>I', data[offset + 8 + size:offset + 12 + size])[0]
        if kind == b'IDAT':
            compressed += body
        offset += size + 12
    rows = zlib.decompress(compressed)
    stride = WIDTH * 3 + 1
    assert len(rows) == stride * HEIGHT and all(rows[y * stride] == 0 for y in range(HEIGHT))
    return b''.join(rows[y * stride + 1:(y + 1) * stride] for y in range(HEIGHT))


def slots(channels, order, prime):
    coordinates = ((x, y) for y in range(HEIGHT) for x in range(WIDTH)) if order == 'xy' else (
        (x, y) for x in range(WIDTH) for y in range(HEIGHT))
    for index, (x, y) in enumerate(coordinates):
        if prime and (index < 2 or any(index % d == 0 for d in range(2, math.isqrt(index) + 1))):
            continue
        for channel in channels:
            yield (y * WIDTH + x) * 3 + 'rgb'.index(channel)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--payload-file', type=Path)
    parser.add_argument('--stegano-cli', type=Path)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    payload = args.payload_file.read_bytes() if args.payload_file else DEFAULT_PAYLOAD
    if not payload:
        parser.error('payload must not be empty')
    (out / 'payload.sh').write_bytes(payload)
    cover = bytearray(v for y in range(HEIGHT) for x in range(WIDTH)
                      for v in (x * 2, y * 2, (x + y) % 256))
    write_png(out / 'cover.png', cover)
    manifest = dict(payload_sha256=hashlib.sha256(payload).hexdigest(),payload_bytes=len(payload),
                    commands_executed=False,fixtures=[])
    variants = [('rgb-lsb-xy', 'rgb', 'xy', False, 0),
                ('bgr-lsb-yx-prime', 'bgr', 'yx', True, 0),
                ('red-second-bit', 'r', 'xy', False, 1)]
    bits = [(byte >> shift) & 1 for byte in payload + b'\0' for shift in range(7, -1, -1)]
    for name, channels, order, prime, plane in variants:
        positions = list(slots(channels, order, prime))
        if len(bits) > len(positions):
            parser.error(f'payload exceeds {name} carrier capacity')
        pixels = cover.copy()
        for position, bit in zip(positions, bits):
            pixels[position] = (pixels[position] & ~(1 << plane)) | (bit << plane)
        path = out / (name + '.png')
        write_png(path, pixels)
        decoded = read_pixels(path)
        recovered_bits = [(decoded[p] >> plane) & 1 for p in positions[:len(bits)]]
        recovered = bytes(sum(recovered_bits[i + j] << (7 - j) for j in range(8))
                          for i in range(0, len(recovered_bits), 8))
        assert recovered == payload + b'\0', name
        (out / (name + '.recovered')).write_bytes(recovered[:-1])
        manifest['fixtures'].append(dict(path=str(path),generator='stdlib Python',channels=channels,
                                         order=order,prime=prime,bit_plane=plane,roundtrip=True,
                                         sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    if args.stegano_cli:
        for name, options in [('stegano-sequential', []), ('stegano-prime', ['--generator', 'eratosthenes'])]:
            path = out / (name + '.png')
            hide = [str(args.stegano_cli), 'hide', '-i', str(out / 'cover.png'), '-f', str(out / 'payload.sh'),
                    '-o', str(path), *options]
            reveal = [str(args.stegano_cli), 'reveal', '-i', str(path), '-o', str(out / (name + '.recovered')), *options]
            subprocess.run(hide, check=True, capture_output=True)
            subprocess.run(reveal, check=True, capture_output=True)
            assert (out / (name + '.recovered')).read_bytes() == payload, name
            manifest['fixtures'].append(dict(path=str(path),generator='stegano-lsb',command=hide,
                                             roundtrip=True,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f"{len(manifest['fixtures'])} PNG payload fixtures generated and recovered successfully in {out}")


if __name__ == '__main__':
    main()
