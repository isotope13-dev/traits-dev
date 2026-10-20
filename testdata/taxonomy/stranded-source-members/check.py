"""Check stream-read coverage and relocated observations in neutral paths."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--scratch-root', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
repo = root.parents[2]
migration = json.loads((root / 'moves.json').read_text())
mapping = migration['mapping']


def normalize(value):
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()
                if key not in ('id', 'desc')} | {
                    key: mapping.get(item, item)
                    for key, item in value.items() if key == 'id'
                }
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


for old, new in mapping.items():
    if old.endswith('::rocm-experiment'):
        continue  # Consolidated into the existing equivalent identity exception.
    directory, local_id = new.split('::')
    current = []
    for path in (repo / directory).glob('*.yaml'):
        document = yaml.safe_load(path.read_text()) or {}
        for kind in ('traits', 'composite_rules'):
            current.extend({**document.get('defaults', {}), **rule}
                           for rule in document.get(kind, []) if rule['id'] == local_id)
    assert len(current) == 1, new
    original = migration['before'][old]['effective'].copy()
    original.pop('id')
    actual = current[0].copy()
    actual.pop('id')
    assert normalize(original) == normalize(actual), (old, 'changed matching or scope')

cases = {
    'stream-read.php': (['micro-behaviors/fs/read/stream::php-fgets-call'], []),
    'stream-mention.php': ([], ['micro-behaviors/fs/read/stream::php-fgets-call']),
    'child-output.asp': (['micro-behaviors/process/io/stream::wsh-child-output-read-syntax'], []),
    'unrelated-read.asp': ([], ['micro-behaviors/process/io/stream::wsh-child-output-read-syntax']),
}
selected = {root / name: expected for name, expected in cases.items()}
# Reuse existing positives and near misses for traversal, UI and prose.
for manifest in [repo / 'testdata/stranded-empire-seclists/cases.json',
                 root.parent / 'stranded-payload-semantics/cases.json',
                 root.parent / 'stranded-shell-members/cases.json',
                 repo / 'testdata/triage/stranded-member-observations/cases.json']:
    data = json.loads(manifest.read_text())
    entries = data.get('fixtures')
    if entries is None:
        entries = [dict(path=str(manifest.parent / name), **case)
                   for name, case in data.items() if name.endswith('.zip')]
    for case in entries:
        ids = case.get('matched', []) + case.get('not_matched', [])
        relevant = any(('metadata/file/archive::' in t or
                        'metadata/lang/natural/vocabulary::reverse-shell-term' in t or
                        '::php-password-input-element' in t or
                        '::php-command-named-form-control' in t) for t in ids)
        if relevant:
            source = Path(case['path'])
            if not source.is_absolute():
                source = repo / source
            selected[source] = (case.get('matched', []), case.get('not_matched', []))
with tempfile.TemporaryDirectory(prefix='member-controls-', dir=args.scratch_root) as tmp:
    targets, expected = [], {}
    for i, (source, case) in enumerate(selected.items()):
        target = Path(tmp) / f'{i}-{source.name}'
        shutil.copyfile(source, target)
        targets.append(str(target))
        expected[str(target)] = case
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(repo), CLEAVE_VALIDATE='0', CLEAVE_SKIP_CACHE='1')
    result = subprocess.run(['cleave', '--format', 'json', *targets],
                            env=env, capture_output=True, text=True, check=True)
    decoder, remaining, seen = json.JSONDecoder(), result.stdout.strip(), set()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in report.get('files', []):
            if file['path'] not in expected:
                continue
            seen.add(file['path'])
            actual = {t['id'] for t in file.get('traits', [])}
            required, absent = expected[file['path']]
            assert set(required) <= actual, (file['path'], 'missing', set(required) - actual)
            assert not set(absent) & actual, (file['path'], 'unexpected', set(absent) & actual)
    assert len(seen) == len(expected), (len(seen), len(expected))
    print(f'{len(expected)} positive and near-miss controls passed')
