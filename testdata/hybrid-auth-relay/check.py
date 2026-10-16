#!/usr/bin/env python3
"""Check relay detections and the absence of convictions on nearby controls."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--report", type=Path, help="Use a previously generated JSON report")
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
if args.report:
    output = args.report.read_text()
else:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json",
         "analyze", *[case["path"] for case in cases]],
        cwd=root, text=True, capture_output=True, check=True,
    )
    output = result.stdout
reports = {}
for line in output.splitlines():
    for report in json.loads(line).get("files", []):
        reports[report["path"]] = {trait["id"] for trait in report.get("traits", [])}
failures = []
for case in cases:
    observed = reports.get(case["path"])
    if observed is None:
        failures.append(f"{case['path']}: missing file report")
        continue
    missing = set(case["matched"]) - observed
    unexpected = set(case["not_matched"]) & observed
    if missing or unexpected:
        failures.append(f"{case['path']}: missing={sorted(missing)}, unexpected={sorted(unexpected)}")
if failures:
    raise SystemExit("\n".join(failures))
print(f"PASS: {len(cases)} relay and control fixtures")
