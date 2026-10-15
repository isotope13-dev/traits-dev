#!/usr/bin/env python3
"""Hardcoded session-open follow-and-mute must convict; caller-supplied follow
must not.

`hardcoded-channel-connect-follow-and-mute` fires when one file combines a
connection-update handler, an open-connection branch, a hardcoded newsletter
channel JID, a follow invocation, and a mute. A bot that follows a
caller-supplied target without muting must stay silent.

Run `python3 testdata/baileys-connect-follow-mute/check.py <scratch-directory>`.
Fixtures are copied outside testdata so file-path suppressors cannot mask the
findings under test.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

CHAN = 'micro-behaviors/communications/messaging/channel'
HOSTILE = ('objectives/impact/ui/manipulation/social::'
           'hardcoded-channel-connect-follow-and-mute')
SUSPICIOUS = ('objectives/impact/ui/manipulation/social::'
              'connect-time-whatsapp-newsletter-follow-and-mute')
expected = {
    # Implant shape: hostile present, all legs live.
    'positive-hardcoded-follow-mute.js': (True, {
        f'{CHAN}::whatsapp-connection-update-handler',
        f'{CHAN}::whatsapp-connection-open-branch',
        f'{CHAN}::whatsapp-newsletter-jid',
        f'{CHAN}::whatsapp-newsletter-follow-api-call',
        f'{CHAN}::whatsapp-newsletter-mute-api-call',
    }),
    # Legitimate bot shape: follow leg live, no verdict.
    'negative-caller-supplied-follow.js': (False, {
        f'{CHAN}::whatsapp-newsletter-follow-api-call',
    }),
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for fixture in sorted(expected):
    target = scratch / fixture
    shutil.copyfile(Path(__file__).parent / fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    hostile = set()
    suspicious = set()
    seen = set()
    for entry in report['files']:
        for trait in entry['traits']:
            if trait['crit'] == 5:
                hostile.add(trait['id'])
            elif trait['crit'] == 4:
                suspicious.add(trait['id'])
            seen.add(trait['id'])
    want_hostile, want_legs = expected[fixture]
    assert (HOSTILE in hostile) == want_hostile, (fixture, sorted(hostile))
    if not want_hostile:
        assert HOSTILE not in seen and SUSPICIOUS not in suspicious, (
            fixture, sorted(hostile), sorted(suspicious))
    missing = want_legs - seen
    assert not missing, (fixture, sorted(missing))
    print(f'{fixture}: passed')
