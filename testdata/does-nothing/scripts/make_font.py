#!/usr/bin/env python3
"""Generate minimal, structurally valid fonts using only the standard library.

Two containers, because they exercise different code paths in the font
extractor: a bare sfnt (`.ttf`), whose table directory is walked entry by
entry and checked for coverage, and a WOFF2 (`.woff2`), whose Brotli-packed
table data is not addressable so only the fixed header is validated.

Both are deliberately boring: every declared table lies end to end after the
directory, nothing is appended, and the header sizes agree with the file. A
scan of either must produce no findings at all — that is the point of a
does-nothing fixture, and it is what keeps the font coverage metrics
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
    """A WOFF2 whose header sizes agree with the file it is written into."""
    payload = bytes(512)
    # totalSfntSize is what the font would inflate to; totalCompressedSize is
    # the on-disk table block. Only the latter is checked against the file.
    length = 48 + len(payload)
    header = struct.pack(
        ">4sIIHHIIHHIIIII",
        b"wOF2",
        0x00010000,  # flavor: sfnt 1.0
        length,  # total file size
        len(TABLES),  # numTables
        0,  # reserved
        4096,  # totalSfntSize
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
    return header + payload


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
