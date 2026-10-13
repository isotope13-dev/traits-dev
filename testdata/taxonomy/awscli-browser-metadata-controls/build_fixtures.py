#!/usr/bin/env python3
"""Build deterministic AWS CLI-named wheels for metadata-host controls."""
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
COMMON = {
    "awscli-0.0.0.dist-info/METADATA": (
        "Metadata-Version: 2.1\nName: awscli\nVersion: 0.0.0\n\n"
    ),
    "awscli-0.0.0.dist-info/WHEEL": (
        "Wheel-Version: 1.0\nGenerator: taxonomy-control\n"
        "Root-Is-Purelib: true\nTag: py3-none-any\n"
    ),
    "awscli/__init__.py": "",
}
CASES = {
    # This unrelated Python member contains the metadata hostname as text.
    # The fixture does not claim that the package contacts the endpoint.
    "positive-unrelated-member": {
        "addon/site_config.py": 'METADATA_HOST = "169.254.169.254"\n',
    },
    # A different host is not the cloud metadata hostname under review.
    "near-miss-different-host": {
        "addon/site_config.py": 'METADATA_HOST = "169.254.169.253"\n',
    },
}

for case, members in CASES.items():
    with ZipFile(ROOT / f"{case}.whl", "w") as archive:
        for name, content in sorted({**COMMON, **members}.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
