#!/usr/bin/env python3
"""Identify direct npm test self-recursion without matching other scripts."""
import json
import pathlib
import subprocess
import tempfile

cases = {
    'recursive': ({'scripts': {'test': 'npm run test'}}, True),
    'short-form': ({'scripts': {'test': 'npm test'}}, True),
    'unit-test': ({'scripts': {'test': 'npm run test:unit'}}, False),
    'other-script': ({'scripts': {'build': 'npm run test'}}, False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (data, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.json')
        path.write_text(json.dumps(data))
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::npm-test-self-recursion') for t in report['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('npm test recursion boundaries passed.')
