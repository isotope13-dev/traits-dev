#!/usr/bin/env python3
"""A guarded socket-to-stdin transfer must use the same received value."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
TRAIT = "micro-behaviors/process/stdio/relay::python-received-data-to-stdin"
BASE = """\
def relay(sock, proc):
    data = sock.recv(1024)
    if len(GUARD) > 0:
        proc.stdin.write(WRITE)
"""

with tempfile.TemporaryDirectory() as temp:
    for name, guard, write, expected in (
        ("matching", "data", "data", True),
        ("other_guard", "other", "data", False),
        ("other_input", "data", "other", False),
    ):
        path = Path(temp) / f"{name}.py"
        path.write_text(BASE.replace("GUARD", guard).replace("WRITE", write))
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format=json", str(path)],
            check=True, capture_output=True, text=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        report = json.loads(result.stdout)
        found = any(t["id"] == TRAIT for f in report["files"] for t in f.get("traits", []))
        assert found == expected, (name, found)

print("Guarded socket-to-stdin data-flow boundaries passed")
