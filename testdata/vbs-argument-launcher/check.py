#!/usr/bin/env python3
"""Check full-scan coverage of the short helper and its semantic near misses."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
env = dict(os.environ, CLEAVE_VALIDATE="0", CLEAVE_SKIP_CACHE="1")
proc = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--format", "json", str(Path(__file__).parent)],
    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
)
assert not proc.stderr.strip(), proc.stderr
remaining = proc.stdout
decoder = json.JSONDecoder()
reports = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report.get("files", []):
        reports[Path(file["path"]).name] = file

argument = "micro-behaviors/process/argument/positional::wscript-first-argument"
launch = "micro-behaviors/process/create/exec::vbs-inline-shell-first-argument"
flags = "micro-behaviors/process/create/flags::wsh-hidden-async-run"
covered = {argument, launch, flags}
cases = {
    "hidden-argument.vbs": covered,
    "case-variant.vbs": covered,
    "visible-argument.vbs": {argument, launch},
    "synchronous-argument.vbs": {argument, launch},
    "other-argument.vbs": {flags},
    "commented.vbs": {argument},
    "object-only.vbs": set(),
    "argument-only.vbs": {argument},
}
for name, expected in cases.items():
    traits = reports[name].get("traits", [])
    actual = {trait["id"] for trait in traits}
    assert actual & covered == expected, (name, expected, actual & covered)
    assert all(trait["crit"] <= 3 for trait in traits), (name, traits)
fragment = {trait["id"] for trait in reports["environment-fragment.js"]["traits"]}
assert "micro-behaviors/data/string/replace::node-environment-fragment-unicode-replace" in fragment
assert not any(trait.startswith("micro-behaviors/process/create/exec::") for trait in fragment)
print("PASS: 8 VBS controls and a non-executing JavaScript fragment")
