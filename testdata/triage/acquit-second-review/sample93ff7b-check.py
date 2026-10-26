#!/usr/bin/env python3
"""Check the 93f7/ff78/7bb5 review's source-flow and retained-fixture results.

Usage: python3 sample93ff7b-check.py <cleave JSON stream>
"""
import json
import pathlib
import sys

source = pathlib.Path(sys.argv[1]).read_text()
reports = []
decoder = json.JSONDecoder()
while source.strip():
    source = source.lstrip()
    report, end = decoder.raw_decode(source)
    reports.append(report)
    source = source[end:]
files = {file['path']: file for report in reports for file in report['files']}

def ids(suffix):
    matches = [f for p, f in files.items() if p.endswith(suffix)]
    assert len(matches) == 1, (suffix, len(matches))
    return {t['id'] for t in matches[0].get('traits', [])}

root = 'testdata/triage/acquit-second-review/'
sink = 'micro-behaviors/process/deploy/script-eval::python-get-response-text-exec'
payload = 'objectives/execution/payload/script-eval::pypi-setup-network-code-execution'
result = 'micro-behaviors/fs/read/file/full::node-file-map-base64-result'
assert {sink, payload} <= ids(root + 'compiled-response/setup.py')
assert not {sink, payload} & ids(root + 'local-compilation/setup.py')
assert result in ids(root + 'direct-file-result.js')
assert result not in ids(root + 'unrelated-file-result.js')
assert result in ids('testdata/pivot-framed-review/fixtures/framed-agent.js')
assert result not in ids('testdata/pivot-framed-review/fixtures/different-file-map.js')
read = 'micro-behaviors/fs/read/file/target::host-or-target-named-file-read'
assert read in ids(root + 'target-file.py')
assert read not in ids(root + 'hosts-file.py')
assert 'micro-behaviors/fs/path/config/system::config-hosts' in ids(root + 'hosts-file.py')
assert payload in ids('testdata/hostile/setup-response-execution.tar.gz')
assert 'objectives/exfiltration/stealer/env::python-env-harvest' in ids(
    'testdata/hostile/supply-chain/audit-pypi-build-environment/pypi-build-environment.tar.gz')
for suffix in [root + 'hostname-report.py', root + 'local-compilation/setup.py',
               'testdata/benign/salt-3008.3-fixture.tar.gz',
               'testdata/benign/supply-chain/audit-pypi-build-constant-post/source/setup.py',
               'testdata/benign/npm-versioned-webhook-notify.tgz']:
    f = next(f for p, f in files.items() if p.endswith(suffix))
    assert not [t for t in f.get('traits', []) if t['crit'] >= 4], suffix
cases = json.loads(pathlib.Path('testdata/taxonomy/ruby-env-json-http-flow/cases.json').read_text())
for case in cases['fixtures']:
    actual = ids(case['path'])
    assert set(case['matched']) <= actual, case['path']
    assert not set(case['not_matched']) & actual, case['path']
print('PASS: response execution, file results, target reads, Ruby and retained controls')
