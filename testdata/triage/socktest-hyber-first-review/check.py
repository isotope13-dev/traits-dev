"""Static controls using original CIL and same-length evidence ablations.

Usage: python3 check.py SAMPLE WORK_DIR
No specimen or fixture is executed. No endpoint or chosen output name gates
these detections. The PE builder is reused for older recorder controls.
"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'objectives/'
RULES = {
    'browser': PREFIX + 'credential-access/browser/chromium::managed-keylogger-browser-store-copy-references',
    'usb': PREFIX + 'lateral-movement/usb-worm/autorun::dotnet-autorun-drive-worm',
    'service': PREFIX + 'impact/degrade/services::managed-keylogger-security-service-stop-references',
    'defender': PREFIX + 'evasion/anti-av/platform/defender::managed-keylogger-defender-disable-command',
    'safeboot': PREFIX + 'impact/ransom/recovery-inhibition::managed-keylogger-safeboot-delete-references',
    'shadow': PREFIX + 'impact/ransom/recovery-inhibition::managed-keylogger-shadow-copy-deletion',
    'restore': PREFIX + 'impact/ransom/recovery-inhibition::managed-keylogger-systemrestore-disable-references',
    'association': PREFIX + 'persistence/system/registry/surface::managed-keylogger-file-association-selfpath-references',
    'screen': PREFIX + 'collection/screenshot::managed-ransom-keylogger-screen-capture',
}
ADMISSION = PREFIX + 'exfiltration/stealer/input::managed-ransom-hook-keylog-form-post'


def main():
    sample, work = map(Path, sys.argv[1:])
    work.mkdir(parents=True, exist_ok=True)
    original = sample.read_bytes()
    assert hashlib.sha256(original).hexdigest() == 'dcc11d42b751ffdc0827744f425304f46db4a52761d3e5098bf9019ed605de00'
    cases = [(sample, {**dict.fromkeys(RULES, True), ADMISSION: True})]

    def changed(name, replacements, absent=(), present=()):
        blob = original
        for old, new, encoding in replacements:
            old, new = old.encode(encoding), new.encode(encoding)
            assert len(old) == len(new) and old in blob, (name, old)
            blob = blob.replace(old, new)
        path = work / (name + '.exe')
        path.write_bytes(blob)
        cases.append((path, {**dict.fromkeys(absent, False), **dict.fromkeys(present, True)}))

    changed('no-recording', [('AppendAllText', 'XppendAllText', 'ascii')],
            absent=list(RULES) + [ADMISSION])
    changed('no-hook', [('SetWindowsHookEx', 'XetWindowsHookEx', 'ascii')],
            absent=list(RULES) + [ADMISSION])
    changed('different-browser-store', [('Login Data', 'Other Data', 'utf-16le')],
            absent=['browser'], present=['usb', 'service', 'screen'])
    changed('no-drive-type', [('get_DriveType', 'get_XriveType', 'ascii')],
            absent=['usb'], present=['browser', 'service', 'screen'])
    changed('no-service-command', [('stop ', 'show ', 'utf-16le')],
            absent=['service'], present=['browser', 'usb', 'screen'])
    changed('no-defender-command', [('Set-MpPreference', 'Get-MpPreference', 'utf-16le')],
            absent=['defender'], present=['browser', 'service', 'screen'])
    changed('no-safeboot-path', [('SafeBoot', 'TestBoot', 'utf-16le')],
            absent=['safeboot'], present=['restore', 'shadow', 'screen'])
    changed('no-restore-value', [('DisableSR', 'ExampleSR', 'utf-16le')],
            absent=['restore'], present=['safeboot', 'shadow', 'screen'])
    changed('no-shadow-command', [('delete shadows /all /quiet', 'query  shadows /all /quiet', 'utf-16le')],
            absent=['shadow'], present=['safeboot', 'restore', 'screen'])
    changed('no-association-hive', [('ClassesRoot', 'ExampleRoot', 'ascii')],
            absent=['association'], present=['browser', 'service', 'screen'])
    changed('no-screen-capture', [('CopyFromScreen', 'XopyFromScreen', 'ascii')],
            absent=['screen'], present=['browser', 'usb', 'service'])
    changed('renamed-endpoint-and-output', [
        ('http://socolivezaf.tv', 'http://example12.test', 'utf-16le'),
        ('.stolen', '.backup', 'utf-16le')], present=list(RULES))

    fixture = runpy.run_path(str(ROOT / 'testdata/managed-records-review/verify.py'))
    refs = ['sc', 'stop ', 'WinDefend', 'start= disabled', 'ProcessStartInfo',
            'RegistryKey', 'DeleteSubKeyTree', r'SYSTEM\CurrentControlSet\Control\SafeBoot']
    for name, markers, yes in [
        ('ordinary-admin-apis', refs, False),
        ('older-buffered-recorder', fixture['KEYLOG_MARKERS'] + refs, True),
        ('older-file-recorder', ['WH_KEYBOARD_LL', 'SetWindowsHookEx',
            'UnhookWindowsHookEx', 'CallNextHookEx', 'keylog keyboard', 'AppendAllText'] + refs, True),
    ]:
        path = work / (name + '.exe')
        fragment = bytes.fromhex('05 73 00 63 00 00 0B 73 00 74 00 6F 00 70 00 20 00 00')
        path.write_bytes(fixture['build_pe'](markers, fragment))
        cases.append((path, {'service': yes, 'safeboot': yes, 'screen': False, ADMISSION: False}))

    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--disable', 'third-party', '--format', 'jsonl', 'analyze', *[str(p) for p, _ in cases]],
        text=True, capture_output=True, check=True)
    (work / 'scan.jsonl').write_text(result.stdout)
    (work / 'scan.log').write_text(result.stderr)
    reports = {f['path']: f for line in result.stdout.splitlines()
               for f in json.loads(line)['files']}
    results = []
    for path, expected in cases:
        found = {t['id'] for t in reports[str(path)]['traits']}
        actual = {k: RULES.get(k, k) in found for k in expected}
        assert actual == expected, (path.name, expected, actual)
        results.append({'case': path.name, 'expected': expected, 'actual': actual})
    (work / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} static controls passed')


if __name__ == '__main__':
    main()
