#!/usr/bin/env python3
"""Check dormant installer helpers against invoked and unrelated controls."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
fixture_dir = Path(__file__).resolve().parent
repo = fixture_dir.parents[2]
result = subprocess.run(
    [args.cleave, "--traits-dir", str(repo), "--json", "analyze", str(fixture_dir)],
    cwd=repo, text=True, stdout=subprocess.PIPE, check=True,
)
files = [f for line in result.stdout.splitlines() for f in json.loads(line)["files"]]
findings = {Path(f["path"]).resolve(): {t["id"] for t in f.get("traits", [])} for f in files}
cases = json.loads((fixture_dir / "cases.json").read_text())["fixtures"]
for case in cases:
    observed = findings[repo / case["path"]]
    missing = set(case["matched"]) - observed
    unexpected = set(case["not_matched"]) & observed
    if missing or unexpected:
        raise SystemExit(f"FAIL {case['path']}: missing={missing}, unexpected={unexpected}")
print(f"PASS: {len(cases)} instruction-writer boundary cases")
