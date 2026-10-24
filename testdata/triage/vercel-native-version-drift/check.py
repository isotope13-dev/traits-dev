#!/usr/bin/env python3
"""Generate inert format controls in scratch; never execute fixture bytes."""
import ast
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(sys.argv[1]).resolve()
DEST.mkdir(parents=True, exist_ok=True)
CPU = 'micro-behaviors/os/sysinfo/cpu::genuineintel-vendor-word-comparison'
HTTP = 'micro-behaviors/communications/http/message::'
ELECTRON = 'well-known/lib/runtime/scripted/electron::'
NODE = 'well-known/lib/runtime/scripted/node-runtime::nodejs-webstorage-marker'
VM = 'objectives/anti-analysis/vm-detect/instruction::x64-cpuid-hypervisor-bit-vendor-gate'
OLD = 'objectives/anti-analysis/vm-detect/instruction::stripped-elf-cpuid-vendor-check'
PROTO = 'metadata/build/artifact::protobuf-generated-schema-header'


def elf(code=b'\xc3', data=b'', large=False, malformed=False):
    # One load segment, separate code/read-only-data section facts, no symbols.
    shoff = max(0x600, 0x400 + len(data))
    if large:
        shoff = max(shoff, 0x110000)
    shoff = (shoff + 7) & ~7
    buf = bytearray(shoff + 4 * 64)
    ident = b'\x7fELF\x02\x01\x01' + bytes(9)
    struct.pack_into('<16sHHIQQQIHHHHHH', buf, 0, ident, 2, 62, 1,
                     0x400200, 64, shoff, 0, 64, 56, 1, 64, 4, 3)
    struct.pack_into('<IIQQQQQQ', buf, 64, 1, 5, 0, 0x400000, 0x400000,
                     len(buf), len(buf), 4096)
    buf[0x200:0x200 + len(code)] = code
    buf[0x400:0x400 + len(data)] = data
    names = b'\0.text\0.rodata\0.shstrtab\0'
    buf[0x180:0x180 + len(names)] = names
    for i, fields in enumerate([
        (1, 1, 6, 0x400200, 0x200, len(code)),
        (7, 1, 2, 0x400400, 0x400, shoff - 0x400),
        (15, 3, 0, 0, 0x180, len(names)),
    ], 1):
        struct.pack_into('<IIQQQQIIQQ', buf, shoff + i * 64,
                         *fields, 0, 0, 1, 0)
    if malformed:
        struct.pack_into('<Q', buf, 40, len(buf) + 4096)
    return buf


# Reuse the repository's established inert PE builder, without invoking tests.
module = ast.parse((ROOT / 'testdata/taxonomy/byte-transform-bounds/check.py').read_text())
ns = {'struct': struct}
exec(compile(ast.Module(body=[n for n in module.body
                             if isinstance(n, ast.FunctionDef) and n.name == 'image'],
                        type_ignores=[]), '<fixture-builder>', 'exec'), ns)
pe = ns['image']
vendor = bytes.fromhex('B8 00 00 00 00 0F A2 81 FB 47 65 6E 75 75 17 '
                       '81 FA 69 6E 65 49 75 0F 81 F9 6E 74 65 6C C3')
v8 = b'v8::Isolate\0v8_enable_pointer_compression\0'
gate = bytes.fromhex('B8 01 00 00 00 33 C9 0F A2 89 44 24 30 89 5C 24 34 '
                     '89 54 24 3C 85 C9 78 07 33 FF E9 00 00 00 00 '
                     'B8 00 00 00 40 33 C9 0F A2')
cases = [
    ('intel-vendor.elf', elf(vendor), {CPU}, {OLD}),
    ('intel-vendor-malformed.elf', elf(vendor, malformed=True), {CPU}, {OLD}),
    ('vendor-near-miss.elf', elf(vendor.replace(b'ntel', b'xxxx')), set(), {CPU, OLD}),
    ('node-http-example.elf', elf(data=b"firstLine in the case of request is: 'GET /index.html HTTP/1.1\0"),
     {HTTP + 'node-http-example-request-line', HTTP + 'generic-index-request-line-raw',
      }, set()),
    ('fetch-example.elf', elf(data=b'must send HTTP headers (e.g., "POST / HTTP/1.1")\0'),
     {HTTP + 'fetch-header-example-request-line'}, set()),
    ('http-near-miss.elf', elf(data=b'GETTING /index.html HTTP/1.1\0'),
     set(), {HTTP + 'generic-index-request-line-raw'}),
    ('generated-schema.elf', elf(data=b'// @generated from file rpc/v1/service.proto (package example.rpc.v1, syntax proto3)\0'),
     {PROTO}, set()),
    ('schema-without-generation.elf', elf(data=b'// file rpc/v1/service.proto (package example.rpc.v1, syntax proto3)\0'),
     set(), {PROTO}),
    ('node-v8-webstorage.elf', elf(data=v8 + b'nodejs_webstorage\0', large=True),
     {NODE}, {ELECTRON + 'electron-app-runtime', ELECTRON + 'electron-chromium-runtime-strong'}),
    ('chromium-v8-mojo.elf', elf(data=v8 + b'network.mojom.NetworkService\0', large=True),
     {ELECTRON + 'electron-chromium-runtime-strong'}, set()),
    ('chromium-policy-mojo.elf', elf(data=b'chrome_policy\0network.mojom.NetworkService\0', large=True),
     {ELECTRON + 'electron-chromium-runtime-strong'}, set()),
    ('electron-v8.elf', elf(data=v8 + b'electron_node\0', large=True),
     {ELECTRON + 'electron-chromium-runtime-strong'}, set()),
    ('real-hypervisor-gate.exe', pe(gate), {VM}, set()),
    ('ordinary-cpuid-leaf.exe', pe(gate.replace(bytes.fromhex('B8 00 00 00 40'),
                                              bytes.fromhex('B8 00 00 00 00'))), set(), {VM}),
    ('hypervisor-bytes-in-data.exe', pe(b'\xc3', gate), set(), {VM}),
]
paths = []
for name, contents, _, _ in cases:
    path = DEST / name
    path.write_bytes(contents)
    paths.append(path)
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                         '--format', 'json', *map(str, paths)], capture_output=True, text=True)
(DEST / 'stderr.txt').write_text(result.stderr)
(DEST / 'reports.json').write_text(result.stdout)
assert result.returncode == 0, result.stderr
remaining, files = result.stdout, []
while remaining.strip():
    obj, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files.extend(obj['files'])
for (name, _, required, forbidden), path in zip(cases, paths):
    traits = {t['id']: t['crit'] for f in files if f['path'] == str(path)
              for t in f.get('traits', [])}
    assert required <= traits.keys(), (name, 'missing', required - traits.keys())
    assert not forbidden & traits.keys(), (name, 'unexpected', forbidden & traits.keys())
    if CPU in traits:
        assert traits[CPU] == 3, (name, traits[CPU])
    print('PASS ' + name)
