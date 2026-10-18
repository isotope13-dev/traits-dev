"""Run focused controls outside testdata's intentional corpus exclusions."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
cases = json.loads((root / 'cases.json').read_text())['fixtures']
destination = Path(sys.argv[1]).resolve()
destination.mkdir(parents=True, exist_ok=True)
paths = []
for case in cases:
    source = Path(case['path'])
    target = destination / source.name
    shutil.copyfile(source, target)
    paths.append(str(target))
env = os.environ.copy()
env.update(SCAN_HOPPER='', SCAN_FOLLOW='none', SCAN_FETCH='none')
result = subprocess.run(
    ['atomscan', '--no-update', '--mode', 'slow', '--follow=none', '-f', 'json',
     'path', *paths, '--hopper='],
    capture_output=True, text=True, env=env,
)
(destination / 'scan.jsonl').write_text(result.stdout)
(destination / 'scan.stderr').write_text(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    files = json.loads(line).get('raw', {}).get('files', [])
    if files:
        reports[Path(files[0]['path']).name] = {
            trait['id']: trait
            for file in files for trait in file.get('traits', [])
        }
failures = []
for case in cases:
    name = Path(case['path']).name
    traits = reports.get(name, {})
    missing = [rule for rule in case['matched'] if rule not in traits]
    unexpected = [rule for rule in case['not_matched'] if rule in traits]
    hostile = [rule for rule, value in traits.items() if value['crit'] == 5]
    if name not in reports or missing or unexpected or hostile:
        failures.append(dict(path=name, missing=missing,
                             unexpected=unexpected, hostile=hostile))
print(json.dumps(dict(cases=len(cases), failures=failures), indent=2))
raise SystemExit(bool(failures))
