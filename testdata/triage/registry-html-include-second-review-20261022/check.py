#!/usr/bin/env python3
"""Check changed claims without path-based test exemptions masking results."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
P = 'objectives/execution/exploit/include-gadget::'
S = 'objectives/evasion/masquerade/source-review::'
ROOT_RULE = P + 'request-controlled-include-root'
SHADOW_RULE = S + 'request-constant-shadows-literal-constant'
MOVED = {
 'objectives/execution/exploit/include-gadget::path-constant-from-request-value':
 'micro-behaviors/data/property/define::php-path-constant-from-superglobal',
 'objectives/exfiltration/messaging/webhook::send-message-channel-class-marker':
 'metadata/lang/source/naming/interface::send-message-channel-text',
 'micro-behaviors/os/privilege/licensing::licensekey-field':
 'metadata/lang/source/naming/setting::licensekey-text',
}

def run(scratch, phase):
    # Keep testdata/ and fixtures/ out of analysis paths: those are deliberate
    # exclusion contexts in several original rules, including shadowing.
    cases = scratch / 'cases'
    cases.mkdir(exist_ok=True)
    def copy(source, target):
        target.unlink(missing_ok=True)
        shutil.copy2(source, target)

    for source in HERE.iterdir():
        if source.suffix in {'.php', '.js'}:
            copy(source, cases / source.name)
    for relative in [
      'testdata/hostile/python-webhook-site-env-exfil.py',
      'testdata/hostile/powershell-doc-archive-webhook-stealer.ps1',
      'testdata/discord-webhook-request-builder/positive-discord-webhook-post.js',
    ]:
        source = ROOT / relative
        copy(source, cases / source.name)
    control = scratch / 'codeception-control/generic/c3.php'
    if control.exists():
        copy(control, cases / 'codeception-c3.php')
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT))
    result = subprocess.run([
        'atomscan', '--no-update', '--mode', 'slow', '--follow=none',
        '-f', 'json', str(cases),
    ], cwd=ROOT, env=env, text=True, capture_output=True)
    (scratch / f'controls.{phase}.jsonl').write_text(result.stdout)
    (scratch / f'controls.{phase}.log').write_text(result.stderr)
    if 'ERROR' in result.stderr or not result.stdout.strip():
        raise RuntimeError(result.stderr)
    records = {}
    for line in result.stdout.splitlines():
        for file in json.loads(line)['raw']['files']:
            records[Path(file['path']).name] = {
                trait['id']: trait['crit'] for trait in file.get('traits', [])
            }
    root_expected = {
      'header-shadow.php': (True, True),
      'renamed-shadow.php': (True, True),
      'get-include.php': (True, False),
      'direct-file-include.php': (True, False),
      'arithmetic-include.php': (False, False),
      'request-include.php': (True, False),
      'different-fallback.php': (True, False),
      'guarded-fallback.php': (True, False),
      'unrelated-constants.php': (False, False),
      'no-include.php': (False, False),
      'server-environment.php': (False, False),
      'session-root.php': (False, False),
      'quoted-source.php': (False, False),
      'interpolated-constant.php': (False, False),
      'interpolated-key.php': (False, False),
      'interpolated-fallback.php': (True, False),
      'codeception-c3.php': (False, False),
    }
    for name, expected in root_expected.items():
        if name not in records:
            if name == 'codeception-c3.php':
                continue
            raise AssertionError(name)
        found = (ROOT_RULE in records[name], SHADOW_RULE in records[name])
        assert found == expected, (name, found, expected)
    assert records['openx-reader.php']['micro-behaviors/process/interpreter/eval/source::php-read-then-include-same-path'] == 3
    assert P+'asset-reader-executes-its-argument' not in records['openx-reader.php']
    webhook = 'objectives/exfiltration/messaging/webhook::'
    assert records['license-webhook.js'][webhook+'license-validator-webhook'] == 5
    assert records['license-webhook.js'][webhook+'webhook-license-credential-exfil'] == 5
    assert records['message-channel-name.js'][MOVED[next(k for k in MOVED if 'send-message' in k)]] == 3
    assert records['license-name.js'][MOVED[next(k for k in MOVED if 'licensekey' in k)]] == 3
    before_path = scratch/'controls.before.jsonl'
    if before_path.exists():
        before = {}
        for line in before_path.read_text().splitlines():
            for file in json.loads(line)['raw']['files']:
                before[Path(file['path']).name] = {t['id']:t['crit'] for t in file.get('traits', [])}
        for name in ['license-webhook.js','python-webhook-site-env-exfil.py',
                     'powershell-doc-archive-webhook-stealer.ps1',
                     'positive-discord-webhook-post.js','apps-script-license.js',
                     'discord-api-channel-name.js']:
            for old_id, crit in before[name].items():
                new_id = MOVED.get(old_id, old_id)
                assert records[name].get(new_id) == crit, (name, old_id, crit)
    (scratch/'controls-summary.json').write_text(json.dumps(records,indent=2)+'\n')
    print(f'{len(records)} focused cases passed')
    return records

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', type=Path, required=True)
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    run(args.scratch, 'after')
