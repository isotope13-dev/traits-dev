"""Run focused trait controls from the repository root."""
import json
import os
from pathlib import Path
import subprocess

cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", ".", "--format", "json",
     *[case["path"] for case in cases]],
    capture_output=True, text=True, check=True,
)
# Multiple inputs produce adjacent reports, one per input.
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.extend(report["files"])
    remaining = remaining[end:].lstrip()
failures = []
for case in cases:
    actual = {trait["id"] for item in files
              if item["path"].endswith(case["path"])
              for trait in item.get("traits", [])}
    missing = set(case["matched"]) - actual
    unwanted = set(case["not_matched"]) & actual
    if missing or unwanted:
        failures.append({"path": case["path"], "missing": sorted(missing),
                         "unwanted": sorted(unwanted)})
    print("FAIL" if missing or unwanted else "PASS", case["path"])
if failures:
    raise SystemExit(json.dumps(failures, indent=2))
