#!/usr/bin/env python3
"""Check neutral primitive placement, retained attacks, and overflow near misses."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
TIMER = 'micro-behaviors/time/schedule/timeout::async-arrow-callback'
DECODE = 'micro-behaviors/data/decode/utf8::base64-buffer-default-text'
FOLLOW = 'objectives/impact/ui/manipulation/social::covert-channel-follow'
OVERFLOW = 'micro-behaviors/ui/window/style::browser-dom-overflow-suppressed'
OPTION = 'micro-behaviors/process/argument/option::noninteractive-flag'
PLUGIN = 'metadata/lang/source/naming/resource::remote-plugin-stage-identifier'
REGISTRATION = 'metadata/lang/source/naming/resource::registration-id-identifier'
LIBRARY = 'micro-behaviors/fs/path/library::certutil-dll-path-reference'

cases = [
    (HERE / 'timer-decoder-follow.js', {TIMER, DECODE, FOLLOW}, set()),
    (HERE / 'explicit-follow.js', {DECODE}, {FOLLOW}),
    (HERE / 'timer-only.js', {TIMER}, {FOLLOW, DECODE}),
    (HERE / 'root-overflow.js', {OVERFLOW}, {FOLLOW}),
    (HERE / 'overflow-read.js', set(), {OVERFLOW}),
    (HERE / 'neutral-options.js', {OPTION, PLUGIN, REGISTRATION}, {FOLLOW}),
    (HERE / 'library-reference.bat', {LIBRARY}, set()),
    (ROOT / 'testdata/hostile/unattended-agent-destruction.js',
     {'objectives/impact/destroy/agent-directed::unattended-agent-destructive-goal'}, set()),
    (ROOT / 'testdata/hostile/encoded-invite-follow.js',
     {'objectives/impact/ui/manipulation/social::encoded-invite-resolved-whatsapp-newsletter-follow'}, set()),
]
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT))
# Test bytes outside a testdata path: the option deliberately retains its
# existing test-harness exclusion, which would otherwise mask the positive.
with tempfile.TemporaryDirectory(prefix='npm-review-', dir=ROOT) as temporary:
    targets = []
    for path, _, _ in cases:
        target = Path(temporary) / path.name
        shutil.copyfile(path, target)
        targets.append(str(target))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'jsonl', *targets],
        text=True, capture_output=True, env=env, check=True)
decoder = json.JSONDecoder()
data = result.stdout
reports = []
while data.strip():
    data = data.lstrip()
    report, end = decoder.raw_decode(data)
    reports.append(report)
    data = data[end:]
by_name = {Path(report["files"][0]["path"]).name: report for report in reports}
for path, required, forbidden in cases:
    report = by_name[path.name]
    files = report.get('files', [report])
    traits = {t['id'] for f in files for t in f.get('traits', [])}
    missing = required - traits
    unexpected = forbidden & traits
    assert not missing and not unexpected, (path.name, sorted(missing), sorted(unexpected))
assert len(reports) == len(cases), (len(reports), len(cases))
print('9 primitive, attack, and near-miss controls passed')
