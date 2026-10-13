#!/usr/bin/env python3
"""Check emitted findings and the separately filtered baseline control."""
import json
import os
from pathlib import Path
import subprocess

fixture_dir = Path(__file__).resolve().parent
repo = fixture_dir.parent.parent
engine = os.environ.get("CLEAVE", "cleave")
cases = json.loads((fixture_dir / "cases.json").read_text())
result = subprocess.run(
    [engine, "--traits-dir", str(repo), "--format", "json", str(fixture_dir)],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for file in report.get("files", [report]):
        files[Path(file["path"]).name] = file

for name, case in cases.items():
    ids = {trait["id"] for trait in files[name].get("traits", [])}
    missing = set(case.get("required", [])) - ids
    unexpected = set(case.get("forbidden", [])) & ids
    assert not missing, (name, "missing", missing)
    assert not unexpected, (name, "unexpected", unexpected)
    for key, label in [("matched_only", "MATCHED"), ("not_matched_only", "NOT MATCHED")]:
        for trait in case.get(key, []):
            trace = subprocess.run(
                [engine, "--traits-dir", str(repo), "test-rules",
                 str(fixture_dir / name), "--rules", trait],
                check=True, capture_output=True, text=True,
            )
            assert any(line.startswith(label + " " + trait + " ")
                       for line in trace.stdout.splitlines()), (name, trait, trace.stdout)
print(f"Passed {len(cases)} triage fixtures.")
