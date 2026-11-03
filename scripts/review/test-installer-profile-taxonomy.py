#!/usr/bin/env python3
"""Keep installer-hook context distinct from a proven network execution."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='installer-profile-') as tmp:
    root = Path(tmp)
    sample = '#!/bin/sh\necho /etc/profile.d/example\ncurl -fs https://example.org/file\n'
    cases = {'preinstall': sample, 'other.sh': sample}
    for name, content in cases.items():
        (root / name).write_text(content)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    profile = 'objectives/execution/trigger/package/lifecycle::macpkg-hook-profile-curl-clues'
    assert profile in ids['preinstall'], ids['preinstall']
    assert profile not in ids['other.sh']
    assert not any(t.startswith('objectives/supply-chain/install-hook/') for group in ids.values() for t in group)
    print('Installer-hook profile remains distinct from an ordinary shell script.')
