"""Check the native-host profile's boundary without executing fixture code."""
import concurrent.futures
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())

def check(case):
    wanted = case['matched'] + case['not_matched']
    result = subprocess.run(
        ['cleave', '--traits-dir', str(root), 'test-rules',
         str(root / case['path']), '--rules', ','.join(wanted)],
        text=True, capture_output=True, timeout=180, check=True)
    matched = {line.split()[1] for line in result.stdout.splitlines()
               if line.startswith('MATCHED ')}
    assert set(case['matched']) <= matched, (case['path'], result.stdout)
    assert not set(case['not_matched']) & matched, (case['path'], result.stdout)
    return case['path']

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for path in pool.map(check, cases['fixtures']):
        print('PASS', path)
