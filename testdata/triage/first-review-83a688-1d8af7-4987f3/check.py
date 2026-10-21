"""Offline controls; never execute the specimens or generated PE images.

Usage: python3 check.py OUTER_SAMPLE GO_SAMPLE BENIGN_RESOLVER_DLL SCRATCH
Compile DependencyResolver.cs with a 128 KiB high-entropy embedded resource.
Requires pefile and cleave on PATH. All generated binaries stay in SCRATCH.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

import pefile

ROOT = Path(__file__).resolve().parents[3]
WRITER = 'micro-behaviors/os/registry/write::x86-stubpath-expand-string-write'
PERSIST = 'objectives/persistence/login/registry/autostart::flood-implant-active-setup-persistence'
COPY = 'objectives/persistence/login/registry/autostart::active-setup-self-copy-dll-injector'
FAMILY = 'well-known/malware/rat/gravityrat::gravityrat-gx-managed-rat'
RETIRED = {
    'objectives/command-and-control/dropper/staging/runtime::dotnet-resource-appdomain-reflective-loader',
    'well-known/malware/rat/gravityrat::gravityrat-gx-keylog-upload-rat',
    'well-known/malware/rat/gravityrat::gx-keylog-hidden-command-pair',
    'well-known/malware/rat/gravityrat::gx-upload-command-pair',
    'micro-behaviors/os/registry/write::active-setup-stubpath-write-api-cluster',
}


def change(data, offset, replacement):
    result = bytearray(data)
    result[offset:offset + len(replacement)] = replacement
    return bytes(result)


def main():
    outer_path, go_path, resolver_path, work = map(Path, sys.argv[1:5])
    work.mkdir(parents=True, exist_ok=True)
    outer = outer_path.read_bytes()
    go = go_path.read_bytes()
    dll = outer[0x5060:0x5060 + 0x9c00]
    rat = go[0x599e08:0x599e08 + 0xa1400]
    cecil = go[0x5f5440:0x5f5440 + 0x44800]
    damaged_cecil = go[0x83b127:0x83b127 + 0x44800]
    assert dll[:2] == rat[:2] == cecil[:2] == damaged_cecil[:2] == b'MZ'
    assert outer[0x1a41:0x1a45] == bytes.fromhex('6a026a00')

    # Real writer instructions, with one operand changed at a time.
    cases = {
        'stubpath-writer.exe': (outer, {WRITER: True, COPY: True}),
        'other-value-writer.exe': (
            change(outer, 0x1a46, struct.pack('<I', 0x404334)),
            {WRITER: False, COPY: False}),
        'other-api-writer.exe': (
            change(outer, 0x1a4d, struct.pack('<I', 0x403028)),
            {WRITER: False, COPY: False}),
        'stubpath-reader.dll': (dll, {WRITER: False, PERSIST: False}),
        'rat.exe': (rat, {FAMILY: True}),
        'rat-without-task-namespace.exe': (
            rat.replace(b'LSASS.Core.Tasks', b'Z' * 16), {FAMILY: False}),
        'cecil.dll': (cecil, {FAMILY: False}),
        'damaged-cecil.dll': (damaged_cecil, {FAMILY: False}),
    }

    # A both-claims case: a flood implant containing a genuine bound write.
    pe = pefile.PE(data=dll)
    assert pe.get_data(0x1aa0, 8) == b'stubpath'
    code = (bytes.fromhex('6a026a0068') + struct.pack('<I', 0x10001aa0) +
            bytes.fromhex('51ff15') + struct.pack('<I', 0x1000101c))
    with_write = bytearray(change(dll, 0x87c0, code))
    struct.pack_into('<I', with_write, pe.sections[0].get_file_offset() + 36,
                     pe.sections[0].Characteristics | 0x20000000)
    cases['flood-with-stubpath-write.dll'] = (with_write, {WRITER: True, PERSIST: True})

    # Resource and overlay vocabulary must not identify the containing library.
    tokens = [b'LSASS.Core.Tasks', 'USBJOBSTARTED'.encode('utf-16le'),
              'FileNotCreatedAgainstCommand'.encode('utf-16le'),
              'PARENTHASH'.encode('utf-16le')]
    overlay = rat
    for token in tokens:
        assert token in overlay
        overlay = overlay.replace(token, b'X' * len(token)) + token + b'\0\0'
    cases['family-only-in-overlay.exe'] = (overlay, {FAMILY: False})
    resolver = resolver_path.read_bytes()
    cases['resolver.dll'] = (resolver, {FAMILY: False})
    pe = pefile.PE(data=resolver)
    clr = pe.OPTIONAL_HEADER.DATA_DIRECTORY[14].VirtualAddress
    resource = struct.unpack_from('<I', pe.get_data(clr + 24, 4))[0]
    offset = pe.get_offset_from_rva(resource) + 32
    resource_tokens = b'\0'.join(tokens)
    cases['resolver-with-family-resource.dll'] = (
        change(resolver, offset, resource_tokens), {FAMILY: False})

    for name, (data, _) in cases.items():
        (work / name).write_bytes(data)
    process = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', *[str(work / name) for name in cases]],
        text=True, capture_output=True, check=True)
    (work / 'scans.json').write_text(process.stdout)
    (work / 'stderr.txt').write_text(process.stderr)
    assert not process.stderr.strip(), process.stderr
    decoder = json.JSONDecoder()
    remaining = process.stdout.strip()
    observed = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].strip()
        for entry in report['files']:
            ids = {t['id'] for t in entry.get('traits', [])}
            assert not ids & RETIRED, (entry['path'], ids & RETIRED)
            if '!!' not in entry['path']:
                observed[Path(entry['path']).name] = entry
    results = []
    for name, (_, checks) in cases.items():
        entry = observed[name]
        traits = {t['id']: t for t in entry['traits']}
        for rule, expected in checks.items():
            assert (rule in traits) == expected, (name, rule, expected)
        if WRITER in traits:
            assert traits[WRITER]['crit'] == 3, name
        if name in ('resolver.dll', 'resolver-with-family-resource.dll', 'cecil.dll', 'damaged-cecil.dll'):
            assert not [t for t in entry['traits'] if t['crit'] >= 4], name
        results.append({'case': name, 'checks': checks})
    (work / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'PASS: {len(results)} writer, resource-loader and CLR-identity controls')


if __name__ == '__main__':
    main()
