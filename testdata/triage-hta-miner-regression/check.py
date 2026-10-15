#!/usr/bin/env python3
"""Check HTA/miner triage fixtures: new hostile composites plus FP guards.

Some legs carry test-directory exclusions that suppress matches on
repository fixture paths, so fixtures are scanned as copies outside the
repo and matched back to cases by basename.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOSTILE = {
    "objectives/command-and-control/dropper/delivery/hidden-stage::hta-chr-concealed-shell-launch",
    "objectives/anti-static/obfuscation/wsh::chr-concatenated-com-progid",
    "objectives/impact/cryptojacking/miner/signatures::coinhive-encoded-miner-startup",
    "objectives/command-and-control/dropper/delivery/web-injection::coinhive-unescape-loader-injection",
}

root = Path(__file__).resolve().parents[2]
cases = json.loads((Path(__file__).with_name("cases.json")).read_text())["fixtures"]
if len(sys.argv) == 2:
    output = Path(sys.argv[1]).read_text()
else:
    tmp = Path(tempfile.mkdtemp(prefix="triage-hta-miner-"))
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
    for hid in HOSTILE & set(case["matched"]):
        assert traits[hid]["crit"] == 5, (name, hid)
print(f"PASS: {len(cases)} HTA/miner triage fixtures")
