"""Static regression checks for the reviewed wheel, Fabric JAR and IoT bot.

Run with the three original sample paths. Never execute a specimen.
"""
import argparse
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
TASK = 'objectives/command-and-control/botnet/iot::x86-64-framed-attack-task-code'
BOT = 'objectives/command-and-control/botnet/iot::x86-64-framed-credential-bot'
REMOTE = 'objectives/impact/dos/attack/botnet::x86-64-framed-udp-flood'
LOCAL = 'objectives/impact/dos/udp-flood::hidden-credential-udp-flood-code'
POST = 'objectives/exfiltration/stealer/token::minecraft-token-handoff-raw-tls-post'
HANDOFF = 'objectives/credential-access/gaming/minecraft::minecraft-token-jar-handoff'
MEMBER = 'metadata/package/files/name::libseal-container-member'
SEALED = 'micro-behaviors/os/module/load::python-libseal-load-call'
STATIC = 'objectives/command-and-control/botnet/iot::static-iot-watchdog-c2-bot'


def repack(raw, skip=(), replace=None):
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(raw)) as source, zipfile.ZipFile(output, 'w') as dest:
        for item in source.infolist():
            if any(item.filename.endswith(x) for x in skip):
                continue
            data = source.read(item)
            if replace:
                data = data.replace(*replace)
            dest.writestr(item, data)
    return output.getvalue()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('wheel', type=Path)
    ap.add_argument('jar', type=Path)
    ap.add_argument('elf', type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    cases = {}

    def add(name, data, yes=(), no=()):
        cases[name] = (bytes(data), set(yes), set(no))

    elf = args.elf.read_bytes()
    add('original.elf', elf, [TASK, BOT, REMOTE, LOCAL, STATIC])
    # Relative targets, rather than incidental presence of a recv wrapper.
    for name, offset in [('peek', 0x53ef), ('length', 0x5414),
                         ('body', 0x5440), ('parser', 0x545e)]:
        changed = bytearray(elf)
        assert changed[offset] == 0xe8
        struct.pack_into('<i', changed, offset + 1, 0x9008 - offset - 5)
        add('redirect-' + name + '.elf', changed, [LOCAL], [TASK, BOT, REMOTE, STATIC])
    changed = bytearray(elf)
    changed[0x53bb + 159] ^= 0x10
    add('different-parser-buffer.elf', changed, [LOCAL], [TASK, BOT, REMOTE, STATIC])
    changed = bytearray(elf)
    for offset in [40, 104, 159]:
        changed[0x53bb + offset] = 0x20
    add('alternate-body-offset.elf', changed, [TASK, BOT, REMOTE, LOCAL, STATIC])
    # All former static-bot predicates survive with no task/scanner code.
    changed = bytearray(elf)
    changed[0x100:0xb616] = bytes(0xb616 - 0x100)
    changed[0xb9af:0xbc00] = bytes(0xbc00 - 0xb9af)
    add('watchdog-address-only.elf', changed, [
        'metadata/binary/symbols/table::full-symbol-table-absent-or-empty',
        'metadata/binary/linking/dynamic::elf-needed-libs-zero',
        'micro-behaviors/communications/ip/literal::external-ipv4-shaped-text-binary',
        'micro-behaviors/fs/path/device/special::multi-watchdog-device-cluster',
        'metadata/arch/x86::elf-machine-x86-64-value',
    ], [TASK, BOT, REMOTE, LOCAL, STATIC])
    changed = bytearray(elf)
    struct.pack_into('<H', changed, 18, 183)
    add('wrong-architecture.elf', changed, no=[TASK, BOT, REMOTE, LOCAL])
    changed = elf.replace(b'\0.text\0', b'\0.blob\0')
    add('outside-text.elf', changed, no=[TASK, BOT, REMOTE, LOCAL])

    jar = args.jar.read_bytes()
    add('original.jar', jar, [POST, HANDOFF])
    add('without-transport.jar', repack(jar, skip=('/$.class',)), [HANDOFF], [POST])
    add('without-token-source.jar', repack(jar, replace=(b'method_1674', b'method_1675')), no=[POST, HANDOFF])
    with zipfile.ZipFile(io.BytesIO(jar)) as z:
        helper = next(n for n in z.namelist() if n.endswith('/$.class'))
        add('transport-only.class', z.read(helper), no=[POST, HANDOFF])

    add('original.whl', args.wheel.read_bytes(), [MEMBER])
    for name, member, yes in [('sealed-name.zip', 'plugin.libseal', [MEMBER]),
                              ('suffix-near-miss.zip', 'plugin.libseal.txt', [])]:
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w') as z:
            z.writestr(member, 'ordinary data: suffix is not proof of encryption')
        add(name, out.getvalue(), yes, [] if yes else [MEMBER])
    add('sealed-api.py', b'from libseal import load_sealed_sync\nm = load_sealed_sync(file=p, module_path="plugin", password=k)\n', [SEALED])
    add('sealed-import-only.py', b'from libseal import load_sealed_sync\n', no=[SEALED])

    with tempfile.TemporaryDirectory(prefix='fallout-controls-', dir=args.scratch) as tmp:
        paths = []
        for name, (data, _, _) in cases.items():
            path = Path(tmp, name)
            path.write_bytes(data)
            paths.append(str(path))
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--no-update-check',
                                 '--disable', 'radare2,upx,third-party', '--format', 'json',
                                 *paths], capture_output=True, text=True, check=True)
        remaining = result.stdout.lstrip()
        decoder = json.JSONDecoder()
        files = {}
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.update({Path(f['path']).name: f for f in report['files']})
            remaining = remaining[end:].lstrip()
        records = []
        for name, (_, yes, no) in cases.items():
            found = {t['id'] for t in files[name].get('traits', [])}
            assert yes <= found, (name, 'missing', sorted(yes - found))
            assert not no & found, (name, 'unexpected', sorted(no & found))
            records.append({'case': name, 'required': sorted(yes), 'absent': sorted(no), 'passed': True})
            print('PASS', name)
        Path(args.scratch, 'controls.json').write_text(json.dumps(records, indent=2) + '\n')
    print(len(cases), 'static controls passed')


if __name__ == '__main__':
    main()
