#!/usr/bin/env python3
"""Exercise module controls without repository test-directory suppressors."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--scratch", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
source = root / "testdata/benign/node-aead-module-controls"
inputs = [*source.glob("*.js"), root / "testdata/performance/node-aead-module-controls/caller-keyed-wrapper.js"]
with tempfile.TemporaryDirectory(prefix="aead-control-", dir=args.scratch) as tmp:
    staged = Path(tmp)
    for path in inputs:
        shutil.copyfile(path, staged / path.name)
    result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
        "--format", "jsonl", str(staged)], text=True, capture_output=True, check=True)
    files = []
    # JSON permits Unicode line separators inside strings; split on LF only.
    for line in result.stdout.split("\n"):
        if line.strip():
            files.extend(json.loads(line)["files"])
    seen = set()
    key = "micro-behaviors/os/module/dynamic-load::caller-keyed-decipher-module-path"
    generic = "micro-behaviors/os/module/dynamic-load::node-scrypt-gcm-buffer-field-require"
    suspicious = "objectives/anti-static/obfuscation/crypto::caller-data-aead-module-loading"
    for file in files:
        name = Path(file["path"]).name
        traits = file.get("traits", [])
        ids = {trait["id"] for trait in traits}
        assert not any(trait["crit"] == 5 for trait in traits), name
        assert generic in ids, name
        if name == "caller-keyed-wrapper.js":
            assert key in ids and suspicious in ids, name
        else:
            assert key not in ids and suspicious not in ids, name
            assert not any(trait["crit"] == 4 for trait in traits), name
        seen.add(name)
        print(name, "PASS")
    assert seen == {path.name for path in inputs}
