"""Scan file-operation controls without executing their AppleScript."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(ROOT / case["path"]) for case in cases]],
    check=True, capture_output=True, text=True)
# Some CLI builds emit adjacent JSON reports, without line separators.
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        reports[Path(file["path"]).name] = {
            trait["id"]: trait["crit"] for trait in file.get("traits", [])}

checks = 0
for case in cases:
    observed = reports[Path(case["path"]).name]
    for trait in case["matched"]:
        assert observed.get(trait) == 3, (case["path"], trait, observed)
        checks += 1
    for trait in case["not_matched"]:
        assert trait not in observed, (case["path"], trait, observed)
        checks += 1
    assert not any(level >= 4 for level in observed.values()), case["path"]
    checks += 1
print(f"PASS: {checks} assertions across {len(cases)} static controls")
