"""Check range-probe composition and inline-script/comment boundaries.

Requires cleave and Go. Builds Windows controls into a caller-provided scratch
folder; none of the resulting executables or JavaScript is executed.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRATCH = Path(sys.argv[1]).resolve()
SCRATCH.mkdir(parents=True, exist_ok=True)
SCAN = 'objectives/discovery/network/scan/port/probe::go-cidr-tcp-probe-scanner'
OBF = ('objectives/anti-static/obfuscation/obfuscator/js-obfuscator::'
       'plain-javascript-obfuscator-string-array-runtime')
ROTATE = ('objectives/anti-static/obfuscation/obfuscator/js-obfuscator::'
          'push-shift-bracket-pattern')

cases = []
for stem in ['sweep', 'single-host', 'range-parser']:
    target = SCRATCH / (stem + '.exe')
    subprocess.run(['go', 'build', '-trimpath', '-o', str(target),
                    str(HERE / (stem + '.go'))],
                   env=dict(os.environ, GOOS='windows', GOARCH='amd64'), check=True)
    cases.append((target, SCAN, stem == 'sweep'))
for stem in ['plain-inline', 'ordinary-queue', 'no-rotation', 'checksum-comment']:
    cases.append((HERE / (stem + '.html'), OBF, stem == 'plain-inline'))
cases.append((HERE / 'checksum-comment.html', ROTATE, False))

result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
                         str(ROOT), '--format', 'json',
                         *dict.fromkeys(str(p) for p, _, _ in cases)],
                        check=True, capture_output=True, text=True)
s = result.stdout
decoder = json.JSONDecoder()
reports = {}
while s.strip():
    report, end = decoder.raw_decode(s.lstrip())
    s = s.lstrip()[end:]
    for f in report['files']:
        reports[f['path']] = {t['id'] for t in f.get('traits', [])}
for path, trait, expected in cases:
    matched = trait in reports.get(str(path), set())
    assert matched == expected, (str(path), trait, matched, expected)
    print('PASS', path.name, trait.rsplit('::', 1)[-1], matched)
