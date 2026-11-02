#!/usr/bin/env python3
"""NuGet false-positive controls; never execute extracted package code."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    parser.add_argument('--samples-root', type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    hidden = 'objectives/evasion/process/hidden/execution::hidden-powershell-decoded-eval'
    buf = 'micro-behaviors/fs/write/file/stream::powershell-buf-write-argument'
    ua = 'micro-behaviors/communications/http/user-agent::powershell-webclient-header-add'
    triple = 'metadata/binary/instruction/sequence::x86-call-triple-to-section-start'
    with tempfile.TemporaryDirectory(prefix='nupkg-good-controls-') as directory:
        work = Path(directory)
        launch = 'powershell -WindowStyle Hidden -Command $decoded\nIEX ([Convert]::FromBase64String($payload))\n'
        cases = {
            'decoded-launch.ps1': (launch, {hidden}),
            'plain-launch.ps1': ('powershell -WindowStyle Hidden -File .\\tray.ps1\n', set()),
            'separated.ps1': ('powershell -WindowStyle Hidden -File .\\tray.ps1\n' + '\n' * 20 + 'IEX $localCommand\n' + '\n' * 20 + '[Convert]::FromBase64String($doc.Password)\n', set()),
            'buffer.ps1': ('$stream.Write($buf, 0, $buf.Length)\n', {buf}),
            'buffer-near-miss.ps1': ('$stream.Read($buf, 0, $buf.Length)\n', set()),
            'agent.ps1': ('$wc.Headers.Add("User-Agent", "DriverUpdater")\n', {ua}),
            'agent-near-miss.ps1': ('$wc.Headers.Add("Accept", "application/json")\n', set()),
        }
        required = {}
        for name, (source, ids) in cases.items():
            (work / name).write_text(source)
            required[name] = ids
        # Minimal PE with three ordinary calls, the last targeting section start.
        # This is instruction layout, not evidence of XOR or payload decoding.
        image = bytearray(0x600)
        image[:2] = b'MZ'
        struct.pack_into('<I', image, 0x3c, 0x80)
        image[0x80:0x84] = b'PE\0\0'
        struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
        opt = 0x98
        struct.pack_into('<H', image, opt, 0x10b)
        struct.pack_into('<I', image, opt + 16, 0x1000)
        struct.pack_into('<I', image, opt + 28, 0x400000)
        struct.pack_into('<II', image, opt + 32, 0x1000, 0x200)
        struct.pack_into('<II', image, opt + 56, 0x2000, 0x200)
        struct.pack_into('<H', image, opt + 68, 3)
        section = opt + 224
        image[section:section + 8] = b'.text\0\0\0'
        struct.pack_into('<IIII', image, section + 8, 0x400, 0x1000, 0x400, 0x200)
        struct.pack_into('<I', image, section + 36, 0x60000020)
        for off in [0x220, 0x228, 0x230]:
            image[off] = 0xe8
            struct.pack_into('<i', image, off + 1, 0x200 - off - 5)
        (work / 'calls.exe').write_bytes(image)
        required['calls.exe'] = {triple}
        image[0x230] = 0x90
        (work / 'two-calls.exe').write_bytes(image)
        required['two-calls.exe'] = set()
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format', 'json', str(work)], check=True, capture_output=True, text=True)
        observed = {}
        for line in result.stdout.strip().split('\n'):
            for file in json.loads(line)['files']:
                observed[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
        focus = {hidden, buf, ua, triple}
        for name, expected in required.items():
            assert observed.get(name, set()) & focus == expected, (name, observed.get(name, set()) & focus, expected)
    if args.samples_root:
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format', 'json', str(args.samples_root)], check=True, capture_output=True, text=True)
        count = 0
        for line in result.stdout.strip().split('\n'):
            report = json.loads(line)
            count += 1
            for file in report['files']:
                flags = [t['id'] for t in file.get('traits', []) if t['crit'] >= 4]
                assert not flags, (file['path'], flags)
        assert count == 10, count
    print('NuGet good controls passed')


if __name__ == '__main__':
    main()
