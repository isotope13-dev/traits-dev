"""Exercise CLR interface/call binding and preserve the UPX overlay observation.

The mutated implant copies test matcher dependencies, not benign verdicts.
The Rifaien source is the independently traced self-submission utility.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CLR = 'micro-behaviors/process/interpreter/runtime/clr::native-appdomain-load-byte-array'
LAYOUT = 'metadata/binary/layout/overlay::writable-upx-with-substantial-opaque-overlay'
OLD = 'objectives/anti-static/pack/upx::writable-upx-with-substantial-opaque-overlay'
IID = bytes.fromhex('DC 96 F6 05 29 2B 63 36 AD 8B C4 38 9C F2 A7 13')
LOAD = bytes.fromhex('8B 38 8D 4C 24 34 8B E8 81 C7 B4 00 00 00')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rifaien', type=Path, required=True)
    parser.add_argument('--clr', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    native = args.clr.read_bytes()
    assert native.count(IID) == 1 and native.count(LOAD) == 1
    no_iid = native.replace(IID, bytes(16))
    no_load = native.replace(LOAD, LOAD.replace(b'\xB4', b'\xB8'))
    variant = bytearray(native)
    off = native.index(LOAD)
    variant[off + 5] = 0x38  # same operation, different local stack slot
    # The relative helper and IAT addresses are intentionally wildcarded.
    variant[off + 15:off + 19] = b'\x11\x22\x33\x44'
    rifaien = args.rifaien.read_bytes()
    cases = {
        'renamed-clr.exe': (native, {CLR}),
        'different-stack-and-helper.exe': (bytes(variant), {CLR}),
        'interface-only.exe': (no_load, set()),
        'call-sequence-only.exe': (no_iid, set()),
        'neither-clue.exe': (no_iid.replace(LOAD, bytes(len(LOAD))), set()),
        'self-submission.exe': (rifaien, {LAYOUT}),
        'self-submission-without-trailer.exe': (rifaien[:0x14C00], set()),
        'self-submission-zero-trailer.exe': (
            rifaien[:0x14C00] + bytes(len(rifaien) - 0x14C00), set()),
    }
    for filename, (data, _) in cases.items():
        (args.scratch / filename).write_bytes(data)

    def scan(item):
        filename, (_, expected) = item
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(args.scratch / filename)],
            check=True, text=True, capture_output=True)
        report = json.loads(result.stdout)
        ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
        assert OLD not in ids, (filename, 'retired objective remains')
        assert ids & {CLR, LAYOUT} == expected, (filename, expected, ids & {CLR, LAYOUT})
        (args.scratch / (filename + '.report.json')).write_text(result.stdout)
        return {'case': filename, 'expected': sorted(expected), 'passed': True}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(scan, cases.items()))
    (args.scratch / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Passed {len(results)} CLR and UPX boundary cases')


if __name__ == '__main__':
    main()
