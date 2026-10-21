#!/usr/bin/env python3
"""Focused static-detection controls; never execute fixture code."""
import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--report", type=Path)
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
if args.report:
    stream = args.report.read_text()
else:
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(ROOT), "--format", "json"]
        + [case["path"] for case in cases],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    stream = result.stdout
decoder = json.JSONDecoder()
files = []
while stream.strip():
    stream = stream.lstrip()
    report, end = decoder.raw_decode(stream)
    files.extend(report["files"])
    stream = stream[end:]
for case in cases:
    matching = [item for item in files if item["path"].endswith(case["path"])]
    assert matching, f"Missing report: {case['case_id']}"
    traits = {trait["id"]: trait for item in matching for trait in item.get("traits", [])}
    missing = set(case["required_emitted"]) - traits.keys()
    unexpected = set(case["forbidden_emitted"]) & traits.keys()
    assert not missing and not unexpected, (case["case_id"], missing, unexpected)
    if case["case_id"] != "social-shell-tasks.ps1":
        assert all(trait["crit"] < 4 for trait in traits.values()), case["case_id"]
print(f"PASS: {len(cases)} focused cases")
