#!/usr/bin/env python3
"""Static mutation controls; reads specimens but never executes them.
Usage: python3 check.py <native-sample> <output-directory> [cleave]
"""
import concurrent.futures
import json
import pathlib
import struct
import subprocess
import sys

sample = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
engine = sys.argv[3] if len(sys.argv) > 3 else 'cleave'
original = sample.read_bytes()
root = pathlib.Path(__file__).resolve().parents[3]
# Reviewed x86 instruction site, used only to produce controls. The matcher
# itself searches all .text bytes and resolves the import without fixed RVAs.
setup = bytes.fromhex('57 53 68 c0 74 40 00 6a 0d ff 15 80 22 41 00')
assert original.count(setup) == 1
site = original.index(setup)
record = '[ENTER]\r\n'.encode('utf-16-le')
assert original.count(record) == 1
hook = 'micro-behaviors/hardware/input/keyboard/hook::x86-iat-low-level-keyboard-hook'
record_trait = 'micro-behaviors/hardware/input/keyboard/label::utf16-enter-key-line-record'
logger = 'objectives/collection/keylog/hook::native-keyboard-hook-recording'
creds = 'objectives/credential-access/browser/multi-target::keyboard-recorder-browser-password-decryption'
query = 'micro-behaviors/data/db/access::select-all-login-table'

def mutate(offset, data):
    b = bytearray(original)
    b[offset:offset + len(data)] = data
    return bytes(b)

cases = [
    ('positive', original, {hook, record_trait, logger, creds, query}, set()),
    ('non-keyboard-hook', mutate(site + 8, b'\x07'), {record_trait, query}, {hook, logger, creds}),
    ('unrelated-iat-call', mutate(site + 11, struct.pack('<I', 0x4120ac)), {record_trait, query}, {hook, logger, creds}),
    ('no-line-record', original.replace(record, b'\x00' * len(record)), {hook, query}, {record_trait, logger, creds}),
    ('no-nss-decrypt', original.replace(b'PK11SDR_Decrypt', b'x' * len(b'PK11SDR_Decrypt')), {hook, logger, query}, {creds}),
    ('other-table', original.replace(b'SELECT * FROM logins', b'SELECT * FROM visits'), {hook, logger}, {creds, query}),
    ('wide-hook-api', original.replace(b'SetWindowsHookExA\0', b'SetWindowsHookExW\0'), {hook, logger, creds}, set()),
]

# A source file can mention stores and kill processes without establishing theft.
source_control = b'void inspect(void) {\n  OpenProcess(1, 0, 10);\n  TerminateProcess(0, 0);\n  CreateToolhelp32Snapshot(2, 0);\n  Process32First(0, 0);\n  Process32Next(0, 0);\n  const char *a = "chrome.exe";\n  const char *b = "firefox.exe";\n  const char *c = "Google/Chrome/User Data/Default/Login Data";\n}\n'
source_profile = 'micro-behaviors/process/terminate/kill::browser-store-process-termination-api-profile-source'
cases.extend([
    ('source-store-and-kill', source_control, {source_profile}, {logger, creds}),
    ('source-no-store', source_control.replace(b'Google/Chrome/User Data/Default/Login Data', b'ordinary-file.txt'), set(), {source_profile, logger, creds}),
])

def run(case):
    name, data, present, absent = case
    if not name.startswith('source-'):
        assert len(data) == len(original), (name, 'mutation changed file size')
    suffix = '.c' if name.startswith('source-') else '.exe'
    p = out / (name + suffix)
    p.write_bytes(data)
    result = subprocess.run([engine, '--traits-dir', str(root), str(p), '--format', 'json'], capture_output=True, text=True)
    (out / (name + '.err')).write_text(result.stderr)
    assert result.returncode == 0, (name, result.stderr)
    report = json.loads(result.stdout)
    (out / (name + '.json')).write_text(result.stdout)
    ids = {t['id'] for t in report['files'][0]['traits']}
    assert present <= ids, (name, 'missing', sorted(present - ids))
    assert not absent & ids, (name, 'unexpected', sorted(absent & ids))
    return {'case': name, 'result': 'pass', 'required': sorted(present), 'absent': sorted(absent)}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, cases))
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print('PASS: %d static positive and near-miss controls' % len(results))
