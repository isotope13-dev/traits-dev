#!/usr/bin/env python3
"""Check call evidence and source-map path boundaries against the local rules."""
import argparse
import json
import re
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
for case in cases:
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(root), "--format", "json",
         str(root / case["path"])], check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    ids = {trait["id"] for item in report["files"]
           for trait in item.get("traits", [])}
    missing = set(case["required"]) - ids
    unexpected = set(case["forbidden"]) & ids
    assert not missing and not unexpected, (case["path"], missing, unexpected)
    for trait_id in case.get("matched", []) + case.get("not_matched", []):
        trace = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "test-rules",
             str(root / case["path"]), "--rules", trait_id],
            check=True, capture_output=True, text=True,
        )
        matched = bool(re.search(r"^MATCHED " + re.escape(trait_id) + r" \(", trace.stdout, re.M))
        assert matched == (trait_id in case.get("matched", [])), trace.stdout
    print("PASS", case["path"])
