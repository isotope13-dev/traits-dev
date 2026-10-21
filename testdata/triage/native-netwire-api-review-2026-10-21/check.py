"""Static mutation controls; never execute a specimen.

Pass the reviewed 05fccd853803 carrier, an official AutoIt3.exe, and a scratch
work directory. The additional Elex positive comes from the repository.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
KEY = 'objectives/collection/keylog/device::native-translated-scrambled-key-log'
CODE = 'objectives/collection/keylog/device::native-translated-scrambled-key-write-code'
CODEC = 'micro-behaviors/data/encoding/substitution::x86-rotated-64-symbol-substitution'
ELEX = 'well-known/malware/trojan/elex/identity::elex-resource-dll-renamed-rundll32-scrambled'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sample', type=Path, required=True)
    ap.add_argument('--runtime', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    ap.add_argument('--smb-sample', type=Path)
    ap.add_argument('--smb-only', action='store_true')
    args = ap.parse_args()
    carrier = args.sample.read_bytes()
    assert hashlib.sha256(carrier).hexdigest() == '05fccd8538039ce87628bf19df2f634a65dda41e001d6164c779635e4bca8b4a'
    original = carrier[0x10a4d4:0x10a4d4+180224]
    assert original[:2] == b'MZ'
    positive = {KEY, CODE, CODEC}
    cases = [('payload.exe', original, positive, set())]

    def mutate(name, changes, present=None, absent=None):
        data = bytearray(original)
        for va, expected, replacement in changes:
            at = va - 0x400000 - 0xc00  # .text raw/RVA delta
            assert data[at:at+len(expected)] == expected, name
            assert len(expected) == len(replacement)
            data[at:at+len(expected)] = replacement
        cases.append((name, bytes(data), positive if present is None else present,
                      set() if absent is None else absent))

    # Different XOR/add constants preserve the recording technique.
    mutate('alternate-scramble.exe', [(0x40d732, b'\x9d', b'\x81'),
                                     (0x40d735, b'\x24', b'\x30')])
    for name, va in [('unbound-log-call.exe', 0x40e111),
                     ('unbound-scramble-call.exe', 0x40d9cd),
                     ('unbound-key-handler.exe', 0x40e27a)]:
        at = va-0x400000-0xc00
        mutate(name, [(va, original[at:at+4], bytes(4))], {CODEC}, {KEY, CODE})
    mutate('toascii-thunk-rebound.exe', [(0x41d1c6, struct.pack('<I', 0x429564),
                                        struct.pack('<I', 0x429528))], {CODEC}, {KEY, CODE})
    mutate('writefile-thunk-rebound.exe', [(0x41cf16, struct.pack('<I', 0x429484),
                                          struct.pack('<I', 0x429460))], {CODEC}, {KEY, CODE})
    mutate('non-keyboard-raw-input.exe', [(0x40e24c, b'\x01', b'\x02')], {CODEC}, {KEY, CODE})
    # Keep device code but remove the required recording context.
    changed = original.replace(b'[Log Started] - [%', b'[New Session] - [%')
    assert changed != original and len(changed) == len(original)
    cases.append(('no-session-log.exe', changed, {CODEC}, {KEY, CODE}))
    mutate('different-table-modulus.exe', [(0x40b7ba, b'\x3f', b'\x7f')], {KEY, CODE}, {CODEC})
    cases.append(('official-runtime.exe', args.runtime.read_bytes(), set(), positive))
    elex = lzma.decompress((ROOT/'testdata/hostile/elex-scrambled-resource-dropper.exe.xz').read_bytes())
    cases.append(('external-elex-positive.exe', elex, {ELEX}, positive))
    if args.smb_sample:
        smb = args.smb_sample.read_bytes()
        assert hashlib.sha256(smb).hexdigest() == 'c2527a8094cb6c94989a8ec00f0a8848f87eb86a2c47d2c97385cda9fc7926a0'
        trait = 'objectives/lateral-movement/brute-force/smb::native-ipc-share-credential-pair-loop'
        if args.smb_only:
            cases = []
        cases.append(('smb-positive.exe', smb, {trait}, set()))
        data = bytearray(smb)
        data[0x5fa4:0x5fa8] = bytes(4)
        cases.append(('smb-unbound-helper.exe', bytes(data), set(), {trait}))
        # Keep all addresses valid: replace just one byte of the API name.
        data = smb.replace(b'WNetAddConnection2A', b'XNetAddConnection2A')
        cases.append(('smb-unrelated-api.exe', data, set(), {trait}))
        data = bytearray(smb)
        assert data[0x5fb4:0x5fb6] == b'\xc7\x04'
        data[0x5fb5] = 8  # breaks the independent username-list advance
        cases.append(('smb-no-username-loop.exe', bytes(data), set(), {trait}))
    args.work_dir.mkdir(parents=True, exist_ok=True)

    def scan(case):
        name, data, present, absent = case
        path = args.work_dir/name
        path.write_bytes(data)
        proc = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--json', str(path)],
                              capture_output=True, text=True, check=True, cwd=ROOT)
        (args.work_dir/(name+'.json')).write_text(proc.stdout)
        (args.work_dir/(name+'.stderr')).write_text(proc.stderr)
        report = json.loads(proc.stdout)
        ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
        return {'case': name, 'pass': present <= ids and not absent & ids,
                'missing': sorted(present-ids), 'unexpected': sorted(absent & ids)}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(scan, cases))
    summary = {'passed': sum(x['pass'] for x in results), 'total': len(results), 'cases': results}
    (args.work_dir/'results.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    assert all(x['pass'] for x in results)


if __name__ == '__main__':
    main()
