#!/usr/bin/env python3
"""Keep package commands and unbound interpreter argument text as evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='interpreter-config-') as tmp:
    root = Path(tmp)
    cases = {
        'package.json': json.dumps({'name': 'fixture', 'version': '1.0.0',
                                    'scripts': {'preinstall': 'python3 -c "print(1)"'}}),
        'args.py': 'args = ["python3", "-c", code]\n',
        'negative.py': 'args = ["python3", "-m", code]\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    script = 'metadata/package/scripts/inline::npm-preinstall-python-inline-command'
    fragment = 'metadata/file/profile/execution-api::python-interpreter-code-argument'
    assert set(ids) == set(cases), ids.keys()
    assert script in ids['package.json'], ids['package.json']
    assert fragment in ids['args.py'] and fragment not in ids['negative.py'], ids
    print('Interpreter configuration and argument clues remain available.')
