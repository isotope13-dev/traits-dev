"""Check source/path binding without executing the analyzed fixtures."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOADER = 'micro-behaviors/process/deploy/module-load::python-http-file-helper-child-module'
JSON = 'micro-behaviors/data/serialize/json::python-aliased-json-dump'
MANIFEST = 'micro-behaviors/data/config/read::python-manifest-urlopen-error-handler'
NATIVE = 'objectives/supply-chain/hidden-payload/native-extension::python-fail-open-unverified-native-stage'
PARSE = 'micro-behaviors/data/parse/json::python-credential-json-parse'
LOG = 'objectives/credential-access/cloud/token/metadata::python-token-parse-failure-log-leak'
PRIOR = ROOT / 'testdata/triage/loader-tunnel-redirect-20261024'
CASES = [
    (HERE / 'renamed-loader.py', [LOADER, JSON], [MANIFEST]),
    (HERE / 'different-return.py', [JSON], [LOADER, MANIFEST]),
    (HERE / 'different-write.py', [JSON], [LOADER, MANIFEST]),
    (HERE / 'different-child-argument.py', [JSON], [LOADER, MANIFEST]),
    (HERE / 'different-bootstrap-source.py', [JSON], [LOADER, MANIFEST]),
    (HERE / 'unrelated-download.py', [], [LOADER, JSON, MANIFEST]),
    (HERE / 'json-alias-near-miss.py', [], [JSON]),
    (HERE / 'credential-json-parse.py', [PARSE, LOG], []),
    (PRIOR / 'remote-runner.py', [LOADER, JSON], [MANIFEST]),
    (PRIOR / 'local-job-runner.py', [], [LOADER, JSON, MANIFEST]),
    (ROOT / 'testdata/hostile/python-silent-native-stage-controls.py', [MANIFEST, NATIVE], []),
    (ROOT / 'testdata/benign/python-transparent-native-provisioner-controls.py', [MANIFEST], [NATIVE]),
]
run = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', *[str(p) for p, _, _ in CASES]],
    env={**os.environ, 'CLEAVE_VALIDATE': '0'},
    check=True, capture_output=True, text=True,
)
remaining = run.stdout.lstrip()
decoder = json.JSONDecoder()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report['files']:
        files[Path(file['path']).resolve()] = {t['id']: t['crit'] for t in file.get('traits', [])}
for path, required, forbidden in CASES:
    traits = files[path.resolve()]
    assert not (set(required) - traits.keys()), (path, 'missing', set(required) - traits.keys())
    assert not (set(forbidden) & traits.keys()), (path, 'unexpected', set(forbidden) & traits.keys())
    if LOADER in traits:
        assert traits[LOADER] == 3
print(f'PASS: {len(CASES)} static controls; native-stage and token-log coverage retained')
