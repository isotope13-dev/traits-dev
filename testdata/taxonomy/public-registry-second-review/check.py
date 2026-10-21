"""Exercise request-to-execution and unrelated-operation boundaries statically."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']

def check(case):
    result = subprocess.run(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(ROOT / case['path'])],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    findings = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    failures = [f'missing {name}' for name in case['matched'] if name not in findings]
    failures += [f'unexpected {name}' for name in case['not_matched'] if name in findings]
    # All ordinary configuration and download controls must remain free of
    # hostile findings. Request-driven PHP payloads intentionally retain them.
    if not case['path'].endswith(('request-eval.png', 'request-command.png')):
        failures += [f'unexpected hostile {name}' for name, t in findings.items() if t['crit'] == 5]
    return case['path'], failures

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, CASES))
for path, failures in results:
    print(('FAIL' if failures else 'PASS'), path, '; '.join(failures))
sys.exit(any(failures for _, failures in results))
