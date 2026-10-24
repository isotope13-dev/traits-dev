#!/usr/bin/env python3
"""Exercise option-value provenance, taxonomy moves, and retained consumers."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WRITE = 'micro-behaviors/data/config/write::wordpress-update-option'
STORE = 'micro-behaviors/data/config/write::wordpress-stores-created-user-id'
EQUALS = 'metadata/lang/source/syntax/assignment::uppercase-token-equals-label'
COLON = 'metadata/lang/source/syntax/key-value::uppercase-token-colon-label'
BUFFER = 'micro-behaviors/data/config/schema::config-label-near-byte-array'
CONTEXT = 'metadata/lang/source/shape::source-syntax-known-benign-context'
PANEL = 'objectives/command-and-control/backdoor/webshell/recon::sensitive-path-panel'
CREATE = 'micro-behaviors/os/user/account::wordpress-create-user-admin-role'
CAPTURE = 'objectives/credential-access/capture/input::wordpress-authenticate-password-option-capture'
PROFILE = 'micro-behaviors/mem/create/shared::wordpress-shm-option-api-profile'
OLD = {
    'micro-behaviors/data/db/access::php-update-option',
    'micro-behaviors/data/config/schema::api-named-byte-array-const--rx-7',
    'objectives/persistence/login/account/create::wp-rogue-admin-creation',
}
checks = {
    'option-created-id.php': ({WRITE, STORE}, set()),
    'option-created-with-error-check.php': ({WRITE, STORE}, set()),
    'option-unrelated-id.php': ({WRITE}, {STORE}),
    'option-reassigned-id.php': ({WRITE}, {STORE}),
    'option-definition.php': (set(), {WRITE, STORE}),
    'option-credential-capture.php': ({WRITE, CAPTURE}, {STORE}),
    'option-family-consumer.php': ({WRITE, 'well-known/malware/backdoor/r-evil::r-evil-hacktool-main'}, {STORE}),
    'option-local-profile.php': ({WRITE, PROFILE}, {STORE}),
    'configuration-label.py': ({EQUALS}, {COLON}),
    'label-prose.php': (set(), {BUFFER}),
    'label-near-miss.py': (set(), {EQUALS, COLON}),
    'token-buffer.js': ({EQUALS, BUFFER}, {COLON}),
    'typed-token.py': ({COLON}, {EQUALS}),
    'panel-token-label.php': ({COLON, PANEL}, {CONTEXT}),
    'panel-existing-context.php': (set(), {PANEL}),
    'visible-admin.php': ({CREATE}, set()),
    'hidden-administrator.php': ({CREATE, 'objectives/persistence/login/account/create::wordpress-dashboard-excluded-administrator'}, set()),
    'shared-cache-mesh.php': ({WRITE, PROFILE, 'objectives/persistence/system/supervised::wordpress-concealed-memory-restoration'}, set()),
    'visible-cache-restore.php': ({WRITE, PROFILE}, set()),
}
paths = sorted((HERE / 'controls').glob('*'))
paths += [ROOT / p for p in (
    'testdata/wordpress-dashboard-concealment/visible-admin.php',
    'testdata/wordpress-dashboard-concealment/hidden-administrator.php',
    'testdata/hostile/php-offdisk-restoration/shared-cache-mesh.php',
    'testdata/benign/php-offdisk-restoration/visible-cache-restore.php',
)]
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_UPDATE='1', SCAN_HOPPER='')
result = subprocess.run(
    ['atomscan', '--no-update', '--analyze', 'local', '--mode', 'slow',
     '--follow=none', '--format', 'json', *map(str, paths)],
    env=env, capture_output=True, text=True, timeout=300,
)
assert result.returncode in (0, 1), result.stderr
records = []
for line in result.stdout.splitlines():
    for file in json.loads(line)['raw']['files']:
        name = Path(file['path']).name
        traits = {t['id']: t for t in file.get('traits', [])}
        yes, no = checks[name]
        assert yes <= traits.keys(), (name, 'missing', yes - traits.keys())
        assert not (no | OLD) & traits.keys(), (name, 'unexpected', (no | OLD) & traits.keys())
        if name == 'visible-admin.php':
            assert traits[CREATE]['crit'] == 3
            assert not any(t['crit'] >= 4 for t in traits.values())
        records.append({'file': name, 'passed': True})
assert {r['file'] for r in records} == checks.keys()
print(json.dumps({'passed': len(records), 'fixtures': records}, indent=2))
