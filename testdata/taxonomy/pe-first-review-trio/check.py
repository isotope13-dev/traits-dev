#!/usr/bin/env python3
"""Independent PE/header, reference-only, and native-code near-miss controls."""
import argparse
import json
from pathlib import Path
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]

def align(n, a):
    return (n + a - 1) // a * a

def pe(name, content=b'\xc3', section='.text', nt=0x80, size=0):
    headers = align(nt + 24 + 224 + 40, 512)
    rva = align(headers, 4096)
    rawlen = align(max(len(content), 512), 512)
    data = bytearray(max(size, headers + rawlen))
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, nt)
    # Nonzero DOS-stub bytes at the old matcher's erroneous offset.
    data[0x7a:0x7e] = b'ABCD'
    data[nt:nt+4] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, nt+4, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = nt + 24
    struct.pack_into('<H', data, opt, 0x10b)
    for off, value in {4: rawlen, 16: rva, 20: rva, 28: 0x400000,
                       32: 4096, 36: 512, 56: rva+align(rawlen, 4096),
                       60: headers, 72: 0x100000, 76: 4096,
                       80: 0x100000, 84: 4096, 92: 16}.items():
        struct.pack_into('<I', data, opt+off, value)
    struct.pack_into('<H', data, opt+40, 4)
    struct.pack_into('<H', data, opt+48, 4)
    struct.pack_into('<H', data, opt+68, 2)
    sec = opt+224
    data[sec:sec+8] = section.encode().ljust(8, b'\0')
    struct.pack_into('<IIII', data, sec+8, len(content), rva, rawlen, headers)
    struct.pack_into('<I', data, sec+36, 0x60000020)
    data[headers:headers+len(content)] = content
    (args.output / name).write_bytes(data)

H = 'metadata/binary/header/malformed::pe-header-offset-high'
B = 'micro-behaviors/data/buffer/record::x86-helper-result-indexed-byte-store'
P = 'micro-behaviors/fs/path/self::vb6-app-executable-path-profile'
R = 'micro-behaviors/fs/file/rename::cmd-target-die-extension-rename'
U = 'micro-behaviors/communications/http/user-agent::navigator-useragent-substring-branch'
E = 'metadata/binary/section/header::entry-in-upx0'
C = 'metadata/binary/section/label::c2r-section-name'
pe('ordinary-stub.exe')
pe('high-header.exe', nt=0x10000)
store = bytes.fromhex('50 ff 15 10 20 40 00 8b 55 dc 8b 4a 0c 8b 95 0c ff ff ff 88 04 11')
pe('byte-store.exe', store+b'\xc3')
pe('word-store.exe', store[:-3]+b'\x89\x04\x11\xc3')
pe('data-store.exe', store, section='.rdata')
app = bytes.fromhex('79 4f ad 33 99 66 cf 11 b7 0c 00 aa 00 60 d3 93')
methods = bytes.fromhex('ff 52 50 db e2')+b'\x90'*233+bytes.fromhex('ff 52 58 db e2')
pe('app-methods.exe', app+methods+b'\0'+'.exe'.encode('utf-16le')+b'\0\0')
pe('unrelated-methods.exe', app+methods.replace(b'\xff\x52\x58',b'\xff\x52\x60')+b'\0'+'.exe'.encode('utf-16le')+b'\0\0')
cmd = 'cmd /c rename "'.encode('utf-16le')+b'\0\0'
pe('near-rename.exe', cmd+'.die'.encode('utf-16le')+b'\0\0')
pe('far-rename.exe', cmd+b'\0'*2048+'.die'.encode('utf-16le')+b'\0\0')
pe('upx-entry.exe', section='UPX0')
pe('damaged-command.exe', bytes(c if i % 2 == 0 else 0x81 for i, c in enumerate(cmd)))
refs = [b'Software\\Adobe\\CommonFiles\\Usage', b'SOFTWARE\\Policies\\Adobe\\APIP',
        b'HLLog.config', b'User-Agent: Adobe Log Transport', b'perfboost.pdb',
        b'LZMA_ELF00', b'ELFMAINX', b'ELFMAINZ']
pe('references-only.exe', b'\xc3\0'+b'\0'.join(refs)+b'\0', section='.c2r', size=2500000)
for name, source in {
    'includes.js': 'if (navigator.userAgent.includes("Windows")) display();',
    'indexof.js': 'if (navigator.userAgent.indexOf("Windows")) display();',
    'unrelated.js': 'if (userAgent.includes("Windows")) display();',
}.items():
    (args.output/name).write_text(source)
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                         str(args.output)], capture_output=True, text=True, check=True)
(args.output.parent/'controls-result.json').write_text(result.stdout)
# Directory JSON mode streams adjacent report objects without delimiters.
files = []
decoder = json.JSONDecoder()
remaining = result.stdout
while remaining.strip():
    doc, consumed = decoder.raw_decode(remaining.lstrip())
    files.extend(doc['files'])
    remaining = remaining.lstrip()[consumed:]
found = {}
for f in files:
    ts = f.get('traits', f.get('findings', []))
    found[Path(f['path']).name] = {t['id'] for t in ts}
    assert not any(t.get('crit') in (5, 'hostile') for t in ts), f['path']
cases = {
 'ordinary-stub.exe': ([], [H]), 'high-header.exe': ([H], []),
 'byte-store.exe': ([B], []), 'word-store.exe': ([], [B]), 'data-store.exe': ([], [B]),
 'app-methods.exe': ([P], []), 'unrelated-methods.exe': ([], [P]),
 'near-rename.exe': ([R], []), 'far-rename.exe': ([], [R]),
 'upx-entry.exe': ([E], []),
 'damaged-command.exe': ([], ['micro-behaviors/fs/file/rename::utf16-cmd-rename-quoted-target']),
 'references-only.exe': ([C, 'metadata/binary/debug::perfboost-pdb-reference',
   'micro-behaviors/os/registry/keys/product::adobe-usage-registry-key',
   'micro-behaviors/os/registry/keys/policy::adobe-apip-policy-key',
   'micro-behaviors/fs/path/config/app::adobe-hllog-config',
   'micro-behaviors/communications/http/user-agent::adobe-logtransport-user-agent',
   *['metadata/build/protector::'+s for s in
     ['upx-lzma-elf32-stub-name','upx-elfmainx-stub-name','upx-elfmainz-stub-name']]], []),
 'includes.js': ([U], []), 'indexof.js': ([U], []), 'unrelated.js': ([], [U]),
}
for name, (yes, no) in cases.items():
    assert name in found, ('missing file', name, list(found))
    assert set(yes) <= found[name], (name, 'missing', set(yes)-found[name])
    assert not set(no) & found[name], (name, 'unexpected', set(no)&found[name])
print(f'PASS: {len(cases)} controls; relocated references, header offsets, byte stores, method pairs, proximity, and substring spellings')
