"""Check the codec operation, architecture and section boundaries."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[2]
cases = json.loads((root / 'cases.json').read_text())['fixtures']
loader_cases = json.loads((repo / 'testdata/native-loader-first-review/cases.json').read_text())
# Reuse these benign boundaries for the moved identity observations. Their
# historical HTTP-matcher expectations are independent of this review.
identity_prefix = 'well-known/malware/botnet/mirai/identity::'
for name, case in loader_cases.items():
    cases.append({'path': 'testdata/native-loader-first-review/' + name,
                  'matched': [x for x in case['matched'] if x.startswith(identity_prefix)],
                  'not_matched': [x for x in case['not_matched'] if x.startswith(identity_prefix)],
                  'hostile': 0})
result = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'cleave',
                         '--traits-dir', str(repo), '--format', 'json',
                         *[case['path'] for case in cases]],
                        cwd=repo, text=True, capture_output=True)
if result.returncode:
    sys.exit(result.stderr or result.stdout)
pending = result.stdout.lstrip()
files = {}
while pending:
    report, end = json.JSONDecoder().raw_decode(pending)
    files.update({Path(item['path']).name: item for item in report['files']})
    pending = pending[end:].lstrip()
for case in cases:
    observed = {item['id'] for item in files[Path(case['path']).name]['traits']}
    for item in case['matched']:
        assert item in observed, (case['path'], 'missing', item)
    for item in case['not_matched']:
        assert item not in observed, (case['path'], 'unexpected', item)
    if 'hostile' in case:
        traits = files[Path(case['path']).name]['traits']
        count = sum(item.get('crit') in ('hostile', 5) for item in traits)
        assert count == case['hostile'], (case['path'], 'hostile count', count)
print(f'PASS: {len(cases)} codec and loader-boundary fixtures')
