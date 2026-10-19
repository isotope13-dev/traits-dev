"""Check precision boundaries without executing any specimen or fixture."""
import concurrent.futures
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = Path(__file__).with_name('cases.json')
def check(case):
    report = json.loads(subprocess.check_output(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(ROOT / case['path'])],
        cwd=ROOT, timeout=120))
    report = report.get('raw', report)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    missing = set(case['matched']) - traits.keys()
    unexpected = set(case['not_matched']) & traits.keys()
    assert not missing and not unexpected, (case['path'], sorted(missing), sorted(unexpected))
    if case['path'].endswith('harmless-encrypted-exec.py'):
        for name in case['matched']:
            assert traits[name]['crit'] == 4, (name, traits[name])
        assert not any(t['crit'] == 5 for t in traits.values())
    return {'path': case['path'], 'passed': True}

if __name__ == '__main__':
    cases = json.loads(CASES.read_text())['fixtures']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, cases))
    print(json.dumps(results, indent=2))
