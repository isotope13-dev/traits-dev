"""Exercise source-to-sink distinctions outside test-directory exclusions.

The Rust control performs an unverified fetch/write/spawn sequence, but has no
attacker-specific admission evidence. A fresh Unix file also lacks execute
permission. The JavaScript control defines an uncalled local runner, computes
stdout/stderr into an unused variable, and posts a fixed literal body; its HTTP
URL is incompatible with https.request. Neither establishes C2 or exfiltration.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
old = root / 'testdata/taxonomy/unconvicted-hostile-triage/files'
spawn = 'micro-behaviors/process/create/subprocess::rust-command-spawn-call'
write = 'micro-behaviors/fs/write/file/response-body::rust-ureq-get-body-to-file'
label = 'metadata/lang/source/declaration::c2-url-constant-assignment'
cases = [
    (old / 'rust-fetch-spawn/build.rs', 'download/build.rs', {spawn, write}, set()),
    (old / 'c2-exec-postback.js', 'postback.js', {label,
        'micro-behaviors/process/create/shell/bridge::js-exec',
        'micro-behaviors/communications/http/request/body::node-bound-request-write-end'}, set()),
    (fixtures / 'deferred.rs', 'deferred.rs', {spawn}, {write}),
    (fixtures / 'thread.rs', 'thread.rs', set(), {spawn, write}),
    (fixtures / 'unrelated-download.rs', 'unrelated/build.rs', {spawn, write}, set()),
    (fixtures / 'unrelated-write.rs', 'unrelated-write.rs', set(), {spawn, write}),
]
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), CLEAVE_SKIP_CACHE='1')
with tempfile.TemporaryDirectory(prefix='flow-review-', dir=args.scratch) as temp:
    targets = []
    for source, name, _, _ in cases:
        target = Path(temp) / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        targets.append(target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'jsonl', *map(str, targets)],
        env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    files = {f['path']: f for report in reports for f in report['files']}
    for target, (_, name, required, absent) in zip(targets, cases):
        traits = files[str(target)].get('traits', [])
        matched = {t['id'] for t in traits}
        assert required <= matched, (name, 'missing', required - matched)
        assert not absent & matched, (name, 'unexpected', absent & matched)
        assert not [t for t in traits if t['crit'] >= 4], (name, 'unsupported intent')
        print('PASS', name)
