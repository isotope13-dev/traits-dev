#!/usr/bin/env python3
"""Check neutral capability placement and PE false-positive boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
scratch = os.environ.get("TRIAGE_SCRATCH", str(root.parents[1] / "scratch"))
# Scan ordinary paths so test-directory exclusions cannot hide the behavior
# the controls are intended to measure.
with tempfile.TemporaryDirectory(prefix="capability-controls-", dir=scratch) as work:
    targets = []
    for case in cases:
        target = Path(work) / Path(case["path"]).name
        target.write_bytes((root / case["path"]).read_bytes())
        targets.append(str(target))
    run = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json",
         *targets], cwd=root, text=True, capture_output=True,
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
    missing = set(case["matched"]) - reports[name]
    unexpected = set(case["not_matched"]) & reports[name]
    if missing or unexpected:
        failures.append((name, sorted(missing), sorted(unexpected)))
assert not failures, failures
print(f"PASS: {len(cases)} capability and PE boundary controls")
