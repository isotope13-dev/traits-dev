#!/usr/bin/env python3
"""Build deterministic AWS CLI-named wheels for agent-prompt matcher controls."""
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
    # Synthetic prompt text models an unrelated payload co-located with an
    # AWS CLI package claim. It makes no claim about AWS CLI's own behavior.
    "positive-unrelated-member": {
        "addon/prompt.txt": (
            "You are an AI agent with access to filesystem tools.\n"
        ),
    },
    # This prompt names an agent and a filesystem adapter but does not grant
    # filesystem access in the wording required by the matcher.
    "near-miss-no-filesystem-grant": {
        "addon/prompt.txt": (
            "You are an AI agent. Use a local filesystem adapter.\n"
        ),
    },
    # Exercise the existing path-scoped exception without asserting that a
    # real AWS CLI example contains this synthetic prompt.
    "near-miss-example-path": {
        "awscli/examples/prompt.txt": (
            "You are an AI agent with access to filesystem tools.\n"
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
