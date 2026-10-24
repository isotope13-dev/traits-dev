#!/usr/bin/env python3
"""Check campaign reconstructions and benign/near-miss controls with local traits."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REQUEST = 'micro-behaviors/communications/http/request/superglobal::php-request-hash-equals-comparison'
CAP = 'micro-behaviors/os/user/account::wordpress-privileged-cap-grant'
LOGIN = 'objectives/command-and-control/backdoor/auth-bypass::wordpress-request-token-backdoor-login'
ADMIN = 'objectives/command-and-control/backdoor/auth-bypass::wordpress-fixed-token-administrator-login'
CREATE = 'objectives/persistence/login/account/create::wordpress-token-privileged-user-bootstrap'

expected = {
    'privileged-service-account.php': {REQUEST, CAP, LOGIN, CREATE},
    'administrator-bootstrap.php': {REQUEST, LOGIN, CREATE},
    'existing-administrator-login.php': {REQUEST, LOGIN, ADMIN},
    'token-only.php': {REQUEST},
    'request-carrier-variants.php': {REQUEST},
    'dynamic-magic-login.php': {REQUEST},
    'editor-registration.php': {REQUEST},
    'capability-explicit-grant.php': {CAP},
    'capability-denial.php': set(),
    'documented-api-names.php': set(),
    'unrelated-comparison.php': set(),
}
paths = sorted(HERE.glob('*.php')) + sorted((HERE / 'controls').glob('*.php'))
assert {p.name for p in paths} == set(expected)
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_UPDATE='1', SCAN_HOPPER='')
result = subprocess.run(
    ['atomscan', '--mode', 'slow', '--follow=none', '--format', 'json', *map(str, paths)],
    env=env, check=False, capture_output=True, text=True, timeout=180,
)
assert result.returncode in (0, 1), result.stderr
seen = set()
for line in result.stdout.splitlines():
    for file in json.loads(line)['raw']['files']:
        path = Path(file['path'])
        seen.add(path.name)
        traits = file.get('traits', [])
        ids = {t['id'] for t in traits}
        assert expected[path.name] <= ids, (path.name, expected[path.name] - ids)
        if path.parent.name == 'controls':
            assert not [t for t in traits if t['crit'] >= 4], path.name
            if path.name in {'documented-api-names.php', 'unrelated-comparison.php'}:
                assert REQUEST not in ids, path.name
            if path.name == 'capability-denial.php':
                assert CAP not in ids, path.name
        else:
            assert sum(t['crit'] == 5 for t in traits) >= 2, path.name
assert seen == set(expected), (seen, set(expected))
print(f'Passed: {len(seen)} reconstructions and controls; each hostile sample has at least two hostile traits.')
