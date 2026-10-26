#!/usr/bin/env python3
"""Generate a 1x1 white PNG using only the Python standard library."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path


def chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1, 1
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    raw = b"".join(b"\x00" + b"\xff\xff\xff" * width for _ in range(height))
    idat = zlib.compress(raw, 9)

    target.write_bytes(
        signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
