#!/usr/bin/env python3
"""Check static observations; never execute fixture or sample code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CLEAVE = os.environ.get("CLEAVE", "cleave")
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    [CLEAVE, "--traits-dir", str(ROOT), "--format", "jsonl", str(HERE)],
    capture_output=True, text=True, check=True,
)
assert not result.stderr.strip(), result.stderr
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line)["files"]:
        reports[Path(report["path"]).name] = {
            trait["id"] for trait in report.get("traits", [])
        }

zero_id = "micro-behaviors/data/buffer/alloc::node-explicit-zero-fill-buffer"
for case in cases:
    path = ROOT / case["path"]
    actual = reports[path.name]
    # This engine strips unreferenced baseline findings at emission. Inspect
    # the matcher directly instead of raising a neutral operation's severity.
    if zero_id in case["matched"] + case["not_matched"]:
        trace = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "test-rules", str(path),
             "--rules", zero_id],
            capture_output=True, text=True, check=True,
        )
        diagnostic = trace.stdout + trace.stderr
        assert not any(word in diagnostic for word in
                       ("Warning:", "ERROR", "validation failed")), diagnostic
        if "\nMATCHED " + zero_id in trace.stdout:
            actual.add(zero_id)
        else:
            assert "\nNOT MATCHED " + zero_id in trace.stdout, trace.stdout
    missing = set(case["matched"]) - actual
    unwanted = set(case["not_matched"]) & actual
    assert not missing and not unwanted, (case["case_id"], missing, unwanted)
    print("PASS", case["case_id"])
print(f"Passed {len(cases)} static coverage controls")
