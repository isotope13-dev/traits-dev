#!/usr/bin/env python3
"""Recognize bare absolute-path prefix comparisons without conflating boundaries."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "micro-behaviors/fs/path/check::python-absolute-path-string-prefix"

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("bare", "abspath(child).startswith(abspath(parent))\n", True),
        ("qualified", "os.path.abspath(c).startswith(os.path.abspath(p))\n", True),
        ("separator", "abspath(c).startswith(abspath(p) + os.sep)\n", False),
        ("other", "basename(c).startswith(basename(p))\n", False),
    ):
        path = Path(temp) / f"{name}.py"
        path.write_text(source)
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format=json", str(path)],
            check=True, capture_output=True, text=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        report = json.loads(result.stdout)
        found = any(t["id"] == RULE for f in report["files"] for t in f.get("traits", []))
        assert found == expected, (name, found)

print("Absolute-path prefix boundaries passed")
