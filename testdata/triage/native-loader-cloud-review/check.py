"""Static controls: accurate observations survive; attack context stays required."""
from pathlib import Path
import json
import os
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CMD = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json']
ENV = dict(os.environ, CLEAVE_VALIDATE='0')

def scan(path):
    r = subprocess.run(CMD + [str(path)], text=True, capture_output=True, check=True, env=ENV)
    assert not r.stderr.strip(), r.stderr
    return {t['id'] for f in json.loads(r.stdout)['files'] for t in f.get('traits', [])}

observations = {
    'micro-behaviors/communications/http/services/aws::ssm-parameters-endpoint-reference',
    'metadata/lang/source/literal::internal-ip-or-family-literal',
    'metadata/lang/source/syntax/key-value::json-body-session-or-hash-key-text',
    'metadata/lang/source/syntax/key-value::markdown-name-call-value',
    'metadata/lang/source/syntax/key-value::repeated-allow-array-fields',
    'metadata/lang/source/naming/setting::claude-code-entrypoint-identifier',
    'metadata/lang/natural/vocabulary/content-word::agent-browser-name-text',
    'metadata/lang/source/syntax/command::gh-auth-login-token-context',
}
positive = scan(HERE / 'observations.js')
assert observations <= positive, observations - positive
negative = scan(HERE / 'near-misses.js')
# The quoted "session:" text remains an honest source-form observation; it
# does not establish a real session field or an HTTP transfer.
assert not (observations - {'metadata/lang/source/syntax/key-value::json-body-session-or-hash-key-text'}) & negative
assert not any(i.startswith(('objectives/exfiltration/', 'objectives/credential-access/')) for i in positive)

bypass = 'objectives/privilege-escalation/elevation-control/uac-bypass/inf::cmstp-inf-mshta-shell-bypass'
assert bypass in scan(HERE / 'cmstp-shell.ps1')
assert bypass not in scan(HERE / 'cmstp-vpn.ps1')
assert bypass not in scan(ROOT / 'testdata/taxonomy/loader-review-boundaries/inf-install.ps1')
old_bypass = 'objectives/privilege-escalation/elevation-control/uac-bypass/inf::cmstp-inf-presetup-bypass-kit'
assert old_bypass in scan(ROOT / 'testdata/taxonomy/loader-review-boundaries/cmstp-disable-uac.ps1')

# An executable's name and an enum word do not establish Defender identity
# or a PowerShell registry policy. The neutral observations remain visible.
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'DefenderHarness.exe'
    path.write_bytes((ROOT / 'testdata/stranded-modmanager-review/php-log-only.exe').read_bytes() + b'\0Unrestricted\0')
    ids = scan(path)
    assert 'metadata/file/naming::defender-related-basename' in ids
    assert 'metadata/lang/natural/vocabulary/content-word::unrestricted-text' in ids
    assert 'well-known/app/security/defender::is-defender-named' not in ids
    assert not any(i.startswith('micro-behaviors/os/registry/access::powershell-policy-state') for i in ids)
print('Passed observation, bypass, identity and policy controls')
