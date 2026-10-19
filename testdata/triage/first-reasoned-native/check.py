"""Focused controls; analyze specimen bytes without executing them.

Usage: python3 check.py MIPS STORM WRAPPER SCRATCH
Mutation cases test rule dependencies, not benign verdicts on altered malware.
"""
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
C2 = 'objectives/command-and-control/remote-command/dispatch::concealed-native-module-upload-dispatch'
SERVICE = 'objectives/persistence/system/service/install::concealed-module-agent-auto-service'
FLOOD = 'objectives/impact/dos/attack/flood::native-raw-udp-burst-flood'
STORM = 'well-known/malware/botnet/stormattack::stormattack-ddos-module'
LOOT = 'micro-behaviors/communications/http/request/body::native-sensitive-path-report-context'


def reports(output):
    decoder = json.JSONDecoder()
    output = output.strip()
    result = {}
    while output:
        report, stop = decoder.raw_decode(output)
        for f in report['files']:
            result[Path(f['path']).name] = {t['id']: t for t in f['traits']}
        output = output[stop:].strip()
    return result


def main():
    mips, storm, wrapper = (Path(p).read_bytes() for p in sys.argv[1:4])
    scratch = Path(sys.argv[4]) / 'focused-controls'
    scratch.mkdir(parents=True, exist_ok=True)
    assert wrapper[0x3b000:0x3b002] == b'MZ'
    agent = wrapper[0x3b000:]
    # This PE's .text RVA is 0x1000 and its raw offset is 0x400.
    delta = 0x400000 + 0x1000 - 0x400

    def patch_agent(address, old, new):
        offset = address - delta
        assert agent[offset:offset + len(old)] == old
        assert len(old) == len(new)
        return agent[:offset] + new + agent[offset + len(old):]

    image = runpy.run_path(str(ROOT / 'testdata/triage-sighted/build_pe_fixtures.py'))['image']
    # Minimal inert big-endian MIPS ELF with ordinary proc/shell/HTTP strings.
    neutral_mips = bytearray(0x5a0)
    neutral_mips[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', neutral_mips, 16,
                     2, 8, 1, 0x400100, 52, 0x500, 0x70001007,
                     52, 32, 1, 40, 4, 3)
    struct.pack_into('>IIIIIIII', neutral_mips, 52,
                     1, 0, 0x400000, 0x400000, 0x500, 0x500, 5, 0x1000)
    neutral_mips[0x100:0x110] = bytes.fromhex('24020fa10000000c03e0000800000000')
    neutral_strings = b'/proc/self/exe\0/bin/sh\0GET /health HTTP/1.0\0'
    neutral_mips[0x200:0x200 + len(neutral_strings)] = neutral_strings
    names = b'\0.text\0.rodata\0.shstrtab\0'
    neutral_mips[0x400:0x400 + len(names)] = names
    for offset, fields in [
        (0x528, (1, 1, 6, 0x400100, 0x100, 16, 0, 0, 4, 0)),
        (0x550, (7, 1, 2, 0x400200, 0x200, len(neutral_strings), 0, 0, 1, 0)),
        (0x578, (15, 3, 0, 0, 0x400, len(names), 0, 0, 1, 0)),
    ]:
        struct.pack_into('>IIIIIIIIII', neutral_mips, offset, *fields)
    # RET entry points: inert data controls, not executable network clients.
    ua = b'User-Agent:Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)\0'
    generic = (b'Network Services\0%u.%u.%u.%u:%u\0WS2_32.dll\0'
               b'socket\0connect\0WSAStartup\0'
               b'Software\\Microsoft\\Windows\\CurrentVersion\\Run\0')
    cases = {
        'mips-original.elf': mips,
        'mips-no-read-helper.elf': mips.replace(b'read_and_send\0', b'read_and_wait\0'),
        'storm-original.dll': storm,
        'storm-no-raw-udp.dll': storm.replace(
            bytes.fromhex('53 53 53 6a 11 6a 03 6a 02'),
            bytes.fromhex('53 53 53 6a 06 6a 03 6a 02')),
        'storm-no-burst.dll': storm.replace(
            bytes.fromhex('6a 0c 5e 8d 45 e8 6a 10'),
            bytes.fromhex('6a 01 5e 8d 45 e8 6a 10')),
        'agent-original.exe': agent,
        'agent-no-module-command.exe': patch_agent(0x402914, b'\x3c\x88', b'\x3c\x87'),
        'agent-no-autostart.exe': patch_agent(0x4044ce, b'\x6a\x02', b'\x6a\x03'),
        'uploader-only.exe': wrapper[:0x3b000],
        'uploader-empty-overlay.exe': wrapper[:0x3b000] + bytes(len(agent)),
        'browser-user-agent.exe': image(b'.text', ua, 0x1000),
        'service-client-strings.exe': image(b'.data', generic, 0x1000),
        'neutral-http-mips.elf': bytes(neutral_mips),
        'redis-admin.sh': (b'#!/bin/sh\nredis-cli CONFIG SET dir /var/lib/redis\n'
                           b'redis-cli CONFIG SET dbfilename dump.rdb\nredis-cli SAVE\n'),
        'redis-ssh-config-only.sh': (b'#!/bin/sh\n'
                                    b'printf "CONFIG SET dir /root/.ssh\\n'
                                    b'CONFIG SET dbfilename authorized_keys\\nSAVE\\n"\n'),
    }
    paths = []
    for name, content in cases.items():
        path = scratch / name
        path.write_bytes(content)
        paths.append(str(path))
    completed = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', *paths,
    ], capture_output=True, text=True, check=True)
    (scratch / 'reports.jsonl').write_text(completed.stdout)
    (scratch / 'stderr.txt').write_text(completed.stderr)
    observed = reports(completed.stdout)
    for name in cases:
        traits = observed[name]
        if name.startswith('storm-'):
            assert STORM in traits, name
            assert (FLOOD in traits) == (name == 'storm-original.dll'), name
        elif name.startswith('agent-'):
            assert (C2 in traits) == (name != 'agent-no-module-command.exe'), name
            assert (SERVICE in traits) == (name == 'agent-original.exe'), name
        elif name.startswith('mips-'):
            assert (LOOT in traits) == (name == 'mips-original.elf'), name
        else:
            assert not [t for t in traits.values() if t['crit'] == 5], name
        if name == 'redis-admin.sh':
            assert 'micro-behaviors/data/db/redis::snapshot-path-configuration' in traits
            assert not [t for t in traits.values() if t['crit'] >= 4], name
    print(json.dumps({'cases': len(cases), 'failures': []}, indent=2))


if __name__ == '__main__':
    main()
