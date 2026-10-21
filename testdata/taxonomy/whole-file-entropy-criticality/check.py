"""Exercise entropy criticality, near misses and retained archive detections."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[3]
NEW = 'metadata/file/data-blob::near-maximum-entropy-file'
OLD = 'metadata/file/data-blob::near-maximum-entropy-file'
ARCHIVE = 'objectives/anti-static/pack/archive::encrypted-7zaes-windows-exe'
LOCKED = 'objectives/anti-static/pack/archive::header-encrypted-7z-payload'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--traits', type=Path, default=ROOT)
    parser.add_argument('--old', action='store_true')
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    data = b''.join(hashlib.sha256(str(i).encode()).digest() for i in range(12288))
    for name, body in [('high.bin', data), ('low.bin', bytes(len(data))),
                       ('small.bin', data[:65536]), ('carrier.exe', data)]:
        (args.scratch / name).write_bytes(body)
    # The archive fixture tests member-name observations, not executable code.
    for name, options in [
        ('ordinary.zip', ['-tzip']),
        ('encrypted-exe.7z', ['-t7z', '-pcontrol', '-mhe=off', '-m0=Copy']),
        ('locked-exe.7z', ['-t7z', '-pcontrol', '-mhe=on', '-m0=Copy']),
    ]:
        path = args.scratch / name
        path.unlink(missing_ok=True)
        subprocess.run(['7zz', 'a', *options, str(path),
                        str(args.scratch / 'carrier.exe')],
                       capture_output=True, check=True)
    (args.scratch / 'carrier.exe').unlink()

    def chunk(kind, body):
        return (struct.pack('>I', len(body)) + kind + body
                + struct.pack('>I', zlib.crc32(kind + body)))

    rows = b''.join(b'\0' + data[i:i + 1536] for i in range(0, len(data), 1536))
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', 512, 256, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))
    with zipfile.ZipFile(args.scratch / 'theme.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('manifest.json', json.dumps({
            'manifest_version': 2, 'name': 'Entropy control', 'version': '1.0',
            'theme': {'images': {'theme_frame': 'images/theme_frame.png'}}}))
        z.writestr('images/theme_frame.png', png)

    expected = {'high.bin': True, 'low.bin': False, 'small.bin': False,
                'ordinary.zip': True, 'encrypted-exe.7z': True,
                'locked-exe.7z': True, 'theme.zip': False}
    run = subprocess.run([
        'cleave', '--traits-dir', str(args.traits), '--format', 'json',
        'analyze', '--zip-password', 'control',
        *(str(args.scratch / name) for name in expected)],
        capture_output=True, text=True, check=True)
    (args.scratch / 'scan.json').write_text(run.stdout)
    decoder = json.JSONDecoder()
    remaining = run.stdout
    files = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        files.update({f['path']: f for f in report['files']})
    trait = OLD if args.old else NEW
    results = []
    for name, present in expected.items():
        file = files[str(args.scratch / name)]
        traits = {t['id']: t['crit'] for t in file.get('traits', [])}
        assert (trait in traits) == present, (name, traits)
        if present:
            assert traits[trait] == (1 if args.old else 3), (name, traits[trait])
        if name == 'encrypted-exe.7z':
            assert traits[ARCHIVE] == 4, traits
        if name == 'locked-exe.7z':
            assert traits[LOCKED] == 5, traits
        results.append({'case': name, 'matched': present, 'passed': True})
    # The baseline theme helper can be stripped from ordinary report output.
    # Confirm the actual exclusion, rather than treating an absent finding
    # as evidence that the exception worked.
    diagnostic = subprocess.run([
        'cleave', '--traits-dir', str(args.traits), 'test-rules',
        str(args.scratch / 'theme.zip'), '--rules',
        'metadata/permission/manifest::chrome-theme-archive,' + trait],
        capture_output=True, text=True, check=True).stdout
    assert 'MATCHED metadata/permission/manifest::chrome-theme-archive' in diagnostic
    assert "Skipped by 'unless'" in diagnostic
    (args.scratch / 'theme-diagnostic.txt').write_text(diagnostic)
    (args.scratch / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
