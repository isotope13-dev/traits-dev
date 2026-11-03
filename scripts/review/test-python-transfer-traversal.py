#!/usr/bin/env python3
"""Check transfer traversal findings against paths and inert text."""

import json
import pathlib
import subprocess
import tempfile


CASES = {
    "shadow": (
        'client.download_file("/opt/appmesh/../../etc/shadow", "out")\n',
        {"python-download-traversal-shadow"},
    ),
    "write": (
        'client.upload_file(local_file="x", remote_file="/tmp/../../../etc/evil.txt")\n',
        {"python-upload-traversal-etc"},
    ),
    "not-root": ('client.download_file("/a/b/c/../../etc/shadow", "out")\n', set()),
    "ordinary": ('client.download_file("/tmp/etc/shadow", "out")\n', set()),
    "comment": ('# client.download_file("/opt/appmesh/../../etc/shadow", "out")\n', set()),
}

with tempfile.TemporaryDirectory() as tmp:
    for name, (source, expected) in CASES.items():
        path = pathlib.Path(tmp) / f"{name}.py"
        path.write_text(source)
        result = subprocess.check_output(
            ["../cleave/target/release/cleave", "--traits-dir", ".", "--format", "json", str(path)]
        )
        file = json.loads(result)["files"][0]
        actual = {
            trait["id"].split("::")[-1]
            for trait in file.get("traits", [])
            if trait["id"].startswith("objectives/execution/exploit/path-traversal::python-")
        }
        assert actual == expected, (name, actual, expected)

print("Python transfer traversal boundaries passed.")
