#!/usr/bin/env python3
"""Static detection controls; none of the fixture JavaScript is executed."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json"]
    + [str(ROOT / case["path"]) for case in cases],
    capture_output=True, text=True, check=True,
)
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        reports[Path(report["path"]).name] = report
for case in cases:
    report = reports[Path(case["path"]).name]
    ids = {trait["id"] for trait in report.get("traits", [])}
    missing = set(case["required_emitted"]) - ids
    extra = set(case["forbidden_emitted"]) & ids
    assert not missing and not extra, (case["case_id"], missing, extra)
    if case["case_id"] != "root-truncate":
        hostile = [t["id"] for t in report.get("traits", []) if t["crit"] == 5]
        assert not hostile, (case["case_id"], hostile)
print(f"Passed {len(cases)} static detection controls")
