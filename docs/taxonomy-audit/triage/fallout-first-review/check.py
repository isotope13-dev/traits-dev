#!/usr/bin/env python3
"""Verify real PE/raw NetWire coverage and altered data-flow controls statically."""
from pathlib import Path
import argparse
import json
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CODEC = 'micro-behaviors/data/codec::x86-rotated-alphabet-substitution'
KEYS = 'objectives/collection/keylog/device::native-translated-scrambled-key-log'
BROWSER = 'objectives/credential-access/browser/multi-target::native-keylogger-substituted-browser-password-stores'
RUN = 'objectives/persistence/login/registry/run-key::native-keylogger-substituted-run-persistence'
FOCUSED = {CODEC, KEYS, BROWSER, RUN}


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        value, end = decoder.raw_decode(text.lstrip())
        yield value
        text = text.lstrip()[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = (ROOT / 'testdata/hostile/netwire-resource-payload.exe').read_bytes()
    raw = (ROOT / 'testdata/hostile/netwire-headerless-excerpt.bin').read_bytes()
    assert data[0x800:0x900] == raw[:0x100]
    cases = {'positive.exe': (data, FOCUSED)}

    def displacement(name, offset, expected):
        body = bytearray(data)
        struct.pack_into('<i', body, offset, struct.unpack_from('<i', body, offset)[0] + 1)
        cases[name] = (bytes(body), expected)

    displacement('broken-record-handoff.exe', 0xcd11 + 0x800, {CODEC})
    displacement('broken-run-writer.exe', 0xb465 + 0x800, FOCUSED - {RUN})
    body = bytearray(data)
    body[0xb435 + 0x800] ^= 1
    cases['wrong-run-target.exe'] = (bytes(body), FOCUSED - {RUN})
    token = b'9HGGMarpadY0Zs5'
    assert token in data
    cases['no-nss-decrypt.exe'] = (data.replace(token, b'X' * len(token)), FOCUSED - {BROWSER})
    token = b'\\u6d0 aC5C\\ad8CQi5\\mWn4R aC5C'
    assert token in data
    cases['no-chromium-store.exe'] = (data.replace(token, b'X' * len(token)), FOCUSED - {BROWSER})
    body = bytearray(data)
    pe = struct.unpack_from('<I', body, 0x3c)[0]
    first_section = pe + 24 + struct.unpack_from('<H', body, pe + 20)[0]
    characteristics = first_section + 36
    struct.pack_into('<I', body, characteristics, struct.unpack_from('<I', body, characteristics)[0] & ~0x20000000)
    cases['nonexecutable-code.exe'] = (bytes(body), set())
    body = bytearray(data)
    body[first_section:first_section + 8] = b'.custom\0'
    cases['renamed-executable-section.exe'] = (bytes(body), FOCUSED)
    # An isolated substitution body is a neutral codec, without surveillance.
    cases['table-only.bin'] = (data[0xaa0e:0xabf8], {CODEC})
    cases['api-labels-only.bin'] = (b'GetKeyboardState\0GetKeyState\0ToAscii\0WriteFile\0CryptUnprotectData\0', set())
    results = []
    with tempfile.TemporaryDirectory(prefix='fallout-controls-', dir=ROOT) as td:
        directory = Path(td)
        for name, (body, _) in cases.items():
            (directory / name).write_bytes(body)
        run = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'jsonl', '--all-files', str(directory)], text=True, capture_output=True)
        assert run.returncode == 0, run.stderr
        files = []
        for report in reports(run.stdout):
            files.extend(report.get('files', [report]))
        for f in files:
            name = Path(f['path']).name
            if name not in cases:
                continue
            traits = f.get('traits', f.get('findings', []))
            ids = {t['id'] for t in traits}
            observed = ids & FOCUSED
            assert observed == cases[name][1], (name, observed, cases[name][1])
            if name in {'table-only.bin', 'api-labels-only.bin'}:
                assert not any(t.get('crit') in (4, 5, 'hostile', 'suspicious') for t in traits), traits
            results.append({'case': name, 'focused_traits': sorted(observed), 'passed': True})
    assert len(results) == len(cases)
    text = json.dumps({'passed': len(results), 'cases': results}, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
