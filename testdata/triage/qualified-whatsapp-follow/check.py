#!/usr/bin/env python3
"""Check qualified FOLLOW selectors and retained default-follow controls.

Run with a scratch directory; source controls are scanned outside testdata.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RULE = 'micro-behaviors/communications/messaging/channel::whatsapp-newsletter-follow-query'
FOLLOW = ROOT / 'testdata/taxonomy/whatsapp-default-follow'
CASES = {
    'bare.js': ('newsletterWMexQuery(jid, FOLLOW);', True),
    'namespace.js': ('newsletterWMexQuery(jid, QueryIds.FOLLOW);', True),
    'compiled.js': ('newsletterWMexQuery(jid, Types_1.QueryIds.FOLLOW);', True),
    'qualified-ignore.js': ('executeWMexQueryIgnoreResponse({newsletter_id: jid}, lib.Types.QueryIds.FOLLOW);', True),
    'metadata.js': ('newsletterWMexQuery(jid, Types_1.QueryIds.METADATA);', False),
    'unfollow.js': ('newsletterWMexQuery(jid, Types_1.QueryIds.UNFOLLOW);', False),
    'wrong-argument.js': ('newsletterWMexQuery(Types_1.QueryIds.FOLLOW, Types_1.QueryIds.METADATA);', False),
    'identifier-prefix.js': ('newsletterWMexQuery(jid, Types_1.QueryIds.FOLLOWERS);', False),
}
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
expected = {}
for name, (source, match) in CASES.items():
    (scratch / name).write_text(source + '\n')
    expected[name] = ({RULE} if match else set(), set() if match else {RULE})
qualified = (FOLLOW / 'caller-config-follow.js').read_text().replace('QueryIds.FOLLOW', 'Types_1.QueryIds.FOLLOW')
(scratch / 'qualified-caller-config.js').write_text(qualified)
expected['qualified-caller-config.js'] = ({RULE}, {
    'objectives/impact/ui/manipulation/social::autonomous-whatsapp-newsletter-follow',
    'objectives/impact/ui/manipulation/social::timer-scheduled-default-channel-auto-follow',
})
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json',
     *[str(scratch / name) for name in expected]],
    env=dict(os.environ, CLEAVE_VALIDATE='0'), capture_output=True, text=True, check=True,
)
reports = []
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    reports.extend(report['files'])
assert len(reports) == len(expected), (len(reports), len(expected))
for report in reports:
    name = Path(report['path']).name
    traits = {t['id']: t['crit'] for t in report.get('traits', [])}
    want, absent = expected[name]
    assert not (want - traits.keys()), (name, 'missing', want - traits.keys())
    assert not (absent & traits.keys()), (name, 'unexpected', absent & traits.keys())
    if name in CASES or name == 'qualified-caller-config.js':
        assert not any(c >= 4 for c in traits.values()), (name, traits)
(scratch / 'results.json').write_text(json.dumps(reports, indent=2) + '\n')
print(f'Qualified follow and retained controls: {len(reports)} passed')
