"""Static raw-UDP controls. No specimen or generated mutation is executed."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CAP = 'micro-behaviors/communications/flood::x64-bound-raw-udp-target-loop'
ATTACK = 'objectives/impact/dos/udp-flood::hidden-credential-raw-udp-flood-code'
OLD = 'micro-behaviors/communications/flood::x86-64-udp-flood-send-loop'
TASK = 'objectives/command-and-control/botnet/iot::x86-64-framed-attack-task-code'
SCAN = 'objectives/lateral-movement/brute-force/iot-creds::x64-hidden-telnet-credential-scanner'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('sample', type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    original = args.sample.read_bytes()
    assert hashlib.sha256(original).hexdigest() == 'c9018cee6b41d2664a06abe1a90aaa7d551f20af9abf33a139ec4361eb51fb18'
    cases = {}

    def add(name, data, yes=(), no=()):
        path = args.scratch / name
        path.write_bytes(data)
        cases[str(path)] = (set(yes), set(no))

    add('retained-raw-loop.elf', original, [CAP, ATTACK, TASK, SCAN], [OLD])
    # Restore the independently disabled connected-datagram send. Both packet
    # mechanisms must then be visible; this is a positive, not an original file.
    changed = bytearray(original)
    call = 0x336c
    assert changed[call] == 0xe8
    assert call + 5 + struct.unpack_from('<i', changed, call + 1)[0] == 0xb487
    struct.pack_into('<i', changed, call + 1, 0xb488 - call - 5)
    add('connected-send-restored.elf', changed, [CAP, ATTACK, TASK, SCAN, OLD])
    for label, call in [('raw-send', 0x3b22), ('raw-socket', 0x38b9)]:
        changed = bytearray(original)
        assert changed[call] == 0xe8
        struct.pack_into('<i', changed, call + 1, 0xb487 - call - 5)
        add(label + '-redirected.elf', changed, [TASK, SCAN], [CAP, ATTACK, OLD])
    for label, offset in [('descriptor-slot', 0x3af8),
                          ('counter-reset-slot', 0x3a3d),
                          ('counter-increment-slot', 0x3b2a),
                          ('counter-store-slot', 0x3b33),
                          ('outer-back-edge', 0x3b3e),
                          ('inner-back-edge', 0x3b36)]:
        changed = bytearray(original)
        changed[offset] ^= 0x10
        add(label + '.elf', changed, [TASK, SCAN], [CAP, ATTACK, OLD])
    changed = bytearray(original)
    changed[0x38a7] = 6  # TCP is not UDP.
    add('other-protocol.elf', changed, [TASK, SCAN], [CAP, ATTACK])
    changed = bytearray(original)
    changed[0xede8:0xefa0] = bytes(0xefa0 - 0xede8)
    add('packet-capability-without-credentials.elf', changed, [CAP, TASK], [ATTACK, SCAN])
    changed = original.replace(b'\0.text\0', b'\0.blob\0')
    add('outside-text.elf', changed, no=[CAP, ATTACK])
    changed = bytearray(original)
    struct.pack_into('<H', changed, 18, 183)
    add('other-architecture.elf', changed, no=[CAP, ATTACK])
    # Vary all counter slots coherently, and independently vary the socket slot.
    # Registers, offsets, addresses and filenames are not specimen identifiers.
    changed = bytearray(original)
    for offset in [0x3a3d, 0x3aee, 0x3b2a, 0x3b33]:
        assert changed[offset] == 0x54
        changed[offset] = 0x58
    for offset in [0x38c4, 0x3af8]:
        assert changed[offset] == 0x28
        changed[offset] = 0x2c
    add('alternate-consistent-slots.elf', changed, [CAP, ATTACK, TASK, SCAN], [OLD])
    for relative in ['testdata/benign/taxonomy-map-unmap.elf',
                     'testdata/taxonomy/native-byte-evidence-review/socket-wrapper.elf',
                     'testdata/native-loader-first-review/honest-busybox-updater.elf']:
        cases[str(ROOT / relative)] = (set(), {CAP, ATTACK})

    result = subprocess.run([args.cleave, '--traits-dir', str(ROOT),
                             '--disable', 'radare2,upx,third-party',
                             '--format', 'json', *cases],
                            capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.lstrip()
    files = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.update({f['path']: f for f in report['files']})
        remaining = remaining[end:].lstrip()
    records = []
    for path, (yes, no) in cases.items():
        found = {t['id'] for t in files[path].get('traits', [])}
        assert yes <= found, (path, 'missing', sorted(yes - found))
        assert not no & found, (path, 'unexpected', sorted(no & found))
        records.append({'case': Path(path).name, 'required': sorted(yes),
                        'forbidden': sorted(no), 'passed': True})
        print('PASS', Path(path).name)
    (args.scratch / 'results.json').write_text(json.dumps(records, indent=2) + '\n')
    print(len(records), 'static controls passed')


if __name__ == '__main__':
    main()
