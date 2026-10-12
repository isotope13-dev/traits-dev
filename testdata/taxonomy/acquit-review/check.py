"""Focused rule controls, including transparent composites hidden in JSON."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

cases = json.loads(Path(__file__).with_name('cases.json').read_text())
env = {**os.environ, 'CLEAVE_VALIDATE': '0'}

def check(case):
    wanted = case['matched'] + case['not_matched']
    if case['path'].endswith(('.xz', '.xpi')):
        # Fixture naming suppresses IP facts. Stage archives outside testdata
        # and inspect the full analysis tree rather than debugging its root.
        with tempfile.TemporaryDirectory(prefix='acquit-controls-', dir='.') as tmp:
            staged = Path(tmp) / ('sample' + Path(case['path']).suffix)
            shutil.copyfile(case['path'], staged)
            result = subprocess.run(
                ['cleave', '--traits-dir', '.', '--json', str(staged)],
                text=True, capture_output=True, env=env, check=True)
        found = {trait['id'] for line in result.stdout.splitlines()
                 for file in json.loads(line)['files'] for trait in file['traits']}
        assert set(case['matched']) <= found, (case['path'], set(case['matched']) - found)
        assert not set(case['not_matched']) & found, case['path']
    else:
        result = subprocess.run(
            ['cleave', '--traits-dir', '.', 'test-rules', case['path'],
             '--rules', ','.join(wanted)], text=True, capture_output=True,
            env=env, check=True)
        for rule in case['matched']:
            assert '\nMATCHED ' + rule + ' ' in result.stdout, (case['path'], rule, result.stdout)
        for rule in case['not_matched']:
            assert '\nNOT MATCHED ' + rule + ' ' in result.stdout, (case['path'], rule, result.stdout)
    print('PASS', case['path'], flush=True)

with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(check, cases['fixtures']))
