#!/usr/bin/env python3
"""Check that embedded keys are actually redirected into authorized_keys."""
import json
import pathlib
import subprocess
import tempfile

key = 'ssh-ed25519 ' + 'A' * 68 + ' example'
cases = {
    'replace': (f'echo "{key}" > /home/user/.ssh/authorized_keys', True),
    'append': (f'echo "{key}" >> /root/.ssh/authorized_keys', True),
    'other-file': (f'echo "{key}" > /tmp/authorized_keys', False),
    'path-only': ('echo "$KEY" > /home/user/.ssh/authorized_keys', False),
    'comment': (f'# echo "{key}" > /home/user/.ssh/authorized_keys', False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (body, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.sh')
        path.write_text('#!/bin/sh\n' + body + '\n')
        data = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::shell-embedded-key-redirect') for t in data['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('Embedded SSH public key redirect boundaries passed.')
