#!/usr/bin/env python3
"""Check field binding and the relocated naming/declaration observations."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
cases += json.loads((root / "testdata/taxonomy/ifs-log-injection/cases.json").read_text())["fixtures"]
cmd = [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir", str(root), "--format", "json"]
with tempfile.TemporaryDirectory(prefix=".cleave-controls-", dir=root) as temp:
    staged = []
    for index, case in enumerate(cases):
        source = root / case["path"]
        target = Path(temp) / f"case-{index}" / source.name
        target.parent.mkdir()
        target.write_bytes(source.read_bytes())
        staged.append(str(target))
    result = subprocess.run(cmd + staged, text=True, capture_output=True)
if result.returncode:
    sys.stderr.write(result.stderr)
    sys.stderr.write(result.stdout)
    raise SystemExit(result.returncode)

decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report.get("files", []):
        files[str(Path(file["path"]).resolve())] = {t["id"] for t in file.get("traits", [])}
    remaining = remaining[end:].lstrip()

failures = []
for case, path in zip(cases, staged):
    if path not in files:
        failures.append(f"Missing report: {case['path']}")
        continue
    ids = files[path]
    missing = set(case["matched"]) - ids
    unexpected = set(case["not_matched"]) & ids
    if missing or unexpected:
        failures.append(f"{case['path']}: missing={sorted(missing)}, unexpected={sorted(unexpected)}")
if failures:
    raise SystemExit("\n".join(failures))
print(f"PASS: {len(cases)} positive and near-miss fixtures")
