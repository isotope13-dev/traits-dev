#!/usr/bin/env python3
"""Check the focused cases against JSONL produced by cleave --json."""
import json
import sys
from pathlib import Path

cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
reports = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line]
files = [file for report in reports for file in report.get('files', [])]
failures = []
for case in cases:
    matching = [file for file in files if file['path'].endswith('/' + Path(case['path']).name)]
    ids = {trait['id'] for file in matching for trait in file.get('traits', [])}
    missing = set(case['matched']) - ids
    unexpected = set(case['not_matched']) & ids
    if not matching or missing or unexpected:
        failures.append((case['case_id'], sorted(missing), sorted(unexpected)))
if failures:
    raise SystemExit(str(failures))
print(f"Passed {len(cases)} focused cases")
