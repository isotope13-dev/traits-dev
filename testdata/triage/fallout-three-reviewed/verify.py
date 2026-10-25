#!/usr/bin/env python3
"""Static mutation controls. Inputs are read as bytes and never executed."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, required=True)
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--before-traits', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.scratch.mkdir(parents=True, exist_ok=True)
vb = (args.samples / '0bad645c0037/QaCnurm.decoded.IvMsuF.txt.bin.gunzip').read_bytes()
cil = (args.samples / '03b12f133dd1/QaCnurm.decoded.JSAmBw.txt.bin').read_bytes()
persist = 'objectives/persistence/login/registry/autostart::vb6-surveillance-active-setup-registration'
keylog = 'objectives/collection/keylog/hook::vb6-keyboard-hook-buffered-recording'
conceal = 'objectives/anti-static/obfuscation/imports/concealment::managed-encoded-injection-api-resolution'
hollow = 'objectives/evasion/process/injection/hollowing/process::cil-base64-delegate-image-replacement'
old_profile = 'objectives/anti-static/obfuscation/imports/concealment::vb6-runtime-windowproc-process-scan'
new_profile = 'micro-behaviors/process/enumerate/snapshot::vb6-windowproc-process-api-profile'


def replace(data, old, new):
    assert len(old) == len(new) and old in data
    return data.replace(old, new)


def write(name, data):
    path = args.scratch / name
    path.write_bytes(data)
    return path


hook_pattern = rb'\xf5\x0d\x00\x00\x00\x5e..\x10\x00\x71..\x3c'
no_hook, count = re.subn(hook_pattern, lambda m: m[0][:1] + b'\x0e' + m[0][2:], vb)
assert count
cases = [
    ('vb-positive', write('vb-positive.bin', vb), {persist, keylog, new_profile}, set()),
    ('vb-no-stubpath', write('vb-no-stubpath.bin', replace(vb, 'StubPath'.encode('utf-16le'), 'StubPaxx'.encode('utf-16le'))), {keylog}, {persist}),
    ('vb-no-keyboard-hook-type', write('vb-no-keyboard-hook-type.bin', no_hook), {persist}, {keylog}),
    ('cil-positive', write('cil-positive.bin', cil), {conceal, hollow}, set()),
    ('cil-no-encoded-create', write('cil-no-encoded-create.bin', replace(cil, 'Q3JlYXRlUHJvY2Vzc0E='.encode('utf-16le'), 'Q3JlYXRlUHJvY2Vzc0I='.encode('utf-16le'))), set(), {conceal, hollow}),
]


def scan(path, traits):
    result = subprocess.run(['cleave', '--traits-dir', str(traits), '--format', 'json', str(path)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report.get('files'), result.stderr
    return {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}


def check(case):
    name, path, required, forbidden = case
    traits = scan(path, root)
    assert required <= traits.keys(), (name, required - traits.keys())
    assert not forbidden & traits.keys(), (name, forbidden & traits.keys())
    return name, {'required_present': sorted(required), 'forbidden_absent': sorted(forbidden),
                  'hostile': sorted(t for t, crit in traits.items() if crit == 5)}


with ThreadPoolExecutor(max_workers=3) as pool:
    results = dict(pool.map(check, cases))

# Real checked-in control artifacts outside this batch: preserve the complete
# attack finding set and avoid assigning the newly added objectives to them.
for rel in ['testdata/benign/crashpad-client-injection-controls.exe',
            'testdata/benign/keylog-dropper-controls.exe',
            'testdata/hostile/native-directory-result-hide-hook.exe']:
    before = scan(root / rel, args.before_traits)
    after = scan(root / rel, root)
    assert not ({persist, keylog, conceal} & after.keys()), rel
    assert {k for k, v in before.items() if v >= 4} <= after.keys(), rel
    results[rel] = {'lost': sorted(before.keys() - after.keys()),
                    'added': sorted(after.keys() - before.keys())}

# The relocated observation keeps every required leg. Its exact consumer must
# retain that observation as a required leg under its new canonical ID.
old_source = args.before_traits / 'objectives/anti-static/obfuscation/imports/concealment/vb6-windowproc-process-scan.yaml'
new_source = root / 'micro-behaviors/process/enumerate/snapshot/vb6-windowproc.yaml'
old_legs = re.findall(r'^      - id: (.*)$', old_source.read_text(), re.M)
new_legs = re.findall(r'^      - id: (.*)$', new_source.read_text(), re.M)
assert old_legs == new_legs
consumer = (root / 'objectives/impact/infect/binary/rewrite/vb6-binder.yaml').read_text()
assert new_profile in consumer and old_profile not in consumer
results['relocation'] = {'preserved_legs': old_legs, 'exact_consumer_updated': True}
(args.scratch / 'controls.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'{len(cases)} mutation controls, 3 outside artifacts, and relocation checks passed')
