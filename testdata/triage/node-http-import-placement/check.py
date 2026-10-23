"""Imports remain notable metadata; imports alone cannot satisfy GET selectors."""
import json
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parent
root = base.parents[2]
report = subprocess.check_output([
    'cleave', '--no-update-check', '--traits-dir', str(root), '--format', 'json',
    str(base / 'import-only.js'), str(base / 'prefixed-import-only.js'),
    str(base / 'comment-only.js'),
], text=True)
decoder = json.JSONDecoder()
pos = 0
checked = 0
while pos < len(report):
    if report[pos].isspace():
        pos += 1
        continue
    data, pos = decoder.raw_decode(report, pos)
    for file in data['files']:
        traits = {trait['id']: trait for trait in file['traits']}
        assert not any(t.startswith('micro-behaviors/communications/http/get::')
                       for t in traits), file['path']
        for module in ('http', 'https'):
            group = 'metadata/import/builtin::node-' + module + '-module-required'
            prefixed = 'metadata/import/builtin::node-prefixed-' + module + '-require'
            plain = 'metadata/import/builtin::require-' + module
            if file['path'].endswith('/comment-only.js'):
                assert not {group, prefixed, plain} & traits.keys(), file['path']
            else:
                if file['path'].endswith('/prefixed-import-only.js'):
                    assert traits[prefixed]['crit'] == 3, file['path']
                else:
                    assert traits[plain]['crit'] == 3, file['path']
                if group in traits:
                    assert traits[group]['crit'] == 3, file['path']
        checked += 1
        print('PASS', Path(file['path']).name)
assert checked == 3, checked
