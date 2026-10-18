#!/usr/bin/env python3
"""Check reviewed source-to-send boundaries and neutral observation homes."""
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads(pathlib.Path(__file__).with_name("cases.json").read_text())
result = subprocess.run(
    ["cleave", "--traits-dir", str(root), "--format", "json"]
    + [case["path"] for case in cases["fixtures"]],
    cwd=root, capture_output=True, text=True,
)
assert result.returncode == 0, result.stderr
reports = []
remaining = result.stdout.lstrip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
assert len(reports) == len(cases["fixtures"]), "Missing fixture report"
for case, report in zip(cases["fixtures"], reports):
    ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    missing = set(case["matched"]) - ids
    unexpected = set(case["not_matched"]) & ids
    assert not (missing or unexpected), (case["case_id"], missing, unexpected)
print(f'{len(reports)} focused cases passed')
