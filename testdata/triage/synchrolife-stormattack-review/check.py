"""Static rule controls. PE inputs are parsed, never executed.

python3 check.py --samples PATH --work-dir PATH [--cleave cleave]
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SEND = 'objectives/exfiltration/stealer/multi-source::managed-records-webclient-send-profile'
SHAPE = 'metadata/binary/instruction/sequence::cil-local-literal-argument-virtual-call'
OLD = 'micro-behaviors/process/create/start-process::dotnet-hidden-process-launch'
SETUP = 'micro-behaviors/process/create/hidden::dotnet-hidden-process-launch-setup'
SAMPLES = [
    ('bd0e540860b7/2026-10-19_c2b39a85a3cbb6a3472753864def9ac1_elex_remcos_wannacry',
     'bd0e540860b7b97d6f129f84f650f3febbc938adfa2913c72f49244121907976'),
    ('7e767a5cb2c0/synchrolife.io_chrome.exe',
     '7e767a5cb2c0efb4eef247e7e7360b71482ce5fba7258fd77e23aa5872d9e225'),
    ('286d0bf63df5/synchrolife.io_hyber.exe',
     '286d0bf63df535dbe92409077586879c077a0e3ff08506becbe6acb554898e45'),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--samples', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    fixtures = args.work_dir / 'fixtures'
    fixtures.mkdir(parents=True, exist_ok=True)
    data = []
    for name, sha in SAMPLES:
        content = (args.samples / name).read_bytes()
        assert hashlib.sha256(content).hexdigest() == sha
        data.append(content)
    cases = {}

    def add(name, content, expected):
        (fixtures / name).write_bytes(content)
        cases[name] = {OLD: False, **expected}

    add('native.exe', data[0], {SEND: False, SHAPE: False})
    add('chrome.exe', data[1], {SEND: True, SHAPE: True, SETUP: True})
    add('hyber.exe', data[2], {SEND: False, SETUP: True})
    add('renamed.exe', data[1], {SEND: True, SHAPE: True})
    # Delete the actual UploadString instruction while preserving its
    # metadata name, the URL and all three source/recording implementations.
    # This is an inert static near miss, not an executable test program.
    patched = bytearray(data[1])
    assert patched[0x429c:0x42a1] == bytes.fromhex('6f3500000a')
    patched[0x429c:0x42a1] = b'\x00' * 5
    add('no-send-instruction.exe', patched, {SEND: False, SHAPE: False})
    for name, before, after in [
        ('no-upload-name', b'UploadString', b'OtherMethodX'),
        ('no-keylog-record', 'KEYLOG'.encode('utf-16le'), 'NORMAL'.encode('utf-16le')),
        ('no-screen-record', 'SCREEN:'.encode('utf-16le'), 'NORMAL:'.encode('utf-16le')),
        ('no-file-record', 'FILE:'.encode('utf-16le'), 'NOTE:'.encode('utf-16le')),
    ]:
        assert len(before) == len(after) and before in data[1]
        # An unconsumed component can be omitted from rendered scan output.
        add(name + '.exe', data[1].replace(before, after), {SEND: False})
    add('ordinary-client.cs', b'''using System.Net;
class Client { void Send(string data) {
using (var c = new WebClient()) { c.UploadString("https://example.com", data); }
} }
''', {SEND: False, SHAPE: False})
    proc = subprocess.run([
        args.cleave, '--traits-dir', str(ROOT), '--disable', 'radare2,third-party',
        '--format', 'jsonl', str(fixtures),
    ], capture_output=True, text=True)
    (args.work_dir / 'scan.json').write_text(proc.stdout)
    (args.work_dir / 'scan.log').write_text(proc.stderr)
    assert proc.returncode == 0, proc.stderr
    reports = []
    remaining = proc.stdout.lstrip()
    decoder = json.JSONDecoder()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    observed = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
                for report in reports for f in report['files']}
    results = []
    for name, expected in cases.items():
        assert name in observed, name
        actual = {rule: rule in observed[name] for rule in expected}
        assert actual == expected, (name, expected, actual)
        results.append({'case': name, 'expected': expected, 'actual': actual})
    (args.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} static positive and near-miss controls passed')


if __name__ == '__main__':
    main()
