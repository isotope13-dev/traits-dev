"""Check the behavioral boundary without executing any fixture payload."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
def check_case(case, target):
    ids = case.get('matched', []) + case.get('not_matched', [])
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(root), 'test-rules', '--rules', ','.join(ids), str(target)],
        text=True, capture_output=True, check=True)
    observed = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.MULTILINE))
    missing = set(case.get('matched', [])) - observed
    unexpected = set(case.get('not_matched', [])) & observed
    assert not missing and not unexpected, (case['path'], missing, unexpected, result.stdout, result.stderr)
    print('PASS', case['path'])

for case in cases['fixtures']:
    check_case(case, root / case['path'])

remote = 'objectives/command-and-control/remote-command/tasking::polling-json-file-shell-agent'
mesh = 'objectives/command-and-control/channel/yggdrasil::mesh-http-tasking-agent'
source = (root / 'testdata/hostile/mesh-http-tasking/agent.go').read_text()
with tempfile.TemporaryDirectory(prefix='mesh-controls-') as directory:
    target = Path(directory) / 'renamed.go'
    renamed = source.replace('endpoint', 'gateway').replace('uuid', 'agentID')
    renamed = renamed.replace('201:b479:2771:8df4:b5eb:d007:63b0:2838', '0301:db8::7')
    target.write_text(renamed)
    check_case({'path': 'renamed variables and a different mesh address', 'matched': [remote, mesh]}, target)
    target.write_text(renamed.replace('0301:db8::7', '2001:db8::7'))
    check_case({'path': 'global IPv6 range is not a mesh endpoint', 'matched': [remote], 'not_matched': [mesh]}, target)
