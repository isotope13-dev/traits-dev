"""Focused MIME, filesystem-walk and encoding precision controls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name('cases.json').read_text())

def check(case):
    result = subprocess.run([args.cleave, '--traits-dir', '.', '--format', 'json',
                             case['path']], capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    report = json.loads(result.stdout)
    ids = {trait['id'] for file in report['files']
           for trait in file.get('traits', [])}
    missing = set(case['matched']) - ids
    unexpected = set(case['not_matched']) & ids
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    return case['path']

with ThreadPoolExecutor(max_workers=4) as pool:
    for path in pool.map(check, cases['fixtures']):
        print('PASS', path)
