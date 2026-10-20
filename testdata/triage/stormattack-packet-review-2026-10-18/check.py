"""Offline controls on provided bytes; never execute sample code.

Usage: python3 check.py INTACT_OUTER DAMAGED_OUTER SCRATCH
Generated binary fixtures and complete scan reports stay in SCRATCH.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DEPLOY = 'micro-behaviors/process/deploy/file-exec::x86-packet-task-download-launch'
CONTROL = ('objectives/command-and-control/remote-command/tasking::'
           'packet-flood-download-launch-control')
FAMILY = {
    'well-known/malware/botnet/stormattack::stormattack-server-service-injector',
    'well-known/malware/botnet/stormattack::stormattack-resource-service-dll-injector',
}


def main():
    intact, damaged, scratch = map(Path, sys.argv[1:4])
    work = scratch / 'packet-controls'
    work.mkdir(parents=True, exist_ok=True)
    outer = intact.read_bytes()
    assert outer[0x5060:0x5062] == b'MZ'
    dll = outer[0x5060:]

    def change(data, offset, replacement):
        result = bytearray(data)
        result[offset:offset + len(replacement)] = replacement
        return bytes(result)

    # These offsets address verified instructions in the intact DLL, not
    # sample identity gates. Each control leaves the other roles intact.
    assert dll[0x5fb1] == 0xe8
    assert dll[0x5cc2:0x5cc4] == b'\x8b\x35'
    assert dll[0x5f3b:0x5f3e] == b'\x56\x68\x28'
    renamed = dll
    for old in [b'Storm ddos DNS', b'Welcome to use storm ddos', b'Strom attack',
                b'STORM:%d|%s|%s|%s|%s', 'Storm Ser DLL'.encode('utf-16le')]:
        assert old in renamed
        renamed = renamed.replace(old, b'X' * len(old))
    cases = {
        'intact.dll': (dll, True, True),
        'renamed-family.dll': (renamed, True, True),
        # Keep both dispatcher and downloader; redirect task 5 to MessageBox.
        'unrelated-downloader.dll': (
            change(dll, 0x5fb2, struct.pack('<i', 0x10006535 - 0x10006bb6)),
            False, False),
        'different-launch-path.dll': (
            change(dll, 0x5cc2 + 79, struct.pack('<i', -0x164)), False, False),
        'different-recv-buffer.dll': (
            change(dll, 0x5f3b + 8, b'\xf8'), False, False),
        'different-dispatch-record.dll': (
            change(dll, 0x5f3b + 56, struct.pack('<i', -0x530)), False, False),
        'argument-outside-record.dll': (
            change(dll, 0x5f3b + 113, struct.pack('<i', -0x630)), False, False),
        'no-launch-call.dll': (change(dll, 0x5d17, b'\x90' * 6), False, False),
        # Keep the named API elsewhere, but make GetProcAddress use another
        # string: the rule must follow the referenced API name.
        'unrelated-api-name.dll': (
            change(dll, 0x5cc2 + 18, struct.pack('<I', 0x10001b00)), False, False),
        # Neutral task-driven deployment remains visible without flood abuse.
        'no-raw-udp.dll': (change(dll, 0x16b1, b'\x06'), True, False),
    }
    # The loader family rules must require execution handoff, not imports.
    loader = damaged.read_bytes()
    assert loader[0x1219] == 0x50
    loader_cases = {
        'damaged-loader.exe': (loader, True),
        'api-only-loader.exe': (change(loader, 0x1219, b'\x90' * 0x3a), False),
    }
    paths = []
    for name, case in {**cases, **loader_cases}.items():
        path = work / name
        path.write_bytes(case[0])
        paths.append(str(path))
    proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
                           str(ROOT), '--format', 'json', *paths],
                          capture_output=True, text=True, check=True)
    (work / 'scans.json').write_text(proc.stdout)
    (work / 'stderr.txt').write_text(proc.stderr)
    decoder = json.JSONDecoder()
    remaining = proc.stdout.strip()
    observed = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].strip()
        for file in report['files']:
            observed[Path(file['path']).name] = {t['id'] for t in file['traits']}
    results = []
    for name, (_, deploy, control) in cases.items():
        traits = observed[name]
        assert (DEPLOY in traits) == deploy, name
        assert (CONTROL in traits) == control, name
        results.append({'case': name, 'deployment': deploy, 'hostile_control': control})
    for name, (_, family) in loader_cases.items():
        traits = observed[name]
        assert FAMILY.intersection(traits) == (FAMILY if family else set()), name
        results.append({'case': name, 'injector_family': family})
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
