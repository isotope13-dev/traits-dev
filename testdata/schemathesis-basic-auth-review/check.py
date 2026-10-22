#!/usr/bin/env python3
"""Check help prose versus header literals, including existing attack fixtures."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREFIX = "micro-behaviors/communications/http/authorization-header::"
LITERAL = PREFIX + "basic-auth-credential-literal"
HARDCODED = PREFIX + "hardcoded-basic-auth-credential"
cases = [
    (HERE / "cli-help.py", set(), {LITERAL, HARDCODED}),
    (HERE / "header-map.py", {LITERAL, HARDCODED}, set()),
    (HERE / "header-index.js", {LITERAL, HARDCODED}, set()),
    (HERE / "header-wire.py", {LITERAL, HARDCODED}, set()),
    (ROOT / "testdata/calibration-first-review/probe.py", {LITERAL}, set()),
    (ROOT / "testdata/calibration-first-review/probe.js", {LITERAL}, set()),
    (ROOT / "testdata/calibration-first-review/alternate-probe.js", {LITERAL}, set()),
    (ROOT / "testdata/calibration-first-review/normal-form.py", {LITERAL}, set()),
    (ROOT / "testdata/hostile/wan-credential-injection/setwan-wire.py", {LITERAL}, set()),
    (ROOT / "testdata/couchdb-rewrite/normal.js", {LITERAL}, set()),
    (ROOT / "testdata/couchdb-rewrite/encoded.js", {LITERAL}, set()),
]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(p) for p, _, _ in cases]],
    capture_output=True, text=True, check=True,
)
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
files = []
while remaining:
    report, consumed = decoder.raw_decode(remaining)
    files.extend(report["files"])
    remaining = remaining[consumed:].lstrip()
for path, required, forbidden in cases:
    selected = [f for f in files if f["path"] == str(path)]
    assert selected, path
    traits = {t["id"] for f in selected for t in f.get("traits", [])}
    assert required <= traits, (path, "missing", required - traits)
    assert not forbidden & traits, (path, "unexpected", forbidden & traits)
    print(path.relative_to(ROOT), "PASS")
