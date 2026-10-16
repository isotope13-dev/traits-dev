#!/usr/bin/env python3
"""Build deterministic archive fixtures for Scapy's outer-scope suppressor."""
from __future__ import annotations

import base64
import bz2
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PAYLOAD = base64.b64encode(
    bz2.compress((ROOT / "testdata/benign/dotnet-normal-loader-controls.exe").read_bytes())
).decode("ascii")
LOADER = f'const compressedPayload = "{PAYLOAD}";\n'
MARKERS = {
    "generic-header-only": "# This file is part of Scapy\n",
    "unit-infrastructure-only": '"""Unit testing infrastructure for Scapy"""\n',
    "embedded-asset-only": 'UTscapy_js = File("UTscapy.js", url, data)\n',
    "complete-utscapy-source-markers": (
        "# This file is part of Scapy\n"
        '"""Unit testing infrastructure for Scapy"""\n'
        'UTscapy_js = File("UTscapy.js", url, data)\n'
    ),
    "split-utscapy-markers-across-members": "",
    "no-scapy-markers": "",
}


def add_bytes(archive: zipfile.ZipFile, name: str, body: str) -> None:
    info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, body.encode("utf-8"))


for case, marker in MARKERS.items():
    path = HERE / f"{case}.zip"
    with zipfile.ZipFile(path, "w") as archive:
        if case == "split-utscapy-markers-across-members":
            add_bytes(archive, "pkg/scapy-module.py", MARKERS["generic-header-only"])
            add_bytes(
                archive,
                "pkg/UTscapy-assets.py",
                MARKERS["unit-infrastructure-only"] + MARKERS["embedded-asset-only"],
            )
        elif marker:
            add_bytes(archive, "pkg/marker.py", marker)
        add_bytes(archive, "payload/loader.js", LOADER)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
