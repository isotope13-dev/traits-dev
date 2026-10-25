#!/usr/bin/env python3
"""Scan fixtures under neutral paths; never execute fixture commands."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SCRATCH = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch')

def main():
    fixtures = json.loads((HERE / 'cases.json').read_text())['fixtures']
    env = os.environ.copy()
    env.pop('CLEAVE_VALIDATE', None)
    with tempfile.TemporaryDirectory(prefix='acquit-focused-', dir=SCRATCH) as tmp:
        paths = []
        for fixture in fixtures:
            source = ROOT / fixture['path']
            target = Path(tmp) / source.name
            target.write_bytes(source.read_bytes())
            paths.append(str(target))
        result = subprocess.run(
            [env.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json', *paths],
            text=True, capture_output=True, env=env, check=True,
        )
        # splitlines() also splits U+0085/U+2028 inside valid JSON strings.
        files = {Path(f['path']).name: f for line in result.stdout.split('\n')
                 if line.strip() for f in json.loads(line).get('files', [])}
        for fixture in fixtures:
            name = Path(fixture['path']).name
            ids = {t['id'] for t in files[name].get('traits', [])}
            missing = set(fixture['matched']) - ids
            unexpected = set(fixture['not_matched']) & ids
            assert not missing, (name, 'missing', sorted(missing))
            assert not unexpected, (name, 'unexpected', sorted(unexpected))
    print(f'PASS {len(fixtures)} controls under neutral paths')

if __name__ == '__main__':
    main()
