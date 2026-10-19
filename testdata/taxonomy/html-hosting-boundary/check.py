#!/usr/bin/env python3
"""Check hosting observations and path placement without executing fixtures."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
ENTRY = 'metadata/package/entrypoint::patterned-name-html-page-manifest'
ICON = 'micro-behaviors/communications/http/services/google::classroom-product-icon-url'
DEVICE = 'micro-behaviors/fs/path/device/kernel::windows-kernel-device-path-reference'
LINK = 'micro-behaviors/fs/path/device/kernel::windows-dos-device-link-path'
DRIVER = 'micro-behaviors/fs/path/system::windows-driver-image-path'
RETIRED = {
    'objectives/command-and-control/dropper/delivery/html::decoy-mirrored-remote-html-stage',
    'objectives/evasion/decoy/lure::branded-classroom-decoy-loader',
    'objectives/supply-chain/hidden-payload/cdn-hosting::npm-patterned-name-disposable-html-host',
    'well-known/app/productivity/google-classroom::product-icon-reference',
    'metadata/binary/debug::nthook-device-object-path',
    'metadata/binary/debug::nthook-dosdevices-link-name',
    'metadata/binary/debug::nthook-system32-driver-image-path',
    'metadata/binary/debug::nthook-driver-artifact-cluster',
}


def pe(strings):
    """Data-only PE: no entry point and no executable sections."""
    image = bytearray(1024)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', image, opt, 0x10b)
    struct.pack_into('<III', image, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', image, opt + 56, 0x2000, 0x200)
    struct.pack_into('<H', image, opt + 68, 3)
    struct.pack_into('<I', image, opt + 92, 16)
    sec = opt + 224
    image[sec:sec + 8] = b'.rdata\0\0'
    struct.pack_into('<IIII', image, sec + 8, 512, 0x1000, 512, 512)
    struct.pack_into('<I', image, sec + 36, 0x40000040)
    payload = b'\0'.join(s.encode() for s in strings) + b'\0'
    image[512:512 + len(payload)] = payload
    return image


def check(path, expected, absent=(), no_hostile=True):
    result = subprocess.run(
        [CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    assert not RETIRED.intersection(traits), (path, RETIRED.intersection(traits))
    assert set(expected) <= traits.keys(), (path, set(expected) - traits.keys())
    assert not set(absent).intersection(traits), (path, set(absent).intersection(traits))
    assert all(traits[t]['crit'] == 3 for t in expected), path
    if no_hostile:
        assert not [t for t in traits.values() if t['crit'] == 5], path
    print('PASS', path.parent.name, path.name)


with tempfile.TemporaryDirectory(prefix='html-hosting-boundary-') as tmp:
    base = Path(tmp)
    launcher = base / 'launcher.html'
    launcher.write_text('''<!doctype html><title>Site launcher</title>
<link rel="icon" href="https://www.google.com/s2/favicons?domain=classroom.google.com">
<script>
const mirrors = ['https://quantil.jsdelivr.net', 'https://gcore.jsdelivr.net'];
function loadPage(url) {
  return fetch(url).then(r => r.text()).then(html => document.write(html));
}
</script>''')
    check(launcher, [ICON, 'micro-behaviors/communications/http/url/cdn::jsdelivr-mirror-host-set',
                     'micro-behaviors/ui/window/insert-html::browser-document-write'])
    other = base / 'calendar.html'
    other.write_text(launcher.read_text().replace('classroom.google.com', 'calendar.google.com'))
    check(other, [], [ICON])
    for label, name, main, matches in [
        ('html', 'a2b3c', 'index.html', True),
        ('ordinary-name', 'project-site', 'index.html', False),
        ('javascript-entry', 'a2b3c', 'index.js', False),
    ]:
        folder = base / label
        folder.mkdir()
        manifest = folder / 'package.json'
        manifest.write_text(json.dumps({'name': name, 'version': '1.0.1', 'main': main,
                                        'files': ['index.html', 'other.html']}))
        check(manifest, [ENTRY] if matches else [], [] if matches else [ENTRY])
    native = base / 'paths.exe'
    native.write_bytes(pe([r'\\.\NtHook', r'\DosDevices\NtHook',
                           r'C:\Windows\System32\Drivers\NtHook.sys']))
    check(native, [LINK, DRIVER])
    other_native = base / 'other-paths.exe'
    other_native.write_bytes(pe([r'\\.\ExampleHook', r'\DosDevices\ExampleHook',
                                 r'C:\Windows\System32\Drivers\ExampleHook.sys']))
    check(other_native, [DEVICE, LINK, DRIVER])
    bare = base / 'bare-names.exe'
    bare.write_bytes(pe(['NtHook', 'DosDevices', 'NtHook.sys']))
    check(bare, [], [DEVICE, LINK, DRIVER])
