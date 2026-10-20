"""Check WMI observation placement and avoid persistence/kill inferences."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
for case in cases:
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', str(root / case['path'])], capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    files = report.get('files', report.get('raw', {}).get('files', []))
    traits = [t for f in files for t in f.get('traits', f.get('findings', []))]
    ids = {t['id'] for t in traits}
    assert set(case['matched']) <= ids, (case['path'], 'missing', set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], 'unexpected', set(case['not_matched']) & ids)
    assert not [t for t in traits if t.get('crit') in [4, 5, 'suspicious', 'hostile']], (case['path'], 'severity', traits)
    print(case['path'], 'PASS')
