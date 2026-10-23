#!/usr/bin/env python3
"""Static PE controls for native patching, payload decoding and KEM precision.
No fixture is executed. Supply an output directory within the analysis scratch.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
P = argparse.ArgumentParser()
P.add_argument('output', type=Path)
args = P.parse_args()
args.output.mkdir(parents=True, exist_ok=True)

def pe(code=b'', strings=b'', reloc=b'', imports=()):
    data = bytearray(0x1400)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 3, 0, 0, 0, 0xf0, 0x22)
    o = 0x98
    struct.pack_into('<H', data, o, 0x20b)
    struct.pack_into('<II', data, o+16, 0x1000, 0x1000)
    struct.pack_into('<Q', data, o+24, 0x140000000)
    struct.pack_into('<II', data, o+32, 0x1000, 0x200)
    struct.pack_into('<HH', data, o+40, 6, 0)
    struct.pack_into('<II', data, o+56, 0x4000, 0x400)
    struct.pack_into('<H', data, o+68, 3)
    struct.pack_into('<I', data, o+108, 16)
    # Text starts with RET; test instructions are inert observations after it.
    for i, (name, rva, ptr, size, flags) in enumerate([
        (b'.text', 0x1000, 0x400, 0x400, 0x60000020),
        (b'.rdata', 0x2000, 0x800, 0x600, 0x40000040),
        (b'.reloc', 0x3000, 0xe00, 0x600, 0x42000040),
    ]):
        pos = 0x188+i*40
        data[pos:pos+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', data, pos+8, size, rva, size, ptr)
        struct.pack_into('<I', data, pos+36, flags)
    data[0x400:0x404] = b'\xc3\x90\x90\x90'
    data[0x410:0x410+len(code)] = code
    rd = bytearray(0x600)
    if imports:
        struct.pack_into('<II', data, o+112+8, 0x2000, (len(imports)+1)*20)
    cur = 0x80
    for i, name in enumerate(imports):
        dll = b'USER32.dll' if name == 'GetSystemMetrics' else b'KERNEL32.dll'
        off_name = cur
        rd[cur:cur+len(dll)+1] = dll+b'\0'
        cur = (cur+len(dll)+8)&~7
        off_thunk = cur
        cur += 32
        off_hint = cur
        raw = b'\0\0'+name.encode()+b'\0'
        rd[cur:cur+len(raw)] = raw
        cur = (cur+len(raw)+8)&~7
        struct.pack_into('<IIIII', rd, i*20, 0x2000+off_thunk, 0, 0,
                         0x2000+off_name, 0x2000+off_thunk+16)
        struct.pack_into('<Q', rd, off_thunk, 0x2000+off_hint)
        struct.pack_into('<Q', rd, off_thunk+16, 0x2000+off_hint)
    rd[0x400:0x400+len(strings)] = strings
    data[0x800:0xe00] = rd
    data[0xe00:0xe00+len(reloc)] = reloc
    return bytes(data)

ETW = 'objectives/evasion/anti-av/blinding::native-etw-saved-byte-return-patch'
HIDE = 'objectives/anti-analysis/debugger-detect/thread-hide::native-thread-hide-class17-call-profile'
OBF = 'objectives/anti-static/obfuscation/encoding/hex::native-alphabetic-section-decoder'
GATE = 'objectives/anti-analysis/sandbox-detect/suite::native-concealed-payload-resource-rejection'
DEC = 'micro-behaviors/data/decode/hex::x64-a-p-nibble-decoder'
KEM = 'micro-behaviors/crypto/asymmetric/kem::kyber-encapsulation-terms--rx-2'
FNV = 'micro-behaviors/os/api-resolution/hash-based::x64-fnv1a-export-name-resolver'
STUB = 'micro-behaviors/os/syscall/raw::x64-build-indirect-syscall-stub'
MAP = 'micro-behaviors/process/deploy/image-map::x64-pe-tls-directory-entry-call'
patch = bytes.fromhex('0f b6 03 ba 01 00 00 00 88 47 08 48 8b cb c6 03 c3 44 8b 44 24 20')
hide = bytes.fromhex('45 33 c9 45 33 c0 ba 11 00 00 00 48 8b cb ff d0')
decode = bytes.fromhex('41 0f b6 01 44 8d 58 9f 41 80 fb 0f 77 00 83 fa ff 74 00 c1 e2 04 41 09 d3 49 39 ff 0f 84 00 00 00 00 44 88 1f')
cpu = bytes.fromhex('ff 15 00 00 00 00 83 7c 24 50 01 0f 86 00 00 00 00 ff 15 00 00 00 00 85 c0 74 00 48 81 7c 24 68 ff ff ff 5f')
screen = bytes.fromhex('81 fb 7f 02 00 00 41 0f 9e c0 3d df 01 00 00 0f 9e c0 41 08 c0 75 00')
fnv = bytes.fromhex('8b 46 20 45 31 c0 48 8d 1c 01 42 8b 0c 83 ba c5 9d 1c 81 31 c2 0f b6 01 69 d2 93 01 00 01 84 c0 75 00 41 39 d2 8b 46 24 4b 8d 14 41 0f b7 14 02 8b 46 1c')
stub = bytes.fromhex('c7 00 4c 8b d1 b8 89 48 04 66 c7 40 08 ff 25 c7 40 0a 00 00 00 00 48 89 50 0e')
words = (('abcdefghijklmnop '*8+'\n')*3).encode()
api = b'EtwEventWrite\0NtSetInformationThread\0'
imp = ('VirtualProtect', 'GetNativeSystemInfo', 'GetSystemMetrics')
cases = []

def case(name, content, required=(), forbidden=(), suffix='.exe'):
    path = args.output/(name+suffix)
    path.write_bytes(content)
    cases.append((path, set(required), set(forbidden)))

case('patch-and-hide', pe(patch+b'\x90'*16+hide, api, imports=imp), [ETW,HIDE], [OBF,GATE])
case('no-etw-target', pe(patch+hide, b'NtSetInformationThread\0', imports=imp), [HIDE], [ETW])
case('normal-byte-patch', pe(patch.replace(b'\xc6\x03\xc3', b'\xc6\x03\x90')+hide, api, imports=imp), [HIDE], [ETW])
case('other-thread-class', pe(patch+hide.replace(b'\xba\x11',b'\xba\x10'),api,imports=imp), [ETW], [HIDE])
case('no-thread-api', pe(hide, imports=imp), [], [HIDE,ETW])
case('no-protect-api', pe(patch,api), [], [ETW])
case('alphabetic-resource-gates', pe(decode+cpu+screen, reloc=words,imports=imp), [DEC,OBF,GATE], [ETW,HIDE])
case('data-without-decoder', pe(cpu+screen,reloc=words,imports=imp), [], [DEC,OBF,GATE])
case('decoder-without-data', pe(decode+cpu+screen,imports=imp), [DEC], [OBF,GATE])
case('wrong-digit-offset', pe(decode.replace(b'\x58\x9f',b'\x58\xa0')+cpu+screen,reloc=words,imports=imp), [], [DEC,OBF,GATE])
case('no-cpu-check', pe(decode+screen,reloc=words,imports=imp), [OBF], [GATE])
case('no-screen-check', pe(decode+cpu,reloc=words,imports=imp), [OBF], [GATE])
mapper = bytes.fromhex('41 8b 96 d4 00 00 00 41 8b 86 d0 00 00 00 85 d2 74 00 85 c0 0f 85 00 00 00 00 41 8b 46 28 48 01 f0 ff d0')
case('mapped-pe-entry', pe(mapper), [MAP])
case('unrelated-entry-field', pe(mapper.replace(b'\x46\x28', b'\x46\x2c')), [], [MAP])
case('fnv-export',pe(fnv),[FNV])
case('fnv-wrong-prime',pe(fnv.replace(bytes.fromhex('93 01 00 01'),bytes.fromhex('95 01 00 01'))),[],[FNV])
case('indirect-stub',pe(stub),[STUB])
case('plain-jump-stub',pe(stub.replace(bytes.fromhex('4c 8b d1 b8'),b'\x90'*4)),[],[STUB])
case('kem-routines',b'void OQS_KEM_decaps(void);\nvoid MLKEM768_decap(void);\nvoid crypto_kem_decapsulate(void);\nvoid kyber_decapsulate(void);\n',[KEM],suffix='.c')
case('random-alphabetic-word',pe(strings=b'kemigbmpokdecapj\0'),[],[KEM])
case('network-decapsulation',b'void vxlan_decapsulate(void);\nvoid gre_decapsulation(void);\n',[],[KEM],suffix='.c')
cmd = [os.environ.get('CLEAVE','cleave'),'--traits-dir',str(ROOT),'--format','jsonl']
r = subprocess.run(cmd+[str(p) for p,_,_ in cases],capture_output=True,text=True)
if r.returncode:
    raise SystemExit(r.stderr)
(args.output/'controls.after.jsonl').write_text(r.stdout)
reports = [json.loads(x) for x in r.stdout.splitlines() if x.strip()]
files = {str(Path(f['path']).resolve()): f for d in reports for f in d.get('files',[d])}
for p,required,forbidden in cases:
    ids={t['id'] for t in files[str(p.resolve())].get('traits',[])}
    assert required<=ids,(p.name,'missing',required-ids)
    assert not forbidden&ids,(p.name,'unexpected',forbidden&ids)
    print('PASS',p.name)
print(len(cases),'static controls passed')
