#!/usr/bin/env python3
"""Check document deception and ordinary AutoIt backup/installer controls."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]


def check(case):
    ids = case.get("matched", []) + case.get("not_matched", [])
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(root), "test-rules",
         str(root / case["path"]), "--rules", ",".join(ids)],
        text=True, capture_output=True, check=True,
    )
    matched = {line.split()[1] for line in result.stdout.splitlines()
               if line.startswith("MATCHED ")}
    expected = set(case.get("matched", []))
    assert matched == expected, (case["case_id"], matched, result.stdout, result.stderr)
    assert "Skipped: File type mismatch" not in result.stdout, result.stdout
    return case["case_id"]


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for name in pool.map(check, cases):
        print("PASS", name)
