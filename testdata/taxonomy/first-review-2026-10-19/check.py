#!/usr/bin/env python3
"""Check CLI identity, naming, and hashing against nearby benign forms."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", str(HERE / "fixtures")],
    capture_output=True, text=True, check=True,
)
files = {}
for line in result.stdout.splitlines():
    report = json.loads(line)
    for entry in report["files"]:
        files[Path(entry["path"]).name] = {t["id"] for t in entry.get("traits", [])}
for case in json.loads((HERE / "cases.json").read_text()):
    found = files[Path(case["path"]).name]
    missing = set(case["present"]) - found
    unexpected = set(case["absent"]) & found
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print("PASS: 4 positive and near-miss source controls")
