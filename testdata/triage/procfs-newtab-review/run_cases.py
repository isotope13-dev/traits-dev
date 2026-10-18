#!/usr/bin/env python3
"""Scan inert fixtures outside testdata to exercise unsuppressed matchers."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--staging", required=True, type=Path)
args = parser.parse_args()
fixture_dir = Path(__file__).resolve().parent
repo = fixture_dir.parents[2]
cases = json.loads((fixture_dir / "cases.json").read_text())
args.staging.mkdir(parents=True, exist_ok=True)
for name in cases:
    shutil.copyfile(fixture_dir / name, args.staging / name)
result = subprocess.run(
    [args.cleave, "--traits-dir", str(repo), "--json", str(args.staging)],
    capture_output=True, text=True, check=True,
)
if result.stderr.strip():
    print(result.stderr.strip())
seen = set()
for line in result.stdout.splitlines():
    for report in json.loads(line)["files"]:
        name = Path(report["path"]).name
        if name not in cases:
            continue
        seen.add(name)
        traits = report.get("traits", [])
        ids = {t["id"] for t in traits}
        case = cases[name]
        missing = set(case["matched"]) - ids
        unexpected = set(case["not_matched"]) & ids
        assert not missing, (name, "missing", missing)
        assert not unexpected, (name, "unexpected", unexpected)
        assert all(t["crit"] < 5 for t in traits), (name, "hostile finding")
        if name != "proc-rdwr.c":
            assert all(t["crit"] < 4 for t in traits), (name, "suspicious finding")
        print("PASS", name)
assert seen == set(cases), ("unscanned cases", set(cases) - seen)
print(f"{len(seen)} cases passed")
