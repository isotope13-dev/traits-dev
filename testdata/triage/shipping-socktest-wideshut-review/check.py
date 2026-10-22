#!/usr/bin/env python3
"""Review controls; never execute specimen code. Supply the unpacked PE."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--wide', type=Path, required=True)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.scratch.mkdir(parents=True, exist_ok=True)
blob = args.wide.read_bytes()
header = bytes.fromhex('8B 45 0C C6 00 4D 8B 4D 0C C6 41 01 5A')
assert blob.count(header) == 1
native = 'objectives/execution/payload/file-exec::header-restoring-hashed-api-file-stager'
service = 'objectives/persistence/system/service/loader::mz-stager-msdtc-oci-service-replacement'
variants = {
    'positive': (blob, {native, service}),
    'no-mz-restore': (blob.replace(header, header[:5] + b'N' + header[6:]), set()),
    'no-oci': (blob.replace('oci.dll'.encode('utf-16le'), 'ocx.dll'.encode('utf-16le')), {native}),
    'no-msdtc-config': (blob.replace('sc config msdtc'.encode('utf-16le'), 'sc config msdtx'.encode('utf-16le')), {native}),
}
results = []
for name, (data, required) in variants.items():
    path = args.scratch / (name + '.exe')
    path.write_bytes(data)
    run = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', str(path)],
                         text=True, capture_output=True, check=True)
    report = json.loads(run.stdout)
    traits = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    actual = traits & {native, service}
    assert actual == required, (name, actual, required)
    results.append({'case': name, 'matched': sorted(actual)})
    print('PASS', name)
(args.scratch / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
