#!/usr/bin/env python3
"""Positive and near-miss controls for UKit source trait corrections."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
repo = here.parents[2]
cases = json.loads((here / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
     "--format", "json", *[str(here / c["file"]) for c in cases]],
    check=True, capture_output=True, text=True,
)
assert not result.stderr.strip(), result.stderr
reports = []
text = result.stdout
while text.strip():
    report, end = json.JSONDecoder().raw_decode(text.lstrip())
    reports.extend(report["files"])
    text = text.lstrip()[end:]
by_name = {Path(f["path"]).name: {t["id"] for t in f.get("traits", [])}
           for f in reports}
for case in cases:
    ids = by_name[case["file"]]
    assert set(case["present"]) <= ids, (case["file"], set(case["present"]) - ids)
    assert not set(case["absent"]) & ids, (case["file"], set(case["absent"]) & ids)
print(f"Passed {len(cases)} positive and near-miss controls")
