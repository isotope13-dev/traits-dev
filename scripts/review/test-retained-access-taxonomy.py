#!/usr/bin/env python3
"""Check remote SSH key deployment and sshd override evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
assert not (repo / 'objectives/persistence/login/ssh-authorized-keys').exists()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
attack = '''for _, cred in ipairs(credentials) do
 local cmd = string.format("sshpass -p %s ssh -o StrictHostKeyChecking=no %s@%s 'echo key >> ~/.ssh/authorized_keys'", cred.password, cred.user, host)
 os.execute(cmd)
end
'''
with tempfile.TemporaryDirectory(prefix='retained-access-') as tmp:
    root = Path(tmp)
    cases = {
        'redis.sh': '#!/bin/sh\n# CONFIG SET dbfilename authorized_keys\n# CONFIG SET dir /root/.ssh\n# SET k ssh-rsa AAAAkey\n# SAVE\\r\\n\n',
        'redis_no_save.sh': '#!/bin/sh\n# CONFIG SET dbfilename authorized_keys\n# CONFIG SET dir /root/.ssh\n# SET k ssh-rsa AAAAkey\n',
        'implant.php': '<?php file_put_contents("/root/.ssh/authorized_keys", "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA' + 'A' * 42 + '");',
        'key_only.php': '<?php $key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA' + 'A' * 42 + '";',
        'ssh-reference.swift': 'let path = "/root/.ssh/authorized_keys"\nlet key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA' + 'A' * 42 + ' backdoor@example"\n',
        'ssh-eviction.sh': '#!/bin/sh\nrm -rf .ssh && mkdir .ssh\necho key >> .ssh/authorized_keys\n',
        'ssh-reset-only.sh': '#!/bin/sh\nrm -rf .ssh && mkdir .ssh\n',
        'deploy.lua': attack,
        'no_execution.lua': attack.replace('os.execute(cmd)', 'print(cmd)'),
        'override.sh': "printf 'ExecStart=\\nExecStart=/usr/sbin/sshd -D -o AuthorizedKeysFile=/var/lib/keys' > /etc/systemd/system/sshd.service.d/override.conf\n",
        'unrelated.sh': "printf 'ExecStart=\\nExecStart=/usr/sbin/sshd -D' > /etc/systemd/system/sshd.service.d/override.conf\n",
    }
    for name, text in cases.items():
        (root / name).write_text(text)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    php_backdoor = 'objectives/command-and-control/backdoor/ssh::php-ssh-backdoor'
    php_write = 'micro-behaviors/communications/ssh/keys::php-authorized-keys-write'
    assert php_backdoor in ids['implant.php'], ids['implant.php']
    assert php_write in ids['implant.php']
    assert php_backdoor not in ids['key_only.php']
    swift_profile = 'metadata/file/profile/credential-terms::swift-ssh-key-path-backdoor-text-clues'
    eviction = 'objectives/command-and-control/backdoor/ssh::ssh-trust-store-eviction'
    assert swift_profile in ids['ssh-reference.swift'], ids['ssh-reference.swift']
    assert eviction in ids['ssh-eviction.sh'], ids['ssh-eviction.sh']
    assert eviction not in ids['ssh-reset-only.sh']
    redis = 'objectives/command-and-control/backdoor/install::redis-authorized-keys-backdoor'
    assert redis in ids['redis.sh'], ids['redis.sh']
    assert redis not in ids['redis_no_save.sh']
    deployment = 'objectives/lateral-movement/ssh/deploy-backdoor::lua-credential-loop-installs-ssh-key'
    override = 'micro-behaviors/communications/ssh/server::sshd-service-alternate-key-override'
    profile = 'objectives/persistence/login/ssh::rpm-sshd-override-write-clues'
    assert deployment in ids['deploy.lua'], ids['deploy.lua']
    assert deployment not in ids['no_execution.lua']
    assert override in ids['override.sh'], ids['override.sh']
    assert override not in ids['unrelated.sh']
    assert profile not in ids['override.sh']
    print('SSH key deployment, service configuration and installer evidence remain distinct.')
