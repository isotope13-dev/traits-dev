#!/usr/bin/env python3
"""Run controls outside fixture paths, which the depth heuristic excludes."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = Path(__file__).resolve().parent
traits = source.parents[2]
cases = json.loads((source / 'cases.json').read_text())
args.scratch.mkdir(parents=True, exist_ok=True)
for case in cases:
    shutil.copyfile(source / case['name'], args.scratch / case['name'])
result = subprocess.run(
    [args.cleave, '--traits-dir', str(traits), '--format', 'json', str(args.scratch)],
    check=True, capture_output=True, text=True,
)
# Directory scans emit concatenated JSON objects.
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
units = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    units.extend(report.get('files', [report]))
    remaining = remaining[end:].lstrip()
by_name = {Path(unit['path']).name: unit for unit in units}
for case in cases:
    matches = {trait['id'] for trait in by_name[case['name']].get('traits', [])}
    missing = set(case['present']) - matches
    unexpected = set(case['absent']) & matches
    if missing or unexpected:
        raise SystemExit(f"{case['name']}: missing={missing}, unexpected={unexpected}")
    print(f"PASS {case['name']}")
