#!/usr/bin/env python3
"""Static trait regressions: app names and dialog titles imply no attacker intent."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
base = 'metadata/file/string/application-name::'
reference = 'micro-behaviors/process/create/script/osascript::osascript-settings-reference'
shell_reference = 'micro-behaviors/process/create/script/apple-event::shell-with-settings-reference'
obsolete = {
    'micro-behaviors/process/create/script/osascript::osascript-settings',
    'micro-behaviors/process/create/script/osascript::ref-system-prefs',
    'micro-behaviors/process/create/script/osascript::ref-system-settings',
    'objectives/execution/automation/compiled::automates-settings',
    'objectives/execution/automation/compiled::shell-with-settings',
}
for name, atom in [('dialog', 'system-preferences-name-reference'),
                   ('settings', 'system-settings-name-reference'), ('unrelated', None)]:
    path = root / 'testdata/taxonomy/macos-settings-reference' / (name + '.applescript')
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)],
                            capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    traits = [trait for file in report['files'] for trait in file['traits']]
    ids = {trait['id'] for trait in traits}
    assert not ids & obsolete, (name, ids & obsolete)
    assert not [trait for trait in traits if trait['crit'] >= 4], (name, traits)
    wanted = {reference, shell_reference, base + 'settings-app-name-reference'}
    if atom:
        wanted.add(base + atom)
        assert wanted <= ids, (name, wanted - ids)
    else:
        assert not wanted & ids, (name, wanted & ids)
    print(name + ': passed')
