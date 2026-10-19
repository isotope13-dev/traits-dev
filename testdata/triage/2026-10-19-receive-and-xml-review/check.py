#!/usr/bin/env python3
"""Static controls for the receive-mutated ELF and XML injection configuration.

No specimen is executed. Temporary byte mutations are analyzed by Cleave.
Usage: check.py ELF XML --scratch DIRECTORY [--cleave cleave]
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SYN = 'micro-behaviors/communications/socket/tcp::x64-tcp-syn-telnet-header'
XOR = 'micro-behaviors/data/encoding/xor::x64-counted-byte-xor-cursor-loop'
SCANNER = 'objectives/lateral-movement/brute-force/iot-creds::x64-hidden-telnet-credential-scanner'
FLOOD = 'objectives/impact/dos/udp-flood::hidden-credential-udp-flood-code'
TASK = 'objectives/command-and-control/botnet/iot::x86-64-framed-attack-task-code'
REMOTE = 'objectives/impact/dos/attack/botnet::x86-64-framed-udp-flood'
XML = 'objectives/lateral-movement/exploit/network-device/http::xml-password-encoded-downloader-injection'
FTP = 'objectives/lateral-movement/exploit/network-device/http::iot-password-ftpget-command'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('elf', type=Path)
    ap.add_argument('xml', type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    elf, xml = args.elf.read_bytes(), args.xml.read_bytes()
    assert hashlib.sha256(elf).hexdigest() == 'ab85300d52e9faf318fd3d2c54f1767852c5792acfdac5c5e518501ddb12742b'
    assert hashlib.sha256(xml).hexdigest() == '2232b8a246b7bf17ae20e134fd87d287003bc8f5312d344c08685f897dcc2ccd'
    cases = []

    def add(name, data, yes=(), no=()):
        cases.append((name, bytes(data), set(yes), set(no)))

    add('retained-scanner.elf', elf, [SYN, XOR, SCANNER, FLOOD], [TASK, REMOTE])
    changed = bytearray(elf)
    assert changed[0x6816] == 0x17
    changed[0x6816] = 0x16
    add('different-port.elf', changed, [XOR], [SYN, SCANNER, FLOOD, TASK, REMOTE])
    changed = bytearray(elf)
    for offset in (0x655b, 0x65e7):
        assert changed[offset] == 0x22
        changed[offset] = 0
    add('no-xor-key.elf', changed, [SYN], [XOR, SCANNER, FLOOD])
    changed = bytearray(elf)
    changed[0xede8:0xefa0] = bytes(0xefa0 - 0xede8)
    add('no-credentials.elf', changed, [SYN, XOR], [SCANNER, FLOOD])
    changed = bytearray(elf)
    udp = bytes.fromhex('bf02000000ba11000000be02000000')
    assert udp in changed
    changed = changed.replace(udp, bytes.fromhex('bf02000000ba10000000be02000000'))
    add('no-udp-setup.elf', changed, [SYN, XOR, SCANNER], [FLOOD])
    changed = bytearray(elf)
    loops = list(re.finditer(bytes.fromhex('498b34df418b3c9eb9004000004889ea48ffc3e8') + b'.{4}' + bytes.fromhex('4939dc74caebe1'), elf, re.DOTALL))
    assert loops
    for loop in loops:
        offset = loop.start() + 19
        struct.pack_into('<i', changed, offset + 1, 0xb487 - offset - 5)
    add('redirected-flood-send.elf', changed, [SYN, XOR, SCANNER], [FLOOD])
    changed = bytearray(elf)
    names = changed.rfind(b'\0.text\0')
    assert names > 0
    changed[names + 1:names + 6] = b'.blob'
    add('outside-code-section.elf', changed, no=[SYN, XOR, SCANNER, FLOOD])
    changed = bytearray(elf)
    struct.pack_into('<H', changed, 18, 183)
    add('wrong-architecture.elf', changed, no=[SYN, XOR, SCANNER, FLOOD])
    add('account-config.sh', xml, [XML, FTP])
    # Same executable text outside a password field is not XML injection.
    add('different-field.sh', xml.replace(b'<Password', b'<Comment').replace(b'</Password>', b'</Comment>'), no=[XML, FTP])
    # Plain account data must not acquire execution behavior from its wrapper.
    add('ordinary-password.sh', b'<Account><User1><Password Level="40/40">admin1234</Password></User1></Account>', no=[XML, FTP])

    with tempfile.TemporaryDirectory(dir=args.scratch, prefix='static-controls-') as tmp:
        paths = []
        for name, data, _, _ in cases:
            path = Path(tmp, name)
            path.write_bytes(data)
            paths.append(str(path))
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json', *paths], text=True, capture_output=True, check=True)
        decoder = json.JSONDecoder()
        remaining = result.stdout.strip()
        files = {}
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.update({Path(f['path']).name: f for f in report['files']})
            remaining = remaining[end:].lstrip()
        for name, _, yes, no in cases:
            found = {t['id'] for t in files[name].get('traits', [])}
            assert yes <= found, (name, 'missing', sorted(yes - found))
            assert not no & found, (name, 'unexpected', sorted(no & found))
            print('PASS', name)
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
