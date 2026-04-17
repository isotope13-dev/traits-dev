#!/usr/bin/env python3
"""Write a minimal Windows Shell Link (.lnk) file.

We emit only the 76-byte ShellLinkHeader with all optional-section flags
cleared, which is a structurally valid .lnk file that references nothing.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

HEADER_SIZE = 0x0000004C
LINK_CLSID = bytes.fromhex("0114020000000000C000000000000046")
SHOW_NORMAL = 1


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    header = struct.pack(
        "<I16sIIQQQIIIHHII",
        HEADER_SIZE,
        LINK_CLSID,
        0,              # LinkFlags (no optional sections)
        0,              # FileAttributes
        0, 0, 0,        # CreationTime, AccessTime, WriteTime
        0,              # FileSize
        0,              # IconIndex
        SHOW_NORMAL,    # ShowCommand
        0,              # HotKey
        0,              # Reserved1
        0, 0,           # Reserved2, Reserved3
    )
    assert len(header) == 0x4C
    target.write_bytes(header)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
