#!/usr/bin/env python3
"""Scan fixtures statically; never execute their boot configuration commands."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPECTED = {
    "micro-behaviors/os/kernel/boot::node-exec-bcdedit-recovery-disable",
    "micro-behaviors/os/kernel/boot::node-exec-bcdedit-ignore-failures",
}
fixtures = sorted(HERE.glob("*.js"))
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json"]
    + [str(path) for path in fixtures],
    capture_output=True, text=True, check=True,
)
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        reports[Path(report["path"]).name] = report
for fixture in fixtures:
    found = {trait["id"] for trait in reports[fixture.name].get("traits", [])}
    wanted = EXPECTED if fixture.name.startswith("command-") else set()
    assert found & EXPECTED == wanted, (fixture.name, found & EXPECTED, wanted)
print(f"Passed {len(fixtures)} static boot-command controls")
