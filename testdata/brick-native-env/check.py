#!/usr/bin/env python3
"""Static controls for the brick native environment stealer; never execute it.

Usage: python3 check.py ORIGINAL_TGZ SCRATCH_DIRECTORY
The original sample remains external. All generated binaries are inert analysis
controls, not benign software; only the payload-free loader is a benign control.
"""
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

archive, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
traits = Path(__file__).resolve().parents[2]
with tarfile.open(archive) as src:
    binary = src.extractfile('package/prebuilds/linux-x64/metrics.node').read()
    loader = src.extractfile('package/index.js').read()
    manifest = json.load(src.extractfile('package/package.json'))

variants = {
    'renamed': binary.replace(b'oob.s4yhii.com', b'api.test.local'),
    'no-secrets': binary,
    'no-detach': binary.replace(b'setsid', b'getpid'),
    'no-post': binary.replace(b'POST /native', b'HEAD /native'),
    'no-json-members': binary.replace(b'%s"%s":"%s"', b' ' * 11),
    'no-socket-options': binary.replace(b'setsockopt', b'X' * 10),
    'no-http-version': binary.replace(b'HTTP/1.0', b'NOPE/0.0'),
    'http2-version': binary.replace(b'HTTP/1.0', b'HTTP/2.0'),
    'http3-version': binary.replace(b'HTTP/1.0', b'HTTP/3.0'),
}
for token in (
    b'AWS_ACCESS_KEY_ID', b'AWS_SECRET_ACCESS_KEY', b'AWS_SESSION_TOKEN',
    b'GITHUB_TOKEN', b'NPM_TOKEN', b'NODE_AUTH_TOKEN', b'SYSTEM_ACCESSTOKEN',
    b'ACTIONS_RUNTIME_TOKEN', b'ACTIONS_ID_TOKEN_REQUEST_TOKEN',
):
    variants['no-secrets'] = variants['no-secrets'].replace(token, b'X' * len(token))
for name, data in variants.items():
    (scratch / (name + '.node')).write_bytes(data)
manifest.update(version='1.0.0', files=['index.js', 'native'])
loader = loader.replace(b'prebuilds', b'native').replace(b'metrics.node', b'addon.node')
for name, payload in [('renamed', variants['renamed']), ('optional-loader', None)]:
    members = [('package/package.json', json.dumps(manifest).encode()),
               ('package/index.js', loader)]
    if payload is not None:
        members.append(('package/native/linux-x64/addon.node', payload))
    with tarfile.open(scratch / (name + '.tgz'), 'w:gz') as out:
        for path, data in members:
            info = tarfile.TarInfo(path)
            info.size = len(data)
            out.addfile(info, io.BytesIO(data))
for name, code in {
    'env-spread': 'const x = {...process.env};',
    'env-keys': 'const x = Object.keys(process.env);',
    'env-entries': 'const x = Object.entries(process.env);',
    'object-keys': 'const x = Object.keys({a: 1});',
}.items():
    (scratch / (name + '.js')).write_text(code + '\n')

result = subprocess.run(['cleave', '--traits-dir', str(traits), '--format', 'json',
                         str(scratch)], check=True, capture_output=True, text=True)
# Directory JSON output consists of consecutive objects.
text = result.stdout.lstrip()
decoder = json.JSONDecoder()
files = {}
while text:
    report, end = decoder.raw_decode(text)
    text = text[end:].lstrip()
    for file in report['files']:
        files[file['path']] = {t['id']: t['crit'] for t in file.get('traits', [])}
def ids(name):
    return files[str(scratch / name)]
def hostile(name):
    return {key for key, crit in ids(name).items() if crit == 5}
core = 'objectives/exfiltration/stealer/env::detached-node-addon-credential-json-http-exfil'
package = 'objectives/exfiltration/stealer/env::npm-native-env-stealer-with-silent-loader'
assert hostile('renamed.node') == {core}
assert hostile('renamed.tgz') == {core, package}
for name in ['no-secrets', 'no-detach', 'no-post', 'no-json-members']:
    assert not hostile(name + '.node'), name
assert not hostile('optional-loader.tgz')
assert sum(c == 4 for c in ids('optional-loader.tgz').values()) <= 1
for trait in ['aws-env-secret-vars', 'aws-secret-access-key-var',
              'aws-access-key-pair-names-binary', 'github-token-name-reference']:
    key = 'micro-behaviors/os/env/secret-name::' + trait
    assert key in ids('renamed.node') and key not in ids('no-secrets.node'), key
for trait in ['actions-runtime-token-name', 'system-accesstoken-name']:
    key = 'micro-behaviors/os/env/ci-credentials::' + trait
    assert key in ids('renamed.node') and key not in ids('no-secrets.node'), key
socket = 'micro-behaviors/communications/socket/configure::setsockopt-import'
assert socket in ids('renamed.node') and socket not in ids('no-socket-options.node')
version = 'micro-behaviors/communications/http/message::'
assert version + 'http-versions' in ids('renamed.node')
assert version + 'http-versions' not in ids('no-http-version.node')
assert version + 'http2-version' in ids('http2-version.node')
assert version + 'http3-version' in ids('http3-version.node')
enumeration = 'micro-behaviors/os/env/enumeration::'
for name, atom in [('env-spread', 'js-process-env-spread'),
                   ('env-keys', 'js-object-keys-env'),
                   ('env-entries', 'js-object-entries-env')]:
    assert enumeration + atom in ids(name + '.js'), name
for atom in ['js-process-env-spread', 'js-object-keys-env', 'js-object-entries-env']:
    assert enumeration + atom not in ids('object-keys.js')
# Pure OR composites and exceptions are intentionally omitted from rendered
# scan output. Check the actual exception, not only its constituent findings.
telemetry = """const report = {packageManager: process.env.npm_config_user_agent};
fetch('https://example.com/event', {method: 'POST',
 headers: {'Content-Type': 'application/json'}, body: JSON.stringify(report)});
"""
exception = 'micro-behaviors/os/env/package-manager::selective-npm-agent-telemetry'
for name, extra, expected in [('selective-telemetry', '', True),
                              ('bulk-telemetry', 'const x = {...process.env};', False)]:
    fixture = scratch / (name + '.js')
    fixture.write_text(telemetry + extra)
    trace = subprocess.run(['cleave', '--traits-dir', str(traits), 'test-rules',
                            str(fixture), '--rules', exception],
                           check=True, capture_output=True, text=True).stdout
    prefix = 'MATCHED ' if expected else 'NOT MATCHED '
    assert '\n' + prefix + exception in trace, trace
print('PASS: renamed payload/archive, four missing-behavior controls, benign loader,')
print('credential-name moves, socket configuration, protocol versions, env enumeration')
