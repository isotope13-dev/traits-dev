#!/usr/bin/env python3
"""Check recovered PE boundaries without executing either program."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--members', required=True)
p.add_argument('--output', required=True)
p.add_argument('--atomscan', default='../scan/target/release/atomscan')
a = p.parse_args()
members = {
    'RDSERVICE.exe': '7ed2a077a1ce34fcb182e5135ae75ad7bd96207c3204c9f343095f967bfa109f',
    'DISKMGR.exe': 'bf41e6af51ccba343098f403093b195fb5f238559f723d4088196a2648fb9272',
}
paths = [Path(a.members) / name for name in members]
for path in paths:
    assert hashlib.sha256(path.read_bytes()).hexdigest() == members[path.name]
scan = subprocess.run([a.atomscan, '--no-update', '--mode', 'slow', '--format', 'json', 'path'] + list(map(str, paths)), env=dict(os.environ, CLEAVE_TRAITS_DIR=str(Path.cwd())), capture_output=True, text=True)
assert scan.returncode in (0, 1), scan.stderr
forbidden = {
    'objectives/collection/keylog/hook::winsta-keyboard-hook-keystate',
    'objectives/collection/keylog/hook::desktop-keyboard-hook-keystate',
    'objectives/exfiltration/stealer/image::recon-image-socket-exfil',
    'objectives/impact/degrade/edr/targeting::security-process-debug-inject',
}
results = []
for line in scan.stdout.splitlines():
    files = json.loads(line)['raw']['files']
    name = Path(files[0]['path']).name
    traits = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
    assert name in members
    assert not forbidden.intersection(traits), (name, forbidden.intersection(traits))
    assert traits.get('micro-behaviors/hardware/input/keyboard/hook::window-station-hook-keystate-api-profile') == 3
    if name == 'RDSERVICE.exe':
        assert max(traits.values()) <= 3, (name, traits)
        assert traits.get('metadata/signed/certificate/signature::pe-authenticode-digest-matches') == 3
    else:
        assert traits.get('micro-behaviors/hardware/input/keyboard/hook::desktop-hook-keystate-api-profile') == 3
        assert traits.get('micro-behaviors/ui/graphics/image::image-winsock-host-api-profile') == 3
    results.append({'name': name, 'sha256': members[name], 'forbidden': sorted(forbidden), 'passed': True})
assert {r['name'] for r in results} == set(members)
Path(a.output).write_text(json.dumps(results, indent=2) + '\n')
print('2 embedded-member boundary cases passed')
