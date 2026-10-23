"""Exercise native concealment and Notes collection without running payloads."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--sample', type=Path, required=True)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
traits = Path(__file__).resolve().parents[3]
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(traits), RAYON_NUM_THREADS='2')
notes = 'micro-behaviors/data/property/enumerate::applescript-notes-bulk-properties'
theft = 'objectives/collection/app-data/notes/app::password-phishing-notes-property-collection'
conceal = 'objectives/anti-static/obfuscation/encoding/xor::sparse-cstring-state-xor-osascript'
exporter = '''tell application "Notes"
set accountsList to every account
repeat with accountItem in accountsList
set records to properties of every note in accountItem
end repeat
end tell
'''
phish = '''set reply to display dialog "Please enter device password to continue." default answer "" with hidden answer with icon caution
set passText to text returned of reply
do shell script "dscl . authonly " & quoted form of (system attribute "USER") & space & quoted form of passText
'''
cases = {}
for name, text, expected in [
    ('exporter.applescript', exporter, {notes}),
    ('phishing-notes.applescript', phish + exporter, {notes, theft}),
    ('phishing-without-notes.applescript', phish, set()),
    ('different-app.applescript', phish + exporter.replace('"Notes"', '"Reminders"'), set()),
    ('properties-word-only.applescript', phish + 'tell application "Notes"\nget name of every note\nend tell', set()),
    ('escaped.sh', 'osascript -e \'run script "' + (phish + exporter).replace('"', '\\\\"').replace('\n', '" & return & "') + '"\'\n', {notes, theft}),
]:
    p = args.scratch / name
    p.write_text(text)
    cases[name] = (p, expected, {notes, theft})
data = args.sample.read_bytes()
# Change the EOR instruction at the independently disassembled ARM64 site.
arm_base = 0x14000
site = arm_base + 0x864
assert data[site:site + 4] == bytes.fromhex('0801094a')
no_xor = bytearray(data)
no_xor[site:site + 4] = bytes.fromhex('0801090b')  # ADD w8,w8,w9
site_x64 = 0x4000 + 0x7f8
assert data[site_x64:site_x64 + 2] == bytes.fromhex('3385')
no_xor[site_x64] = 0x03  # ADD eax,[rbp+displacement]
no_shell = data.replace(b'_system\0', b'_systex\0')
assert no_shell != data
for name, content, expected in [
    ('native-original', data, {notes, theft, conceal}),
    ('native-add-instead-of-xor', no_xor, {notes, theft}),
    ('native-without-system-import', no_shell, {notes, theft}),
]:
    p = args.scratch / name
    p.write_bytes(content)
    cases[name] = (p, expected, {notes, theft, conceal})
results = []
for name, (p, expected, selected) in cases.items():
    result = subprocess.run(['cleave', '--traits-dir', str(traits), '--json', str(p)],
                            env=env, text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    observed = {t['id'] for f in report['files'] for t in f.get('traits', [])} & selected
    assert observed == expected, (name, expected, observed, result.stderr)
    levels = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])
              if t['id'] in selected}
    assert all(levels[t] == {notes: 3, theft: 4, conceal: 4}[t] for t in observed)
    results.append({'case': name, 'matched': sorted(observed)})
print(json.dumps({'status': 'passed', 'cases': results}, indent=2))
