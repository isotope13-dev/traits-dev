#!/usr/bin/env python3
"""Check positive and near-miss traits without executing fixture code."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
cases = json.loads((Path(__file__).with_name("cases.json")).read_text())["fixtures"]
result = subprocess.run(
    ["cleave", "--no-update-check", "--traits-dir", str(root), "--format", "json",
     *[case["path"] for case in cases]], cwd=root, capture_output=True, text=True,
    check=True,
)
if result.stderr.strip():
    raise SystemExit(result.stderr)
# Multi-file JSON output is a stream of concatenated objects.
remaining = result.stdout
reports = {}
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for file in report.get("files", []):
        reports[file["path"]] = {trait["id"] for trait in file.get("traits", [])}
for case in cases:
    actual = reports[case["path"]]
    missing = set(case["matched"]) - actual
    unexpected = set(case["not_matched"]) & actual
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"Passed {len(cases)} positive and near-miss detection cases.")
