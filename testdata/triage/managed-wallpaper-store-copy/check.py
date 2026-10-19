"""Static controls for numeric wallpaper calls and copied browser stores.

Requires the three reviewed samples, in queue order. Executes none.
python3 check.py --samples <managed-rat> <native-installer> <managed-locker> \
    --work-dir <scratch-directory> [--cleave cleave]
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--samples', nargs=3, type=Path, required=True)
ap.add_argument('--work-dir', type=Path, required=True)
ap.add_argument('--cleave', default='cleave')
a = ap.parse_args()
root = Path(__file__).resolve().parents[3]
a.work_dir.mkdir(parents=True, exist_ok=True)
hashes = [
    '63b53219fe86ae320d4513a203302e16d2a9851a89f11964f960f1e9374f9dca',
    '3d41ef71f323ce5ba5224f6b57887353c6e7342c12149d56bf54f2b23c82b94c',
    '7b22ce94da9b3a182e7794119567652455a61b9b7e6f62e1a481f8fa6bb8a647',
]
data = [path.read_bytes() for path in a.samples]
assert [hashlib.sha256(b).hexdigest() for b in data] == hashes
wall = 'micro-behaviors/ui/wallpaper::managed-wallpaper-update-references'
copy = ('objectives/credential-access/browser/chromium::'
        'managed-keylogger-browser-store-copy-references')
read = ('objectives/credential-access/browser/chromium::'
        'managed-keylogger-browser-store-read-references')
deface = 'objectives/impact/deface/wallpaper::ransomware-wallpaper-defacement'
cases = [(a.samples[0], {wall: True, read: True, copy: False}),
         (a.samples[1], {wall: False, read: False, copy: False}),
         (a.samples[2], {wall: True, copy: True, deface: True})]


def changed(name, replacements, expected):
    blob = data[2]
    for old, new in replacements:
        assert len(old) == len(new) and old in blob, (name, old)
        blob = blob.replace(old, new)
    path = a.work_dir / (name + '.exe')
    path.write_bytes(blob)
    cases.append((path, expected))


def ascii_pair(old, new):
    return old.encode(), new.encode()


def wide_pair(old, new):
    return old.encode('utf-16le'), new.encode('utf-16le')


changed('no-wallpaper-api', [ascii_pair('SystemParametersInfo', 'XystemParametersInfo')],
        {wall: False, deface: False, copy: True})
changed('different-spi-action', [(bytes.fromhex('1f1416061928'),
                                  bytes.fromhex('1f1516061928'))],
        {wall: False, deface: False, copy: True})
changed('no-desktop-key', [wide_pair('Control Panel\\Desktop', 'Control Panel\\Example')],
        {wall: False, deface: False, copy: True})
changed('no-login-store', [wide_pair('Login Data', 'Other Data')],
        {wall: True, copy: False})
changed('no-copy-name', [(b'\0Copy\0', b'\0Xopy\0')],
        {wall: True, copy: False})
changed('different-copy-argument', [(
    bytes.fromhex('284800000a17285500000a'),
    bytes.fromhex('284800000a16285500000a'))],
    {wall: True, copy: False})
# A normal store backup can share the path and copy shape; recording is
# independently required. Hook names occur inside Unhook/CallNext names too.
changed('no-recording-admission', [
    ascii_pair('SetWindowsHookEx', 'XetWindowsHookEx'),
    ascii_pair('GetAsyncKeyState', 'XetAsyncKeyState')],
    {wall: True, copy: False})
# Neither a chosen staging suffix nor the sample's filename gates detection.
changed('renamed-output', [wide_pair('.stolen', '.backup')],
        {wall: True, copy: True})
for rel in ['testdata/benign/dotnet-default-manifest.dll',
            'testdata/benign/keylog-dropper-controls.exe']:
    cases.append((root / rel, {wall: False, copy: False}))


def run(case):
    path, expected = case
    result = subprocess.run(
        [a.cleave, '--traits-dir', str(root), 'test-rules', str(path),
         '--rules', ','.join(expected)], capture_output=True, text=True,
        check=True)
    output = result.stdout + result.stderr
    actual = {rule: any(line.startswith('MATCHED ' + rule + ' ')
                        for line in output.splitlines()) for rule in expected}
    (a.work_dir / (path.name + '.trace')).write_text(output)
    assert actual == expected, (str(path), actual, expected, output)
    return {'case': path.name, 'actual': actual, 'expected': expected}


with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, cases))
(a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'{len(results)} static controls passed')
