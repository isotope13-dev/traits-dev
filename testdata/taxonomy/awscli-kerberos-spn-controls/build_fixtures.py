#!/usr/bin/env python3
"""Build minimal AWS CLI-identified wheels for Kerberos matcher controls."""
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
DIST_INFO = "awscli-0.0.0.dist-info"
COMMON = {
    f"{DIST_INFO}/METADATA": (
        "Metadata-Version: 2.1\nName: awscli\nVersion: 0.0.0\n\n"
    ),
    f"{DIST_INFO}/WHEEL": (
        "Wheel-Version: 1.0\nGenerator: taxonomy-control\n"
        "Root-Is-Purelib: true\nTag: py3-none-any\n"
    ),
    "awscli/__init__.py": "",
}
CASES = {
    "positive-spns": 'spns = ["HTTP/app.example.test:80"]\n',
    "near-miss-service-accounts": (
        'service_accounts = ["AWSServiceRoleForSupport"]\n'
    ),
    "near-miss-iam-service-principals": (
        'service_principals = ["ec2.amazonaws.com"]\n'
    ),
}

for case, source in CASES.items():
    path = ROOT / f"{case}.whl"
    with ZipFile(path, "w") as archive:
        entries = {**COMMON, "awscli/kerberos_targets.py": source}
        for name, content in sorted(entries.items()):
            info = ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
