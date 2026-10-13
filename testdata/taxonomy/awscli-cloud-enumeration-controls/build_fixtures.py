#!/usr/bin/env python3
"""Build deterministic AWS CLI-named wheels for cloud-enumeration controls."""
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
    # The unrelated member contains an operation-shaped call. This records a
    # capability signal only; it does not establish a successful request.
    "positive-unrelated-ec2-operation": {
        "addon/enumerate.py": "ec2.describe_instances()\n",
    },
    "positive-unrelated-s3-operation": {
        "addon/buckets.py": "s3.list_buckets()\n",
    },
    # A prose mention or bare string is not an operation invocation.
    "near-miss-description-text": {
        "addon/readme.md": "The describe_instances method can enumerate instances.\n",
    },
    "near-miss-name-string": {
        "addon/config.py": 'operation_name = "describe_instances"\n',
    },
}

for case, members in CASES.items():
    with ZipFile(ROOT / f"{case}.whl", "w") as archive:
        for name, content in sorted({**COMMON, **members}.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
