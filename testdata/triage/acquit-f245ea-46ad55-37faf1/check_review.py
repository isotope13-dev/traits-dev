"""Assert attack flow bindings and retained external positive controls.

Usage: python3 check_review.py <cleave JSONL from the fixture scan>
"""
import json
import sys
from pathlib import Path

reports = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    for f in json.loads(line).get('files', []):
        reports[Path(f['path']).name] = {t['id']: t['crit'] for t in f.get('traits', [])}
wallet = 'objectives/impact/crypto-manipulation/clipboard::'
lure = 'objectives/execution/lure/clipboard/page::'
expect = {
    'table-replacement.py': [wallet + 'python-multichain-wallet-clipboard-replacement'],
    'renamed-table.py': [wallet + 'python-multichain-wallet-clipboard-replacement'],
    'browser-table.js': [wallet + 'browser-multichain-table-clipboard-replacement'],
    'browser-table-renamed.js': [wallet + 'browser-multichain-table-clipboard-replacement'],
    'verification-msi.html': [lure + 'clickfix-msiexec-clipboard-install', lure + 'verification-command-lure-with-payload-api'],
    'no-payload-update.html': [lure + 'clickfix-msiexec-clipboard-install'],
    'table_clipper.py': [wallet + 'python-clipboard-crypto-clipper', wallet + 'python-multichain-clipboard-crypto-clipper'],
    'table_clipper.js': [wallet + 'browser-multichain-table-clipboard-replacement'],
    'positive.py': [wallet + 'polled-eth-clipboard-hijacker'],
    'renamed.ts': [wallet + 'polled-eth-clipboard-hijacker'],
    'tagged-run-lure.html': [lure + 'clickfix-msiexec-clipboard-install'],
}
benign = ['address-normalizer.py', 'copy-unrelated-text.py', 'patterns-only.py',
          'browser-copy-unrelated.js', 'browser-recognizes-only.js', 'browser-checks-unrelated.js',
          'verification-copy-help.html', 'honest-run-help.html', 'no-clipboard.html',
          'no-run-instruction.html', 'payload-comments-only.html', 'shortcut-help.html',
          'quoted-command-copy.html', 'ordinary-mfa.html']
for name, ids in expect.items():
    for ident in ids:
        assert reports[name].get(ident) == 5, (name, ident)
for name in benign:
    assert not any(crit == 5 for crit in reports[name].values()), name
assert not any(crit >= 4 for crit in reports['verification-copy-help.html'].values())
assert not any(crit >= 4 for crit in reports['honest-run-help.html'].values())
assert 'micro-behaviors/ui/controls/captcha::cloudflare-copyright-text' in reports['verification-copy-help.html']
assert 'micro-behaviors/ui/help::html-run-paste-execution-sequence' in reports['honest-run-help.html']
print(f'{len(expect) + len(benign)} focused positive and negative cases passed')
