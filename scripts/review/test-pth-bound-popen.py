#!/usr/bin/env python3
"""Check that startup-code detection binds the path and file handle."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "objectives/persistence/login/python-startup::pth-write-bound-popen-source"
SOURCE = '''\
def install(base, name, program):
    path = os.path.join(base, name + ".pth")
    if not os.path.exists(path):
        with open(path, "w") as handle:
            handle.write("import subprocess; subprocess.Popen('{}')".format(program))
'''

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("bound", SOURCE, True),
        ("other_path", SOURCE.replace('open(path, "w")', 'open(other, "w")'), False),
        ("rebound_path", SOURCE.replace('    if not os.path.exists(path):', '    path = other\n    if not os.path.exists(path):'), False),
        ("other_handle", SOURCE.replace("handle.write", "other.write"), False),
        ("rebound_handle", SOURCE.replace('            handle.write', '            handle = other\n            handle.write'), False),
        ("other_suffix", SOURCE.replace('".pth"', '".txt"'), False),
        ("extended_suffix", SOURCE.replace('".pth"', '".pth.tar"'), False),
        ("read_mode", SOURCE.replace('open(path, "w")', 'open(path, "r")'), False),
        ("inert_text", SOURCE.replace("subprocess.Popen", "subprocess.PIPE"), False),
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

print("Bound .pth startup-code boundaries passed")
