"""Static positive/near-miss controls. Generated PE stubs return immediately.

Usage: python3 check.py <scratch-directory>
No fixture or specimen is executed. Marker tables test the stated references,
not runtime behavior or reachability; those are established by specimen CIL.
"""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'managed_fixture', ROOT / 'testdata/managed-records-review/verify.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
SERVICE = 'objectives/impact/degrade/services::managed-keylogger-security-service-stop-references'
UNHOOK = 'objectives/evasion/anti-av/ntdll-unhook::dotnet-ntdll-unhooking'
MODULE = 'metadata/binary/symbols/name::dotnet-processmodule-type-name'
STOP = 'micro-behaviors/os/service/stop::dotnet-sc-stop-command-fragments'
MAP = 'micro-behaviors/mem/map::dotnet-map-view-of-file-name'
FRAGMENTS = bytes.fromhex('05 73 00 63 00 00 0B 73 00 74 00 6F 00 70 00 20 00 00')


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    services = fixture.KEYLOG_MARKERS + ['WinDefend', 'start= disabled', 'ProcessStartInfo']
    cases = [
        ('module-type', ['ProcessModule'], b'', {MODULE: True}),
        ('native-mapping-name', ['MapViewOfFile'], b'', {MAP: False}),
        ('other-module-type', ['ProcessModules'], b'', {MODULE: False}),
        ('window-hook-cleanup', ['UnhookWindowsHookEx', 'ntdll.dll', 'MapViewOfFile'],
         b'', {UNHOOK: False}),
        ('explicit-ntdll-unhook', ['UnhookNtdll', 'ntdll.dll', 'MapViewOfFile'],
         b'', {UNHOOK: True, MAP: True}),
        ('unhook-label-only', ['UnhookNtdll', 'ntdll.dll'], b'', {UNHOOK: False}),
        ('both-module-and-unhook', ['ProcessModule', 'UnhookNtdll', 'MapViewOfFile'],
         b'', {UNHOOK: True, MODULE: True}),
        ('security-service-commands', services, FRAGMENTS, {SERVICE: True, STOP: True}),
        ('other-service', [m.replace('WinDefend', 'ExampleService') for m in services],
         FRAGMENTS, {SERVICE: False, STOP: True}),
        ('without-keylog-admission', ['WinDefend', 'start= disabled', 'ProcessStartInfo'],
         FRAGMENTS, {SERVICE: False, STOP: True}),
        ('without-disabling', [m for m in services if m != 'start= disabled'],
         FRAGMENTS, {SERVICE: False, STOP: True}),
        ('other-command', services, FRAGMENTS.replace(b't\x00o\x00p\x00', b'h\x00o\x00w\x00'),
         {SERVICE: False, STOP: False}),
    ]

    def run(case):
        name, markers, cil, expected = case
        path = dest / (name + '.exe')
        blob = fixture.build_pe(markers, cil)
        if name == 'native-mapping-name':
            # No CLR directory: a native executable may carry this API name.
            directory = 0x98 + 96 + 14 * 8
            blob[directory:directory + 8] = bytes(8)
        path.write_bytes(blob)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), 'test-rules',
             str(path), '--rules', ','.join(expected), '--format', 'terminal'],
            capture_output=True, text=True, check=True)
        output = result.stdout + result.stderr
        (dest / (name + '.trace')).write_text(output)
        actual = {id: any(line.startswith('MATCHED ' + id + ' ')
                         for line in output.splitlines()) for id in expected}
        assert actual == expected, (name, actual, expected, output)
        return {'case': name, 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, cases))
    (dest / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} static positive/near-miss controls passed')


if __name__ == '__main__':
    main()
