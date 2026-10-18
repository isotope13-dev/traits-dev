#!/usr/bin/env python3
"""Static positive/ablation/near-miss controls; never execute the specimens."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--samples-dir', type=Path, required=True)
parser.add_argument('--scratch-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
args.scratch_dir.mkdir(parents=True, exist_ok=True)
hive = (args.samples_dir / '1fd626505a13/globalhive.io_hyber.exe').read_bytes()
career = (args.samples_dir / '2fe8a179c1eb/careergpt.io_hyber.exe').read_bytes()
cyber = (args.samples_dir / '21c322408ed5/jaffacakes118_Trojan.Win32.Llac.kzfk.72ddaa203d426efbdfa10').read_bytes()
post = 'objectives/exfiltration/stealer/input::managed-file-keylog-form-post-cooccurrence'
firefox = 'objectives/credential-access/browser/firefox::native-signons-nss-injector-profile'
hook = 'micro-behaviors/ui/window/hook::windows-hook-key-translation-api-profile'
packed = 'micro-behaviors/crypto/decrypt::packed-nss-secret-decrypt-name-fragments'
vm = 'micro-behaviors/process/inject/remote-thread::unsigned-vboxservice-process-walk-api-profile'
resource = 'micro-behaviors/os/registry/manipulate::resource-shell-temp-run-key-api-profile'
allocation = 'micro-behaviors/mem/alloc/virtual::xor-decoded-virtual-alloc-api'
remote = 'micro-behaviors/process/inject/remote-thread::remote-thread-api-reference'
tracked = {post, firefox, hook, packed, vm, resource, allocation, remote}
retired = {
    'objectives/collection/keylog/hook::hook-to-ascii',
    'objectives/persistence/login/startup/registry::rsrc-temp-shellexec-run-key',
    'objectives/evasion/process/injection/runtime::unsigned-vm-aware-mutex-remote-thread-injector',
    'objectives/anti-static/obfuscation/decoders::xor-decoded-virtual-alloc-api',
    'micro-behaviors/process/inject/dll::create-remote-thread',
    'micro-behaviors/process/inject/runtime/call::create-remote-thread-dup',
}


def change(data, old, new):
    assert len(old) == len(new) and old in data, old
    return data.replace(old, new)


def inert_pe(text):
    """RET entry point plus inert data; enough structure to select PE rules."""
    content = b'\xc3' + text
    size = (len(content) + 511) & ~511
    data = bytearray(512 + size)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    for offset, value in {4: size, 16: 0x1000, 20: 0x1000, 28: 0x400000,
                          32: 0x1000, 36: 512, 56: 0x2000, 60: 512,
                          72: 0x100000, 76: 0x1000, 80: 0x100000, 84: 0x1000,
                          92: 16}.items():
        struct.pack_into('<I', data, opt + offset, value)
    for offset in (40, 48):
        struct.pack_into('<H', data, opt + offset, 5)
    struct.pack_into('<H', data, opt + 68, 3)
    section = opt + 224
    data[section:section + 8] = b'.text\0\0\0'
    struct.pack_into('<IIII', data, section + 8, len(content), 0x1000, size, 512)
    struct.pack_into('<I', data, section + 36, 0x60000020)
    data[512:512 + len(content)] = content
    return bytes(data)


managed_expected = {post, remote}
native_expected = {firefox, hook, vm, resource, allocation, remote}
cases = [
    ('managed-a-renamed', hive, managed_expected),
    ('managed-b-renamed', career, managed_expected),
    ('native-renamed', cyber, native_expected),
    ('plaintext-nss', inert_pe(b'NSS_Init\0PK11SDR_Decrypt\0'), set()),
    ('packed-nss-fragments', inert_pe(b'NSS_Ini\x01binary\x05SDR_Decrypt\0'), {packed}),
    ('unrelated-nss-prefix', inert_pe(b'NSS_Initial\0SDR_Decrypt\0'), set()),
    ('legacy-signons-alone', inert_pe(b'\\signons3.txt\0PK11SDR_Decrypt\0'), set()),
    ('managed-transport-alone', inert_pe(b'ReadAllText\0PostAsync\0FormUrlEncodedContent\0JavaScriptSerializer\0keylog\0'), set()),
]
for token in (b'ReadAllText', b'PostAsync', b'FormUrlEncodedContent', b'JavaScriptSerializer'):
    cases.append(('managed-without-' + token.decode(), change(hive, token, b'X' * len(token)), {remote}))
# Mutations test detection requirements, not the verdict of an altered program.
for name, token, absent in (
    ('nss', b'PK11SDR_Decrypt', {firefox}),
    ('signons', b'signons', {firefox}),
    ('translation', b'ToAscii', {hook}),
    ('guest-name', b'VBoxService.exe', {vm}),
    ('resource-lock', b'LockResource', {resource}),
):
    cases.append(('native-without-' + name, change(cyber, token, b'X' * len(token)), native_expected - absent))


def run(case):
    name, data, expected = case
    path = args.scratch_dir / (name + '.exe')
    path.write_bytes(data)
    proc = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json', str(path)], capture_output=True, text=True)
    assert proc.returncode == 0 and proc.stdout, (name, proc.stderr)
    report = json.loads(proc.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    actual = ids & tracked
    assert actual == expected, (name, actual, expected)
    assert not ids & retired, (name, ids & retired)
    return {'case': name, 'matched': sorted(actual), 'status': 'PASS'}


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, cases))
(args.scratch_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(result['case'] + ': PASS')
