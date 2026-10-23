"""Static controls; never execute the inspected Go or shell code."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent
CLEAVE = os.environ.get('CLEAVE', 'cleave')

def reports(output):
    decoder = json.JSONDecoder()
    while output.strip():
        obj, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        yield obj

paths = [p for p in FIXTURES.iterdir() if p.suffix in {'.go', '.sh', '.zip'} or p.name == 'model-evasion.py']
result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', *map(str, paths)], check=True, capture_output=True, text=True)
by_path = {f['path']: f for r in reports(result.stdout) for f in r['files']}

def traits(name):
    return {t['id']: t['crit'] for t in by_path[str(FIXTURES / name)].get('traits', [])}

tls = 'micro-behaviors/communications/tls/verify/disable::insecure-skip-verify'
unzip = 'micro-behaviors/data/archive/extract/zip::shell-unzip-command-call'
identity = 'well-known/lib/network/grpc-go::grpc-go-library'
assert traits('tls-disabled_test.go')[tls] == 3
assert tls not in traits('tls-verified_test.go')
assert traits('unzip-command.sh')[unzip] == 3
assert unzip not in traits('unzip-mention.sh')
assert traits('genproto-consumer.go')['metadata/import/package::google-genproto-module-import'] == 3
assert not any(t.startswith('well-known/lib/format/google-genproto::') for t in traits('genproto-consumer.go'))
assert identity in traits('source-layout.zip')
assert identity not in traits('module-only.zip')
assert not any(t.startswith('well-known/lib/network/grpc-go::') for t in traits('marker-reference.sh'))
assert 'micro-behaviors/os/env/cicd::multi-ci-provider-env-refs-three-plus' in traits('three-ci.sh')
assert 'micro-behaviors/os/env/cicd::multi-ci-provider-env-refs-three-plus' not in traits('one-ci.sh')

# Low-tier context atoms may be stripped from rendered reports. Query the
# evaluator directly so a filtered alias does not look like lost coverage.
for name, rule in [
    ('one-ci.sh', 'micro-behaviors/os/env/cicd::ci-provider-env-reference-set'),
    ('analysis-wording.sh', 'metadata/lang/natural/phrasing::static-analysis-wording'),
    ('model-evasion.py', 'objectives/anti-static/obfuscation/payload/polymorphic/generator::llm-variant-evasion-directive'),
]:
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(FIXTURES / name), '--rules', rule], check=True, capture_output=True, text=True)
    assert 'MATCHED ' + rule in result.stdout, (name, result.stdout, result.stderr)

for path, f in by_path.items():
    if Path(path).name == 'model-evasion.py':
        continue
    assert not [t for t in f.get('traits', []) if t['crit'] >= 4], path
print('PASS: TLS, unzip, dependency/identity, CI cardinality, and LLM wording controls')
