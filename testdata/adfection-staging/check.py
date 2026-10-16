#!/usr/bin/env python3
"""Check AdFection mechanism coverage and its benign near misses."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cases = json.loads((Path(__file__).parent / "cases.json").read_text())["fixtures"]
run = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json",
     str(Path(__file__).parent)],
    cwd=root, text=True, capture_output=True,
)
if run.returncode:
    raise RuntimeError(run.stderr or run.stdout)
reports = {}
for line in run.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        reports[Path(report["path"]).name] = {
            trait["id"] for trait in report.get("traits", [])
        }
failures = []
for case in cases:
    name = Path(case["path"]).name
    assert name in reports, f"Missing report: {name}"
    traits = reports[name]
    missing = set(case["matched"]) - traits
    unexpected = set(case["not_matched"]) & traits
    if missing or unexpected:
        failures.append((name, sorted(missing), sorted(unexpected)))
assert not failures, failures
print(f"PASS: {len(cases)} AdFection staging and WebSocket cases")
