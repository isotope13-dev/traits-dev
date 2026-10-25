#!/usr/bin/env python3
"""Static controls for packer output and the symbol-placement corrections.

All generated files have inert RET code. No supplied executable is run.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch-dir', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
args.scratch_dir.mkdir(parents=True, exist_ok=True)


def pe(section, payload, machine=0x14c):
    raw_size = (len(payload) + 511) & ~511
    data = bytearray(512 + raw_size)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, machine, 1, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', data, optional, 0x10b)
    for position, value in {4: raw_size, 16: 0x1000, 20: 0x1000,
                            28: 0x400000, 32: 0x1000, 36: 512,
                            56: 0x2000, 60: 512, 92: 16}.items():
        struct.pack_into('<I', data, optional + position, value)
    struct.pack_into('<H', data, optional + 68, 3)
    struct.pack_into('<8sIIIIIIHHI', data, optional + 224, section,
                     len(payload), 0x1000, raw_size, 512, 0, 0, 0, 0, 0x60000020)
    data[512:512 + len(payload)] = payload
    return data


def elf(symbol, name_in_code=None, pclntab=None):
    """A small ELF with a real function symbol, or an unbound name string."""
    names = b'\0.text\0.strtab\0.symtab\0.shstrtab\0.gopclntab\0'
    text = b'\xc3\0' + (name_in_code or b'')
    strings = b'\0' + symbol + b'\0'
    symbols = bytes(24) + struct.pack('<IBBHQQ', 1, 0x12, 0, 1, 0x400100, 1)
    contents = [text, strings, symbols, names, pclntab or b'']
    data = bytearray(0x100)
    offsets = []
    for content in contents:
        offsets.append(len(data))
        data.extend(content)
        data.extend(bytes((-len(data)) % 8))
    shoff = len(data)
    headers = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
               (1, 1, 6, 0x400100, offsets[0], len(text), 0, 0, 16, 0),
               (7, 3, 0, 0, offsets[1], len(strings), 0, 0, 1, 0),
               (15, 2, 0, 0, offsets[2], len(symbols), 2, 1, 8, 24),
               (23, 3, 0, 0, offsets[3], len(names), 0, 0, 1, 0)]
    if pclntab is not None:
        headers.append((33, 1, 0, 0, offsets[4], len(contents[4]), 0, 0, 1, 0))
    for h in headers:
        data.extend(struct.pack('<IIQQQQIIQQ', *h))
    ident = b'\x7fELF\x02\x01\x01' + bytes(9)
    struct.pack_into('<16sHHIQQQIHHHHHH', data, 0, ident, 2, 62, 1,
                     0x400100, 0, shoff, 0, 64, 56, 0, 64, len(headers), 4)
    return data


stub = bytes.fromhex('60 e8 03 00 00 00 e9 eb 04 5d 45 55 c3 e8 01 00 00 00 '
                     'eb 5d bb ed ff ff ff 03 dd 81 eb 00 90 00 00')
packer = 'metadata/build/protector::aspack-x86-unpacking-stub'
name = 'metadata/binary/symbols/name/token::dotnet-processstartinfo-name'
go = 'micro-behaviors/process/create/spawn::go-cmd-start-method-symbol'
combined = 'micro-behaviors/process/create/subprocess::go-cmd-start-symbol'
pclntab_name = 'metadata/binary/symbols/name::go-cmd-start-pclntab'
retired = {'metadata/binary/symbols/descriptor::dotnet-processstartinfo-name',
           'metadata/binary/symbols/name::go-cmd-start-symbol'}
# The metadata fingerprint intentionally says only that these instruction
# bytes exist in the packer section, even in an inert control.
cases = [
    ('aspack-sequence.exe', pe(b'.aspack', b'\xc3' + stub), {packer}, set()),
    ('aspack-reference.exe', pe(b'.aspack', b'\xc3ASPack\0'), set(), {packer}),
    ('aspack-broken-getpc.exe', pe(b'.aspack', b'\xc3' + stub.replace(b'\x5d\x45', b'\x5d\x46')),
     set(), {packer}),
    ('aspack-other-section.exe', pe(b'.text', b'\xc3' + stub), set(), {packer}),
    ('aspack-other-arch.exe', pe(b'.aspack', b'\xc3' + stub, machine=0x1c4),
     set(), {packer}),
    ('process-type.exe', pe(b'.text', b'\xc3\0ProcessStartInfo\0'), {name}, set()),
    ('process-type-absent.exe', pe(b'.text', b'\xc3\0ProcessStartInfX\0'), set(), {name}),
    ('process-type-other-section.exe', pe(b'.rdata', b'\xc3\0ProcessStartInfo\0'),
     set(), {name}),
    ('go-start-symbol.elf', elf(b'os/exec.(*Cmd).Start'), {go}, set()),
    ('go-start-string.elf', elf(b'ordinary', b'os/exec.(*Cmd).Start\0'),
     set(), {go, combined}),
    ('go-start-near-symbol.elf', elf(b'os/exec.(*Cmd).StartProcess'),
     set(), {go, combined}),
    ('go-start-pclntab.elf', elf(b'ordinary', pclntab=b'os/exec.(*Cmd).Start\0'),
     {pclntab_name}, {go}),
]
for filename, content, _, _ in cases:
    (args.scratch_dir / filename).write_bytes(content)
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                         *[str(args.scratch_dir / name) for name, *_ in cases]],
                        capture_output=True, text=True, check=True)
reports = {}
remaining = result.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.update({Path(f['path']).name: f for f in report['files']})
    remaining = remaining[end:].lstrip()
for filename, _, required, forbidden in cases:
    traits = {t['id']: t for t in reports[filename]['traits']}
    assert required <= traits.keys(), (filename, 'missing', required - traits.keys())
    assert not (forbidden | retired) & traits.keys(), (filename, 'unexpected',
                                                     (forbidden | retired) & traits.keys())
    for tid in required:
        assert traits[tid]['crit'] == 3, (filename, tid, traits[tid]['crit'])
    assert not [t for t in traits.values() if t['crit'] >= 4], filename
    print('PASS', filename)

# The existing any-only Go umbrella is evaluated for consumers but omitted
# from rendered findings. Check its internal truth value as well as the atoms.
for filename, expected in [('go-start-symbol.elf', True),
                           ('go-start-pclntab.elf', True),
                           ('go-start-string.elf', False),
                           ('go-start-near-symbol.elf', False)]:
    probe = subprocess.run([args.cleave, '--traits-dir', str(root), 'test-rules',
                            str(args.scratch_dir / filename), '--rules', combined],
                           capture_output=True, text=True, check=True)
    assert ('\nMATCHED ' + combined in probe.stdout) == expected, (filename, probe.stdout)
    print('PASS internal Go umbrella', filename)
