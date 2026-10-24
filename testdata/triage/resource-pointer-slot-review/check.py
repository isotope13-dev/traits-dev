#!/usr/bin/env python3
"""Static relationship controls; never execute original or mutated PE code."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
STAGE = 'micro-behaviors/process/deploy/file-exec::x86-resource-buffer-stage-launch'
LOADER = 'objectives/execution/payload/file-exec::self-deleting-complement-state-resource-loader'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sample', type=Path, required=True)
    ap.add_argument('--retained-positive', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    b = a.sample.read_bytes()
    assert hashlib.sha256(b).hexdigest() == 'cbe0c4dd14fd5d7c60a709dd2af416d8b7c1f33a729055de14cf4193dc2f7a04'
    assert hashlib.sha256(a.retained_positive.read_bytes()).hexdigest() == 'f6604fbf6ddd90ce420ed7989fa848a826b5f425099d97efa82ee5d83a45da27'

    def patch(offset, value):
        changed = bytearray(b)
        struct.pack_into('<I', changed, offset, value)
        return bytes(changed)

    cases = [('supplied-import-slot.exe', b, True, True)]
    # Keep the complete staging bodies but independently sever each link.
    for name, offset, value in [
        ('different-launch-path', 0x259a+69, 0xfffffdcc),
        ('different-size-slot', 0x259a+28, 0xfffffdc4),
        ('unrelated-resource-call', 0x259a+11, 0),
        ('unrelated-preparation-call', 0x259a+41, 0),
        ('wrong-launch-api', 0x259a+78, 0x41c198),
        ('wrong-resource-api', 0x2974+27, 0x41c060),
        ('unrelated-store-call', 0x2278+131, 0),
        ('wrong-write-api', 0x8bfe+75, 0x41c070),
        ('pointer-call-outside-iat', 0x2974+61, 0x401000),
        ('pointer-call-unaligned', 0x2974+61, 0x41c035),
    ]:
        cases.append((name+'.exe', patch(offset, value), False, False))
    # The old exact LockResource spelling and the modified spelling describe
    # the same attempted resource flow. Neither implies runtime success.
    assert b.count(b'SetHandleCount\0') >= 1
    repaired = b.replace(b'SetHandleCount\0', b'LockResource\0\0\0')
    assert len(repaired) == len(b)
    cases.append(('lockresource-slot.exe', repaired, True, True))
    renamed = b.replace(b'_vslite.bat', b'_rename.bat')
    for old, new in [('HGDraw.dll', 'Rename.dll'), ('golfinfo.ini', 'abcdefgh.ini'),
                     ('golfset.ini', 'abcdefg.ini')]:
        renamed = renamed.replace(old.encode('utf-16le'), new.encode('utf-16le'))
    cases.append(('renamed-artifacts.exe', renamed, True, True))
    cases.append(('no-state-magic.exe', b.replace(b'MSMP', b'ABCD'), True, False))
    zip_header = b'PK\x03\x04\x14\x00\x09\x00\x08\x00'
    assert zip_header in b
    cases.append(('no-encrypted-archive.exe', b.replace(zip_header, zip_header[:6]+b'\x08'+zip_header[7:]), True, False))
    paths = []
    expected = {}
    for name, data, stage, loader in cases:
        path = a.scratch/name
        path.write_bytes(data)
        paths.append(path)
        expected[str(path)] = (stage, loader)
    paths.append(a.retained_positive)
    expected[str(a.retained_positive)] = (True, True)
    for name in ['gui-resource-editor.exe']:
        path = ROOT/'testdata/taxonomy/native-first-review-2026-10-17'/name
        paths.append(path)
        expected[str(path)] = (False, False)
    run = subprocess.run([a.cleave, '--traits-dir', str(ROOT), '--format', 'json',
                          *map(str, paths)], capture_output=True, text=True, check=True)
    assert not any(token in run.stderr.lower() for token in ['failed to load', 'skipped', 'failed to compile']), run.stderr
    decoder = json.JSONDecoder()
    remaining = run.stdout.strip()
    reports = {}
    while remaining:
        record, end = decoder.raw_decode(remaining)
        for f in record['files']:
            reports[f['path']] = {t['id'] for t in f.get('traits', [])}
        remaining = remaining[end:].lstrip()
    results = []
    for path, (stage, loader) in expected.items():
        ids = reports[path]
        assert (STAGE in ids) == stage, (path, 'staging', ids & {STAGE, LOADER})
        assert (LOADER in ids) == loader, (path, 'admission', ids & {STAGE, LOADER})
        results.append({'case': Path(path).name, 'stage': stage, 'loader': loader, 'pass': True})
    (a.scratch/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(f'{len(results)} resource staging controls passed')


if __name__ == '__main__':
    main()
