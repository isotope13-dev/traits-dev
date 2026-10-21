"""Source-bound wallet regression and direction-neutral native XOR controls."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('stage', type=Path)
parser.add_argument('--native', type=Path)
args = parser.parse_args()
args.stage.mkdir(parents=True, exist_ok=True)
WALLET = 'objectives/exfiltration/stealer/wallet::wallet-input-telemetry-http-exfiltration'
NUMERIC = 'objectives/anti-static/obfuscation/string/charcode-url::js-numeric-endpoint-json-post'
GENERIC = 'micro-behaviors/data/property/access::value-alias-timer-reporting-call'
XOR = 'micro-behaviors/data/encoding/xor::x86-padded-register-stride-dword-xor-loop'

original = ROOT / 'testdata/triage/registry-conviction-review/wallet-export.xpi'
with zipfile.ZipFile(original) as z:
    members = {n: z.read(n).decode() for n in z.namelist()}

for name, wired in [('detached.xpi', False), ('wired.xpi', True), ('renamed.xpi', True)]:
    current = dict(members)
    if wired:
        manifest = json.loads(current['manifest.json'])
        manifest['browser_action'] = {'default_popup': 'form.html'}
        current['manifest.json'] = json.dumps(manifest)
        current['form.html'] = current['form.html'].replace('</body>',
            '<script src="sender.js"></script><script src="entry.js"></script></body>')
        current['entry.js'] += '\ndocument.querySelector("input").addEventListener("input", e => onInput(e.target));\n'
    if name == 'renamed.xpi':
        current = {n: s.replace('collectMetrics', 'reportPayload').replace('entered', 'captured').replace('onInput', 'handleEdit')
                   for n, s in current.items()}
    with zipfile.ZipFile(args.stage / name, 'w') as z:
        for n, s in current.items():
            z.writestr(n, s)

# A minimal PE whose entry returns; the uncalled transform fragment is only a
# capability fixture. Change keys/padding, then remove the memory XOR entirely.
def pe(code):
    b = bytearray(1024)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 1, 0, 0, 0, 0xe0, 0x102)
    o = 0x98
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<III', b, o + 16, 0x1000, 0x1000, 0)
    struct.pack_into('<III', b, o + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', b, o + 56, 0x2000, 0x200)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<I', b, o + 92, 16)
    s = o + 0xe0
    b[s:s+8] = b'.text\0\0\0'
    struct.pack_into('<IIII', b, s+8, 0x200, 0x1000, 0x200, 0x200)
    struct.pack_into('<I', b, s+36, 0x60000020)
    b[0x200:0x201] = b'\xc3'
    b[0x210:0x210+len(code)] = code
    return b

for name, key, padding, operation in [('xor-a.exe', 0x12345678, 1, b'\x31\x30'),
                                      ('xor-b.exe', 0xfedcba98, 4, b'\x31\x30'),
                                      ('zero-register.exe', 0x12345678, 1, b'\x31\xc0')]:
    code = b'\xbe' + struct.pack('<I', key) + b'\x90'*padding + operation + b'\x90'*padding + b'\x01\xf8' + b'\x90'*padding
    code += b'\xe2' + bytes([(-(len(code)-5+2)) & 255])
    (args.stage / name).write_bytes(pe(code))
    if name == 'xor-a.exe':
        (args.stage / 'forward-branch.exe').write_bytes(pe(code[:-1] + b'\x01'))

paths = sorted(args.stage.glob('*.xpi')) + sorted(args.stage.glob('*.exe'))
paths += [ROOT / 'testdata/hostile/wallet-seed-clipboard-extension.xpi',
          ROOT / 'testdata/hostile/wallet-seed-clipboard-extension-evasive.xpi']
real_wallets = paths[-2:]
FAMILY = 'well-known/malware/backdoor/padodor::berbew-karton-card-phishing-backdoor'
if args.native:
    native = args.native.read_bytes()
    renamed = bytearray(native)
    # Locate the section table with its standard COFF fields.
    coff = struct.unpack_from('<I', native, 0x3c)[0] + 4
    table = coff + 20 + struct.unpack_from('<H', native, coff+16)[0]
    count = struct.unpack_from('<H', native, coff+2)[0]
    for offset in range(table, table + count*40, 40):
        if native[offset:offset+8].rstrip(b'\0') == b'.tls':
            renamed[offset:offset+8] = b'.data\0\0\0'
    (args.stage/'karton-data.exe').write_bytes(renamed)
    # Preserve phishing/persistence but remove the required protocol marker.
    key = struct.pack('<I', 0x4419106c)
    old = b'X-okRecv11'
    encoded = bytes(c ^ key[(0x9c7e-0x7400+i)%4] for i,c in enumerate(old))
    assert native.count(encoded) == 1
    (args.stage/'karton-no-receiver.exe').write_bytes(native.replace(encoded, bytes(len(encoded))))
    paths += [args.native, args.stage/'karton-data.exe', args.stage/'karton-no-receiver.exe']
r = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json', *map(str, paths)],
                   check=True, capture_output=True, text=True)
s = r.stdout.strip()
reports = {}
decoder = json.JSONDecoder()
while s:
    report, n = decoder.raw_decode(s)
    s = s[n:].strip()
    for f in report['files']:
        reports[f['path']] = {t['id'] for t in f.get('traits', [])}

def has(name, trait):
    return trait in reports[str(args.stage / name)]

assert not has('detached.xpi', WALLET)
assert has('detached.xpi', NUMERIC) and has('detached.xpi', GENERIC)
for name in ['wired.xpi', 'renamed.xpi']:
    assert has(name, WALLET), name
for name in ['xor-a.exe', 'xor-b.exe']:
    assert has(name, XOR), name
assert not has('zero-register.exe', XOR)
assert not has('forward-branch.exe', XOR)
for p in real_wallets:
    assert WALLET in reports[str(p)], p
if args.native:
    assert FAMILY in reports[str(args.native)]
    assert has('karton-data.exe', FAMILY)
    assert not has('karton-no-receiver.exe', FAMILY)
    assert has('karton-no-receiver.exe', 'objectives/credential-access/financial/credit-card::pe-card-verification-phish')
    assert has('karton-no-receiver.exe', 'objectives/persistence/login/registry/autostart::pin-lure-shellservice-autoload')
    print('3 native identity controls pass: original .tls, renamed .data, removed receiver marker')
print('9 controls pass: detached, wired, renamed, two real stealers, two XOR keys, register-only and forward-branch near misses')
