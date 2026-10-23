"""Check callback co-occurrence and Go GCM receiver binding on neutral paths.

Run with TMPDIR pointing to scratch; testdata-path exclusions must not supply
an artificial near miss. No fixture code is executed and no network is used.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
names = ['quiet-status.py', 'unused-oob.py', 'gcm.go', 'unrelated-seal.go',
         'gcm-decrypt.go', 'gcm-overwritten.go']
seal = 'micro-behaviors/crypto/encrypt::go-gcm-seal'
callback = ('micro-behaviors/communications/http/request/beacon::'
            'python-urlopen-oob-suppressed-errors')
old = 'objectives/exfiltration/oob/endpoint::python-urlopen-oob-swallowed-beacon'
results = []
with tempfile.TemporaryDirectory(prefix='fallout-capability-') as temporary:
    paths = []
    for name in names:
        path = Path(temporary) / name
        path.write_bytes((fixtures / name).read_bytes())
        paths.append(str(path))
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format',
                             'json', *paths], check=True, capture_output=True,
                            text=True, env={**os.environ, 'CLEAVE_VALIDATE': '0'})
    pending = result.stdout
    decoder = json.JSONDecoder()
    while pending.strip():
        pending = pending.lstrip()
        document, offset = decoder.raw_decode(pending)
        pending = pending[offset:]
        for file in document['files']:
            name = Path(file['path']).name
            traits = {t['id']: t for t in file['traits']}
            assert (seal in traits) == (name == 'gcm.go'), (name, 'Seal receiver')
            assert (callback in traits) == name.endswith('.py'), (name, 'callback')
            assert old not in traits, name
            assert all(t['crit'] <= 3 for t in traits.values()), (name, 'high severity')
            if name == 'gcm-decrypt.go':
                assert 'micro-behaviors/crypto/decrypt::go-gcm-open' in traits
            results.append({'case': name, 'passed': True})
assert len(results) == len(names)
print(json.dumps(results, indent=2))
