#!/usr/bin/env python3
"""Static controls for socketcall dispatch, XMRig identity, and RPC bodies.
Generated ELF entries return immediately; fixture instruction tails are inert.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
PREFIX = 'micro-behaviors/communications/socket/'
SOCKET = PREFIX + 'create::i386-socketcall-socket'
BIND = PREFIX + 'bind/function::i386-socketcall-bind'
CONNECT = PREFIX + 'connect::i386-socketcall-connect'
ARM32 = PREFIX + 'create::arm-socket-literal-syscall-wrapper'
ARM_META = 'metadata/arch/arm::arm'
ARM64 = PREFIX + 'create::aarch64-socket-syscall-wrapper'
IDENTITY = 'well-known/app/finance/xmrig::xmrig-binary-markers'
HEARTBEAT = 'micro-behaviors/communications/rpc::jsonrpc-keepalive-request-body'
TCP_SCHEME = 'micro-behaviors/communications/url/scheme::stratum-tcp-url'
TLS_SCHEME = 'micro-behaviors/communications/url/scheme::stratum-ssl-url'
MERGED = PREFIX + 'connect::socket-connect-function-call'
OLD = {PREFIX + 'syscall::' + x for x in (
    'i386-socketcall-socket', 'i386-socketcall-bind',
    'i386-socketcall-connect', 'aarch64-socket-syscall-wrapper')}


def elf(code=b'', rodata=b'', arm64=False, arm=False):
    b = bytearray(2048)
    names = b'\0.text\0.rodata\0.shstrtab\0'
    b[0x500:0x500 + len(names)] = names
    if arm64:
        b[:16] = b'\x7fELF\x02\x01\x01' + bytes(9)
        struct.pack_into('<HHIQQQIHHHHHH', b, 16, 2, 183, 1, 0x400100,
                         0, 0x600, 0, 64, 0, 0, 64, 4, 3)
        entry = bytes.fromhex('c0 03 5f d6')
        for i, (name, flags, addr, off, size) in enumerate([
            (1, 6, 0x400100, 0x100, len(entry) + len(code)),
            (7, 2, 0x400200, 0x200, len(rodata)),
            (15, 0, 0, 0x500, len(names)),
        ], 1):
            struct.pack_into('<IIQQQQIIQQ', b, 0x600 + i * 64,
                             name, 3 if i == 3 else 1, flags, addr,
                             off, size, 0, 0, 4, 0)
    else:
        b[:16] = b'\x7fELF\x01\x01\x01' + bytes(9)
        struct.pack_into('<HHIIIIIHHHHHH', b, 16, 2, 40 if arm else 3, 1, 0x8048100,
                         0, 0x600, 0, 52, 0, 0, 40, 4, 3)
        entry = bytes.fromhex('1e ff 2f e1') if arm else b'\xc3'
        for i, (name, flags, addr, off, size) in enumerate([
            (1, 6, 0x8048100, 0x100, len(entry) + len(code)),
            (7, 2, 0x8048200, 0x200, len(rodata)),
            (15, 0, 0, 0x500, len(names)),
        ], 1):
            struct.pack_into('<IIIIIIIIII', b, 0x600 + i * 40,
                             name, 3 if i == 3 else 1, flags, addr,
                             off, size, 0, 0, 4, 0)
    b[0x100:0x100 + len(entry) + len(code)] = entry + code
    b[0x200:0x200 + len(rodata)] = rodata
    return b


def main():
    socket = bytes.fromhex('BA 01 00 00 00') + b'\x90'*8 + bytes.fromhex(
        'B8 66 00 00 00 87 DA 65 FF 15 10 00 00 00 87 DA')
    bind = bytes.fromhex('B8 66 00 00 00 BA 02 00 00 00') + b'\x90'*8 + bytes.fromhex(
        '87 DA 65 FF 15 10 00 00 00 87 DA')
    connect = bytes.fromhex(
        '6A 00 6A 00 6A 00 6A 00 8D 44 24 1C 50 6A 03 6A 66 E8 00 00 00 00')
    arm64 = bytes.fromhex('C8 18 80 D2 01 00 00 D4')
    arm32 = bytes.fromhex('84 70 9F E5 03 40 A0 E1 03 50 A0 E1 00 00 00 EF') + bytes(124) + bytes.fromhex('19 01 00 00')
    old_arm32 = bytes.fromhex('28 70 9F E5 00 00 00 EF') + bytes(40) + bytes.fromhex('19 01 00 00')
    markers = b'xmrig\0XMRIG_EXE_DIR\0dev donate started\0'
    keepalive = b'{"id":1,"jsonrpc":"2.0","method":"keepalived","params":{"id":"%s"}}\0'
    cases = [
        ('socket', elf(socket), {SOCKET}, {BIND, CONNECT}),
        ('socket-other-selector', elf(socket.replace(b'\xba\x01', b'\xba\x02')), set(), {SOCKET}),
        ('socket-wrong-syscall', elf(socket.replace(b'\xb8\x66', b'\xb8\x65')), set(), {SOCKET}),
        ('socket-no-dispatch', elf(socket[:-11]), set(), {SOCKET}),
        ('bind', elf(bind), {BIND}, {SOCKET, CONNECT}),
        ('bind-other-selector', elf(bind.replace(b'\xba\x02', b'\xba\x03')), set(), {BIND}),
        ('connect', elf(connect), {CONNECT}, {SOCKET, BIND}),
        ('connect-other-selector', elf(connect.replace(b'\x6a\x03', b'\x6a\x02')), set(), {CONNECT}),
        ('connect-wrong-syscall', elf(connect.replace(b'\x6a\x66', b'\x6a\x65')), set(), {CONNECT}),
        ('generic-calls', elf(bytes.fromhex('6A 01 E8 00000000 6A 02 E8 00000000 6A 03 E8 00000000')),
         set(), {SOCKET, BIND, CONNECT}),
        ('data-collision', elf(rodata=socket + bind + connect), set(), {SOCKET, BIND, CONNECT}),
        ('arm32-socket', elf(arm32, arm=True), {ARM32, ARM_META}, set()),
        ('arm32-old-wrapper', elf(old_arm32, arm=True), {ARM32}, set()),
        ('arm32-wrong-literal', elf(arm32[:-4] + bytes.fromhex('1A 01 00 00'), arm=True), set(), {ARM32}),
        ('arm32-wrong-pool-distance', elf(arm32.replace(bytes.fromhex('84 70 9F E5'), bytes.fromhex('80 70 9F E5')), arm=True), set(), {ARM32}),
        ('arm32-data-collision', elf(rodata=arm32, arm=True), set(), {ARM32}),
        ('arm32-wrong-architecture', elf(arm32), set(), {ARM32, ARM_META}),
        ('arm64-socket', elf(arm64, arm64=True), {ARM64}, set()),
        ('arm64-other-syscall', elf(arm64.replace(b'\xc8\x18', b'\xe8\x18'), arm64=True), set(), {ARM64}),
        ('arm64-data-collision', elf(rodata=arm64, arm64=True), set(), {ARM64}),
        ('identity', elf(rodata=markers), {IDENTITY}, set()),
        ('name-reference', elf(rodata=b'xmrig\0'), set(), {IDENTITY}),
        ('missing-donation-marker', elf(rodata=b'xmrig\0XMRIG_EXE_DIR\0'), set(), {IDENTITY}),
        ('missing-path-marker', elf(rodata=b'xmrig\0dev donate started\0'), set(), {IDENTITY}),
        ('stratum-schemes', elf(rodata=b'stratum+tcp://\0stratum+ssl://\0'), {TCP_SCHEME, TLS_SCHEME}, {SOCKET, CONNECT, BIND}),
        ('other-url-scheme', elf(rodata=b'https://example.com\0'), set(), {TCP_SCHEME, TLS_SCHEME}),
        ('heartbeat', elf(rodata=keepalive), {HEARTBEAT}, set()),
        ('different-rpc', elf(rodata=keepalive.replace(b'keepalived', b'initialize')), set(), {HEARTBEAT}),
        ('name-only-rpc', elf(rodata=b'keepalived\0'), set(), {HEARTBEAT}),
    ]
    with tempfile.TemporaryDirectory(prefix='xmrig-controls-') as tmp:
        tmp = Path(tmp)
        controls = {}
        for name, data, yes, no in cases:
            path = tmp / (name + '.elf')
            path.write_bytes(data)
            controls[str(path)] = (name, yes, no | OLD)
        for ext, source in [('c', 'void f(void) { socket_connect(fd, addr); }'),
                            ('php', '<?php socket_connect($s, "127.0.0.1", 3333);')]:
            path = tmp / ('function-call.' + ext)
            path.write_text(source)
            controls[str(path)] = ('function-call.' + ext, {MERGED}, set())
        r = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json',
                            *controls], text=True, capture_output=True)
        assert r.returncode == 0, r.stderr + r.stdout
        decoder = json.JSONDecoder()
        remaining = r.stdout.lstrip()
        report = {'files': []}
        while remaining:
            item, end = decoder.raw_decode(remaining)
            report['files'].extend(item.get('files', []))
            remaining = remaining[end:].lstrip()
        seen = set()
        for f in report['files']:
            name, yes, no = controls[f['path']]
            got = {t['id'] for t in f.get('traits', [])}
            assert yes <= got, (name, 'missing', yes - got)
            assert not no & got, (name, 'unexpected', no & got)
            seen.add(f['path'])
            print('PASS', name)
        assert seen == set(controls)
        print(f'{len(seen)} static controls passed')


if __name__ == '__main__':
    main()
