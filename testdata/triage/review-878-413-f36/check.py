"""Check footer-fragment placement with inert controls; never execute a PE.

Usage: python3 check.py SAMPLE_878 --out SCRATCH_DIR [--cleave cleave]
"""
import argparse
import json
from pathlib import Path
import re
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'metadata/binary/instruction::'
ATOMS = {
    'x64-indirect-call-result-zero-edx-fragment': (0x2a282, 23),
    'x64-tail-pair-read-decrement-fragment': (0x2a2e5, 23),
    'x64-paired-four-byte-call-setups': (0x2a376, 46),
    'x64-counter-stride-loop-fragment': (0x2a423, 32),
}
GROUP = PREFIX + 'x64-tail-read-paired-call-fragments'
ALTERNATIVES = PREFIX + 'x64-tail-call-loop-fragments'
OBJECTIVE = 'objectives/impact/dos/resource::trailer-counter-self-replica-launch'


def inert_image(source, distant=False, missing_read=False, section=b'UPX0'):
    data = bytearray(0x1200)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x20b)
    struct.pack_into('<I', data, opt + 16, 0x1000)
    struct.pack_into('<Q', data, opt + 24, 0x140000000)
    for off, value in {32: 0x1000, 36: 0x200, 56: 0x2000,
                       60: 0x200, 108: 16}.items():
        struct.pack_into('<I', data, opt + off, value)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<8sIIIIIIHHI', data, opt + 240, section, 0x1000,
                     0x1000, 0x1000, 0x200, 0, 0, 0, 0, 0x60000020)
    data[0x200] = 0xc3  # RET; fragments below are unreachable fixture data.
    positions = [0x240, 0x300, 0x840 if distant else 0x380, 0x420]
    for (name, (offset, length)), dest in zip(ATOMS.items(), positions):
        data[dest:dest + length] = source[offset:offset + length]
        if missing_read and name == 'x64-tail-pair-read-decrement-fragment':
            data[dest] = 0x90
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sample', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    source = args.sample.read_bytes()
    atoms = {PREFIX + name for name in ATOMS}
    altered = bytearray(source)
    altered[0x2a423] = 0x90
    cases = [
        ('sample', source, atoms | {GROUP, OBJECTIVE}, set()),
        ('sample-no-counter-loop', bytes(altered),
         (atoms - {PREFIX + 'x64-counter-stride-loop-fragment'}) | {GROUP},
         {PREFIX + 'x64-counter-stride-loop-fragment', OBJECTIVE}),
        ('inert-fragments', inert_image(source), atoms | {GROUP}, {OBJECTIVE}),
        ('distant-write-fragment', inert_image(source, distant=True), atoms,
         {GROUP, OBJECTIVE}),
        ('missing-read-fragment', inert_image(source, missing_read=True),
         atoms - {PREFIX + 'x64-tail-pair-read-decrement-fragment'},
         {GROUP, OBJECTIVE, PREFIX + 'x64-tail-pair-read-decrement-fragment'}),
        ('different-section', inert_image(source, section=b'.text'), set(),
         atoms | {GROUP, OBJECTIVE}),
    ]
    results = []
    for name, data, present, absent in cases:
        if atoms & present:
            present = present | {ALTERNATIVES}
        else:
            absent = absent | {ALTERNATIVES}
        path = args.out / (name + '.exe')
        path.write_bytes(data)
        # Component composites can be omitted from rendered findings when
        # their objective does not fire. Trace evaluation itself to test the
        # preserved proximity and scope, independently of output filtering.
        selected = ','.join(sorted(atoms | {GROUP, ALTERNATIVES, OBJECTIVE}))
        run = subprocess.run([args.cleave, '--traits-dir', str(ROOT),
                              'test-rules', str(path), '--rules', selected],
                             capture_output=True, text=True, check=True, timeout=300)
        (args.out / (name + '.trace.txt')).write_text(run.stdout)
        ids = set(re.findall(r'^MATCHED (\S+)', run.stdout, re.MULTILINE))
        assert present <= ids, (name, 'missing', present - ids)
        assert not absent & ids, (name, 'unexpected', absent & ids)
        results.append({'case': name, 'passed': True,
                        'required_present': sorted(present),
                        'required_absent': sorted(absent)})
    (args.out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Passed {len(results)} controls')


if __name__ == '__main__':
    main()
