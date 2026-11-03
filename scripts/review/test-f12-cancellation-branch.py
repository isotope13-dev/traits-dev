#!/usr/bin/env python3
"""Distinguish cancellation in the F12 branch from an allow branch."""
import json
import pathlib
import subprocess
import tempfile

cases = {
    'blocked': ('if (e.key === "F12") { e.preventDefault(); }', True),
    'allowed': ('if (e.key === "F12") return false;\nif (e.key === "F5") e.preventDefault();', False),
    'other-key': ('if (e.key === "F5") { e.preventDefault(); }', False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (body, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.js')
        path.write_text('function handle(e) {\n' + body + '\n}\n')
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::f12-cancellation-branch') for t in report['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
with tempfile.TemporaryDirectory() as tmp:
    for name in ('blocked', 'allowed'):
        body, expected = cases[name]
        path = pathlib.Path(tmp) / (name + '.html')
        path.write_text('<html><script>function handle(e) {' + body + '}</script></html>')
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::html-f12-near-event-cancellation') for t in report['files'][0].get('traits', []))
        assert found == expected, ('html-' + name, found, expected)
print('F12 cancellation branch boundaries passed.')
