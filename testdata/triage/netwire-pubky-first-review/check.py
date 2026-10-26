#!/usr/bin/env python3
"""Static regression checks; never executes the specimen or generated controls."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
KEYLOG = 'objectives/collection/keylog/device::native-translated-scrambled-key-log-data'
BROWSER = 'objectives/credential-access/browser/multi-target::native-keylogger-substituted-browser-password-stores'
PERSIST = 'objectives/persistence/login/registry/run-key::native-keylogger-substituted-run-persistence'
NEW = {KEYLOG, BROWSER, PERSIST}
OLD = {
    'objectives/credential-access/email/outlook::outlook-account-credential-harvest',
    'objectives/evasion/self-delete/file/delay::ping-delayed-batch-self-delete',
    'third_party/SigBase/Unspecified/Jan18',
    'well-known/malware/rat/netwire::native-netwire-payload',
    'well-known/malware/rat/netwire::native-netwire-proxy-rat',
}

def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        value, end = decoder.raw_decode(text.lstrip())
        yield value
        text = text.lstrip()[end:]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', default='cleave')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    data = (ROOT / 'testdata/hostile/netwire-headerless-excerpt.bin').read_bytes()
    assert hashlib.sha256(data).hexdigest() == 'd9f56cc21d757ddc8e87a66f0e98b1e7eee632721e77b5205b61e817a9759a8e'
    cases = {'positive.bin': (data, NEW)}
    def mutation(name, offset, expected, displacement=False):
        b = bytearray(data)
        if displacement:
            struct.pack_into('<i', b, offset, struct.unpack_from('<i', b, offset)[0] + 1)
        else:
            b[offset] ^= 1
        cases[name + '.bin'] = (bytes(b), expected)
    mutation('broken-record-handoff', 0xcd11, set(), True)
    mutation('broken-scramble-handoff', 0xc5cd, set(), True)
    mutation('broken-translation-thunk', 4316612 - 0x402000, set())
    mutation('broken-write-thunk', 4315924 - 0x402000, set())
    mutation('missing-mozilla-query', 0x1db9e, NEW - {BROWSER})
    mutation('missing-nss-decrypt-name', 0x1db24, NEW - {BROWSER})
    store = b'\\u6d0 aC5C\\ad8CQi5\\mWn4R aC5C'
    assert data.count(store) >= 3
    cases['missing-chromium-store.bin'] = (data.replace(store, b'X' * len(store)), NEW - {BROWSER})
    mutation('wrong-run-key-pointer', 0xb435, NEW - {PERSIST})
    mutation('broken-run-writer-handoff', 0xb465, NEW - {PERSIST}, True)
    cases['create-suspended-only.bin'] = (data[0x1b554:0x1b68f], set())
    cases['base64-encode.rs'] = (b'fn main() { let x = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"abc"); }', set())
    cases['base64-comment.rs'] = (b'// base64::Engine::encode(&engine, data);\nfn main() {}', set())
    results = []
    with tempfile.TemporaryDirectory(prefix='netwire-regression-', dir=ROOT) as td:
        controls = Path(td)
        for name, (body, _) in cases.items():
            (controls / name).write_bytes(body)
        run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'jsonl', '--all-files', str(controls)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert run.returncode == 0, run.stderr
        files = []
        for obj in reports(run.stdout):
            files.extend(obj.get('files', [obj]))
        for f in files:
            name = Path(f['path']).name
            if name not in cases:
                continue
            ts = f.get('traits', f.get('findings', []))
            ids = {t['id'] for t in ts}
            observed = ids & NEW
            expected = cases[name][1]
            assert observed == expected, (name, observed, expected)
            if name == 'positive.bin':
                assert OLD <= ids, OLD - ids
            if name == 'create-suspended-only.bin':
                assert not any(t.get('crit') in (4, 5, 'hostile', 'suspicious') for t in ts), ts
                assert 'metadata/binary/instruction/operand::raw-x86-stack-slot-14-value-4' in ids
            if name.startswith('base64-'):
                encoded = 'micro-behaviors/data/encode/base64::rust-base64-engine-encode' in ids
                assert encoded == (name == 'base64-encode.rs'), (name, encoded)
            results.append({'case': name, 'required_new_hostile_traits': sorted(observed), 'passed': True})
    assert len(results) == len(cases), (len(results), len(cases))
    output = json.dumps({'cases': results, 'passed': len(results)}, indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    print(output)

if __name__ == '__main__':
    main()
