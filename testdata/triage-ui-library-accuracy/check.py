#!/usr/bin/env python3
"""Scan fixtures as ordinary files, without executing any fixture code."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--scratch", required=True, type=Path)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]

# Several rules suppress files under test directories. Stage the same bytes
# outside that context so a passing near miss cannot be caused by that gate.
with tempfile.TemporaryDirectory(prefix="ui-accuracy-", dir=args.scratch) as tmp:
    def check(case):
        source = ROOT / case["path"]
        target = Path(tmp) / source.name
        shutil.copyfile(source, target)
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", str(target)], capture_output=True, text=True)
        if result.returncode:
            return case["path"], [result.stderr]
        report = json.loads(result.stdout)
        found = {trait["id"] for file in report["files"]
                 for trait in file.get("traits", [])}
        errors = ["missing " + rule for rule in case["matched"]
                  if rule not in found]
        errors += ["unexpected " + rule for rule in case["not_matched"]
                   if rule in found]
        return case["path"], errors

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    for path, errors in results:
        print(("FAIL " if errors else "PASS ") + path)
        for error in errors:
            print(error)
    raise SystemExit(any(errors for _, errors in results))
