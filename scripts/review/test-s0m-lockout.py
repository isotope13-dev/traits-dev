#!/usr/bin/env python3
"""Exercise serialized policy records and notice context without malware."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/ransom/scareware::s0m-lockout-and-payment-notice'
PREFIX = b'\x0a\x01\x00\x00\x49\x00\x00\x00Program: \x00Protection: \x00Cracker: \x00Group: \x00Released: \x00Title\x00\xff\x93\x01\x00\x00\x00\x7e\x00\x00\x00\x00'
VALUE = b'\0\x08\0\0\0\x04\0\0\0\x01\0\0\0'
NAMES = [b'DisableTaskMgr', b'DisableRegistryTools', b'NoControlPanel', b'NoRun']
NOTICE = b'\xa2LegalNoticeText\0' + 'восстанов пришли test@example.org код пополн'.encode('cp1251') + b'\0'
SOURCE = PREFIX + b''.join(b'\xa4' + n + VALUE for n in NAMES) + NOTICE

def matches(data):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'demo.s0m'
        path.write_bytes(data)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        return any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))

assert matches(SOURCE)
for name in NAMES:
    assert not matches(SOURCE.replace(b'\xa4' + name, b'\xa3' + name)), name
assert not matches(SOURCE.replace(VALUE, VALUE[:-4] + b'\0\0\0\0'))
assert not matches(SOURCE.replace(b'LegalNoticeText', b'LegalNoticeOmit'))
assert not matches(SOURCE.replace('пополн'.encode('cp1251'), 'отчёт'.encode('cp1251')))
assert not matches(SOURCE.replace(b'test@example.org', b'test.example.org'))
print('Serialized lockout finding requires each policy record and payment notice context')
