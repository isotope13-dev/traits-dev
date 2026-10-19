#!/usr/bin/env python3
"""Check trait placement, factory references, and nearby nonmatching syntax."""
import json
import pathlib
import subprocess
import shutil
import tempfile

root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads((pathlib.Path(__file__).with_name("cases.json")).read_text())["fixtures"]
# Test source semantics without test-directory allowlisting suppressing them.
with tempfile.TemporaryDirectory(prefix=".stream-controls-", dir=root) as temp:
    targets = []
    for case in cases:
        target = pathlib.Path(temp) / pathlib.Path(case["path"]).name
        shutil.copyfile(root / case["path"], target)
        targets.append(str(target))
    proc = subprocess.run(["cleave", "--traits-dir", str(root), "--format", "json"] +
                          targets, check=True, capture_output=True, text=True)
data = proc.stdout
reports = []
while data.strip():
    report, end = json.JSONDecoder().raw_decode(data.lstrip())
    reports.append(report)
    data = data.lstrip()[end:]
assert len(reports) == len(cases), (len(reports), len(cases))
for case, report in zip(cases, reports):
    traits = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    missing = set(case["required_emitted"]) - traits
    extra = set(case["forbidden_emitted"]) & traits
    assert not missing and not extra, (case["case_id"], missing, extra)
    print("PASS", case["case_id"])
