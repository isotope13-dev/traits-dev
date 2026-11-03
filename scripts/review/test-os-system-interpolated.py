#!/usr/bin/env python3
"""Recognize interpolated os.system commands without matching literals."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "micro-behaviors/process/create/shell/command-mode::python-os-system-interpolated-command"

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("interpolated", "os.system(f'ln -s {target} {link}')\n", True),
        ("literal", "os.system('ln -s target link')\n", False),
        ("other_receiver", "platform.system(f'{value}')\n", False),
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

print("Interpolated os.system boundaries passed")
