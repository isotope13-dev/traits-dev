#!/usr/bin/env python3
"""Check lexical facts using Atomscan's unstripped JSON report."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
env = {**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'CLEAVE_TRAITS_DIR': str(ROOT),
       'SCAN_FOLLOW': 'none'}
# Synthetic controls are local analysis, without corpus publication or registry context.
env.pop('SCAN_HOPPER', None)
env.pop('SCAN_REGISTRY_MAP', None)
def debug_components(case):
    return subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         'test-rules', str(ROOT / case['path']), '--rules',
         ','.join(case['matched'] + case['not_matched'])],
        cwd=ROOT, capture_output=True, text=True, env=env,
    )


pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
debug = {c['case_id']: pool.submit(debug_components, c)
         for c in cases if c.get('debug_components')}
result = subprocess.run(
    ['atomscan', '--no-update', '--mode', 'slow', '--format', 'json', 'path',
     *[str(ROOT / c['path']) for c in cases if not c.get('debug_components')]],
    cwd=ROOT, capture_output=True, text=True, env=env,
)
if result.returncode:
    raise SystemExit(result.stderr)
reports = []
source = result.stdout.strip()
decoder = json.JSONDecoder()
while source:
    report, consumed = decoder.raw_decode(source)
    reports.append(report)
    source = source[consumed:].lstrip()
files = [f for report in reports for f in report['raw']['files']]
failed = []
for case in cases:
    if case.get('debug_components'):
        result = debug[case['case_id']].result()
        output = result.stdout + result.stderr
        ids = set(re.findall(r'^MATCHED (\S+)', output, re.MULTILINE))
        errors = ['missing ' + i for i in case['matched'] if i not in ids]
        errors += ['unexpected ' + i for i in case['not_matched'] if i in ids]
        if result.returncode or 'validation failed:' in output:
            errors.append('Rule evaluation failed: ' + output[-1000:])
    else:
        file = next((f for f in files if f['path'].endswith(case['path'])), None)
        if file is None:
            errors = ['missing analysis']
        else:
            ids = {t['id'] for t in file.get('traits', [])}
            errors = ['missing ' + i for i in case['matched'] if i not in ids]
            errors += ['unexpected ' + i for i in case['not_matched'] if i in ids]
    if errors:
        failed.append({'case_id': case['case_id'], 'errors': errors})
    print(case['case_id'], errors or 'PASS')
(HERE / 'results.json').write_text(json.dumps({'cases': len(cases), 'failed': failed}, indent=2) + '\n')
pool.shutdown()
raise SystemExit(bool(failed))
