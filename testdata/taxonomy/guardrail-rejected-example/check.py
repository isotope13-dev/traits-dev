"""Scan documentation and attack controls without executing their content."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--json"] + [c["path"] for c in cases],
    cwd=root, text=True, capture_output=True, check=True,
)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        reports[file["path"]] = file
for case in cases:
    file = reports[case["path"]]
    ids = {t["id"] for t in file.get("traits", [])}
    missing = set(case["matched"]) - ids
    unexpected = set(case["not_matched"]) & ids
    assert not (missing or unexpected), (case["path"], missing, unexpected)
    print("PASS", case["path"])
print(f"Passed {len(cases)} static controls")
