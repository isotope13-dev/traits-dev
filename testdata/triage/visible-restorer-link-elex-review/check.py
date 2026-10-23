#!/usr/bin/env python3
"""Focused native argument binding, renamed export and benign restoration controls."""
import argparse
import json
import lzma
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=True)
original = lzma.decompress(Path('testdata/hostile/elex-scrambled-resource-dropper.exe.xz').read_bytes())
hide = 'micro-behaviors/fs/attributes/flags::x86-set-hidden-attribute'
conceal = 'objectives/evasion/file-hiding/attributes::hidden-subtract-decoded-resource-stager'
launch = 'objectives/execution/lolbin/rundll32::subtract-resource-copied-rundll32-launch'
decoder = 'micro-behaviors/data/decode/custom::x86-three-phase-subtract-byte-decoder'
family = 'well-known/malware/trojan/elex/identity::elex-resource-dll-renamed-rundll32-any-section'
forward = 'micro-behaviors/ui/window/click::extension-broad-host-link-click-forwarding'
restore = 'micro-behaviors/process/interpreter/eval/source::php-shared-memory-file-recreation-inclusion'
slot = bytes.fromhex('6a0250ff1534104300')
assert original.count(slot) == 1
variants = {}
variants['original.exe'] = (original, [hide, conceal, launch, family], [])
# No chosen export verb is required by the behavioral launch rule.
variants['renamed.exe'] = (original.replace(b',Viewer %s', b',Export %s'), [hide, conceal, launch, family], [])
variants['normal-attribute.exe'] = (original.replace(slot, bytes.fromhex('6a2050ff1534104300')), [launch, family], [hide, conceal])
# Same immediate 2, but bound to CopyFileA instead of SetFileAttributesA.
variants['unrelated-api.exe'] = (original.replace(slot, bytes.fromhex('6a0250ff152c104300')), [launch, family], [hide, conceal])
start = bytes.fromhex('8bc1be0300000099f7fe8bf2')
assert original.count(start) == 1
variants['without-decoder.exe'] = (original.replace(start, b'\x90' * len(start)), [hide], [decoder, conceal, launch, family])
cases = []
for name, (content, matched, absent) in variants.items():
 path = a.output / name
 path.write_bytes(content)
 cases.append((path, matched, absent, False))
cases += [
 (Path('testdata/benign/php-offdisk-restoration/visible-cache-restore.php'), [restore], [], True),
 (Path('testdata/benign/extension-link-forwarding.xpi'), [forward], [], True),
 (Path('testdata/benign/extension-download-click-controls/download-interceptor.js'), [], [], True),
]
env = dict(os.environ, CLEAVE_VALIDATE='0')
r = subprocess.run([a.cleave, '--json', *[str(c[0]) for c in cases]], env=env, text=True, capture_output=True, check=True)
(a.output / 'focused.jsonl').write_text(r.stdout)
reports = [json.loads(x) for x in r.stdout.splitlines() if x.strip()]
files = {f['path']: f for report in reports for f in report['files']}
for path, matched, absent, no_hostile in cases:
 f = files[str(path)]
 traits = {t['id']: t for t in f.get('traits', [])}
 assert set(matched) <= traits.keys(), (path, set(matched) - traits.keys())
 assert not set(absent) & traits.keys(), (path, set(absent) & traits.keys())
 assert not no_hostile or all(t['crit'] < 5 for t in traits.values()), path
 print('PASS', path.name)
# Existing concealed restoration controls retain their two independent claims.
concealed = ['testdata/hostile/php-offdisk-restoration/' + n for n in ('shared-cache-mesh.php', 'sysv-option-mesh.php', 'direct-db-mesh.php')]
r = subprocess.run([a.cleave, '--json', *concealed], env=env, text=True, capture_output=True, check=True)
(a.output / 'concealed.jsonl').write_text(r.stdout)
for line in r.stdout.splitlines():
 report = json.loads(line)
 for f in report['files']:
  ids = {t['id'] for t in f.get('traits', []) if t['crit'] == 5}
  assert {'objectives/persistence/system/supervised::wordpress-concealed-memory-restoration', 'objectives/persistence/system/supervised::wordpress-concealed-option-restoration'} <= ids, (f['path'], ids)
  print('PASS', Path(f['path']).name)
