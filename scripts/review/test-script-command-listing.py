#!/usr/bin/env python3
"""Verify command listings require actual rows and independent attack context."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/degrade/system/policy::listing-lockout-with-copy-and-run-reference'
POLICIES = ['DisableTaskMgr', 'DisableRegistryTools', 'NoControlPanel', 'NoRun']

def fixture():
    rows = [f'<tr><td>Write binary data to registry</td><td>{n}</td><td>Binary data [8 byte(s)] 0400000001000000</td></tr>' for n in POLICIES]
    rows += [r'<tr><td>Copy file</td><td>example.exe</td><td>C:\WINDOWS\demo.exe</td></tr>',
             r'<tr><td>Open registry key</td><td>HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run</td></tr>',
             '<tr><td>Write string value to registry</td><td>LegalNoticeText</td><td>восстанов пришли test@example.org код пополн</td></tr>']
    return '<html><body><table>' + ''.join(rows) + '</table></body></html>'

def matches(source):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'listing.html'
        path.write_bytes(source.encode('cp1251'))
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        return any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))

source = fixture()
assert matches(source)
for old, new in [('DisableTaskMgr', 'ExampleTaskMgr'), ('DisableRegistryTools', 'ExampleTools'),
                 ('NoControlPanel', 'PanelExample'), ('NoRun</td>', 'NoRuntime</td>'),
                 ('Copy file', 'Read file'), ('CurrentVersion\\Run', 'CurrentVersion\\Other'),
                 ('LegalNoticeText', 'LegalNoticeCaption'), ('пополн', 'отчёт'),
                 ('test@example.org', 'test.example.org')]:
    assert not matches(source.replace(old, new)), old
assert not matches(source.replace('0400000001000000', '0400000000000000'))
print('Command listing requires enabling writes, copy, Run reference, and recovery/payment context')
