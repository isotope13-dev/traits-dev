"""Focused controls for reference placement and V8 intent admission.

Copy out of testdata so unrelated testing-context exclusions cannot supply
the result. These byte fixtures are never executed.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parent
repo = root.parents[2]
scratch = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-e78afdd4/scratch')
with tempfile.TemporaryDirectory(prefix='reasoned-controls-', dir=scratch) as tmp:
    cases = [p for p in root.iterdir() if p.suffix in ('.exe', '.yml')]
    for p in cases:
        shutil.copyfile(p, Path(tmp) / p.name)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
         '--format', 'json', tmp],
        capture_output=True, text=True, check=True)
    rest = result.stdout
    reports = {}
    while rest.strip():
        data, end = json.JSONDecoder().raw_decode(rest.lstrip())
        rest = rest.lstrip()[end:]
        for f in data['files']:
            reports[f['path']] = {t['id'] for t in f.get('traits', [])}
    def traits(name):
        return reports[str(Path(tmp) / name)]
    aws = 'metadata/build/ci/step::aws-configure-credentials-action-reference'
    call = 'metadata/lang/source/syntax/call/invocation::wide-include-require-call-text'
    php = 'metadata/lang/encoded/wide::php'
    xor = 'micro-behaviors/data/encoding/xor::v8-modulo-xor-indexed-store'
    calls = 'metadata/binary/code/bytecode::v8-paired-calls-reuse-register'
    hostile = 'objectives/anti-static/obfuscation/encoding/xor::pkg-v8-xor-with-hidden-defender-exclusion'
    oidc = 'objectives/credential-access/api-harvest/ci-oidc::oidc-permission-with-opaque-shell-step'
    spawn = 'metadata/binary/symbols/name/token::v8-overlay-spawn-name'
    assert aws in traits('keys.yml') and aws in traits('oidc.yml')
    assert aws not in traits('without-aws.yml')
    assert oidc in traits('without-aws.yml')
    assert oidc not in traits('keys.yml') and oidc not in traits('oidc.yml')
    assert call in traits('wide-require.exe') and php not in traits('wide-require.exe')
    assert call in traits('wide-php.exe') and php in traits('wide-php.exe')
    assert call not in traits('wide-without-call.exe')
    assert {xor, calls} <= traits('xor-call-profile.exe')
    assert hostile not in traits('xor-call-profile.exe')
    assert spawn in traits('overlay-spawn.exe')
    assert spawn not in traits('overlay-spawn-near.exe')
    dns = 'third_party/GCTI/Cobaltstrike/Resources/Dnsstager/Bin/V1/47/Through/V4/X'
    alpha = 'metadata/file/profile/string-population::dnsa-push-fragments-only-in-alphabetic-overlay-runs'
    for name in ['resolver-alpha-overlay.exe', 'resolver-crossing-run.exe']:
        assert alpha in traits(name)
        assert dns not in traits(name)
    for name in ['resolver-code-and-alpha.exe', 'resolver-shellcode-overlay.exe']:
        assert alpha not in traits(name)
        assert dns in traits(name)
    print('PASS: AWS key/OIDC references and consumer preservation; UTF-16 PHP/Node')
    print('PASS: generic V8 XOR/calls stay neutral; overlay spawn word boundary')
    print('PASS: alphabetic-overlay DNS false hit removed; code and mixed positives retained')
