#!/usr/bin/env python3
"""Focused behavior, relocation, and retained-attack controls."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'metadata/lang/source/naming/interface::wordpress-lowercase-api-symbol'
PASS = 'metadata/lang/source/syntax/key-value::wordpress-user-password-field'
LOGIN = 'metadata/lang/source/naming/target::user-login-token'
COOKIE = 'micro-behaviors/os/security/auth/session::wordpress-persistent-auth-cookie'
EDITOR = 'micro-behaviors/os/user/account::wordpress-create-editor'
CAP = 'micro-behaviors/os/user/account::wordpress-privileged-cap-grant'
ELEVATION = 'objectives/privilege-escalation/elevation-control/permission::wordpress-token-backdoor-editor-elevation'
BYPASS = 'objectives/command-and-control/backdoor/auth-bypass::wordpress-request-token-backdoor-login'
ADMIN = 'objectives/command-and-control/backdoor/auth-bypass::wordpress-fixed-token-administrator-login'
CREATE = 'objectives/persistence/login/account/create::wordpress-token-privileged-user-bootstrap'
HIDE = 'objectives/command-and-control/backdoor/webshell/hide::wp-user-hiding'
OVERWRITE = 'objectives/execution/exploit/access-control::wordpress-admin-router-password-overwrite'
expected = {
    'request-map-no-send.php': ({PASS}, {'objectives/command-and-control/backdoor/webshell/exec::php-remote-code-forwarder'}),
    'request-code-forwarder.php': ({'objectives/command-and-control/backdoor/webshell/exec::php-remote-code-forwarder'}, set()),
    'persistent-cookie.php': ({COOKIE}, set()),
    'session-cookie.php': (set(), {COOKIE}),
    'editor-customization.php': ({EDITOR, CAP}, {ELEVATION, CREATE, BYPASS}),
    'editor-query.php': (set(), {EDITOR}),
    'array-password.php': ({PASS}, set()),
    'wp-prefix.php': ({PREFIX}, set()),
    'bare-login-token.php': ({LOGIN}, set()),
    'password-overwrite-client.js': ({PASS, OVERWRITE}, set()),
    'user-query-hide.php': ({LOGIN, HIDE}, set()),
    'user-query-only.php': ({LOGIN}, {HIDE}),
    'wp-path-controls.php': ({PREFIX}, set()),
    'privileged-service-account.php': ({BYPASS, CREATE, ELEVATION, EDITOR, COOKIE}, set()),
    'administrator-bootstrap.php': ({BYPASS, CREATE}, {ELEVATION}),
    'existing-administrator-login.php': ({BYPASS, ADMIN, COOKIE}, {ELEVATION}),
}
paths = sorted((HERE / 'controls').glob('*'))
old = ROOT / 'testdata/taxonomy/updraftcentral-key-abuse'
paths += sorted(old.glob('*.php')) + sorted((old / 'controls').glob('*.php'))
for name in ('dynamic-magic-login.php', 'editor-registration.php', 'token-only.php',
             'request-carrier-variants.php', 'capability-denial.php',
             'capability-explicit-grant.php', 'documented-api-names.php',
             'unrelated-comparison.php'):
    expected[name] = (set(), {ELEVATION})
# Existing positive and near-miss fixture consumers from outside this batch.
for relative in ('testdata/wordpress-dashboard-concealment/cases.json',
                 'testdata/triage/smithnode-rule-controls/cases.json'):
    for case in json.loads((ROOT / relative).read_text())['fixtures']:
        path = ROOT / case['path']
        paths.append(path)
        expected[path.name] = (set(case['matched']), set(case['not_matched']))
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_UPDATE='1', SCAN_HOPPER='')
result = subprocess.run(['atomscan', '--mode', 'slow', '--follow=none', '--format',
                         'json', *map(str, paths)], env=env, check=False,
                        capture_output=True, text=True, timeout=600)
assert result.returncode in (0, 1), result.stderr
seen = set()
records = []
for line in result.stdout.splitlines():
    for file in json.loads(line)['raw']['files']:
        name = Path(file['path']).name
        seen.add(name)
        traits = file.get('traits', [])
        ids = {t['id'] for t in traits}
        yes, no = expected[name]
        assert yes <= ids, (name, 'missing', yes - ids)
        assert not no & ids, (name, 'unexpected', no & ids)
        # New benign controls must stay free of inferred malicious intent.
        if Path(file['path']).parent == HERE / 'controls' and name not in {
                'password-overwrite-client.js', 'user-query-hide.php', 'request-code-forwarder.php'}:
            assert not [t for t in traits if t['crit'] >= 4], name
        records.append({'file': name, 'hostile': sum(t['crit'] == 5 for t in traits),
                        'suspicious': sum(t['crit'] == 4 for t in traits)})
assert seen == set(expected), (seen ^ set(expected))
print(json.dumps({'passed': len(seen), 'fixtures': records}, indent=2))
