#!/usr/bin/env python3
"""Check that aliased os.system calls have the matching module import."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
aliases = {'o': 'o', '_os': 'underscore-os', 'os_': 'os-underscore',
           'oslib': 'oslib', 'operating_system': 'operating-system'}
with tempfile.TemporaryDirectory(prefix='python-os-alias-') as tmp:
    root = Path(tmp)
    cases = {f'{slug}.py': f'import os as {alias}\n{alias}.system("echo x")\n'
             for alias, slug in aliases.items()}
    cases.update({'wrong_module.py': 'import other as o\no.system("echo x")\n',
                  'mismatched.py': 'import os as _os\no.system("echo x")\n',
                  'bare.py': 'o.system("echo x")\n'})
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    prefix = 'metadata/file/profile/process/creation-api::python-os-system-alias-'
    for slug in aliases.values():
        assert prefix + slug in ids[f'{slug}.py'], (slug, ids[f'{slug}.py'])
    for name in ('wrong_module.py', 'mismatched.py', 'bare.py'):
        assert not any(i.startswith(prefix) for i in ids[name]), (name, ids[name])
    print('All five os aliases require their matching import and call.')
