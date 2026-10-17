#!/usr/bin/env python3
"""Screen-plus-webcam encrypted-capture suite coverage.

Run `python3 testdata/taxonomy/dotnet-screen-webcam-capture/check.py
<scratch-directory>`. The subject is the case sample (copied to scratch
so file-path testing suppressors cannot mask the findings under test);
override with SAMPLE=<path>.

The obfuscated XWorm client captures screen (CopyFromScreen) and webcam
(avicap32 enum plus Video for Windows window) inside an unsigned
assembly with AES-backed HTTP and staged downloads, but carries no
tasked redirected shell. This pins the new capture-suite hostile next to
the classic command-set hostile, and pins the tasked-shell webcam
sibling absent to lock the distinction.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SAMPLE = os.environ.get(
    'SAMPLE',
    '/usr/local/var/cyclotron/tmp.noindex/cyclotron-bb4ff6df/samples/'
    '7eff14e1e2b7/7eff14e1e2b71bea8c1d541180589c3ba5d09bd9c9daea0ca1570447a28baa87',
)

matched = {
    'objectives/collection/camera::'
    'dotnet-screen-webcam-encrypted-capture-suite',
    'well-known/malware/rat/xworm::xworm-classic-command-set',
}
not_matched = {
    'objectives/collection/camera::dotnet-tasked-implant-webcam-capture',
}

scratch = Path(sys.argv[1]) / 'case'
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]
target = scratch / Path(SAMPLE).name
shutil.copyfile(SAMPLE, target)
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', str(target)],
    env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
    capture_output=True, check=True,
)
report = json.loads(result.stdout)
found = {t['id'] for f in report['files'] for t in f['traits']
         if t['crit'] >= 4}
missing = matched - found
leaked = not_matched & found
if missing or leaked:
    print(f'FAILED missing={sorted(missing)} leaked={sorted(leaked)}')
    sys.exit(1)
print('dotnet-screen-webcam-capture: passed')
