#!/usr/bin/env python3
"""Check compromised-page triage fixtures: remote includes and atob-eval.

Fixtures are scanned as copies outside the repo because some legs carry
test-directory exclusions on repository fixture paths.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOSTILE = {
    "objectives/anti-static/obfuscation/syntax::html-atob-eval-identifier-stager",
    "objectives/command-and-control/dropper/delivery/html::atob-blob-variable-eval-delivery",
}

root = Path(__file__).resolve().parents[2]
cases = json.loads((Path(__file__).with_name("cases.json")).read_text())["fixtures"]
if len(sys.argv) == 2:
    output = Path(sys.argv[1]).read_text()
else:
    tmp = Path(tempfile.mkdtemp(prefix="triage-compromised-page-"))
    copies = []
    for case in cases:
        src = root / case["path"]
        dst = tmp / Path(case["path"]).name
        shutil.copyfile(src, dst)
        copies.append(str(dst))
    output = subprocess.check_output(
        ["cleave", "--traits-dir", str(root), "--disable", "third-party",
         "--format", "json", *copies],
        text=True,
    )
reports = []
decoder = json.JSONDecoder()
while output.strip():
    output = output.lstrip()
    report, end = decoder.raw_decode(output)
    reports.extend(report["files"])
    output = output[end:]
for case in cases:
    name = Path(case["path"]).name
    report = next(r for r in reports if r["path"].endswith(name))
    traits = {t["id"]: t for t in report["traits"]}
    assert not set(case["matched"]) - traits.keys(), name
    assert not set(case["not_matched"]) & traits.keys(), name
    if name == "repeated-script-inject.html":
        assert all(t["crit"] < 4 for t in traits.values()), name
    for hid in HOSTILE & set(case["matched"]):
        assert traits[hid]["crit"] == 5, (name, hid)
print(f"PASS: {len(cases)} compromised-page triage fixtures")
