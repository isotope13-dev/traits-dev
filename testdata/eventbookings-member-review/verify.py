#!/usr/bin/env python3
"""Check behavior and placement boundaries with one rule-set load."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
# Test-path suppressions are intentional for some URL references. Stage the
# same bytes under an ordinary directory to exercise the positive matcher.
with tempfile.TemporaryDirectory(prefix=".eventbookings-fixtures-", dir=root) as stage:
    staged = []
    for case in cases:
        dest = Path(stage) / Path(case["path"]).name
        shutil.copyfile(root / case["path"], dest)
        staged.append(str(dest))
    result = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else "cleave",
                             "--traits-dir", str(root), "--format", "json",
                             *staged], cwd=root, capture_output=True,
                            text=True, check=True)
if result.stderr.strip():
    raise SystemExit(result.stderr)
decoder, offset, reports = json.JSONDecoder(), 0, {}
while offset < len(result.stdout):
    while offset < len(result.stdout) and result.stdout[offset].isspace():
        offset += 1
    if offset == len(result.stdout):
        break
    report, offset = decoder.raw_decode(result.stdout, offset)
    for file in report["files"]:
        reports[Path(file["path"]).name] = {trait["id"] for trait in file.get("traits", [])}
for case in cases:
    ids = reports[Path(case["path"]).name]
    missing = set(case["matched"]) - ids
    unexpected = set(case["not_matched"]) & ids
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print("PASS: %d positive and near-miss fixtures" % len(cases))
