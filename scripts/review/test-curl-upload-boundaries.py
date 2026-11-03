#!/usr/bin/env python3
"""Distinguish an HTTP method override from a file-backed curl upload."""

import json
import pathlib
import subprocess
import tempfile

CASES = {
    "method": ("curl -X POST https://example.test/delete\n", False, True),
    "upload": ("curl --upload-file /tmp/data https://example.test\n", True, False),
    "data": ("curl -d @/tmp/data https://example.test\n", True, False),
    "inline": ("curl -d hello https://example.test\n", True, False),
    "get": ("curl https://example.test\n", False, False),
}
UPLOAD_ATOMS = {
    "curl-long-upload-file",
    "curl-upload-file-or-stdin",
    "curl-data-binary-at-source",
    "curl-short-data-option",
    "curl-data-option",
}

with tempfile.TemporaryDirectory() as tmp:
    for name, (source, expected_upload, expected_method) in CASES.items():
        path = pathlib.Path(tmp) / f"{name}.sh"
        path.write_text("#!/bin/sh\n" + source)
        result = subprocess.check_output(
            ["../cleave/target/release/cleave", "--traits-dir", ".", "--format", "json", str(path)]
        )
        file = json.loads(result)["files"][0]
        ids = {trait["id"].split("::")[-1] for trait in file.get("traits", [])}
        assert bool(ids & UPLOAD_ATOMS) == expected_upload, (name, ids)
        assert ("curl-write-method-text" in ids) == expected_method, (name, ids)

print("curl upload boundaries passed.")
