#!/usr/bin/env python3
"""Static controls for API references versus execution, and Wi-Fi label bounds."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument('--cleave', default='cleave')
ap.add_argument('--sample', type=Path, action='append', default=[])
args = ap.parse_args()
root = Path(__file__).resolve().parents[3]
reflection = 'micro-behaviors/metaprogramming/reflection::'
clr = 'micro-behaviors/process/interpreter/runtime/clr::'
load = 'micro-behaviors/os/module/load::'
encoding = 'metadata/file/encoding::'
wifi = 'objectives/credential-access/wifi::'
main = reflection + 'dotnet-load-invoke-api-references'
callbyname = reflection + 'dotnet-appdomain-callbyname-references'
lateget = reflection + 'dotnet-appdomain-lateget-references'
activator = reflection + 'dotnet-appdomain-activator-references'
access = clr + 'appdomain-accessor-references'
variants = load + 'dotnet-load-member-name-variants'
rev = encoding + 'reversed-load-member-text'
b64 = encoding + 'base64-load-member-text'
create = encoding + 'base64-create-instance-member-text'
label = wifi + 'netsh-wlan-key-content-parse'
old = 'objectives/anti-static/obfuscation/reflection/invoke::'
retired = {old + x for x in (
    'dotnet-assembly-load-invoke', 'dotnet-appdomain-callbyname-load',
    'dotnet-appdomain-lateget-load', 'dotnet-appdomain-activator-load',
    'dotnet-appdomain-access', 'dotnet-assembly-load-token',
    'dotnet-reversed-assembly-load-token', 'dotnet-base64-assembly-load-token',
    'dotnet-base64-create-instance-token')}


def pe(content):
    """Inert PE with a RET entry; marker strings are data, never executed."""
    size = (len(content) + 641) // 512 * 512
    image = bytearray(512 + size)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', image, opt, 0x10b)
    for offset, value in {4: size, 16: 4224, 20: 4096, 28: 0x400000,
                          32: 4096, 36: 512, 56: 4096 + ((size+4095)//4096)*4096,
                          60: 512, 92: 16}.items():
        struct.pack_into('<I', image, opt + offset, value)
    struct.pack_into('<H', image, opt + 68, 2)
    section = opt + 224
    image[section:section+8] = b'.text\0\0\0'
    struct.pack_into('<IIII', image, section+8, size, 4096, size, 512)
    struct.pack_into('<I', image, section+36, 0x60000020)
    # Minimal CLR header and metadata version, with no executable managed body.
    struct.pack_into('<II', image, opt + 96 + 14*8, 4096, 72)
    struct.pack_into('<IHHII', image, 512, 72, 2, 5, 4176, 32)
    struct.pack_into('<IHHII', image, 592, 0x424a5342, 1, 1, 0, 12)
    image[608:620] = b'v4.0.30319\0\0'
    image[640] = 0xc3
    image[642:642+len(content)] = content
    return image


markers = [b'BSJB', b'System.Reflection', b'Assembly.Load', b'MethodBase',
           b'Invoke', b'GetTypes', b'AppDomain', b'get_CurrentDomain', b'Load',
           b'CallByName', b'GetExportedTypes', b'Activator', b'LateGet', b'CreateInstance']
base = b'\0'.join(markers) + b'\0'
all_refs = {main, callbyname, lateget, activator, access, variants}
cases = [('references-only', base, all_refs, set()),
         ('no-invocation', base.replace(b'Invoke\0', b'Absent\0'),
          all_refs - {main}, {main}),
         ('no-late-binding', base.replace(b'CallByName\0', b'Absent\0').replace(b'LateGet\0', b'Absent\0'),
          {main, activator, access, variants}, {callbyname, lateget}),
         ('no-domain-access', base.replace(b'get_CurrentDomain\0', b'Absent\0'),
          {main, variants}, {callbyname, lateget, activator, access}),
         ('reversed-name', b'daoL\0', {rev, variants}, {main, callbyname, lateget, activator}),
         ('base64-name', 'TG9hZA==\0'.encode('utf-16le'), {b64, variants}, {main, callbyname, lateget, activator}),
         ('base64-create', 'Q3JlYXRlSW5zdGFuY2U=\0'.encode('utf-16le'), {create}, {main, callbyname, lateget, activator}),
         ('no-name', b'OtherName\0', set(), {rev, b64, create, variants}),
         ('catalog-near-miss', b'ContainsKey ContentLength\0', set(), {label}),
         ('english-label', b'Key Content\0', {label}, set()),
         ('arabic-label', 'محتوى المفتاح\0'.encode('utf-16le'), {label}, set()),
         ('netsh-key-output', b'netsh wlan show profile name=example key=clear\0Key Content\0',
          {label, wifi + 'native-netsh-wifi-password-harvest'}, set())]
with tempfile.TemporaryDirectory(prefix='reference-controls-') as td:
    paths = []
    expectations = {}
    for name, content, required, forbidden in cases:
        if name in {'base64-name', 'base64-create', 'reversed-name'}:
            path = Path(td) / (name + '.cs')
            path.write_text(content.decode('utf-16le').rstrip('\0') if name != 'reversed-name' else 'daoL')
        elif name == 'arabic-label':
            path = Path(td) / (name + '.py')
            path.write_text('print("محتوى المفتاح")\n')
        else:
            path = Path(td) / (name + '.exe')
            path.write_bytes(pe(content))
        paths.append(path)
        # Bare-any grouping composites and unused components are omitted by
        # the terminal/report projection; test their match state separately.
        expectations[str(path)] = (required - {access, variants, rev}, forbidden | retired)
    cp = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                         str(Path(td))], capture_output=True, text=True)
    if cp.returncode:
        raise RuntimeError(cp.stderr + cp.stdout[:1000])
    reports = []
    remaining = cp.stdout.lstrip()
    decoder = json.JSONDecoder()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    for f in [f for report in reports for f in report['files']]:
        if f['path'] not in expectations:
            continue
        required, forbidden = expectations.pop(f['path'])
        traits = {t['id']: t for t in f.get('traits', [])}
        assert required <= traits.keys(), (f['path'], 'missing', required - traits.keys())
        assert not forbidden & traits.keys(), (f['path'], 'unexpected', forbidden & traits.keys())
        for t in f.get('traits', []):
            if t['id'] in (all_refs - {variants}) | {b64, create}:
                assert t['crit'] == 3, (t['id'], t['crit'])
    assert not expectations, expectations
    cp = subprocess.run([args.cleave, '--traits-dir', str(root), 'test-rules',
                         str(Path(td) / 'reversed-name.cs'), '--rules', rev], capture_output=True, text=True, check=True)
    assert 'Summary: 1 matched, 0 not matched' in cp.stdout, cp.stdout
for path in args.sample:
    cp = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)],
                        capture_output=True, text=True, check=True)
    report = json.loads(cp.stdout)
    traits = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert {main, callbyname, lateget, activator} <= traits
    assert not (retired | {label}) & traits
    assert not [(f['path'], t['id']) for f in report['files'] for t in f.get('traits', []) if t['crit'] >= 4]
print(f'{len(cases)} controls and {len(args.sample)} package versions passed')
