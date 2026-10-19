#!/usr/bin/env python3
"""Check the remote-staging boundary without executing the WSH script."""
import argparse
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--sample-js', type=Path, required=True)
p.add_argument('--output-dir', type=Path, required=True)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
a.output_dir.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]
stage = 'objectives/execution/payload/file-exec::obfuscated-wsh-powershell-file-exec'
policy = 'objectives/evasion/security-bypass/policy/execution::obfuscated-js-activex-policy-bypass'
retired = 'objectives/execution/payload/file-exec::obfuscated-wsh-remote-script-file-command'
write = 'micro-behaviors/fs/write/content::powershell-extension-near-text-file-creation'
source = a.sample_js.read_text()
# These mutations test that incidental automation, documentation and partial
# command text cannot retain the staging conviction after a required role goes.
cases = [
    ('original.js', source, {stage, policy}, set()),
    ('local-script.js', re.sub(r'https?://[^\s\x27\x22]+', r'C:\\scripts\\local.ps1', source), set(), {stage, policy}),
    ('no-file-write.js', source.replace('CreateTextFile', 'ReadOnlyTextFile'), set(), {stage, policy}),
    ('file-option-only.js', source.replace(r'powershell.exe\x20-nop\x20-ep\x20bypass\x20-file', r'powershell.exe\x20-file'), set(), {stage, policy}),
    ('no-run-call.js', source.replace("['Run']", "['Inspect']"), set(), {stage, policy}),
    ('ordinary-script-writer.js', 'var ext=".ps1"; var fso=new ActiveXObject("Scripting.FileSystemObject");\nfso.CreateTextFile("generated"+ext,true);\n', {write}, {stage, policy}),
]
results = []
for name, text, required, forbidden in cases:
    path = a.output_dir / name
    path.write_text(text)
    r = subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    report = json.loads(r.stdout)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    assert required <= traits.keys(), (name, 'missing', sorted(required-traits.keys()))
    assert not (forbidden | {retired}) & traits.keys(), (name, 'unexpected', sorted((forbidden | {retired}) & traits.keys()))
    if write in traits:
        assert traits[write]['crit'] == 3, (name, 'neutral script-write observation must be notable')
    if name == 'ordinary-script-writer.js':
        assert not [t for t in traits.values() if t['crit'] >= 4], name
    results.append({'case': name, 'passed': True, 'required': sorted(required), 'forbidden': sorted(forbidden)})
(a.output_dir / 'results.json').write_text(json.dumps(results, indent=2)+'\n')
print(f'{len(results)} WSH staging and neutral script-writing controls passed')
