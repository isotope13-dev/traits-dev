#!/usr/bin/env python3
"""Recognize Python eval of a selected value, not literals or method calls."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "micro-behaviors/process/interpreter/eval/source::python-eval-subscripted-value"

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("subscript", "eval(state['Type'])\n", True),
        ("literal", "eval('42')\n", False),
        ("method", "worker.eval(state['Type'])\n", False),
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

print("Python eval subscript boundaries passed")
