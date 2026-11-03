#!/usr/bin/env python3
"""Check setuid compile target binding and root-shell context."""
import json
import pathlib
import subprocess
import tempfile

source = '''#!/bin/sh
code=$(cat <<EOF
int main() { setuid(0); execl("/bin/sh", "sh", 0); }
EOF
)
build() {
  echo "$code" > ./.helper.c
  gcc -o ./.helper ./.helper.c
  chown root:root OWNED
  chmod u+s PERMITTED
}
'''
cases = {
    'bound': (source.replace('OWNED', './.helper').replace('PERMITTED', './.helper'), True),
    'other-owner-target': (source.replace('OWNED', './other').replace('PERMITTED', './.helper'), False),
    'other-mode-target': (source.replace('OWNED', './.helper').replace('PERMITTED', './other'), False),
    'no-root-shell': (source.replace('setuid(0);', '').replace('OWNED', './.helper').replace('PERMITTED', './.helper'), False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (content, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.sh')
        path.write_text(content)
        data = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::compiled-setuid-root-shell') for t in data['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('Compiled setuid root shell target boundaries passed.')
