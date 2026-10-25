#!/usr/bin/env python3
"""Static data-flow controls for the UCRT-import compiler layout.

Never executes a specimen. Pass --sample and --scratch; changes affect only
temporary copies and test one required relationship at a time.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REPLICA = 'objectives/execution/payload/file-exec::native-footer-self-replica-launch'
BOMB = 'objectives/impact/dos/disk::native-footer-replication-disk-bomb'
MINER = 'objectives/impact/cryptojacking/miner/config::native-footer-replicating-xmrig-miner'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    args = ap.parse_args()
    original = args.sample.read_bytes()
    cases = []
    with tempfile.TemporaryDirectory(prefix='ucrt-replica-', dir=args.scratch) as tmp:
        def add(name, data, yes=(), no=()):
            path = Path(tmp) / name
            path.write_bytes(data)
            cases.append((path, set(yes), set(no)))

        add('renamed.exe', original, (REPLICA, BOMB, MINER))
        low = bytearray(original)
        struct.pack_into('<II', low, len(low) - 8, 2, 3)
        add('small-fanout.exe', low, (REPLICA, MINER), (BOMB,))
        zero = bytearray(original)
        struct.pack_into('<I', zero, len(zero) - 8, 0)
        add('zero-depth.exe', zero, (REPLICA,), (BOMB,))
        for name, pattern, delta in [
            ('different-read-api', '49 8b d4 48 8b c8 ff 15', 8),
            ('different-copy-source', 'ba 01 00 00 00 49 8b ce ff 15', 7),
            ('different-depth-writer', '48 8d 4c 24 58 ff 15', 7),
            ('different-fanout-writer', '48 8d 4c 24 54 ff 15', 7),
            ('missing-depth-write', '48 8d 4c 24 58 ff 15', 4),
            ('different-copy-stream', '4c 8b cb ba 04 00 00 00 44 8d 42 fd', 2),
            ('different-converted-path', '48 8b cf e8 60 fc 06 00', 2),
            ('different-launched-path', '4c 8d 40 01 48 8b d7 48 8d 4d 40', 6),
            ('different-launch-api', '48 8d 55 40 33 c9 ff 15', 8),
            ('unlinked-backedge', '8b 4c 24 58 e9', 5),
            ('different-footer-buffer', '43 8b 4c 35 f8 43 8b 54 35 fc', 3),
        ]:
            data = bytearray(original)
            pos = data.index(bytes.fromhex(pattern))
            data[pos + delta] ^= 1
            add(name + '.exe', data, (), (REPLICA, BOMB, MINER))
        # Chosen path names and generated padding strides are not gates.
        labels = original.replace(b'C:\\Windows\\System\\', b'D:\\Windows\\System\\')
        add('different-labels.exe', labels, (REPLICA, BOMB, MINER))
        stride = bytearray(original)
        for pattern, delta in [('41 bc fd 00 00 00 85 c9', 2),
                               ('41 81 c4 fd 00 00 00', 3)]:
            pos = stride.index(bytes.fromhex(pattern))
            stride[pos + delta] ^= 1
        add('different-padding-stride.exe', stride, (REPLICA, BOMB, MINER))
        output = subprocess.check_output([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', '--disable', 'third-party',
            *[str(path) for path, _, _ in cases],
        ]).decode().lstrip()
        files = {}
        decoder = json.JSONDecoder()
        while output:
            report, end = decoder.raw_decode(output)
            files.update({f['path']: {t['id'] for t in f.get('traits', [])}
                          for f in report['files']})
            output = output[end:].lstrip()
        for path, yes, no in cases:
            actual = files[str(path)]
            assert yes <= actual, (path.name, 'missing', sorted(yes - actual))
            assert not no & actual, (path.name, 'unexpected', sorted(no & actual))
            print('PASS', path.name)
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
