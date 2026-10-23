#!/usr/bin/env python3
"""Check source findings without executing the destructive fixture code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json"]
    + [str(HERE / case["file"]) for case in cases],
    capture_output=True, text=True,
)
assert result.returncode in (0, 1), result.stderr
assert not result.stderr.strip(), result.stderr
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        reports[Path(file["path"]).name] = {
            trait["id"] for trait in file.get("traits", [])
        }
checks = 0
for case in cases:
    got = reports[case["file"]]
    for trait in case["present"]:
        assert trait in got, (case["file"], "missing", trait)
        checks += 1
    for trait in case["absent"]:
        assert trait not in got, (case["file"], "unexpected", trait)
        checks += 1
print(f"{checks} assertions passed across {len(cases)} static fixtures")
