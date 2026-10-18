#!/usr/bin/env python3
"""Check the rdns-table guard on wallet targeting rules.

Fixtures live under testdata/, whose path tokens suppress test-guarded
traits regardless of content, so stage copies into a guard-neutral temp dir
before analyzing: the directory shape (brand rows plus provider rdns names)
must stay quiet while the installed-probe shape (bundle/package checks with
no rdns declarations) retains the bundle reference. Package checks alone do
not establish wallet credential acquisition.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BUNDLE = "micro-behaviors/os/application/target::exodus-bundle"
CLUSTER = "objectives/credential-access/wallet/keywords::crypto-wallet-keyword-cluster"
RDNS = "micro-behaviors/communications/blockchain/client::wallet-provider-rdns-table"
BENIGN = "wallet-directory-benign.js"
POSITIVE = "installed-wallet-probe-positive.js"

with tempfile.TemporaryDirectory(prefix="wbrdns") as tmp:
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
assert RDNS in observed[BENIGN], (BENIGN, observed[BENIGN])
assert BUNDLE not in observed[BENIGN], (BENIGN, observed[BENIGN])
assert CLUSTER not in observed[BENIGN], (BENIGN, observed[BENIGN])
assert BUNDLE in observed[POSITIVE], (POSITIVE, observed[POSITIVE])
assert CLUSTER not in observed[POSITIVE], (POSITIVE, observed[POSITIVE])
assert RDNS not in observed[POSITIVE], (POSITIVE, observed[POSITIVE])
print("Passed 2 wallet-discovery-rdns cases")
