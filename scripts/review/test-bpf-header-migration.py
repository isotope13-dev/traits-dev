#!/usr/bin/env python3
"""Check BPF header bytes and the generic-fixture suppression boundary.

Copies an ELF control and changes header bytes for static analysis; generated
files are never executed. Requires the sibling Cleave release binary.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
SOURCE = ROOT / 'testdata/notable/controls/taxonomy-map-unmap.elf'
HEADER = 'metadata/binary/header/identity::elf-bpf-machine-header-word-one'
CARRIER = 'metadata/binary/layout/stub::elf-image-carried-by-design'

with tempfile.TemporaryDirectory(prefix='bpf-header-migration-') as tmp:
    directory = Path(tmp) / 'fixtures'
    directory.mkdir()
    for name, upper, expected in (('shape', 1, True), ('other-address', 0, False)):
        data = bytearray(SOURCE.read_bytes())
        data[18:20] = b'\xf7\x00'
        data[28:32] = upper.to_bytes(4, 'little')
        sample = directory / (name + '.elf')
        sample.write_bytes(data)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', HEADER + ',' + CARRIER, str(sample)],
                                check=True, capture_output=True, text=True)
        header_status = 'MATCHED ' if expected else 'NOT MATCHED '
        if ('\n' + header_status + HEADER + ' ') not in result.stdout:
            raise SystemExit(f'{name}: wrong header result\n{result.stdout}\n{result.stderr}')
        if ('\nNOT MATCHED ' + CARRIER + ' ') not in result.stdout:
            raise SystemExit(f'{name}: generic fixture path suppressed a carrier\n{result.stdout}')
        print(f'{name}: ok', flush=True)
