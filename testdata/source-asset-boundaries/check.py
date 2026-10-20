"""Static rule controls: disguised source, incomplete shells, and neutral Python."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
here = Path(__file__).resolve().parent
cases = json.loads((here / 'cases.json').read_text())
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json',
     *[str(here / case['file']) for case in cases]],
    cwd=root, text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stderr)
observed = {}
criticals = {}
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report['files']:
        observed[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
        criticals[Path(file['path']).name] = {t['id'] for t in file.get('traits', []) if t['crit'] >= 5}
failures = []
for case in cases:
    actual = observed[case['file']]
    missing = set(case['required']) - actual
    forbidden = set(case['forbidden']) & actual
    if case.get('forbid_hostile'):
        forbidden |= criticals[case['file']]
    if missing or forbidden:
        failures.append((case['file'], sorted(missing), sorted(forbidden)))
if failures:
    raise SystemExit(json.dumps(failures, indent=2))
print(f"Passed {len(cases)} static boundary controls")
