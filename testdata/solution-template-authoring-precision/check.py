#!/usr/bin/env python3
"""Check the solution-template authoring guard on python-solution-read.

Fixtures live under testdata/, whose path token suppresses test-dir-guarded
traits regardless of content, so stage copies into a guard-neutral temp dir
before analyzing: the authoring shape (read template, write derived copy)
must stay quiet while the exfil shape (read answer key, send it onward)
must still match.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RULE = "objectives/evasion/security-bypass/llm/egress::python-solution-read"
BENIGN = "solution-template-authoring-benign.py"
POSITIVE = "solution-exfil-positive.py"

with tempfile.TemporaryDirectory(prefix="solread") as tmp:
    staged = []
    for name in (BENIGN, POSITIVE):
        dest = Path(tmp) / name
        shutil.copy(HERE / name, dest)
        staged.append(str(dest))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "jsonl", "analyze", *staged],
        capture_output=True, text=True,
    )
assert result.returncode == 0, result.stderr
observed = {}
decoder = json.JSONDecoder()
remaining = result.stdout
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for artifact in report.get("files", []):
        observed[Path(artifact["path"]).name] = {
            trait["id"] for trait in artifact.get("traits", [])
        }
assert set(observed) == {BENIGN, POSITIVE}, ("Missing fixtures", observed)
assert RULE not in observed[BENIGN], (BENIGN, observed[BENIGN])
assert RULE in observed[POSITIVE], (POSITIVE, observed[POSITIVE])
print("Passed 2 solution-template-authoring cases")
