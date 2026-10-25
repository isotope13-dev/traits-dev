#!/usr/bin/env python3
"""Inspect static findings; never execute fixture source."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DEEP = "micro-behaviors/os/module/load::deep-single-letter-require-path"
EVAL = "micro-behaviors/process/interpreter/eval/direct::applescript-eval-joined-lines"

def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield from report["files"]

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(p) for p in HERE.iterdir()
                            if p.suffix in (".js", ".sh", ".applescript")]],
    capture_output=True, text=True)
assert result.returncode in (0, 1), result.stderr
assert "validation failed" not in result.stdout, result.stdout
assert "Warning:" not in result.stderr, result.stderr
found = {Path(f["path"]).name: {t["id"]: t["crit"] for t in f.get("traits", [])}
         for f in reports(result.stdout)}
for name in ["require-deep.js", "require-spaced.js"]:
    assert found[name].get(DEEP) == 4, (name, found[name])
for name in ["require-seven.js", "require-partial-eighth.js", "require-comment.js", "require-string.js"]:
    assert DEEP not in found[name], (name, found[name])
for name in ["joined.applescript", "joined-shell.sh"]:
    assert found[name].get(EVAL) == 3, (name, found[name])
for name in ["plain.applescript", "joined-comment.applescript", "joined-echo.sh"]:
    assert EVAL not in found[name], (name, found[name])
print("11 positive and near-miss checks passed")
