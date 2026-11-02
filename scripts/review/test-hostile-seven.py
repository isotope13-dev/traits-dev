#!/usr/bin/env python3
"""Static binding and near-miss checks for the seven hostile-pool artifacts.

Fixtures are read as data and never executed. Tier expectations for the two
Ruby toolkits reflect the explicit endpoint classification policy.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default=os.environ.get('CLEAVE', str(repo.parent / 'cleave/target/release/cleave')))
args = parser.parse_args()
temporary = tempfile.TemporaryDirectory(prefix='hostile-seven-controls-')
directory = Path(temporary.name)
payload = (repo / 'testdata/hostile/generated/ruby-bad-review/unsafe-runner/sample.rb').read_text()
recon = (repo / 'testdata/hostile/generated/ruby-bad-review/recon-helper/sample.rb').read_text()
identity = (repo / 'testdata/hostile/generated/ruby-bad-review/identity-staging/sample.rb').read_text()
manifest = json.loads((repo / 'testdata/hostile/generated/hostile-seven-review/dependency-bundle/package.json').read_text())
ids = {
 'runner': 'objectives/execution/payload/file-exec/command/fetch::ruby-unverified-download-pty-eval-toolkit',
 'pty': 'micro-behaviors/process/tty/pty::ruby-pty-shell-identity-environment-writes',
 'collector': 'objectives/credential-access/files/secret-sweep::ruby-credential-store-host-environment-inventory',
 'identity': 'micro-behaviors/communications/http/request/encoded::ruby-base64-user-platform-post-body-flow',
 'staging': 'objectives/exfiltration/stealer/system-info/profile::ruby-encoded-user-profile-post-staging',
 'token': 'micro-behaviors/os/env/write::decoded-token-environment-assignment',
 'deps': 'metadata/package/dependencies/composition::npm-credential-store-capture-upload-dependencies',
}
cases = []

def add(name, text, expect):
    p = directory / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    cases.append({'path': str(p), 'expect': sorted(expect)})

add('runner-original.rb', payload, {'runner', 'pty'})
add('runner-create.rb', payload.replace('Tempfile.new(', 'Tempfile.create('), {'runner', 'pty'})
add('runner-renamed.rb', payload.replace('PayloadRunner', 'StageSupport').replace('execute_script', 'invoke_script').replace('stdin', 'writer'), {'runner', 'pty'})
add('runner-verified-tls.rb', payload.replace('OpenSSL::SSL::VERIFY_NONE', 'OpenSSL::SSL::VERIFY_PEER'), {'pty'})
add('runner-no-eval.rb', payload.replace('result = eval(code)', 'result = code'), {'pty'})
add('runner-unrelated-io.rb', payload.replace('stdin.puts(', 'unrelated.puts('), set())
add('runner-no-response-flow.rb', payload.replace('execute_script(interpreter, resp.body)', 'execute_script(interpreter, "fixed diagnostics")'), {'pty'})
add('runner-quoted.rb', "example = <<'CODE'\n" + payload + '\nCODE\n', set())
add('collector-original.rb', recon, {'collector'})
add('collector-renamed.rb', recon.replace('patterns', 'targets').replace('content', 'bytes').replace('run_cmd', 'invoke'), {'collector'})
add('collector-no-env.rb', recon.replace('ENV.to_hash.map { |k, v| "#{k}=#{v}" }.join("\\n")', '"not collected"'), set())
add('collector-no-cloud.rb', recon.replace('~/.config/gcloud/credentials.db', '~/.config/app/preferences.json'), set())
add('collector-unrelated-hash.rb', recon.replace('Digest::SHA256.hexdigest(content)', 'Digest::SHA256.hexdigest("fixed control")'), set())
add('collector-quoted.rb', "example = <<'CODE'\n" + recon + '\nCODE\n', set())
add('identity-original.rb', identity, {'identity', 'staging'})
add('identity-renamed.rb', identity.replace('info', 'profile').replace('req.', 'message.').replace('req =', 'message ='), {'identity', 'staging'})
add('identity-unrelated-body.rb', identity.replace('req.body = info', 'req.body = "status=ok"'), set())
add('identity-other-request.rb', identity.replace('req.body = info', 'other.body = info'), set())
add('identity-no-user.rb', identity.replace("#{ENV['USER']}", 'anonymous'), set())
add('identity-dns.rb', identity.replace('45.9.1.2', 'telemetry.example'), {'identity'})
add('identity-quoted.rb', "example = <<'CODE'\n" + identity + '\nCODE\n', set())
add('manifest-original/package.json', json.dumps(manifest), {'deps'})
changed = dict(manifest)
changed.update(name='different-application', author='different-author', version='42.1.0', main='start.js', bin='start.js')
add('manifest-renamed/package.json', json.dumps(changed), {'deps'})
for package in ('@primno/dpapi', 'sqlite3', 'level', 'screenshot-desktop', 'vdf-parser', 'archiver', 'form-data', 'axios'):
    changed = json.loads(json.dumps(manifest))
    del changed['dependencies'][package]
    add('manifest-without-' + package.replace('@', '').replace('/', '-') + '/package.json', json.dumps(changed), set())


encoded = ''.join('\\u%04x' % ord(c) for c in 'process.env.ACCESS_TOKEN = this.accessToken')
add('encoded-token.js', 'const retained = "' + encoded + '";', {'token'})
add('encoded-other-key.js', 'const retained = "' + ''.join('\\u%04x' % ord(c) for c in 'process.env.DEBUG = value') + '";', set())
add('encoded-comparison.js', 'const retained = "' + ''.join('\\u%04x' % ord(c) for c in 'process.env.ACCESS_TOKEN === value') + '";', set())

env = dict(os.environ, CLEAVE_RAYON_THREADS='4', ATOMDRIFT_ENRICHED='0')
result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--json'] + [x['path'] for x in cases],
                        env=env, text=True, capture_output=True, check=True)
seen = {}
for line in result.stdout.splitlines():
    for item in json.loads(line)['files']:
        seen[item['path']] = {k for k, value in ids.items() if any(t['id'] == value for t in item.get('traits', []))}
failures = []
for case in cases:
    actual = seen.get(case['path'])
    if actual != set(case['expect']):
        failures.append((Path(case['path']).relative_to(directory), case['expect'], actual))
assert not failures, failures
temporary.cleanup()
print(f'Hostile-seven binding regressions passed: {len(cases)} cases')
