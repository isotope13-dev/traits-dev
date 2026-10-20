"""Static controls for native implant admission and managed module constructors.

Generated binaries have no payload or useful entry point and are never executed.
Run with --scratch pointing to a disposable directory outside the trait tree.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CTOR = 'micro-behaviors/process/lifecycle/auto-exec::dotnet-module-initializer'
REPEATED = 'metadata/binary/layout/embedded::repeated-reference-assembly-attributes'
KILLER = 'objectives/impact/degrade/rival-bot/competitor::static-elf-rival-miner-proc-bot'
CRON = 'objectives/persistence/system/cron/job::rival-killer-crontab-persistence'
INIT = 'objectives/persistence/system/init/script::startup-script-dropin-shell-launch'
XOR = 'micro-behaviors/data/encoding/xor::mips-cyclic-byte-xor-mix'
HEX = 'micro-behaviors/data/decode/hex::mips-hex-pair-byte-store-loop'
RETIRED = {
    'objectives/command-and-control/backdoor/listener::mips-static-listener-shell-backdoor',
    'objectives/command-and-control/backdoor/evasive::mips-watchdog-self-locating-backdoor',
    'objectives/command-and-control/botnet/iot::mips-watchdog-implant',
    'objectives/command-and-control/infrastructure/ip-port::static-stripped-elf-watchdog-external-c2',
}
spec = importlib.util.spec_from_file_location('pe_controls', ROOT / 'testdata/managed-records-review/verify.py')
pe_controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pe_controls)


def managed(module=True, attribute=True):
    strings = b'\0control\0<Module>\0.cctor\0Plain\0ModuleInitializerAttribute\0Object\0System\0'
    ix = lambda s: strings.index(s.encode() + b'\0')
    valid = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 4) | (1 << 6) | (1 << 32)
    tables = bytearray(struct.pack('<IBBBBQQ', 0, 2, 0, 0, 1, valid, valid))
    tables += struct.pack('<IIIIII', 1, 1, 2, 0, 1, 1)
    tables += struct.pack('<HHHHH', 0, ix('control'), 1, 0, 0)
    tables += struct.pack('<HHH', 0, ix('Object'), ix('System'))
    tables += struct.pack('<IHHHHH', 0, ix('<Module>'), 0, 0, 1, 1)
    tables += struct.pack('<IHHHHH', 0, ix('Plain'), 0, 0, 1, 2 if module else 1)
    tables += struct.pack('<IHHHHH', 0x1100, 0, 0x1891, ix('.cctor'), 1, 1)
    tables += struct.pack('<IHHHHIHHH', 0x8004, 1, 0, 0, 0, 0, 0, ix('control'), 0)
    streams = [('#~', bytes(tables)),
               ('#Strings', strings if attribute else strings.replace(b'ModuleInitializerAttribute', b'X' * len(b'ModuleInitializerAttribute'))),
               ('#Blob', b'\0\x03\x00\x00\x01'), ('#GUID', bytes(range(16)))]
    root = bytearray(b'BSJB' + struct.pack('<HHII', 1, 1, 0, 12) +
                     b'v4.0.30319\0\0' + struct.pack('<HH', 0, len(streams)))
    offset = len(root) + sum(8 + ((len(n) + 4) & ~3) for n, _ in streams)
    data = bytearray()
    for name, body in streams:
        root += struct.pack('<II', offset + len(data), len(body))
        encoded = name.encode() + b'\0'
        root += encoded + bytes((-len(encoded)) % 4)
        data += body + bytes((-len(body)) % 4)
    metadata = root + data
    result = pe_controls.build_pe([], b'\x06\x2a')  # Tiny IL method: ret.
    struct.pack_into('<II', result, 0x218, 0x1400, len(metadata))
    result[0x600:0x600 + len(metadata)] = metadata
    return result


def elf(code, strings):
    names = b'\0.text\0.rodata\0.shstrtab\0'
    data = bytearray(0x100) + code
    ro = len(data)
    data += strings
    shstr = len(data)
    data += names
    data += bytes((-len(data)) % 4)
    shoff = len(data)
    data += bytes(40)
    for name, kind, flags, address, off, size in [
        (1, 1, 6, 0x400100, 0x100, len(code)),
        (7, 1, 2, 0x400000 + ro, ro, len(strings)),
        (15, 3, 0, 0, shstr, len(names)),
    ]:
        data += struct.pack('>IIIIIIIIII', name, kind, flags, address, off, size, 0, 0, 4, 0)
    data[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', data, 16, 2, 8, 1, 0, 0, shoff,
                     0x70001007, 52, 32, 0, 40, 4, 3)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, body, want=(), reject=()):
        path = args.scratch / name
        path.write_bytes(body)
        cases.append((name, set(want), set(reject)))

    add('module.dll', managed(), [CTOR])
    add('attribute-only.dll', managed(False), [], [CTOR])
    add('module-no-attribute.dll', managed(True, False), [CTOR])
    for count in (7, 8):
        body = pe_controls.build_pe(['ReferenceAssemblyAttribute'] * count)
        add('repeated-%d.dll' % count, body, [REPEATED] if count == 8 else [],
            [REPEATED] if count == 7 else [])
    syscall = bytes.fromhex('24 02 0f c5 00 00 00 0c')
    call = bytes.fromhex('24 05 00 09 04 11 00 00 02 20 20 25')
    strings = b'cpuminer\0minerd\0xmrig\0/proc/net/tcp\0'
    cron = b'(crontab -l 2>/dev/null; echo x) | crontab -\0'
    init = b'init.groovy.d\0try{["/bin/sh","-c","nohup \0 >/dev/null 2>&1 &"].execute()}\0'
    add('names-without-kill.elf', elf(call, strings), reject=[KILLER, CRON, INIT])
    add('kill-without-call.elf', elf(syscall, strings), reject=[KILLER])
    add('killer.elf', elf(syscall + call, strings), [KILLER], [CRON, INIT])
    add('cron.elf', elf(syscall + call, strings + cron), [KILLER, CRON])
    add('init.elf', elf(syscall + call + bytes.fromhex('24 02 0f a4 00 00 00 0c'), strings + init),
        [KILLER, INIT])
    add('init-reference.elf', elf(syscall, init), reject=[KILLER, INIT])
    add('watchdog-library.elf', elf(syscall, b'/dev/watchdog\0/dev/misc/watchdog\0/proc/self/exe\0/bin/sh\0' + b'8.8.8.8:443\0'),
        reject=RETIRED | {KILLER, CRON, INIT})
    xor = bytes.fromhex('30 68 00 07 02 03 10 21 02 48 30 21 02 28 40 21 90 42 00 00 02 83 28 21 90 c6 00 00 24 63 00 01 02 62 10 26 00 46 10 26 91 06 00 00 00 46 10 26 14 64 ff f3 a0 a2 00 00')
    pair = bytes.fromhex('00 02 11 00 7c 03 1c 20 25 08 00 01 00 43 10 25 24 84 00 02 14 c8 ff ec a0 e2 00 00 03 e0 00 08 00 00 00 00 24 e9 ff 9f 2d 29 00 06')
    add('transforms.elf', elf(xor + pair, b'control\0'), [XOR, HEX])
    add('non-xor-non-pair.elf', elf(xor.replace(b'\x00\x46\x10\x26', b'\x00\x46\x10\x25') +
        pair.replace(b'\x24\x84\x00\x02', b'\x24\x84\x00\x01'), b'control\0'), reject=[XOR, HEX])
    run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--disable', 'third-party',
                          '--format', 'json', str(args.scratch)], capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError(run.stderr)
    reports, remaining = [], run.stdout.strip()
    decoder = json.JSONDecoder()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    files = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for report in reports for f in report['files']}
    for name, want, reject in cases:
        matched = files[name]
        assert want <= matched, (name, 'missing', want - matched)
        assert not reject & matched, (name, 'unexpected', reject & matched)
        assert not RETIRED & matched, (name, 'retired C2 claim')
        print('PASS', name)


if __name__ == '__main__':
    main()
