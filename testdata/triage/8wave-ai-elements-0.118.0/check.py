#!/usr/bin/env python3
"""Verify decimal tables cannot supply hexadecimal payload evidence."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
here = Path(__file__).resolve().parent
repo = here.parents[2]
rule = "metadata/lang/encoded/hex::long-hex-string-literal"
expected = {
    "decimal-table.js": False,
    "hex.js": True,
    "hex-after-decimal.js": True,
    "hex-before-decimal.py": True,
    "near-miss.js": False,
    "numeric-bigint.js": False,
}
result = subprocess.run(
    [args.cleave, "--traits-dir", str(repo), "--json", "analyze",
     str(here / "fixtures")],
    cwd=repo, text=True, stdout=subprocess.PIPE, check=True,
)
seen = set()
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        name = Path(file["path"]).name
        if name not in expected:
            continue
        seen.add(name)
        found = any(t["id"] == rule for t in file.get("traits", []))
        if found != expected[name]:
            raise SystemExit(f"FAIL {name}: match={found}, expected={expected[name]}")
if seen != set(expected):
    raise SystemExit(f"Missing results: {set(expected) - seen}")
print(f"PASS: {len(seen)} hexadecimal literal controls")
