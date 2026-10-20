"""Check byte-scrambling precision and an inert certificate mismatch."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
here = Path(__file__).parent
paths = [here / name for name in [
    'xor-comprehension.py', 'xor-list.py', 'xor-scalar.py',
    'inert-vendor-certificate.exe']]
result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json',
                         *map(str, paths)], capture_output=True, text=True, check=True)
decoder = json.JSONDecoder()
source = result.stdout
reports = {}
while source.strip():
    report, end = decoder.raw_decode(source.lstrip())
    source = source.lstrip()[end:]
    for file in report.get('files', []):
        reports[Path(file['path']).name] = file.get('traits', [])
xor = 'micro-behaviors/data/encoding/xor::python-xor-bytes-comprehension'
for name in ['xor-comprehension.py', 'xor-list.py']:
    assert xor in {t['id'] for t in reports[name]}, name
assert xor not in {t['id'] for t in reports['xor-scalar.py']}
control = reports['inert-vendor-certificate.exe']
assert 'metadata/signed/certificate/signature::vendor-signature-digest-mismatch' in {t['id'] for t in control}
assert not any(t['crit'] == 5 for t in control), control
assert all('vendor-signature-over-modified-image' not in t['id'] for t in control)
print('4 focused controls passed; inert vendor-certificate mismatch has no hostile traits')
