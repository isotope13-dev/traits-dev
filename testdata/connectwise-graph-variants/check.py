"""Check Graph writes and read/quoted-code boundaries without executing fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(os.environ['CLEAVE_GRAPH_FIXTURES'])
CLOUD = 'micro-behaviors/os/security/auth/cloud::'
RBAC = 'micro-behaviors/os/security/auth/rbac::'
CHAIN = 'objectives/persistence/login/oauth::entra-grant-key-and-password-credential'
KEY = CLOUD + 'graph-identity-key-credential-create'
PASSWORD = CLOUD + 'graph-identity-password-credential-create'
WRITE = CLOUD + 'graph-identity-credential-create'
ROLE = RBAC + 'entra-privileged-admin-role-grant'
ROLE_ID = RBAC + 'entra-privileged-role-admin-role-id'
JS_KEY = CLOUD + 'graph-identity-key-js-sdk-post'
JS_PWD = CLOUD + 'graph-identity-password-js-sdk-post'
FETCH_KEY = CLOUD + 'graph-identity-key-fetch-post'
FETCH_PWD = CLOUD + 'graph-identity-password-fetch-post'
FETCH_ROLE = RBAC + 'graph-directory-role-fetch-post'
SDK_KEYS = {CLOUD + f'graph-{resource}-key-sdk-call' for resource in ('application', 'principal')}
CSHARP = {CLOUD + f'graph-{resource}-{action}-csharp-sdk-call' for resource, action in (
    ('application', 'key'), ('principal', 'key'), ('principal', 'password'))}
WRITES = SDK_KEYS | CSHARP | {KEY, PASSWORD, WRITE, JS_KEY, JS_PWD, FETCH_KEY, FETCH_PWD, FETCH_ROLE, ROLE, CHAIN}

# Pure any-groups are omitted from scan output unless needed as evidence.
# Check SDK atoms here; test-rules separately confirms their aggregate groups.
cases = {
    'sdk-key.py': (SDK_KEYS, {ROLE, CHAIN, PASSWORD}),
    'sdk-key.cs': (CSHARP, {ROLE, CHAIN}),
    'sdk-read.py': (set(), WRITES),
    'quoted.py': (set(), WRITES),
    'quoted.cs': (set(), WRITES),
    'sdk-write.js': ({JS_KEY, JS_PWD, KEY, PASSWORD, ROLE, ROLE_ID, CHAIN}, {FETCH_KEY, FETCH_PWD}),
    'sdk-read-unrelated-post.js': (set(), WRITES),
    'fetch-write.js': ({FETCH_KEY, FETCH_PWD, FETCH_ROLE, KEY, PASSWORD, ROLE, CHAIN}, {JS_KEY, JS_PWD}),
    'fetch-write.ts': ({FETCH_KEY, FETCH_PWD, FETCH_ROLE, KEY, PASSWORD, ROLE, CHAIN}, {JS_KEY, JS_PWD}),
    'fetch-read.js': ({ROLE_ID}, WRITES),
    'role-read.py': ({ROLE_ID}, WRITES),
    'role-grant.ps1': ({ROLE_ID, ROLE}, {KEY, PASSWORD, CHAIN}),
    'role-substring.py': (set(), {ROLE_ID, ROLE, CHAIN}),
}
result = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', '.', '--json',
                         *[str(FIXTURES / name) for name in cases]], cwd=ROOT, text=True, capture_output=True)
if result.returncode:
    sys.exit(result.stderr)
observed = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)['files']:
        observed[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
for name, (required, forbidden) in cases.items():
    assert name in observed, f'No report: {name}'
    assert required <= observed[name], f'{name}: missing {required - observed[name]}'
    assert not forbidden & observed[name], f'{name}: unexpected {forbidden & observed[name]}'
print(f'PASS: {len(cases)} Graph variant and boundary fixtures')
