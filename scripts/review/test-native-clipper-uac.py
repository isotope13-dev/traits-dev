#!/usr/bin/env python3
"""Exercise native clipboard replacement and ComputerDefaults hijack evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
clip = r'''char *a = "^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$";
char *b = "^(?:[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93})$";
void f() { GetClipboardData(CF_TEXT); SetClipboardData(CF_TEXT, ptr);
if (std::regex_match(input, regex) && input != Address) {
    SetClipboardText(Address);
} }
'''
uac = r'''void f(){ system("reg add HKEY_CURRENT_USER\\Software\\Classes\\ms-settings\\Shell\\Open\\command /v DelegateExecute /d x");
system("start /B ComputerDefaults.exe"); }
'''
cases = {'clip.cpp': clip, 'no-address.cpp': clip.replace('[0-9AB]', '[0-9XY]').replace('bc1', 'abc'),
         'no-match.cpp': clip.replace('std::regex_match(input, regex)', 'other_match(input, regex)'),
         'no-swap.cpp': clip.replace('input != Address', 'input == Address'),
         'uac.cpp': uac, 'no-reg.cpp': uac.replace('reg add', 'reg query'),
         'no-target.cpp': uac.replace('ComputerDefaults.exe', 'ordinary.exe')}
with tempfile.TemporaryDirectory(prefix='native-clipper-uac-') as temp:
    root = Path(temp)
    for name, source in cases.items():
        (root / name).write_text(source)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / name) for name in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    clip_id = 'objectives/impact/crypto-manipulation/clipboard::source-native-regex-clipboard-address-replacement'
    uac_id = 'objectives/privilege-escalation/elevation-control/uac-bypass/hijack::native-reg-computerdefaults-hijack'
    assert clip_id in found['clip.cpp']
    for name in ('no-address.cpp', 'no-match.cpp', 'no-swap.cpp'):
        assert clip_id not in found[name], name
    assert uac_id in found['uac.cpp']
    assert uac_id not in found['no-reg.cpp'] and uac_id not in found['no-target.cpp']
    print('Native clipboard and UAC findings require their distinguishing evidence.')
