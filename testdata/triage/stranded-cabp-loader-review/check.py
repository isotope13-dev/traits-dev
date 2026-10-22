"""Static regression controls; sample code is never imported or executed."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--scratch', type=Path, required=True)
p.add_argument('--case', help='Run a single named fixture')
a = p.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).with_name('files')
a.scratch.mkdir(parents=True, exist_ok=True)
eval_id = 'micro-behaviors/process/interpreter/eval/direct::js-eval-variable-argument'
source_id = 'metadata/lang/source/syntax/call::then-eval-ident-callback-source'
gui = 'objectives/impact/degrade/process::ransom-gui-force-kills-explorer'
cryptor = 'objectives/impact/ransom/encrypt/bulk-encryption::ransomware-cbc-glob-encrypt-remove-bytecode'
old = 'objectives/command-and-control/dropper/script-eval/remote-code::then-eval-ident-callback'
cases = [
    ('loader.ejs', {eval_id, source_id, 'metadata/lang/source/syntax/assignment::cjs-exports-pattern'}, {old, gui, cryptor}),
    ('npmrc-auth.js', {'micro-behaviors/fs/write/credential::js-write-credential-dotfile', 'micro-behaviors/fs/path/secret-config::npmrc-credentials', 'micro-behaviors/os/env/secret-name::javascript-credential-env-reference'}, {'micro-behaviors/fs/path/token::developer-credential-stores', 'micro-behaviors/fs/path/credential::token-and-secret-config-paths'}),
    ('recovery-gui.pyc', {gui}, {cryptor}),
    ('file-cryptor.pyc', {cryptor, 'micro-behaviors/fs/search::pyc-iglob-name-record'}, {gui}),
    ('quoted-callback.js', {source_id}, {eval_id, old}),
    ('callback.js', {eval_id, source_id}, {old}),
    ('exports.js', {'metadata/lang/source/syntax/assignment::cjs-exports-pattern'}, set()),
    ('env-write.js', {'micro-behaviors/os/env/secret-name::javascript-credential-env-reference'}, {'micro-behaviors/os/env/secret-name::javascript-credential-env-read'}),
    ('predicate.js', {'metadata/lang/source/syntax/call::js-credential-path-guard'}, {'micro-behaviors/fs/path/credential::js-credential-path-guard'}),
    ('utility-cryptor.pyc', {'micro-behaviors/crypto/symmetric/encrypt::pyc-encrypt-name-record'}, {cryptor, gui}),
    ('gui-without-kill.pyc', {'objectives/impact/ransom/note::close-window-blocks-decryption-warning'}, {gui, cryptor}),
    ('warning.py', {'objectives/impact/ransom/note::close-window-blocks-decryption-warning'}, {gui, cryptor}),
]
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), SCAN_NO_UPDATE='1')
results = []
for name, required, forbidden in cases:
    if a.case and name != a.case:
        continue
    target = a.scratch / name
    shutil.copyfile(fixtures / name, target)
    run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--format', 'json', str(target)], env=env, capture_output=True, text=True)
    assert run.returncode == 0, (name, run.stderr)
    report = json.loads(run.stdout)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    assert required <= traits.keys(), (name, required - traits.keys())
    assert not forbidden & traits.keys(), (name, forbidden & traits.keys())
    if name not in ('recovery-gui.pyc', 'file-cryptor.pyc'):
        ceiling = 4 if name == 'warning.py' else 3
        assert all(t['crit'] <= ceiling for t in traits.values()), (name, [(k, t['crit']) for k, t in traits.items() if t['crit'] > ceiling])
    results.append({'case': name, 'required': sorted(required), 'passed': True})
    print('PASS', name, flush=True)
(a.scratch / ('results-' + a.case + '.json' if a.case else 'results.json')).write_text(json.dumps(results, indent=2) + '\n')
