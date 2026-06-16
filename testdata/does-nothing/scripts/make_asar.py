#!/usr/bin/env python3
"""Build a minimal Electron ASAR archive."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

MESSAGE = b"this sample does nothing\n"


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    header = {
        "files": {
            "sample.txt": {
                "size": len(MESSAGE),
                "offset": "0",
            }
        }
    }
    header_json = json.dumps(header, separators=(",", ":")).encode("utf-8")
    header_size = 8 + len(header_json)
    padding = (4 - (header_size % 4)) % 4
    header_size += padding

    target.write_bytes(
        struct.pack("<IIII", 4, header_size, 4, len(header_json))
        + header_json
        + (b"\0" * padding)
        + MESSAGE
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
