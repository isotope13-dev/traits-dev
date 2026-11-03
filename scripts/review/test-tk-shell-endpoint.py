#!/usr/bin/env python3
"""Check that .tk findings bind shell downloaders to their URL argument."""

import json
import pathlib
import subprocess
import tempfile

CASES = {
    "curl": ("curl -fsSL https://example.tk/a\n", True),
    "wget": ('wget "https://example.tk/a"\n', True),
    "homepage": ('HOMEPAGE="https://example.tk/a"\ncurl https://example.org/file\n', False),
    "comment": ("# curl https://example.tk/a\n", False),
    "tcl": ("curl https://www.tcl.tk/software/\n", False),
}

with tempfile.TemporaryDirectory() as tmp:
    for name, (source, expected) in CASES.items():
        path = pathlib.Path(tmp) / f"{name}.sh"
        path.write_text("#!/bin/sh\n" + source)
        result = subprocess.check_output(
            ["../cleave/target/release/cleave", "--traits-dir", ".", "--format", "json", str(path)]
        )
        file = json.loads(result)["files"][0]
        actual = any(
            trait["id"].endswith("::free-tld-shell-download")
            for trait in file.get("traits", [])
        )
        assert actual == expected, (name, actual, expected)

print("Shell .tk endpoint boundaries passed.")
