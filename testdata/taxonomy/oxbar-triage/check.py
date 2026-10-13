"""Run the triage's positive and near-miss controls without executing fixtures."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
for case in cases:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", case["path"]],
        cwd=root, capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    matched = {trait["id"] for file in report["files"]
               for trait in file.get("traits", [])}
    assert set(case["matched"]) <= matched, (case["path"], set(case["matched"]) - matched)
    assert not (set(case["not_matched"]) & matched), (case["path"], set(case["not_matched"]) & matched)
    print(case["path"], "PASS")
