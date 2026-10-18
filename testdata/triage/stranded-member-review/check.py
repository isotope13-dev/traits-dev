#!/usr/bin/env python3
"""Static positive and near-miss controls; never execute specimen commands."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", *[str(HERE / name) for name in cases]],
    check=True, capture_output=True, text=True,
)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
observed = {
    Path(file["path"]).name: {trait["id"] for trait in file.get("traits", [])}
    for report in reports for file in report["files"]
}
for name, expectation in cases.items():
    assert name in observed, f"No report for {name}"
    missing = set(expectation["required"]) - observed[name]
    unexpected = set(expectation["forbidden"]) & observed[name]
    assert not missing and not unexpected, (name, missing, unexpected)
print(f"Passed {len(cases)} static controls")
