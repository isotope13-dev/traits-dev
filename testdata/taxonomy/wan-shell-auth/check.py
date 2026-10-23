#!/usr/bin/env python3
"""Check curl form authentication binding and retain WAN exploit coverage."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
auth = 'micro-behaviors/communications/http/auth::curl-form-user-auth-option'
identity = 'micro-behaviors/process/user/query::identity-command-token'
hostile = {
    'objectives/execution/exploit/http-command-injection::wan-form-username-shell-injection',
    'objectives/execution/exploit/http-command-injection::wan-form-username-comment-suppression',
}
# Sources are parsed, never executed. Equivalent flag order, line continuation,
# and an absolute executable path must retain the same observation. Quoted
# examples, other programs/protocols, lookalike flags, and unrelated commands
# must not provide the two required arguments to a single curl call.
controls = {
    'long.sh': ('curl --user "$2:$3" --data-urlencode "name=value" "$1"', True),
    'short.sh': ('curl -u "$2:$3" --data-urlencode "name=value" "$1"', True),
    'reordered.sh': ('curl --data-urlencode "name=value" "$1" --user "$2:$3"', True),
    'continued.sh': ('/usr/bin/curl --user "$2:$3" \\\n  --data-urlencode "name=value" "$1"', True),
    'get.sh': ('curl --get --user "$2:$3" --data-urlencode "name=value" "$1"', True),
    'digest.sh': ('curl --digest --user "$2:$3" --data-urlencode "name=value" "$1"', True),
    'user-agent.sh': ('curl --user-agent "agent" --data-urlencode "name=value" "$1"', False),
    'proxy.sh': ('curl --proxy-user "$2:$3" --data-urlencode "name=value" "$1"', False),
    'different-program.sh': ('printf --user "$2:$3" --data-urlencode "name=value"', False),
    'split.sh': ('curl --user "$2:$3" "$1"\ncurl --data-urlencode "name=value" "$1"', False),
    'ftp.sh': ('curl --user "$2:$3" ftp://example.invalid/', False),
    'comment.sh': ('# curl --user "$2:$3" --data-urlencode "name=value" "$1"\ntrue', False),
    'quoted.sh': ('printf "%s" \'curl --user x:y --data-urlencode name=value\'', False),
    'quoted-options.sh': ('curl --data-urlencode "--user" "--data-urlencode" "$1"', False),
    'identity.sh': ('id\nprintf "%s" "x|id > /tmp/value"', False),
}
with tempfile.TemporaryDirectory(prefix='wan-shell-auth-', dir=args.scratch) as temp:
    cases = []
    for name, (source, expected) in controls.items():
        path = Path(temp) / name
        path.write_text('#!/bin/sh\n' + source + '\n')
        required = {auth} if expected else set()
        if name == 'identity.sh':
            required.add(identity)
        cases.append((path, required, set() if expected else {auth}))
    for name in ['setwan-l2tp.sh', 'setwan-background.sh']:
        cases.append((root / 'testdata/hostile/wan-credential-injection' / name,
                      hostile | {auth, identity}, set()))
    for name in ['ordinary-l2tp.sh', 'ordinary-pipeline.sh']:
        cases.append((root / 'testdata/benign/wan-credential-injection' / name,
                      set(), hostile))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--json', 'analyze']
        + [str(path) for path, _, _ in cases],
        capture_output=True, text=True, check=True)
    reports = {}
    for line in result.stdout.splitlines():
        for file in json.loads(line).get('files', []):
            reports[file['path']] = {trait['id'] for trait in file.get('traits', [])}
    for path, required, absent in cases:
        assert str(path) in reports, ('missing report', str(path))
        seen = reports[str(path)]
        assert not required - seen, (str(path), 'missing', sorted(required - seen))
        assert not absent & seen, (str(path), 'unexpected', sorted(absent & seen))
print(f'PASS: {len(cases)} curl authentication, identity, and WAN controls')
