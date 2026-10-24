#!/usr/bin/env python3
"""Check decoded header construction without executing fixture JavaScript."""
import argparse
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--report", type=Path)
args = parser.parse_args()
if args.report:
    source = args.report.read_text()
else:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(HERE)], capture_output=True, text=True,
        check=True,
    )
    assert not result.stderr.strip(), result.stderr
    source = result.stdout
files = {}
while source.strip():
    source = source.lstrip()
    report, end = json.JSONDecoder().raw_decode(source)
    source = source[end:]
    for file in report["files"]:
        files[Path(file["path"]).name] = file.get("traits", [])
cases = json.loads((HERE / "cases.json").read_text())
for case in cases:
    traits = files[case["file"]]
    present = {trait["id"] for trait in traits}
    assert not set(case["present"]) - present, (case["file"], "missing")
    assert not set(case["absent"]) & present, (case["file"], "unexpected")
    assert not any(trait["crit"] == 5 for trait in traits), case["file"]
print(f"{len(cases)} header-concealment controls passed; no hostile findings")
