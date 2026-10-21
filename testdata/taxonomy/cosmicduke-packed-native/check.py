#!/usr/bin/env python3
"""Focused controls; supply an independently retained packed specimen."""
import argparse
import concurrent.futures
import json
import re
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('sample', type=Path)
parser.add_argument('--atomscan', default='atomscan')
args = parser.parse_args()
original = args.sample.read_bytes()
behavior = 'objectives/credential-access/browser/firefox::chrome-disguised-packed-firefox-decryptor'
family = 'well-known/malware/stealer/cosmicduke::packed-credential-stealer'

def change(data, old, new):
    assert len(old) == len(new) and old in data, old
    return data.replace(old, new)

cases = [
    ('renamed-positive', original, {behavior, family}),
    ('no-nss-init', change(original, b'NSS_Ini', b'XYZ_Ini'), set()),
    ('no-decrypt-name', change(original, b'SDR_Decrypt', b'SDR_XXXXXXX'), set()),
    ('no-login-select', change(original, b'select id, hostname, user', b'select id, hostname, xxxx'), set()),
    ('no-chrome-identity', change(original, 'chrome.exe'.encode('utf-16le'), 'foobar.exe'.encode('utf-16le')), {family}),
]
# The handoff opcode is at the end of a register-restore block, rather than
# an arbitrary FF E0 elsewhere in the packed image.
pattern = rb'\x8b\x25....\x8b\x2d....\x8b\x0d....\x8b\x15....\x8b\x35....\x8b\x3d....\x8d\x05....\xff\xe0'
match = re.search(pattern, original, re.DOTALL)
assert match is not None
end = match.end() - 2
no_jump = bytearray(original)
no_jump[end:end + 2] = bytes.fromhex('ffd0')
cases.append(('call-instead-of-tail-handoff', bytes(no_jump), set()))
no_identity = change(original, b'BotGenStudio', b'XXXXXXXXXXXX')
no_identity = change(no_identity, b'AdjustKernelTableFromSSDTSpace2', b'X' * len(b'AdjustKernelTableFromSSDTSpace2'))
cases.append(('no-family-corroboration', no_identity, {behavior}))

with tempfile.TemporaryDirectory(prefix='cosmicduke-controls-', dir=args.sample.parent) as temporary:
    def run(case):
        name, data, expected = case
        path = Path(temporary, name + '.exe')
        path.write_bytes(data)
        result = subprocess.run([args.atomscan, '--no-update', '-f', 'json', str(path)], capture_output=True, text=True)
        assert result.returncode in (0, 1) and result.stdout, result.stderr
        report = json.loads(result.stdout)
        actual = {t['id'] for f in report['raw']['files'] for t in f.get('traits', [])} & {behavior, family}
        assert actual == expected, (name, actual, expected)
        return name + ': PASS'
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(run, cases):
            print(result)
