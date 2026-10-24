#!/usr/bin/env python3
"""Check actual follow guards and preserve shared attack fixtures.

Run: python3 testdata/triage/baileys-hex-stage-review/check.py <scratch-dir>
Copies source controls outside testdata so pathname exclusions cannot hide them.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
GUARD = 'micro-behaviors/data/control-flow/error-handling::whatsapp-follow-empty-catch-guard'
SOCIAL = 'objectives/impact/ui/manipulation/social::connect-swallowed-errors-newsletter-follow'
FORK = 'objectives/supply-chain/trojanized/library/fork-branding::whatsapp-library-fork-connect-swallowed-errors-follow'
expected = {
    'one-channel-follow.js': True,
    'one-channel-follow.ts': True,
    'public-follow.js': True,
    'public-follow-spaced.js': True,
    'plain-follow.js': True,
    'ignore-response-follow.js': True,
    'sidecar-follow.js': True,
    'metadata-read-empty-catch.js': False,
    'metadata-label-follow.js': False,
    'unrelated-catch.js': False,
    'quoted-follow.js': False,
    'reported-follow-error.js': False,
}
shared = [
    ROOT / 'testdata/taxonomy/whatsapp-default-follow/roster-connect-follow-positive.js',
    ROOT / 'testdata/taxonomy/baileys-connect-follow-triage/connect-hardcoded-follow.js',
    ROOT / 'testdata/baileys-connect-follow-mute/positive-hardcoded-follow-mute.js',
]
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
paths = []
for source in [HERE / name for name in expected] + shared:
    target = scratch / source.name
    shutil.copyfile(source, target)
    paths.append(str(target))
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *paths],
    env=dict(os.environ, CLEAVE_VALIDATE='0'), capture_output=True, text=True, check=True,
)
# The CLI may concatenate independent JSON reports without newline separators.
reports = []
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    reports.extend(report['files'])
assert len(reports) == len(paths), (len(reports), len(paths))
for report in reports:
    name = Path(report['path']).name
    traits = {t['id']: t['crit'] for t in report['traits']}
    want = expected.get(name, True)
    assert (GUARD in traits) == want, (name, traits)
    if want:
        assert traits[GUARD] == 3, (name, traits[GUARD])
    else:
        assert SOCIAL not in traits and FORK not in traits, (name, traits)
    if name.startswith('metadata-'):
        assert not any(c >= 4 for c in traits.values()), (name, traits)
    if name.startswith('one-channel-'):
        assert traits[SOCIAL] == 5 and traits[FORK] == 5, (name, traits)
    if name == 'sidecar-follow.js':
        assert 'objectives/impact/ui/manipulation/social::sidecar-newsletter-ids-follow-module' in traits
    print(name + ': passed')
(scratch / 'results.json').write_text(json.dumps(reports, indent=2) + '\n')
