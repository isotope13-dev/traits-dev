import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

# Copy out of testdata: the filename trait deliberately excludes test trees.
root = Path(__file__).resolve().parent
controls = Path(sys.argv[1]).resolve()
controls.mkdir(parents=True, exist_ok=True)
cases = json.loads((root / "cases.json").read_text())["fixtures"]
for case in cases:
    shutil.copyfile(root / case["path"], controls / case["path"])
result = subprocess.run(
    ["cleave", "--traits-dir", str(Path.cwd()), "--format", "json", str(controls)],
    check=True, capture_output=True, text=True)
remaining = result.stdout
decoder = json.JSONDecoder()
findings = {}
while remaining.strip():
    report, used = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[used:]
    for file in report["files"]:
        findings[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
for case in cases:
    actual = findings[case["path"]]
    assert set(case["matched"]) <= actual, case
    assert not set(case["not_matched"]) & actual, case
print(f"Passed {len(cases)} positive and near-miss controls")
