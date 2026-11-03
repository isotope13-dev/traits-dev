#!/usr/bin/env python3
"""Generic repair text must not be described as an exploit retry loop."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
PREFIX = "objectives/execution/automation/agent::"
COOCCURRENCE = PREFIX + "script-verdict-repair-cooccurrence"

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("repair_only", "def repair_cache():\n    pass\n", False),
        ("cooccurrence", "import subprocess\nsubprocess.run(script)\n# VULNERABLE NOT CONFIRMED\n# repair\n", True),
    ):
        path = Path(temp) / f"{name}.py"
        path.write_text(source)
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format=json", str(path)],
            check=True, capture_output=True, text=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        report = json.loads(result.stdout)
        traits = [t for f in report["files"] for t in f.get("traits", [])]
        assert not any(t["id"].endswith("::poc-repair-retry-loop") for t in traits)
        match = next((t for t in traits if t["id"] == COOCCURRENCE), None)
        assert (match is not None) == expected, (name, match)
        if match:
            assert match["crit"] == 4, match

print("PoC text co-occurrence boundaries passed")
