#!/usr/bin/env python3
"""Generate a minimal, single-page PDF containing one harmless sentence."""

from __future__ import annotations

import sys
from pathlib import Path


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        None,  # stream placeholder for content
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    stream_body = b"BT /F1 12 Tf 72 720 Td (this sample does nothing) Tj ET"
    objects[3] = (
        b"<< /Length " + str(len(stream_body)).encode("ascii") + b" >>\nstream\n"
        + stream_body + b"\nendstream"
    )

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: list[int] = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("ascii") + body + b"\nendobj\n"

    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode("ascii")

    target.write_bytes(bytes(out))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
