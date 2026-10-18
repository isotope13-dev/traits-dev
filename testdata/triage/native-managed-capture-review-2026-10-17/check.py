"""Static controls; never execute specimens or generated PE stubs.

Usage: python3 check.py --native-dll <carved-safemon> --managed <sample>
                       --work-dir <scratch-directory>
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[3]
XOR = 'micro-behaviors/data/encode/xor::x86-xor-byte-copy-loop'
NATIVE = 'objectives/collection/keylog/polling::unsigned-xor-key-recording'
SURVEILLANCE = 'objectives/collection/multi-source::polling-recorder-injected-surveillance'
MANAGED = 'objectives/collection/multi-source::managed-file-keylogger-screen-clipboard'
RUN = 'objectives/persistence/login/registry/run-key::dotnet-run-key-autostart-persistence'
LOOP = bytes.fromhex('8a 14 01 80 f2 62 88 10 40 83 ee 01 75 f2')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--native-dll', type=Path, required=True)
    ap.add_argument('--managed', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.work_dir.mkdir(parents=True, exist_ok=True)
    # Shared inert PE builder: native entry is xor eax,eax; ret. Marker tables
    # and unreachable snippets model static evidence, never runtime behavior.
    build = runpy.run_path(str(ROOT / 'testdata/managed-records-review/verify.py'))['build_pe']
    cases = []

    def add(name, data, expected):
        path = a.work_dir / (name + '.exe')
        path.write_bytes(data)
        cases.append((path, expected))

    native = a.native_dll.read_bytes()
    assert native.count(LOOP) == 1
    for key in [0x62, 0x37, 0xff, 0]:
        changed = LOOP[:5] + bytes([key]) + LOOP[6:]
        add('native-xor-%02x' % key, native.replace(LOOP, changed),
            {XOR: key != 0, NATIVE: key != 0, SURVEILLANCE: key != 0})
    add('native-no-key-poll', native.replace(b'GetAsyncKeyState', b'GetAsyncRowState'),
        {XOR: True, NATIVE: False, SURVEILLANCE: False})
    add('native-no-clipboard', native.replace(b'GetClipboardData', b'GetOrdinaryValue'),
        {NATIVE: True, SURVEILLANCE: False})
    add('native-no-record-loop', native.replace(LOOP, bytes(len(LOOP))),
        {NATIVE: False, SURVEILLANCE: False})
    # Encoding and common GUI/input references alone cannot convict.
    add('gui-encoding-only', build(['GetAsyncKeyState', 'GetForegroundWindow',
                                  'GetClipboardData', 'CopyFromScreen', '<Enter>\r\n'], LOOP),
        {XOR: True, NATIVE: False, SURVEILLANCE: False, MANAGED: False})
    add('screen-clipboard-only', build(['OpenClipboard', 'GetClipboardData',
                                      'CopyFromScreen', 'get_PrimaryScreen']),
        {MANAGED: False, RUN: False})
    managed = a.managed.read_bytes()
    add('managed-positive', managed, {MANAGED: True, RUN: True})
    for name, old, new in [
        ('no-screen', b'CopyFromScreen', b'CopyFromBuffer'),
        ('no-clipboard', b'GetClipboardData', b'GetOrdinaryValue'),
        ('no-recording', b'AppendAllText', b'AppendNewText'),
    ]:
        assert len(old) == len(new) and old in managed
        add('managed-' + name, managed.replace(old, new), {MANAGED: False})
    # Login reactivation must not depend on unrelated injection capabilities.
    without_injection = managed
    for old in [b'VirtualAllocEx', b'WriteProcessMemory', b'CreateRemoteThread']:
        assert old in without_injection
        without_injection = without_injection.replace(old, b'X' * len(old))
    add('managed-persistence-without-injection', without_injection,
        {MANAGED: True, RUN: True})
    # API declarations without the durable activation surface are insufficient.
    runpath = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'.encode('utf-16le')
    assert runpath in managed
    add('managed-without-run-key', managed.replace(runpath, bytes(len(runpath))),
        {MANAGED: True, RUN: False})

    def check(case):
        path, expected = case
        result = subprocess.run([a.cleave, '--traits-dir', str(ROOT), '--format', 'terminal',
                                 'test-rules', '--format', 'terminal', str(path),
                                 '--rules', ','.join(expected)], capture_output=True, text=True)
        output = result.stdout + result.stderr
        assert result.returncode == 0 and 'Warning: Rule ' not in output, output
        actual = {rule: any(line.startswith('MATCHED ' + rule + ' ')
                            for line in output.splitlines()) for rule in expected}
        assert actual == expected, (path.name, expected, actual, output)
        (a.work_dir / (path.name + '.trace')).write_text(output)
        return {'case': path.name, 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, cases))
    (a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('%d static controls passed' % len(results))


if __name__ == '__main__':
    main()
