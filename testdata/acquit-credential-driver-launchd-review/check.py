#!/usr/bin/env python3
"""Run only static scans, with fixtures copied outside test-path exclusions."""
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
fixtures = Path(__file__).resolve().parent
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
cleave = os.environ.get('CLEAVE', 'cleave')
AUTO = 'micro-behaviors/os/kernel/driver::native-auto-start-driver-registration'
PERSIST = 'objectives/persistence/system/driver::auto-start-security-killer-driver'
HARVEST = 'objectives/credential-access/validation/check::harvested-aws-credential-live-validation'
LLM = 'objectives/impact/cryptojacking/remote-compute::harvested-aws-bedrock-capacity-probe'
PAIR = 'micro-behaviors/data/db/access::aws-credential-record-pair-correlation'
CAP = 'micro-behaviors/communications/http/services/aws::aws-bedrock-credential-capacity-probe'
APPLE = 'objectives/persistence/system/launchd/masquerade::apple-helper-persistence'
RENDERER = 'objectives/persistence/system/launchd/masquerade::renderer-masquerade-launchd-persistence'

c = (fixtures / 'driver.c').read_text()
py = (fixtures / 'qualifier.py').read_text()
job = plistlib.loads((fixtures / 'job.plist').read_bytes())
cases = {}

def add(name, data, required=(), forbidden=(), maximum=None):
    path = scratch / name
    path.write_bytes(data.encode() if isinstance(data, str) else data)
    cases[name] = (required, forbidden, maximum)

add('driver.c', c, [AUTO, PERSIST], maximum=None)
add('demand-driver.c', c.replace('SERVICE_AUTO_START', 'SERVICE_DEMAND_START'),
    forbidden=[AUTO, PERSIST])
add('ordinary-driver.c', '''void install(void) {
    CreateServiceW(manager, name, display, SERVICE_START,
                   SERVICE_KERNEL_DRIVER, SERVICE_AUTO_START,
                   SERVICE_ERROR_IGNORE, path, 0, 0, 0, 0, 0);
}
''', [AUTO], [PERSIST], 0)
add('separate-start.c', '''void install(void) {
    CreateServiceW(manager, name, display, SERVICE_START,
                   SERVICE_KERNEL_DRIVER, SERVICE_DEMAND_START,
                   SERVICE_ERROR_IGNORE, path, 0, 0, 0, 0, 0);
    configure(SERVICE_AUTO_START);
}
''', forbidden=[AUTO, PERSIST], maximum=0)
add('qualifier.py', py, [PAIR, CAP], [HARVEST, LLM], 0)
# Existing extraction matchers must still distinguish an extracting stage from
# the caller-supplied inventory above. This fixture is scanned, never executed.
extractor = '''
import re
SECRET_PATTERNS = {
    'aws': re.compile(r'aws_access_key_id=([^ ]+)'),
    'secret': re.compile(r'aws_secret_access_key=([^ ]+)'),
    'token': re.compile(r'aws_session_token=([^ ]+)'),
}
def extract(text):
    for kind, pattern in SECRET_PATTERNS.items():
        for value in pattern.findall(text):
            store(kind, value)
'''
add('extracting-qualifier.py', py + extractor, [PAIR, CAP, HARVEST, LLM])
add('job.plist', plistlib.dumps(job), [APPLE, RENDERER])
without_renderer = dict(job, ProgramArguments=job['ProgramArguments'][:1])
add('helper.plist', plistlib.dumps(without_renderer), [APPLE], [RENDERER])
system = dict(job, ProgramArguments=['/System/Library/CoreServices/SyncHelper'])
add('system-job.plist', plistlib.dumps(system), forbidden=[APPLE, RENDERER], maximum=0)
ordinary = dict(job, Label='org.example.cloudsync',
                ProgramArguments=['/Users/build/Library/Example/SyncHelper'])
add('ordinary-job.plist', plistlib.dumps(ordinary), forbidden=[APPLE, RENDERER], maximum=0)

paths = [str(scratch / name) for name in cases]
# These real repository fixtures predate this review, and exercise retained
# malicious launchd behavior and benign secret-scanner/driver near misses.
controls = [
    root / 'testdata/registry-script-review/renamed-agent.py',
    root / 'testdata/benign/pre-commit-secret-scanner-controls.py',
    root / 'testdata/benign/bedrock-billing-controls.py',
    root / 'testdata/registry-source-second-review/driver-type.c',
    root / 'testdata/registry-source-second-review/other-device.c',
    root / 'testdata/hostile/public-github-credential-dump.py',
    root / 'testdata/taxonomy/packed-table-ioctl-boundary/driver-ioctl-call.c',
    root / 'testdata/taxonomy/packed-table-ioctl-boundary/grapheme-packed-table.c',
]
result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'json',
                         *paths, *map(str, controls)],
                        capture_output=True, text=True, check=True)
# The multi-input renderer may concatenate complete JSON objects.
decoder = json.JSONDecoder()
raw = result.stdout
reports = []
while raw.strip():
    report, end = decoder.raw_decode(raw.lstrip())
    reports.append(report)
    raw = raw.lstrip()[end:]
files = [entry for report in reports for entry in report['files']]
records = {}
for entry in files:
    name = Path(entry['path']).name
    found = {t['id']: t['crit'] for t in entry.get('traits', [])}
    records[name] = found
    if name not in cases:
        continue
    required, forbidden, maximum = cases[name]
    assert set(required) <= found.keys(), (name, set(required) - found.keys())
    assert not set(forbidden) & found.keys(), (name, set(forbidden) & found.keys())
    if maximum is not None:
        assert sum(x == 5 for x in found.values()) <= maximum, (name, found)
    print(name, 'passed')
for name in ['pre-commit-secret-scanner-controls.py', 'bedrock-billing-controls.py',
             'driver-type.c', 'other-device.c']:
    assert not any(x == 5 for x in records[name].values()), (name, records[name])
for name in ['renamed-agent.py', 'public-github-credential-dump.py']:
    assert any(x == 5 for x in records[name].values()), (name, records[name])
assert 'micro-behaviors/os/kernel/device::poisonx-compatible-ioctl-constant' in records['driver-ioctl-call.c']
assert 'micro-behaviors/os/kernel/device::poisonx-compatible-ioctl-constant' not in records['grapheme-packed-table.c']
(scratch / 'controls-results.json').write_text(json.dumps(records, indent=2) + '\n')
print('All generated controls and eight pre-existing fixtures passed.')
