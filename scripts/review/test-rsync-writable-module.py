#!/usr/bin/env python3
"""Check writable rsync module observations and their boundaries."""
import json
import pathlib
import subprocess
import tempfile

cases = {
    'writable': ('/etc/rsyncd.conf', 'false', True),
    'read-only': ('/etc/rsyncd.conf', 'true', False),
    'other-config': ('/etc/other.conf', 'false', False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (config, read_only, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.sh')
        path.write_text(f'#!/bin/sh\ncat >> {config} <<EOF\n[share]\npath = /srv/share\nread only = {read_only}\nEOF\n')
        data = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        actual = any(t['id'].endswith('::rsync-daemon-writable-module-text') for t in data['files'][0].get('traits', []))
        assert actual == expected, (name, actual, expected)
print('Rsync writable module observation boundaries passed.')
