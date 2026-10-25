#!/usr/bin/env python3
"""Run focused controls under neutral paths, outside test-harness exclusions."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SCRATCH = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/acquit-review')
THEFT = 'objectives/exfiltration/stealer/env::shell-registry-token-curl-stdin-upload'
HIJACK = 'objectives/supply-chain/trojanized/build-pipeline::ci-bash-env-token-network-exfil'
WRITE = 'micro-behaviors/fs/write/file/redirect::shell-cat-heredoc-file-write'
LOAD = 'micro-behaviors/ui/window/event::window-onload-handler-assignment'
XOR = 'micro-behaviors/data/decode/xor::js-character-xor-near-numeric-array'
XOR_PRIMITIVE = 'micro-behaviors/data/decode/xor::fromcharcode-xor-rebuild'
TRANSFER = 'micro-behaviors/communications/transfer::authentication-upload-helper-call'
RELAY = 'objectives/supply-chain/trojanized/build-pipeline::ci-bash-env-secret-relay'
CASES = {}
for name in ['selected-token-upload.sh', 'echo-token-upload.sh', 'printf-token-upload.sh', 'ci-references-only.sh']:
    CASES[name] = ({THEFT}, {HIJACK})
CASES['ci-token-hijack.sh'] = ({THEFT, HIJACK}, set())
for name in ['unrelated-token-and-upload.sh', 'nonsecret-printenv-upload.sh',
             'token-upload-as-header.sh', 'token-output-before-upload.sh', 'generic-service-token-upload.sh',
             'curl-header-stdin.sh', 'echo-literal-token.sh', 'printf-literal-token.sh',
             'redirected-token.sh', 'separate-command-body-option.sh']:
    CASES[name] = (set(), {THEFT, HIJACK})
for name in ['quoted-heredoc.sh', 'unquoted-heredoc.sh']:
    CASES[name] = ({WRITE}, set())
CASES['cat-no-output.sh'] = (set(), {WRITE})
CASES['load-handler.html'] = ({LOAD}, set())
CASES['commented-handler.html'] = (set(), {LOAD})
CASES['numeric-xor-decoder.js'] = ({XOR, XOR_PRIMITIVE,
    'objectives/execution/interpreter/eval/dynamic::xor-array-eval-loader'}, set())
CASES['numeric-array-only.js'] = (set(), {XOR})
CASES['token-upload-call.js'] = ({TRANSFER}, set())
CASES['ordinary-local-call.js'] = (set(), {TRANSFER})
EXTERNAL = {
    'existing-xor.js': 'testdata/benign/kcli-improve/xor-parentheses.js',
    'existing-xor-stage.js': 'testdata/hostile/relay-eval-callee/xor-eval.js',
    'existing-ci-relay.js': 'testdata/bash-env-ci/bridge.js',
    'existing-renamed-relay.js': 'testdata/triage/registry-script-second-pass-20261025/renamed-bridge.js',
    'existing-authentication.sh': 'testdata/benign/shell-keychain-upload-controls/ordinary-authentication.sh',
    'existing-startup.sh': 'testdata/hostile/github-actions-bash-env-hijacker.sh',
}
CASES['existing-xor.js'] = ({XOR_PRIMITIVE}, set())
CASES['existing-xor-stage.js'] = ({'objectives/execution/interpreter/eval/dynamic::js-eval-xor-decoded'}, set())
CASES['existing-ci-relay.js'] = ({RELAY}, set())
CASES['existing-renamed-relay.js'] = ({RELAY}, set())
CASES['existing-authentication.sh'] = ({'micro-behaviors/communications/http/upload::shell-pipeline-curl-stdin-body', 'micro-behaviors/os/env/pipeline::shell-printf-token-curl-pipe'}, {THEFT, HIJACK})
CASES['existing-startup.sh'] = ({'micro-behaviors/os/env/cicd::github-bash-env-file-write'}, set())

with tempfile.TemporaryDirectory(prefix='neutral-controls-', dir=SCRATCH) as work:
    work = Path(work)
    for name in CASES:
        source = ROOT / EXTERNAL[name] if name in EXTERNAL else HERE / name
        (work / name).write_bytes(source.read_bytes())
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--json', str(work)], text=True, capture_output=True, check=True)
    (SCRATCH / 'controls.neutral.jsonl').write_text(result.stdout)
    seen = set()
    for line in result.stdout.splitlines():
        for file in json.loads(line).get('files', []):
            name = Path(file['path']).name
            if name not in CASES:
                continue
            seen.add(name)
            ids = {trait['id'] for trait in file.get('traits', [])}
            yes, no = CASES[name]
            assert yes <= ids, (name, 'missing', sorted(yes - ids))
            assert not no & ids, (name, 'unexpected', sorted(no & ids))
    assert seen == CASES.keys(), ('unscanned', CASES.keys() - seen)
print(f'{len(CASES)} focused and existing controls passed')
