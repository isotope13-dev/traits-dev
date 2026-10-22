#!/usr/bin/env python3
"""Check stream semantics from neutral paths so test-directory exclusions do not mask them."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
stream = 'micro-behaviors/process/io/stream::curl-pipe-ruby-stdin'
old_pipe = 'objectives/command-and-control/dropper/delivery/pipe::curl-pipe-ruby'
old_path = 'micro-behaviors/os/service/config::workflow-user-service-path'
service = 'micro-behaviors/os/service/config::workflow-user-service-config'
stage = 'objectives/supply-chain/hidden-payload/ci::gha-remote-shell-stage'

with tempfile.TemporaryDirectory(prefix='ruby-pipe-', dir=args.scratch) as work:
    work = Path(work)
    for item in fixtures.iterdir():
        if item.suffix in ('.sh', '.yml'):
            shutil.copyfile(item, work / item.name)
    result = subprocess.run([
        args.cleave, '--traits-dir', str(root), '--format', 'json', str(work),
        str(root / 'testdata/benign/github-actions-service-healthcheck/action.yml'),
        str(root / 'testdata/hostile/gha-pipe-stage-controls.tar'),
    ], check=True, capture_output=True, text=True, timeout=180)
    decoder = json.JSONDecoder()
    pending = result.stdout
    files = []
    while pending.strip():
        pending = pending.lstrip()
        report, end = decoder.raw_decode(pending)
        pending = pending[end:]
        files.extend(report['files'])
    by_path = {file['path']: {t['id']: t['crit'] for t in file['traits']} for file in files}
    for name in ('parse-registry.sh', 'execute-response.sh', 'obfuscated-response.sh'):
        traits = by_path[str(work / name)]
        assert traits.get(stream) == 3, (name, traits)
        assert old_pipe not in traits, name
    assert stream not in by_path[str(work / 'disconnected.sh')]
    assert old_path not in by_path[str(work / 'service-input.yml')]
    assert service not in by_path[str(work / 'service-input.yml')]
    assert service in by_path[str(work / 'systemd-directory.yml')]
    health = str(root / 'testdata/benign/github-actions-service-healthcheck/action.yml')
    assert service in by_path[health]
    archive = str(root / 'testdata/hostile/gha-pipe-stage-controls.tar')
    assert by_path[archive].get(stage) == 5
print('PASS: data parsing, source stdin, disconnected commands, unit configuration, hostile archive')
