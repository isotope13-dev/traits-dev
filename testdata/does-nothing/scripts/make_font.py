#!/usr/bin/env python3
"""Generate inert font containers using only the standard library.

Two containers, because they exercise different code paths in the font
extractor: a bare sfnt (`.ttf`), whose table directory is walked entry by
entry and checked for coverage, and a WOFF2 (`.woff2`), whose uncompressed
variable-length directory and Brotli stream bounds are validated.

Both are deliberately boring: every declared table lies end to end after the
directory, nothing is appended, and the header sizes agree with the file. A
scan of either must produce only neutral format metadata. The zero-filled
table bodies are structural controls, not renderable glyphs. This keeps the
font coverage metrics
(`font.trailing_bytes`, `font.gap_bytes`, `font.unknown_table_bytes`) honest
as thresholds move.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

# Registered OpenType tags only: an unregistered tag would legitimately set
# `font.unknown_table_count`, which is not what this fixture is for.
TABLES: list[tuple[bytes, int]] = [
    (b"OS/2", 96),
    (b"cmap", 32),
    (b"glyf", 256),
    (b"head", 54),
    (b"hhea", 36),
    (b"hmtx", 8),
    (b"loca", 16),
    (b"maxp", 32),
    (b"name", 64),
    (b"post", 32),
]


def build_ttf() -> bytes:
    """A bare sfnt whose tables tile the file with no gaps and no trailing data."""
    count = len(TABLES)
    # sfnt 1.0, then the binary-search hints the format wants. Their values do
    # not affect parsing, but a real font sets them, so set them properly.
    entry_selector = max(count.bit_length() - 1, 0)
    search_range = (2**entry_selector) * 16
    header = struct.pack(
        ">IHHHH",
        0x00010000,
        count,
        search_range,
        entry_selector,
        count * 16 - search_range,
    )

    directory = bytearray()
    body = bytearray()
    offset = 12 + count * 16
    for tag, length in TABLES:
        directory += tag + struct.pack(">III", 0, offset, length)
        body += bytes(length)
        offset += length
    return bytes(header + directory + body)


def build_woff2() -> bytes:
    """A complete table directory followed by a valid inert Brotli stream."""
    flags = {b"OS/2": 6, b"cmap": 0, b"glyf": 202, b"head": 1,
             b"hhea": 2, b"hmtx": 3, b"loca": 203, b"maxp": 4,
             b"name": 5, b"post": 7}
    directory = bytearray()
    for tag, size in TABLES:
        directory.append(flags[tag])
        groups = [size & 127]
        size >>= 7
        while size:
            groups.append((size & 127) | 128)
            size >>= 7
        directory.extend(reversed(groups))
    # Brotli-compressed 626 zero bytes (sum of TABLES lengths). A literal
    # keeps fixture generation standard-library-only; glyf/loca use null
    # transform version 3, so the decoded stream is the original table data.
    payload = bytes.fromhex("1b7102f82700a2b1406005")
    length = 48 + len(directory) + len(payload)
    header = struct.pack(
        ">4sIIHHIIHHIIIII",
        b"wOF2",
        0x00010000,  # flavor: sfnt 1.0
        length,  # total file size
        len(TABLES),  # numTables
        0,  # reserved
        len(build_ttf()),  # totalSfntSize (reference value, not an equality gate)
        len(payload),  # totalCompressedSize
        1,  # majorVersion
        0,  # minorVersion
        0,  # metaOffset
        0,  # metaLength
        0,  # metaOrigLength
        0,  # privOffset
        0,  # privLength
    )
    assert len(header) == 48, len(header)
    return header + directory + payload


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    builders = {".ttf": build_ttf, ".woff2": build_woff2}
    try:
        build = builders[target.suffix]
    except KeyError:
        raise SystemExit(f"unsupported font target: {target.name}") from None
    target.write_bytes(build())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: make_font.py <target>")
    main(Path(sys.argv[1]))
