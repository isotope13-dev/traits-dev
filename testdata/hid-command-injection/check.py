#!/usr/bin/env python3
"""Check HID injection boundaries without executing any fixture payload."""
import json
from pathlib import Path
import subprocess
import sys


root = Path(__file__).resolve().parents[2]
fixture_dir = Path(__file__).resolve().parent
cases = json.loads((fixture_dir / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave",
     "--traits-dir", str(root), "--json", str(fixture_dir)],
    capture_output=True, text=True, check=True,
)
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        reports[Path(report["path"]).name] = report

failures = []
for case in cases:
    name = Path(case["path"]).name
    if name not in reports:
        failures.append(f"{name}: missing analysis report")
        continue
    traits = {trait["id"]: trait for trait in reports[name].get("traits", [])}
    for required in case["matched"]:
        if required not in traits:
            failures.append(f"{name}: missing {required}")
        elif traits[required]["crit"] != 5:
            failures.append(f"{name}: {required} must be hostile")
    for forbidden in case["not_matched"]:
        if forbidden in traits:
            failures.append(f"{name}: unexpected {forbidden}")
    for required in case.get("notable", []):
        if required not in traits or traits[required]["crit"] != 3:
            failures.append(f"{name}: missing notable {required}")

if failures:
    raise SystemExit("\n".join(failures))
print(f"Passed {len(cases)} HID injection cases")
