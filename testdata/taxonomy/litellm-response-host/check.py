#!/usr/bin/env python3
"""Check response-host and encrypted-body positive/near-miss fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--fixtures", required=True, type=Path)
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--traits-dir", default=".")
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
scan = subprocess.run(
    [args.cleave, "--traits-dir", args.traits_dir, "--json", str(args.fixtures)],
    capture_output=True, text=True,
)
if scan.returncode:
    raise SystemExit(scan.stderr or scan.stdout)
reports = {}
for line in scan.stdout.splitlines():
    for entry in json.loads(line).get("files", []):
        reports[str(Path(entry["path"]).resolve())] = entry
failures = []
for case in cases:
    path = str((args.fixtures / case["path"]).resolve())
    report = reports.get(path)
    if report is None:
        failures.append(f"{case['path']}: missing analysis")
        continue
    matched = {trait["id"] for trait in report.get("traits", [])}
    for trait in set(case["matched"]) - matched:
        failures.append(f"{case['path']}: missing {trait}")
    for trait in set(case["not_matched"]) & matched:
        failures.append(f"{case['path']}: unexpected {trait}")
if failures:
    raise SystemExit("\n".join(failures))
print(f"PASS: {len(cases)} response-host/encrypted-body cases")
