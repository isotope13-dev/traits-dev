"""Regression checks for shared-rule corrections and retained attack coverage."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
paths = [str(root / case["path"]) for case in cases]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *paths],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report.get("files", []):
        files[Path(file["path"]).resolve()] = file
for case in cases:
    file = files[(root / case["path"]).resolve()]
    traits = {trait["id"]: trait for trait in file.get("traits", [])}
    for required in case.get("required", []):
        assert required in traits, (case["path"], "missing", required)
    for forbidden in case.get("forbidden", []):
        assert forbidden not in traits, (case["path"], "unexpected", forbidden)
    if "hostile_count" in case:
        assert sum(t["crit"] == 5 for t in traits.values()) == case["hostile_count"], case
    print("PASS", case["path"])
