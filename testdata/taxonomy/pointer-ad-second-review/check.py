#!/usr/bin/env python3
"""Check ad-trap boundaries and retained clickjacking coverage, without execution."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
SOCIAL = 'objectives/impact/ui/manipulation/social::'
OVERLAY = 'objectives/impact/ui/manipulation/overlay::'
STYLE = 'micro-behaviors/ui/window/style::'
EVENT = 'micro-behaviors/ui/window/event::'
AD = 'micro-behaviors/communications/http/client/resource::script-src-ad-label'
TRACKER = STYLE + 'jquery-mousemove-invisible-pointer-tracker'
TRAPS = {SOCIAL + 'pointer-following-invisible-ad-click-trap',
         OVERLAY + 'invisible-remote-ad-pointer-carrier'}
CASES = [
    ('testdata/hostile/clickjack-pointer-ad-trap.html', TRAPS | {AD, TRACKER}, set()),
    ('testdata/benign/hover-dropdown-menu.html', set(), TRAPS | {TRACKER}),
    ('testdata/taxonomy/jquery-mousemove-pointer-tracker/trap-snippet.html', {TRACKER}, TRAPS),
    ('testdata/taxonomy/jquery-mousemove-pointer-tracker/visible-follower.html', set(), TRAPS | {TRACKER}),
    ('testdata/taxonomy/jquery-mousemove-pointer-tracker/hidden-static.html', set(), TRAPS | {TRACKER}),
    ('testdata/taxonomy/pointer-ad-second-review/analytics-pointer-effect.html', {TRACKER}, TRAPS | {AD}),
    ('testdata/taxonomy/pointer-ad-second-review/commented-ad-pointer-effect.html', {TRACKER}, TRAPS | {AD}),
    ('testdata/taxonomy/pointer-ad-second-review/static-ad.html', {AD}, TRAPS | {TRACKER}),
    ('testdata/taxonomy/pointer-ad-second-review/helper-name-only.html', set(),
     {EVENT + 'mouseover-hide-named-call', EVENT + 'mouseout-show-named-call'}),
    ('testdata/hostile/offbrand-like-pointer-trap.html',
     {SOCIAL + 'pointer-following-offbrand-like-trap'}, set()),
    ('testdata/hostile/self-removing-like-follower.html',
     {SOCIAL + 'pointer-following-like-iframe-self-removing'}, set()),
    ('testdata/hostile/mousemove-like-iframe-teardown.html',
     {SOCIAL + 'mousemove-tracked-like-iframe-self-removing'}, set()),
    ('testdata/taxonomy/invisible-ad-iframe-click-trap/trap-snippet.html',
     {OVERLAY + 'mousemove-tracked-invisible-ad-iframe', SOCIAL + 'ad-click-focus-verification-loop'}, set()),
    ('testdata/taxonomy/invisible-ad-iframe-click-trap/benign-visible-iframe.html', set(), TRAPS),
]
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl']
    + [str(ROOT / p) for p, _, _ in CASES],
    env={**os.environ, 'CLEAVE_VALIDATE': '0'}, capture_output=True, text=True, check=True)
(OUT / 'reports.jsonl').write_text(result.stdout)
(OUT / 'scan.log').write_text(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line).get('files', []):
        reports[str(Path(file['path']).resolve())] = file
records = []
for path, required, forbidden in CASES:
    file = reports[str((ROOT / path).resolve())]
    actual = {t['id']: t['crit'] for t in file.get('traits', [])}
    assert required <= actual.keys(), (path, 'missing', required - actual.keys())
    assert not forbidden & actual.keys(), (path, 'unexpected', forbidden & actual.keys())
    if TRACKER in actual:
        assert actual[TRACKER] == 3, (path, 'tracker must remain notable')
    records.append({'path': path, 'matched': sorted(required), 'not_matched': sorted(forbidden)})
(OUT / 'results.json').write_text(json.dumps(records, indent=2) + '\n')
print(f'PASS: {len(CASES)} pointer/ad boundary and retained-attack controls')
