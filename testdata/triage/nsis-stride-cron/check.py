"""Check both attack coverage and benign near misses against the real engine."""
import concurrent.futures, json, os, subprocess
from pathlib import Path
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
def check(case):
    env = dict(os.environ, CLEAVE_VALIDATE='0')
    proc = subprocess.run(['cleave','--format','json',case['path']], env=env, capture_output=True, text=True, check=True)
    report = json.loads(proc.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    failures = [f'missing {x}' for x in case['matched'] if x not in ids]
    failures += [f'unexpected {x}' for x in case['not_matched'] if x in ids]
    return case['path'], failures
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, cases))
for path, failures in results:
    print(('FAIL' if failures else 'PASS'), path, '; '.join(failures))
assert not any(failures for _, failures in results)
print(f'{len(results)} controls passed')
