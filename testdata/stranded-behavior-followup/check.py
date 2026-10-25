#!/usr/bin/env python3
"""Inspect static scan findings; never execute any fixture source."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIXTURES = ROOT / "testdata" / "benign" / "stranded-behavior-followup"
MKDIR = "micro-behaviors/fs/directory/create::applescript-shell-mkdir-parent"
FILE = "micro-behaviors/fs/file/stat::applescript-shell-file-classification"
JOINED = "micro-behaviors/process/interpreter/eval/direct::applescript-eval-joined-lines"
MACRO = "micro-behaviors/process/interpreter/eval/indirect::vba-run-sheet-range"
OLD_JOINED = "micro-behaviors/process/interpreter/eval/constructed::applescript-eval-joined-lines"
OLD_MACRO = "micro-behaviors/process/interpreter/eval/direct::vba-run-sheet-range"
EXPECTED = {
    "operations.applescript": {MKDIR, FILE},
    "embedded.sh": {MKDIR, FILE, JOINED},
    "references.applescript": set(),
    "different-commands.applescript": set(),
    "worksheet-reference.vbs": set(),
    "macro-dispatch.vbs": {MACRO},
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json",
     *[str(FIXTURES / name) for name in EXPECTED]],
    capture_output=True, text=True, check=True)
assert not result.stderr.strip(), result.stderr
observed = {}
for line in result.stdout.splitlines():
    for entry in json.loads(line)["files"]:
        observed[Path(entry["path"]).name] = {
            trait["id"] for trait in entry.get("traits", [])}
for name, expected in EXPECTED.items():
    assert observed[name] & {MKDIR, FILE, JOINED, MACRO} == expected, (name, observed[name])
    assert not observed[name] & {OLD_JOINED, OLD_MACRO}, (name, observed[name])
print(f"{len(EXPECTED)} static behavior and placement controls passed")
