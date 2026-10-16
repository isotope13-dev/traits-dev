#!/usr/bin/env python3
"""Discord webhook request construction is a notable capability, not exfiltration.

Run `python3 testdata/discord-webhook-request-builder/check.py <scratch>`.
Fixtures are copied outside testdata so path suppressors cannot mask them.
A sensitive-data source (not this trait) supplies exfiltration intent in
the objective composites that reference it.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TRAIT = 'micro-behaviors/communications/http/webhook::discord-webhook-request-builder'
OLD = 'objectives/exfiltration/messaging/discord::discord-request-builder'

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]

def scan(fixture):
    target = scratch / fixture
    shutil.copyfile(Path(__file__).parent / fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    return [t for e in json.loads(result.stdout)['files'] for t in e['traits']]

# Executable webhook POST: notable capability fires, old suspicious id gone.
traits = scan('positive-discord-webhook-post.js')
by_id = {t['id']: t for t in traits}
assert TRAIT in by_id and by_id[TRAIT]['crit'] == 3, sorted(by_id)
assert OLD not in by_id, sorted(by_id)
print('positive-discord-webhook-post.js: passed')

# Documentation example with a placeholder secret: same notable capability,
# but no Discord trait at suspicious (4) or hostile (5) criticality.
traits = scan('benign-discord-doc.md')
by_id = {t['id']: t for t in traits}
assert OLD not in by_id, sorted(by_id)
assert not [t for t in traits if 'discord' in t['id'] and t['crit'] >= 4], traits
print('benign-discord-doc.md: passed')

# Bare webhook URL mention without a request method: builder does not fire.
traits = scan('negative-webhook-mention.js')
assert TRAIT not in {t['id'] for t in traits}, traits
print('negative-webhook-mention.js: passed')
