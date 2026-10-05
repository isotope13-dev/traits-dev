#!/usr/bin/env python3
"""Build inert DEX 035 string/type tables; no classes, methods or code.

Format: https://source.android.com/docs/core/runtime/dex-format
Only ASCII descriptors are needed, so their byte and UTF-16 lengths coincide.
"""
import hashlib
import struct
import zlib
from pathlib import Path

root = Path(__file__).resolve().parent.parent
for filename, strings in (
    ("inflater.dex", ["Ljava/util/zip/Inflater;", "Ljava/util/zip/InflaterInputStream;"]),
    ("string-only.dex", ["Ljava/lang/String;"]),
):
    strings = sorted(strings)
    count = len(strings)
    string_off, type_off = 112, 112 + 4 * count
    data_off = type_off + 4 * count
    data, offsets = bytearray(), []
    for value in strings:
        assert len(value) < 128 and value.isascii()
        offsets.append(data_off + len(data))
        data += bytes([len(value)]) + value.encode() + b"\0"
    data += b"\0" * (-len(data) % 4)
    map_off = data_off + len(data)
    entries = [(0, 1, 0), (1, count, string_off), (2, count, type_off),
               (0x2002, count, data_off), (0x1000, 1, map_off)]
    data += struct.pack("<I", len(entries))
    data += b"".join(struct.pack("<HHII", kind, 0, size, offset) for kind, size, offset in entries)
    header = bytearray(112)
    header[:8] = b"dex\n035\0"
    fields = [data_off + len(data), 112, 0x12345678, 0, 0, map_off,
              count, string_off, count, type_off, 0, 0, 0, 0, 0, 0, 0, 0, len(data), data_off]
    struct.pack_into("<20I", header, 32, *fields)
    blob = header + struct.pack("<" + "I" * count, *offsets)
    blob += struct.pack("<" + "I" * count, *range(count)) + data
    blob[12:32] = hashlib.sha1(blob[32:]).digest()
    struct.pack_into("<I", blob, 8, zlib.adler32(blob[12:]))
    (root / filename).write_bytes(blob)
