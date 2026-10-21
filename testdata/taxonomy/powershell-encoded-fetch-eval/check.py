#!/usr/bin/env python3
"""Check literal/decoder/evaluator bindings and same-carrier correlation."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
case_file = Path(__file__).with_name("cases.json")
cases = json.loads(case_file.read_text())["fixtures"]
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave",
     "--traits-dir", str(root), "--format", "json", str(case_file.parent)],
    check=True, capture_output=True, text=True,
)
# Directory scans can emit adjacent JSON objects, including nested reports.
remaining = result.stdout
reports = []
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:]
findings = {
    Path(file["path"]).name: {trait["id"] for trait in file.get("traits", [])}
    for report in reports for file in report.get("files", [])
}
failures = []
for case in cases:
    name = Path(case["path"]).name
    if name not in findings:
        failures.append(f"{name}: missing report")
        continue
    missing = set(case["matched"]) - findings[name]
    unexpected = set(case["not_matched"]) & findings[name]
    if missing or unexpected:
        failures.append(f"{name}: missing={sorted(missing)}, unexpected={sorted(unexpected)}")
if failures:
    raise SystemExit("\n".join(failures))
print(f"Passed {len(cases)} encoded PowerShell controls")
