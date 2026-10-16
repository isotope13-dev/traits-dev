#!/usr/bin/env python3
"""Obfuscated bitmap-crypter pixel decomposition coverage.

Run `python3 testdata/taxonomy/dotnet-pixel-channel-decomposition/check.py
<scratch-directory>`. The tight GetPixel-to-channel-getter IL pattern misses
junk-padded loaders that still read every pixel through the aliased
get_R/get_G/get_B channel getters, so `dotnet-red-channel-byte-collection`
accepts either shape. This pins both: the collection composite fires on the
Transferencia bitmap crypter via the decomposition leg, the narrow IL
sequence still does not, and the two reflective-loader hostile composites
fire with it.

The subject is the case sample (copied to scratch so file-path testing
suppressors cannot mask the findings); override with SAMPLE=<path>.
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
    '905ee64b0c6f/JUSTI_26-08-2026_TRANSFERENCIA-09392832390-pdf.zip',
)
PREFIX = ('/usr/local/var/cyclotron/tmp.noindex/cyclotron-bb4ff6df/'
          'samples/905ee64b0c6f/'
          'JUSTI_26-08-2026_TRANSFERENCIA-09392832390-pdf.zip!!KOGWROgokLzmOLJ.exe')

matched = {
    'objectives/anti-static/obfuscation/steganography/image::'
    'dotnet-pixel-channel-decomposition',
    'objectives/anti-static/obfuscation/steganography/image::'
    'dotnet-red-channel-byte-collection',
    'objectives/anti-static/obfuscation/steganography/image::'
    'dotnet-red-channel-stego-reflective-loader',
    'objectives/command-and-control/dropper/staging/managed::'
    'dotnet-unsigned-bitmap-reflective-invoke-stage',
    'micro-behaviors/ui/graphics/image::dotnet-color-green-accessor',
    'micro-behaviors/ui/graphics/image::dotnet-color-blue-accessor',
}
not_matched = {
    # The narrow IL byte pattern stays narrow: the junk-padded loader
    # must not satisfy it, only the decomposition alternative.
    'micro-behaviors/data/control-flow/sequence::'
    'cil-call-value-getter-call-sequence',
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
found4 = set()
found_all = set()
for f in report['files']:
    found4 |= {t['id'] for t in f['traits'] if t['crit'] >= 4}
    found_all |= {t['id'] for t in f['traits']}
# Notable channel atoms live below the crit-4 line; everything else must
# be suspicious or higher.
missing = ({m for m in matched if 'accessor' in m} - found_all)
missing |= ({m for m in matched if 'accessor' not in m} - found4)
leaked = not_matched & found_all
if missing or leaked:
    print(f'FAILED missing={sorted(missing)} leaked={sorted(leaked)}')
    sys.exit(1)
print('dotnet-pixel-channel-decomposition: passed')
