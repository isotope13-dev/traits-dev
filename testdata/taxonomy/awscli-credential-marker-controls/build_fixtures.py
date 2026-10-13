#!/usr/bin/env python3
"""Build deterministic AWS CLI-named wheels for credential-marker controls."""
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
    "positive-unrelated-member": {
        "addon/credential_handling.py": (
            "import os\n"
            'credentials_path = os.environ.get("AWS_SHARED_CREDENTIALS_FILE")\n'
            'SIGNING_ALGORITHM = "AWS4-HMAC-SHA256"\n'
        ),
    },
    "positive-environment-lookup-variants": {
        "addon/config_path.py": (
            'from os import environ, getenv\n'
            'credentials_path = environ["AWS_SHARED_CREDENTIALS_FILE"]\n'
            'fallback_path = getenv("AWS_SHARED_CREDENTIALS_FILE")\n'
        ),
    },
    # A bare mention documents the variable but does not access the process
    # environment. This also avoids claiming that the text-only SigV4 marker
    # proves a signing operation.
    "near-miss-documentation": {
        "addon/readme.py": (
            'DOCUMENTATION = "Set AWS_SHARED_CREDENTIALS_FILE to choose a path"\n'
        ),
    },
    # A same-named local constant is not evidence that the process environment
    # was queried.
    "near-miss-local-constant": {
        "addon/config_path.py": (
            'AWS_SHARED_CREDENTIALS_FILE = "./credentials"\n'
        ),
    },
}

for case, members in CASES.items():
    with ZipFile(ROOT / f"{case}.whl", "w") as archive:
        for name, content in sorted({**COMMON, **members}.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)

