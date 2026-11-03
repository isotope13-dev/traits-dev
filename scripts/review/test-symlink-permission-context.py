#!/usr/bin/env python3
"""Check co-occurrence of a symlink and privileged permission test."""
import json
import pathlib
import subprocess
import tempfile

source = '''#!/bin/sh
$sudo chmod 700 $tmp
$sudo -u $user ln -s $tmp/target $log
if $sudo test -f $tmp/target; then echo present; fi
'''
cases = {
    'context': (source, True),
    'no-link': (source.replace('ln -s', 'ln'), False),
    'other-mode': (source.replace('chmod 700', 'chmod 755'), False),
    'no-test': (source.replace('test -f', 'test -d'), False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (content, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.sh')
        path.write_text(content)
        data = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::sudo-symlink-file-test') for t in data['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('Symlink permission test context boundaries passed.')
