#!/usr/bin/env python3
"""Exercise IPP Foomatic injection and its data-flow boundaries."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "objectives/execution/exploit/command-injection::ipp-foomatic-directive-injection"
SOURCE = r'''\
def respond(attrs, uri, command, filter_type):
    tag = "printer-attributes-tag"
    value = (
        f'{uri}"\n*FoomaticRIPCommandLine: "{command}"\n'
        f'*cupsFilter2: "{filter_type}'
    )
    attrs[tag] = value
'''

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("injection", SOURCE, True),
        ("different_value", SOURCE.replace("attrs[tag] = value", "attrs[tag] = other"), False),
        ("no_breakout", SOURCE.replace(r"\n*FoomaticRIPCommandLine", " FoomaticRIPCommandLine"), False),
        ("static_text", SOURCE.replace("f'", "'"), False),
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

print("IPP Foomatic injection boundaries passed")
