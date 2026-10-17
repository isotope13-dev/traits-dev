#!/usr/bin/env python3
"""Static controls; never execute either the Java fixture or the PE samples."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--samples', type=Path, required=True)
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
args.scratch.mkdir(parents=True, exist_ok=True)
subprocess.run(['javac', '--release', '21', '-d', str(args.scratch),
                str(fixtures / 'ArchiveLauncher.java')], check=True)
pe = args.samples / '3af3a2821500/2026-10-16_211022f60ed940f86c35145d2e526315_destroyer_elex_glassworm_ngrbot_wannacry'
original = pe.read_bytes()
for label, old, new, encoding in [
    ('no-clipboard-label', 'CLIP:', 'NONE:', 'utf-16le'),
    ('no-clipboard-read', 'GetClipboardData', 'GetNotADataField', 'ascii'),
]:
    before, after = old.encode(encoding), new.encode(encoding)
    assert len(before) == len(after) and before in original
    (args.scratch / (label + '.exe')).write_bytes(original.replace(before, after))
paths = [args.scratch, pe, fixtures / 'codeforge.json',
         fixtures / 'owner-project.json', fixtures / 'no-entrypoint.json']
result = subprocess.run([args.cleave, '--traits-dir', '.', '--format', 'json',
                         *map(str, paths)], check=True, capture_output=True, text=True)
# Multiple roots may be rendered as adjacent JSON documents.
files = {}
remaining = result.stdout.lstrip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    files.update({Path(f['path']).name: f for f in report['files']})
    remaining = remaining[end:].lstrip()
ids = lambda name: {t['id'] for t in files[name]['traits']}
neutral = 'micro-behaviors/data/archive/extract/zip::jvm-control-prefixed-zip-process-apis'
entry = 'metadata/package/entrypoint::fabric-codeforge-root-entrypoint'
clipboard = 'objectives/collection/clipboard/capture::managed-keylogger-clipboard-recording'
assert neutral in ids('ArchiveLauncher.class')
assert not any(t['crit'] in (4, 5) for t in files['ArchiveLauncher.class']['traits'])
assert entry in ids('codeforge.json')
assert entry not in ids('owner-project.json')
assert entry not in ids('no-entrypoint.json')
assert clipboard in ids(pe.name)
assert clipboard not in ids('no-clipboard-label.exe')
assert clipboard not in ids('no-clipboard-read.exe')
retired = {
    'objectives/command-and-control/dropper/staging/runtime::jvm-embedded-base64-zip-launch',
    'objectives/supply-chain/trojanized/app/game-mod::fabric-manifest-codeforge-root-entrypoint',
    'objectives/supply-chain/trojanized/app/game-mod::fabric-mod-self-relaunch-stager',
    'objectives/supply-chain/trojanized/app/game-mod::fabric-mod-session-token-child-stage',
}
assert not any(retired & ids(name) for name in files)
print('PASS: benign archive utility, entrypoint boundaries, clipboard positive and near misses')
