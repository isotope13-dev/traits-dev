#!/usr/bin/env python3
"""Build deterministic AWS CLI-named wheels for domain-reference controls."""
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
    # This standalone Python member holds a commerce-domain text reference.
    # The fixture makes no claim that it contacts the named service.
    "positive-unrelated-member": {
        "addon/site_config.py": 'COMMERCE_HOST = "amazon.com"\n',
    },
    # The same text under the AWS CLI package path remains path-excluded.
    "near-miss-awscli-member-path": {
        "awscli/examples/site_config.py": (
            'COMMERCE_HOST = "amazon.com"\n'
        ),
    },
    # The domain-specific rule should not match a different host.
    "near-miss-different-domain": {
        "addon/site_config.py": 'COMMERCE_HOST = "example.com"\n',
    },
}

for case, members in CASES.items():
    with ZipFile(ROOT / f"{case}.whl", "w") as archive:
        for name, content in sorted({**COMMON, **members}.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
