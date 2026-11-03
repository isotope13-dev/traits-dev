#!/usr/bin/env python3
"""Check that account request clues do not assert completed account creation."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='account-request-') as tmp:
    root = Path(tmp)
    cases = {
        'form.js': 'fetch("/wp-admin/user-new.php?action=createuser&role=administrator");\n',
        'delete.js': 'const url = "https://example.org/?route=/wp/v2/users&_method=DELETE&username=a&email=a@b.com&password=x&roles=administrator";\n',
        'without-role.js': 'const url = "https://example.org/?route=/wp/v2/users&_method=DELETE&username=a&email=a@b.com&password=x";\n',
        'generic.cs': 'class App { string a = "super_admin"; string b = "PHPSESSID"; string c = "/etc/rc.local"; }\n',
        'netscaler.php': '<?php $a = "/nsconfig/nsapppasswd"; $b = "BACKDOOR_USER"; $c = "/flash/nsconfig/nspeers.conf";\n',
        'account-clues.py': "open('/etc/passwd')\nopen('/etc/shadow')\npasswd_entry = 'root:/root:/bin/sh'\nshadow_entry = '/etc/shadow:19000:0:99999'\n",
        'small.bat': '@echo off\nnet user sample S3curePassword /add\n',
        'large.bat': '@echo off\n' + 'REM padding\n' * 120 + 'net user sample S3curePassword /add\n',
        'node-markers.js': 'const a = "backdoor:x:0:0:Backdoor User"; const b = "shadow-modified:true";\n',
        'php-markers.php': '<?php $a = "BACKDOOR_USER"; $shadow_entry = "x"; $b = ":x:{$BACKDOOR_UID}:{$BACKDOOR_GID}";\n',
        'accounts.passwd': 'helper:x:0:0:admin:/root:/bin/sh\n',
        'passwd-shadow.sh': "#!/bin/sh\necho 'helper:x:0:0:admin:/root:/bin/sh' >> /etc/passwd\necho 'helper:HASH:20000:0:99999:7:::' >> /etc/shadow\n",
        'passwd-only.sh': "#!/bin/sh\necho 'helper:x:0:0:admin:/root:/bin/sh' >> /etc/passwd\n",
        'root-account.sh': '#!/bin/sh\nuseradd -ou 0 -g 0 -s /bin/bash account\n',
        'root-cover.sh': '#!/bin/sh\nuseradd -ou 0 -g 0 -s /bin/bash account\nhistory -c\n',
        'endpoint.json': '{"endpoint":"/_security/user/alice","roles":["superuser"]}\n',
    }
    for name, content in cases.items():
        (root / name).write_text(content)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    url = 'micro-behaviors/communications/http/request/account::method-override-admin-account-clues'
    elastic = 'micro-behaviors/data/db/elasticsearch::es-superuser-endpoint-role-clues'
    wp_form = 'micro-behaviors/communications/http/request/account::js-wordpress-admin-form-clues'
    assert wp_form in ids['form.js'], ids['form.js']
    assert not any(t.startswith('objectives/command-and-control/backdoor/account::') for t in ids['form.js'])
    assert url in ids['delete.js'], ids['delete.js']
    assert url not in ids['without-role.js']
    net_profile = 'metadata/file/profile/credential-terms::php-netscaler-account-label-path-clues'
    role_text = 'metadata/file/profile/credential-terms::dotnet-super-admin-role-text'
    assert net_profile in ids['netscaler.php'], ids['netscaler.php']
    assert role_text in ids['generic.cs'], ids['generic.cs']
    assert 'micro-behaviors/communications/http/services/fortios::fortios-admin-api-dotnet' not in ids['generic.cs']
    assert not any('fortios-dotnet-admin-persistence' in t for t in ids['generic.cs'])
    inline_password = 'micro-behaviors/os/user/create::net-user-add-inline-password'
    assert inline_password in ids['small.bat'], ids['small.bat']
    assert inline_password in ids['large.bat'], ids['large.bat']
    assert not any('batch-stub-adds-account-with-fixed-password' in t for t in ids['small.bat'])
    assert 'metadata/file/profile/credential-terms::node-uid-zero-shadow-status-clues' in ids['node-markers.js'], ids['node-markers.js']
    assert 'metadata/file/profile/credential-terms::php-backdoor-account-field-clues' in ids['php-markers.php'], ids['php-markers.php']
    assert 'metadata/file/profile/credential-terms::passwd-filename-uid-zero-entry-clues' in ids['accounts.passwd'], ids['accounts.passwd']
    assert not any(t.startswith('objectives/command-and-control/backdoor/account::') for t in ids['node-markers.js'] | ids['php-markers.php'] | ids['accounts.passwd'])
    append_backdoor = 'objectives/command-and-control/backdoor/account::uid-zero-passwd-shadow-append'
    assert append_backdoor in ids['passwd-shadow.sh'], ids['passwd-shadow.sh']
    assert append_backdoor not in ids['passwd-only.sh']
    root_account = 'micro-behaviors/os/user/modify::root-equivalent-useradd'
    root_cover = 'objectives/evasion/indicator-removal/logs::root-account-shell-history-erasure'
    assert root_account in ids['root-account.sh'], ids['root-account.sh']
    assert root_account in ids['root-cover.sh'], ids['root-cover.sh']
    assert root_cover not in ids['root-account.sh']
    assert root_cover in ids['root-cover.sh'], ids['root-cover.sh']
    unix_clues = 'micro-behaviors/os/user/modify::python-passwd-shadow-entry-clues'
    assert unix_clues in ids['account-clues.py'], ids['account-clues.py']
    assert not any('root-login-backdoor' in trait for trait in ids['account-clues.py'])
    assert elastic in ids['endpoint.json'], ids['endpoint.json']
    assert not any('watcher-recreates' in trait for trait in ids['endpoint.json'])
    print('Account URL and endpoint clues remain distinct from scheduled creation.')
