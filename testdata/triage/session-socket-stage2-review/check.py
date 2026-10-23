"""Check reference-only near misses and named crypto import syntax."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).parent
paths = [fixtures / name for name in ('crypto-imports.js', 'reference-only.js', 'other-module.js')]
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
                         '--format', 'json', *map(str, paths)],
                        check=True, capture_output=True, text=True,
                        env={**os.environ, 'CLEAVE_VALIDATE': '0'})
remaining = result.stdout
reports = {}
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for item in report['files']:
        reports[Path(item['path']).name] = item['traits']
imports = {'metadata/import/builtin::node-' + name + '-esm-import'
           for name in ('pbkdf2sync', 'createcipheriv', 'createdecipheriv')}
for name, traits in reports.items():
    ids = {trait['id'] for trait in traits}
    if name == 'crypto-imports.js':
        assert imports <= ids, imports - ids
    else:
        assert not imports & ids, (name, imports & ids)
    assert not [t['id'] for t in traits if t['crit'] >= 4], name
    assert 'well-known/app/security/bitwarden::bitwarden-app' not in ids
    assert 'well-known/lib/format/node-tar::node-tar-library' not in ids
assert len(reports) == 3
print('PASS: crypto imports, comment/module near misses, reference-only names')
