#!/usr/bin/env python3
"""Static mutation controls; never execute the supplied ELF.

Usage: check.py /path/to/send-call-redirected.elf [--cleave cleave]
Mutations distinguish retained task reception from a redirected UDP send,
require credential context for the bot composite, and refute generic daemon
names as malware identity. Temporary copies remain beside the input sample.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TASK = 'objectives/command-and-control/botnet/iot::x86-64-framed-attack-task-code'
BOT = 'objectives/command-and-control/botnet/iot::x86-64-framed-credential-bot'
FLOOD = 'objectives/impact/dos/attack/botnet::x86-64-framed-udp-flood'
LOOP = 'micro-behaviors/communications/flood::x86-64-udp-flood-send-loop'
XOR = 'micro-behaviors/data/encoding/xor::x64-eight-word-four-lane-xor-loop'
MIRAI = 'well-known/malware/botnet/mirai/stripped::stripped-mirai-iot-botnet'


def call(data, offset, target):
    assert data[offset] == 0xe8
    struct.pack_into('<i', data, offset + 1, target - offset - 5)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('sample', type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    original = args.sample.read_bytes()
    assert hashlib.sha256(original).hexdigest() == (
        'c9018cee6b41d2664a06abe1a90aaa7d551f20af9abf33a139ec4361eb51fb18')
    cases = []

    def add(name, data, yes=(), no=()):
        cases.append((name, bytes(data), set(yes), set(no)))

    add('redirected-send.elf', original, [TASK, BOT, XOR, MIRAI], [FLOOD, LOOP])
    restored = bytearray(original)
    # Original call at 0x336c targets the ret at 0xb487, one byte before send.
    assert restored[0x336c:0x3371] == bytes.fromhex('e8 16 81 00 00')
    call(restored, 0x336c, 0xb488)
    add('restored-send.elf', restored, [TASK, BOT, XOR, FLOOD, LOOP, MIRAI])

    changed = bytearray(restored)
    call(changed, 0x5ba1, 0xb487)
    add('parser-call-redirected.elf', changed, [LOOP, XOR], [TASK, BOT, FLOOD])
    changed = bytearray(restored)
    # Keep recv vocabulary and wrapper bytes; redirect the body receive call.
    call(changed, 0x5b85, 0xb487)
    add('receive-call-redirected.elf', changed, [LOOP, XOR], [TASK, BOT, FLOOD])
    changed = bytearray(restored)
    # Remove the complete credential region, including the early entries.
    changed[0xeda0:0xf330] = bytes(0xf330 - 0xeda0)
    add('no-credential-table.elf', changed, [TASK, LOOP, XOR], [BOT, FLOOD, MIRAI])

    changed = bytearray(original)
    pattern = bytes.fromhex('48 89 d0 48 03 06 44 30 10')
    assert changed.count(pattern) == 2
    changed = changed.replace(pattern, bytes.fromhex('48 89 d0 48 03 06 90 90 90'))
    add('no-four-lane-xor.elf', changed, [TASK, BOT], [XOR])
    changed = bytearray(original)
    assert changed[-704:].find(b'.text\0') >= 0
    section_names = original.rfind(b'\0.text\0')
    assert section_names >= 0
    changed[section_names + 1:section_names + 6] = b'.blob'
    add('patterns-outside-text.elf', changed, no=[TASK, BOT, XOR, FLOOD, LOOP])
    changed = bytearray(original)
    struct.pack_into('<H', changed, 18, 183)
    add('wrong-architecture.elf', changed, no=[TASK, BOT, XOR, FLOOD, LOOP])

    changed = bytearray(original)
    changed[0x100:0xed76] = bytes(0xed76 - 0x100)
    changed[0xeda0:0x108d0] = bytes(0x108d0 - 0xeda0)
    names = (b'/proc/net/tcp\0/proc/self/exe\0/bin/busybox\0/Sofia\0'
             b'/usr/sbin/sshd\0telnetd\0httpd\0/proc/self/maps\0')
    changed[0xeda0:0xeda0 + len(names)] = names
    add('ordinary-daemon-paths.elf', changed, no=[TASK, BOT, XOR, FLOOD, LOOP, MIRAI])

    with tempfile.TemporaryDirectory(prefix='static-controls-', dir=args.sample.parent) as tmp:
        paths = []
        for name, data, _, _ in cases:
            p = Path(tmp) / name
            p.write_bytes(data)
            paths.append(str(p))
        result = subprocess.run([
            args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
            '--disable', 'radare2,upx,third-party', '--format', 'json',
            'analyze', *paths,
        ], capture_output=True, text=True, check=True)
        decoder = json.JSONDecoder()
        files = {}
        output = result.stdout
        while output.strip():
            report, end = decoder.raw_decode(output.lstrip())
            files.update({Path(f['path']).name: f for f in report['files']})
            output = output.lstrip()[end:]
        for name, _, yes, no in cases:
            ids = {t['id'] for t in files[name]['traits']}
            assert yes <= ids, (name, 'missing', sorted(yes - ids))
            assert not no & ids, (name, 'unexpected', sorted(no & ids))
            print('PASS', name)
    print(f'{len(cases)} controls passed')


if __name__ == '__main__':
    main()
