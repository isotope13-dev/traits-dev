#!/usr/bin/env python3
"""Static controls for the argv[0]/inline CreateProcess compiler layout.

Never executes a specimen. Mutants retain the original PE import table and
change one data-flow relationship at a time. Pass --sample and --scratch.
"""
import argparse
import importlib.util
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
UNICODE = 'micro-behaviors/hardware/input/keyboard/layout::to-unicode-str'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    args = ap.parse_args()
    original = args.sample.read_bytes()
    # Reuse the nonfunctional, RET-entry PE builder from the original controls.
    spec = importlib.util.spec_from_file_location('footer_controls', Path(__file__).with_name('check.py'))
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)
    cases = []
    with tempfile.TemporaryDirectory(prefix='inline-replica-', dir=args.scratch) as tmp:
        def add(name, data, yes=(), no=()):
            path = Path(tmp) / name
            path.write_bytes(data)
            cases.append((path, set(yes), set(no)))

        add('renamed.exe', original, (REPLICA, BOMB, MINER), (UNICODE,))
        low = bytearray(original)
        struct.pack_into('<II', low, len(low) - 8, 2, 3)
        add('small-fanout.exe', low, (REPLICA, MINER), (BOMB,))
        for name, pattern, delta in [
            ('missing-depth-write', '4c 8b cb 4d 8b c6 ba 04 00 00 00 48 8d 4c 24 74 e8', 15),
            ('missing-fanout-write', '4c 8b cb 4d 8b c6 ba 04 00 00 00 48 8d 4c 24 70 e8', 15),
            ('different-writer', '4c 8b cb 4d 8b c6 ba 04 00 00 00 48 8d 4c 24 74 e8', 17),
            ('different-launch-api', '48 8d 95 80 00 00 00 33 c9 ff 15', 11),
            ('unlinked-backedge', '8b 4c 24 74 e9', 5),
            ('different-copy-stream', '4c 8b cb 4d 8b c6 ba 04 00 00 00', 2),
            ('different-launch-path', '49 ff c0 42 38 04 07 75 f7 49 ff c0 48 8b d7', 14),
            ('different-read-buffer', '8b 4c 33 f8 8b 54 33 fc', 2),
        ]:
            mutated = bytearray(original)
            position = mutated.index(bytes.fromhex(pattern))
            mutated[position + delta] ^= 1
            add(name + '.exe', mutated, (), (REPLICA, BOMB, MINER))
        # Neither generated path labels nor pool addresses gate the rule.
        renamed = original.replace(b'C:\\Windows\\System32\\', b'D:\\Windows\\System32\\')
        renamed = renamed.replace(b'3.120.209.58:8080', b'8.120.209.58:8081')
        add('changed-labels.exe', renamed, (REPLICA, BOMB, MINER))
        for name, text, expected in [
            ('api-name', b'ToUnicode\0', True),
            ('qualified-api-name', b'Interop.ToUnicode\0', True),
            ('pdf-font-map', b'/ToUnicode 18 0 R>>\0', False),
            ('different-api', b'ToUnicodeEx\0', False),
        ]:
            add(name + '.exe', helpers.pe_text(text),
                (UNICODE,) if expected else (), () if expected else (UNICODE,))

        output = subprocess.check_output([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', '--disable', 'third-party',
            *[str(path) for path, _, _ in cases],
        ])
        decoder = json.JSONDecoder()
        remaining = output.decode().lstrip()
        files = {}
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.update({f['path']: {t['id'] for t in f.get('traits', [])}
                          for f in report['files']})
            remaining = remaining[end:].lstrip()
        for path, yes, no in cases:
            actual = files[str(path)]
            assert yes <= actual, (path.name, 'missing', sorted(yes - actual))
            assert not no & actual, (path.name, 'unexpected', sorted(no & actual))
            print('PASS', path.name)
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
