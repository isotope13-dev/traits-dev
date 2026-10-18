#!/usr/bin/env python3
"""Exercise source/transport roles and renamed native controls without execution."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--samples-dir', type=Path, required=True)
parser.add_argument('--scratch-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
managed = (args.samples_dir / '9c12e5f78385/mitomzao.cc_hyber.exe').read_bytes()
packed = (args.samples_dir / '30bb1fd1244c/no-chrome-identity.exe').read_bytes()
rat = (args.samples_dir / '96c139caa475/2026-10-17_df4c25e653ac476f73e2bcc600e5f7c0_elex_wannacry').read_bytes()
input_post = 'objectives/exfiltration/stealer/input::managed-file-keylog-form-post-cooccurrence'
firefox = 'objectives/credential-access/browser/firefox::packed-firefox-nss-login-decryptor'
family = 'well-known/malware/stealer/cosmicduke::cosmicduke-builder-and-cipher-key'
self_delete = 'objectives/evasion/self-delete/file/script::stack-built-ping-self-delete-x86'
rat_delete = 'objectives/evasion/self-delete/file/script::wininet-office-self-delete-rat'
tasking = 'objectives/command-and-control/remote-command/tasking::native-http-binary-task-dispatch'
tracked = {input_post, firefox, family, self_delete, rat_delete, tasking}
retired = {
    'well-known/malware/stealer/cosmicduke::ssdt-space-kernel-helper',
    'well-known/malware/stealer/cosmicduke::cosmicduke-builder-and-helper',
    'objectives/evasion/self-delete/file/delay::stack-built-ping-self-delete-x86',
    'objectives/evasion/self-delete/file/delay::wininet-office-self-delete-rat',
}

def change(data, old, new):
    assert len(old) == len(new) and old in data, old
    return data.replace(old, new)

def replace_pattern(data, pattern, end_byte):
    match = re.search(pattern, data, re.DOTALL)
    assert match is not None, pattern
    result = bytearray(data)
    result[match.end() - 1] = end_byte
    return bytes(result)

def inert_pe(text):
    """Minimal PE with a RET entry point and inert reference strings."""
    content = b'\xc3' + text
    raw_size = (len(content) + 511) & ~511
    image = bytearray(512 + raw_size)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', image, optional, 0x10b)
    for offset, value in {4: raw_size, 16: 0x1000, 20: 0x1000, 28: 0x400000,
                          32: 0x1000, 36: 512, 56: 0x2000, 60: 512,
                          72: 0x100000, 76: 0x1000, 80: 0x100000, 84: 0x1000,
                          92: 16}.items():
        struct.pack_into('<I', image, optional + offset, value)
    struct.pack_into('<H', image, optional + 40, 5)
    struct.pack_into('<H', image, optional + 48, 5)
    struct.pack_into('<H', image, optional + 68, 3)
    section = optional + 224
    image[section:section + 8] = b'.text\0\0\0'
    struct.pack_into('<IIII', image, section + 8, len(content), 0x1000, raw_size, 512)
    struct.pack_into('<I', image, section + 36, 0x60000020)
    image[512:512 + len(content)] = content
    return bytes(image)

cases = [('managed-renamed-positive', managed, {input_post})]
for token in [b'ReadAllText', b'PostAsync', b'FormUrlEncodedContent', b'JavaScriptSerializer']:
    cases.append(('managed-without-' + token.decode(), change(managed, token, b'X' * len(token)), set()))
# Change the recognized loop shape; this ablation is not a benign verdict.
cases.append(('managed-without-polling-profile', replace_pattern(managed,
    rb'\x06\x20\xff\x00\x00\x00\xfe\x02\x16\xfe\x01\x0b\x07\x2d', 0x2c), set()))
cases += [
    ('packed-renamed-positive', packed, {firefox, family}),
    ('packed-without-nss', change(packed, b'NSS_Ini', b'XYZ_Ini'), {family}),
    ('packed-without-decrypt', change(packed, b'SDR_Decrypt', b'SDR_XXXXXXX'), {family}),
    ('packed-without-login-query', change(packed, b'select id, hostname, user', b'select id, hostname, xxxx'), {family}),
    ('packed-without-builder', change(packed, b'BotGenStudio', b'XXXXXXXXXXXX'), {firefox}),
    ('packed-without-key', change(packed, b'AdjustKernelTableFromSSDTSpace2', b'X' * len(b'AdjustKernelTableFromSSDTSpace2')), {firefox}),
]
handoff = rb'\x8b\x25....\x8b\x2d....\x8b\x0d....\x8b\x15....\x8b\x35....\x8b\x3d....\x8d\x05....\xff\xe0'
cases.append(('packed-without-concealed-tail-handoff', replace_pattern(packed, handoff, 0xd0), {family}))
cases.append(('inert-firefox-recovery-references', inert_pe(
    b'NSS_Init\0PK11SDR_Decrypt\0'
    b'select id, hostname, username, encryptedpassword from moz_logins\0'), set()))
cases.append(('inert-managed-http-references', inert_pe(
    b'ReadAllText\0PostAsync\0FormUrlEncodedContent\0JavaScriptSerializer\0keylog\0'), set()))
cases.append(('rat-renamed-positive', rat, {self_delete, rat_delete, tasking}))
# Keep each stack-store sequence but change del to dir. The native command
# launcher and own-path lookup alone must not retain the self-deletion claim.
match = re.search(rb'\xc6\x45.\x26\xc6\x45.\x64\xc6\x45.\x65\xc6\x45.\x6c', rat, re.DOTALL)
assert match is not None
modified = bytearray(rat)
modified[match.start() + 11] = ord('i')
modified[match.start() + 15] = ord('r')
cases.append(('rat-without-self-delete-command', bytes(modified), {tasking}))
# A different command-count bound must leave the recognized switch profile
# and its Office/self-delete derivative, while retaining deletion evidence.
# This shape test does not imply that the altered program is benign.
modified = change(rat, bytes.fromhex('05 18 FC FF FF 83 F8 13'), bytes.fromhex('05 18 FC FF FF 83 F8 12'))
cases.append(('rat-outside-known-task-switch', modified, {self_delete}))

with tempfile.TemporaryDirectory(prefix='reasoned-native-controls-', dir=args.scratch_dir) as temporary:
    def run(case):
        name, data, expected = case
        path = Path(temporary, name + '.exe')
        path.write_bytes(data)
        proc = subprocess.run([args.cleave, '--traits-dir', str(repo), str(path), '--format', 'json'], capture_output=True, text=True)
        assert proc.returncode == 0 and proc.stdout, (name, proc.stderr)
        report = json.loads(proc.stdout)
        ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
        assert not ids & retired, (name, ids & retired)
        assert ids & tracked == expected, (name, ids & tracked, expected)
        if name.startswith('inert-'):
            high = [t for f in report['files'] for t in f.get('traits', []) if t['crit'] >= 4]
            assert not any(t['crit'] == 5 for t in high), (name, high)
            assert len(high) <= 1, (name, high)
        return name + ': PASS'
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(run, cases):
            print(result, flush=True)
