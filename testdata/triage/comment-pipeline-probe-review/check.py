"""Behavioral controls; scripts are scanned, never executed."""
from pathlib import Path
import json, os, subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
ENV = dict(os.environ, CLEAVE_VALIDATE='0')
command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
           '--format', 'json', str(BASE)]
result = subprocess.run(command, env=ENV, text=True, capture_output=True)
if result.returncode not in (0, 1):
    raise RuntimeError(result.stderr)
# The multi-file JSON CLI emits successive report objects.
reports, rest, decoder = [], result.stdout, json.JSONDecoder()
while rest.strip():
    rest = rest.lstrip()
    report, offset = decoder.raw_decode(rest)
    reports.extend(report['files'])
    rest = rest[offset:]
by_name = {Path(f['path']).name: f for f in reports}
ids = lambda name: {t['id'] for t in by_name[name].get('traits', [])}
hostile = lambda name: {t['id'] for t in by_name[name].get('traits', []) if t['crit'] == 5}
DUMP = 'objectives/supply-chain/recon-exfil/pipeline::github-actions-memdump-downloader'
CURL = 'micro-behaviors/communications/http/download/curl::'
IDENTITY = 'micro-behaviors/communications/http/request/json::urllib-json-body-host-identity'
for name in ('comment-only.js', 'comment-only.sh', 'unused-command.js', 'unrelated-exec.js'):
    assert not hostile(name), (name, hostile(name))
for name in ('memory-pipeline.sh', 'memory-pipeline.js'):
    assert DUMP in hostile(name), (name, hostile(name))
assert CURL + 'shell-curl-output-option-call' in ids('curl-real-output.sh')
assert CURL + 'source-curl-output-option-text' in ids('curl-long-output.cmd')
for name in ('curl-pipe-compiler.sh', 'remote-agent.sh'):
    assert not {CURL + n for n in ('source-curl-output-option', 'source-curl-output-option-text', 'shell-curl-output-option-call')} & ids(name)
for name in ('dockless-utility.sh', 'project-maintenance.sh'):
    assert not hostile(name), (name, hostile(name))
for name in ('setup.py', 'install.py', 'explicit-profile.py'):
    assert IDENTITY in ids(name), (name, ids(name))
assert IDENTITY not in ids('unrelated-profile.py')
assert len(hostile('remote-agent.sh')) >= 4
assert 'micro-behaviors/os/env/enumeration::python-environ-iteration' in ids('setup.py')
assert 'metadata/lang/source/shape::hash-prefixed-security-testing-text' in ids('setup.py')
assert 'metadata/lang/source/syntax/command::curl-memdump-command-text' in ids('comment-only.js')
assert 'metadata/lang/source/syntax/member::files-map-content-access-text' in ids('comment-only.js')
assert 'metadata/lang/source/syntax/command::sudo-interpreter-pipeline-text' in ids('comment-only.js')
print('PASS: executable pipelines, comment controls, compiler boundary, identity flow, and agent behaviors')
