"""Local portable-pty service suppresses the macOS PTY backdoor rule.

Run: python3 testdata/portable-pty-local-service/verify.py <scratch-directory>

Binaries built on the portable-pty Rust crate (terminal emulators and
multiplexer daemons such as opencode-pty) spawn the user's shell and
proxy it over local sockets. That trips every leg of
``macos-pty-socket-shell-backdoor`` even though no remote operator is
involved; the crate registry path marker suppresses the composite while
a crate-free PTY/socket/shell combination still convicts.

Controls: a minimal Mach-O with the PTY, process, socket, and shell
legs but no crate marker must report the hostile; the same image with
the portable-pty marker must report neither the hostile nor lose the
notable crate marker.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKDOOR = ('objectives/command-and-control/backdoor/shell/socket::'
            'macos-pty-socket-shell-backdoor')
CRATE = ('well-known/lib/platform/portable-pty::'
         'portable-pty-crate-reference')

SYMBOLS = ('_fork', '_execv', '_dup2', '_connect', '_send', '_recv')
BASE_STRINGS = ('openpty', '/bin/sh')
CRATE_STRINGS = BASE_STRINGS + ('portable-pty-0.9.0',)


def build_macho(symbols, text_strings):
    """Minimal Mach-O 64 with LC_SYMTAB imports and string payload."""
    strtab = b'\x00'
    entries = []
    for name in symbols:
        entries.append((len(strtab), name))
        strtab += name.encode('ascii') + b'\x00'

    symoff = 32 + 24
    nsyms = len(entries)
    stroff = symoff + nsyms * 16
    blob = bytearray()
    for s in text_strings:
        blob += s.encode('ascii') + b'\x00'
    while len(blob) < 1024:
        blob += b'\x00' * 64
    blob = bytes(blob)

    header = struct.pack('<IIIIIIII', 0xfeedfacf, 0x01000007, 3, 2, 1,
                         24, 0, 0)
    symtab_cmd = struct.pack('<IIIIII', 2, 24, symoff, nsyms, stroff,
                             len(strtab))
    out = bytearray(header + symtab_cmd)
    for strx, _ in entries:
        out += struct.pack('<IBBHQ', strx, 0x01, 0, 0, 0)
    out += strtab + blob
    return bytes(out)


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry['traits']}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    positive = dest / 'pty-backdoor-positive.macho'
    positive.write_bytes(build_macho(SYMBOLS, BASE_STRINGS))
    ids = scan(positive)
    assert BACKDOOR in ids, 'pty/socket/shell pattern must convict'
    print('PASS pty-backdoor-positive.macho', flush=True)

    negative = dest / 'pty-local-service-negative.macho'
    negative.write_bytes(build_macho(SYMBOLS, CRATE_STRINGS))
    ids = scan(negative)
    assert BACKDOOR not in ids, 'portable-pty service must suppress it'
    assert CRATE in ids, 'crate marker must still report'
    print('PASS pty-local-service-negative.macho', flush=True)


if __name__ == '__main__':
    main()
