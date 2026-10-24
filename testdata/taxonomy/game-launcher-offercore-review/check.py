"""Production-path regression checks; generated PE entry points are inert.

Usage: python3 check.py SCRATCH_DIR [LAUNCHER_SAMPLE]
The optional launcher supplies real EXE/DLL-header near-miss controls.
"""
from pathlib import Path
import importlib.util
import json
import os
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'pe_controls', ROOT / 'testdata/taxonomy/managed-tuner-observations/check.py')
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)
WALLET = 'micro-behaviors/os/application/target::native-software-wallet-brand-family'
SERIAL = 'micro-behaviors/hardware/serial::serial-device-name-or-path'
SHA = 'micro-behaviors/crypto/hash/digest::sha256-code-name-reference'
PATH = 'micro-behaviors/fs/path-ops/normalize::final-path-by-handle-api-reference'
UPDATER = 'metadata/binary/resource/identity::updater-role-label-text'
FNV = 'micro-behaviors/data/checksum::opaque-pe-fnv-prime-reference'
DLL = 'metadata/file/extension/mismatch::unsigned-dll-data-extension-structure'


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    imported = bytearray(controls.pe())
    optional = 0x98
    struct.pack_into('<II', imported, optional + 104, 0x2000, 40)
    imported[optional + 224 + 40:optional + 224 + 48] = b'.idata\0\0'
    struct.pack_into('<IIIII', imported, 0x400, 0x2040, 0, 0, 0x2080, 0x2060)
    struct.pack_into('<II', imported, 0x440, 0x20a0, 0)
    struct.pack_into('<II', imported, 0x460, 0x20a0, 0)
    imported[0x480:0x48d] = b'KERNEL32.dll\0'
    api = b'\0\0GetFinalPathNameByHandleW\0'
    imported[0x4a0:0x4a0 + len(api)] = api
    cases = [
        ('import-path.exe', bytes(imported), {'micro-behaviors/fs/path-ops/normalize::final-path-by-handle-import'}, {PATH}),
        ('bodyguard.exe', controls.pe(b'Livro 3 -- Lemur Guarda-costas\0'), set(), {WALLET}),
        ('town-guard.exe', controls.pe('Guarda da Praça\0'.encode()), set(), {WALLET}),
        ('guard-and-wallet.exe', controls.pe(b'Guarda da Pra\0Guarda-costas\0Exodus\0'), {WALLET}, set()),
        ('wallet.exe', controls.pe(b'Guarda\0Exodus\0Coinomi\0'), {WALLET}, set()),
        ('serial.exe', controls.pe(b'COM1\0'), {SERIAL}, set()),
        ('handle-path.exe', controls.pe(b'GetFinalPathNameByHandle\0'), {PATH}, set()),
        ('runtime-path-name.exe', controls.pe(b'GetFinalPathNameByHandleW\0'), set(), {PATH}),
        ('handle-mention.exe', controls.pe(b'GetFinalPathNameByHandleExample\0'), set(), {PATH}),
        ('module-sha.exe', controls.pe(b'SHA256\0'), {SHA}, set()),
        ('resource-updater.exe', controls.pe(resource=b'software updater\0'), {UPDATER}, set()),
        ('code-updater.exe', controls.pe(b'software updater\0'), set(), {UPDATER}),
        ('updater-hidden-paths.exe', controls.pe(b'/opt/.taskfile /usr/lib/.taskfile\0', resource=b'software updater\0'), {UPDATER}, set()),
        ('hidden-paths.exe', controls.pe(b'/opt/.taskfile /usr/lib/.taskfile\0'), set(), {UPDATER}),
        ('aabbccddee112233.bin', controls.pe(b'\x93\x01\x00\x01'), {FNV}, set()),
    ]
    if len(sys.argv) > 2:
        data = bytearray(Path(sys.argv[2]).read_bytes())
        pe_offset = struct.unpack_from('<I', data, 0x3c)[0]
        flags = struct.unpack_from('<H', data, pe_offset + 22)[0]
        cases.append(('real-exe.bin', bytes(data), set(), {DLL}))
        struct.pack_into('<H', data, pe_offset + 22, flags | 0x2000)
        cases.append(('dll-header.bin', bytes(data), {DLL}, set()))
    for name, data, _, _ in cases:
        (scratch / name).write_bytes(data)
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', 'analyze', *[str(scratch / c[0]) for c in cases],
    ], check=True, capture_output=True, text=True)
    # Multi-file JSON output is a sequence of JSON objects.
    decoder, offset, reports = json.JSONDecoder(), 0, {}
    while offset < len(result.stdout):
        while offset < len(result.stdout) and result.stdout[offset].isspace():
            offset += 1
        if offset == len(result.stdout):
            break
        report, offset = decoder.raw_decode(result.stdout, offset)
        for file in report['files']:
            reports[Path(file['path']).name] = {t['id']: t['crit'] for t in file.get('traits', [])}
    output = []
    for name, _, present, absent in cases:
        severities = reports[name]
        observed = set(severities)
        if name == 'updater-hidden-paths.exe':
            expected = 2
            for trait in ('micro-behaviors/fs/path/system::hidden-opt-path-reference',
                          'micro-behaviors/fs/path/library::hidden-library-path-reference'):
                assert severities.get(trait) == expected, (name, trait, severities.get(trait))
        assert present <= observed and not absent & observed, (name, present - observed, absent & observed)
        output.append({'case': name, 'passed': True})
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
