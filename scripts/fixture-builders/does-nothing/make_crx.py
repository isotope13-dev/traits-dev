#!/usr/bin/env python3
"""Generate a harmless Chrome extension (.crx, CRX v3).

The CRX v3 container is: magic 'Cr24' + version + header-length + header +
ZIP body. The header holds protobuf-encoded signature data; detectors key on
the 'Cr24' magic + v3 word, so a zero-length proof header is acceptable.
"""

from __future__ import annotations

import io
import struct
import sys
import zipfile
from pathlib import Path

CRX_MAGIC = b"Cr24"
CRX_VERSION = 3

EXTENSION_MANIFEST = """{
  "manifest_version": 3,
  "name": "Sample",
  "version": "1.0.0",
  "description": "A sample extension that does nothing."
}
"""


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", EXTENSION_MANIFEST)
    zip_bytes = buf.getvalue()

    header = b""  # empty signed header proof
    preamble = (
        CRX_MAGIC
        + struct.pack("<I", CRX_VERSION)
        + struct.pack("<I", len(header))
        + header
    )
    target.write_bytes(preamble + zip_bytes)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
