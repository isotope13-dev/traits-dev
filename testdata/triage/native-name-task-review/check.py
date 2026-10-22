"""Static controls for bound PR_SET_NAME and the 32-bit parser prologue.

Usage: check.py RECEIVE_SYSCALL_CHANGED_ELF --scratch DIRECTORY
Never executes samples or control code. Mutations are analysis fixtures,
not recovered originals.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
NAME = 'micro-behaviors/process/info/current::x64-pr-set-name-call'
ALIAS = 'objectives/evasion/masquerade/process/system-name::native-credential-scanner-daemon-aliases'
TASK = 'objectives/command-and-control/botnet/iot::x86-64-framed-attack-task-code'
BOT = 'objectives/command-and-control/botnet/iot::x86-64-framed-credential-bot'
SCAN = 'objectives/lateral-movement/brute-force/iot-creds::x64-hidden-telnet-credential-scanner'
FLOODS = {
    'objectives/impact/dos/udp-flood::hidden-credential-udp-flood-code',
    'objectives/impact/dos/udp-flood::hidden-credential-raw-udp-flood-code',
}


def call(data, offset, target):
    assert data[offset] == 0xe8
    struct.pack_into('<i', data, offset + 1, target - offset - 5)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('sample', type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    original = args.sample.read_bytes()
    assert hashlib.sha256(original).hexdigest() == (
        'ab85300d52e9faf318fd3d2c54f1767852c5792acfdac5c5e518501ddb12742b')
    args.scratch.mkdir(parents=True, exist_ok=True)
    cases = {}

    def add(name, data, yes=(), no=()):
        p = args.scratch / (name + '.elf')
        p.write_bytes(data)
        cases[str(p)] = (set(yes), set(no))

    retained = {NAME, ALIAS, SCAN} | FLOODS
    add('changed-receive-syscall', original, retained, [TASK, BOT])
    normal = bytearray(original)
    normal[0xb460] = 45  # Restore recvfrom only in this labeled control.
    add('canonical-parser', normal, retained | {TASK, BOT})
    changed = bytearray(normal)
    call(changed, 0x5ba1, 0x411)
    add('parser-32-bit-first-save', changed, retained | {TASK, BOT})
    changed = bytearray(normal)
    call(changed, 0x5ba1, 0xb44b)  # ret: no parser invocation.
    add('parser-returns-without-parsing', changed, retained, [TASK, BOT])
    changed = bytearray(normal)
    call(changed, 0x5b85, 0xb44b)
    add('body-receive-returns', changed, retained, [TASK, BOT])
    changed = bytearray(normal)
    call(changed, 0x5b36, 0xb44b)
    # EAX retains the nonzero length across the bypassed availability peek;
    # consuming the header and receiving the body still reach the parser.
    add('body-peek-returns', changed, retained | {TASK, BOT})
    changed = bytearray(normal)
    call(changed, 0x5b36, 0x9258)  # An arbitrary wrapper is not a peek bypass.
    add('body-peek-other-operation', changed, retained, [TASK, BOT])
    changed = bytearray(normal)
    changed[0x5390:0x5390 + 2] = bytes.fromhex('33 c0')
    add('unrelated-instruction-change', changed, retained | {TASK, BOT})
    changed = bytearray(original)
    assert changed[0x53ab] == 15
    changed[0x53ab] = 4  # PR_SET_DUMPABLE is not PR_SET_NAME.
    add('other-prctl-operation', changed, {SCAN} | FLOODS, [NAME, ALIAS])
    changed = bytearray(original)
    call(changed, 0x53b4, 0xb44c)
    add('name-call-target-is-recv', changed, {SCAN} | FLOODS, [NAME, ALIAS])
    changed = bytearray(original)
    changed[0x9260] = 1  # Wrapper invokes write, not prctl.
    add('wrapper-is-not-prctl', changed, {SCAN} | FLOODS, [NAME, ALIAS])
    changed = bytearray(original)
    changed[0xede8:0xef35] = bytes(0xef35 - 0xede8)
    add('name-setting-without-credentials', changed, [NAME], [ALIAS, SCAN])
    # Keep only the neutral operation, at different addresses, with neither
    # credential data nor daemon aliases. It remains notable, not masquerade.
    changed = bytearray(original)
    changed[0x100:0xed76] = bytes(0xed76 - 0x100)
    changed[0xeda0:0x108d0] = bytes(0x108d0 - 0xeda0)
    changed[0x1000:0x100f] = original[0x53aa:0x53b9]
    changed[0x1100:0x110e] = original[0x9258:0x9266]
    call(changed, 0x100a, 0x1100)
    add('isolated-relocated-name-setter', changed, [NAME], [ALIAS, SCAN, TASK, BOT])
    add('patterns-outside-text', original.replace(b'\0.text\0', b'\0.blob\0'),
        no=[NAME, ALIAS, TASK, BOT])
    changed = bytearray(original)
    struct.pack_into('<H', changed, 18, 183)
    add('other-architecture', changed, no=[NAME, ALIAS, TASK, BOT])
    for relative in ['testdata/benign/taxonomy-map-unmap.elf',
                     'testdata/taxonomy/native-byte-evidence-review/socket-wrapper.elf',
                     'testdata/native-loader-first-review/honest-busybox-updater.elf']:
        cases[str(ROOT / relative)] = (set(), {NAME, ALIAS, TASK, BOT})

    result = subprocess.run([
        args.cleave, '--traits-dir', str(ROOT), '--disable',
        'radare2,upx,third-party', '--format', 'json', *cases,
    ], capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    output = result.stdout
    seen = set()
    rows = []
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        for f in report['files']:
            path = f['path']
            if path not in cases:
                continue
            yes, no = cases[path]
            ids = {t['id'] for t in f.get('traits', [])}
            assert yes <= ids, (path, 'missing', yes - ids)
            assert not no & ids, (path, 'unexpected', no & ids)
            seen.add(path)
            rows.append({'file': Path(path).name, 'passed': True})
    assert seen == set(cases), set(cases) - seen
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
