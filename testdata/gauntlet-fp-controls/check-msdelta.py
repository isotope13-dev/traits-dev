"""Exercise header boundaries, not decompression or Microsoft authenticity."""
import argparse
import json
import subprocess
import tempfile
import zlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    trait_id = 'metadata/file/magic/identity::msdelta-header'
    cases = []
    tail = bytes(range(64))
    for magic in (b'PA19', b'PA30', b'PA31'):
        data = magic + tail
        cases.append((magic.decode() + '-raw.bin', data, True))
        crc = zlib.crc32(data).to_bytes(4, 'little')
        cases.append((magic.decode() + '-crc.bin', crc + data, True))
    # Position alone is not CRC validation; the description must not imply it.
    cases.append(('unchecked-wrapper.bin', b'\0' * 4 + b'PA31' + tail, True))
    for offset in (1, 2, 3, 5, 8, 32):
        cases.append((f'misplaced-{offset}.bin', b'\0' * offset + b'PA31' + tail, False))
    for magic in (b'PA18', b'PA29', b'PA32', b'pa31'):
        cases.append((magic.decode() + '-near.bin', magic + tail, False))
    cases.extend([
        ('short.bin', b'PA31', False),
        ('documentation.txt', b'The PA31 header is used by delta patches.\n', False),
        ('misnamed.dll', b'ordinary data\0' + tail, False),
    ])
    with tempfile.TemporaryDirectory(prefix='msdelta-header-controls-') as directory:
        root = Path(directory)
        for name, data, _ in cases:
            (root / name).write_bytes(data)
        result = subprocess.run(
            [args.cleave, '--traits-dir', str(repo), '--format=json', str(root)],
            text=True, capture_output=True, check=True,
        )
        decoder = json.JSONDecoder()
        pending = result.stdout.lstrip()
        files = {}
        while pending:
            report, end = decoder.raw_decode(pending)
            for item in report['files']:
                files[Path(item['path']).name] = item
            pending = pending[end:].lstrip()
        errors = []
        for name, _, expected in cases:
            matches = [trait for trait in files[name].get('traits', [])
                       if trait['id'] == trait_id]
            if bool(matches) != expected:
                errors.append(f'{name}: expected match={expected}; got {bool(matches)}')
            if matches and matches[0]['crit'] not in ('notable', 3):
                errors.append(f'{name}: unexpected criticality {matches[0]["crit"]}')
        if errors:
            raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(cases)} MSDelta header and near-miss controls')


if __name__ == '__main__':
    main()
