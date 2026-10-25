#!/usr/bin/env python3
"""Check saved JSONL from controls copied outside testing paths; execute no sample."""
import json
from pathlib import Path
import sys
reports = {}
for line in Path(sys.argv[1]).read_text().split('\n'):
    if line:
        report = json.loads(line)
        file = report['raw']['files'][0]
        reports[Path(file['path']).name] = {t['id']: t['crit'] for t in file.get('traits', [])}
flag = 'micro-behaviors/process/create/flags::python-create-no-window-hex'
com = 'objectives/persistence/system/registry/com-hijack::typelib-scriptlet-hijack'
library = 'micro-behaviors/fs/path/library::windows-lib-directory-component'
for name in ['window-direct.py', 'window-alias.py', 'window-wrapper.py']:
    assert flag in reports[name], name
for name in ['window-unrelated.py', 'window-overwritten.py']:
    assert flag not in reports[name], name
for name in ['python-lib.py', 'other-lib.py']:
    assert library in reports[name], name
for name in ['com-scriptlet.py', 'typelib-read.py', 'installer.py']:
    assert not any(c >= 4 for c in reports[name].values()), name
assert library not in reports['com-scriptlet.py']
for name in ['typelib-write.py', 'zipline-stage-excerpt.ps1', 'f531bec8ad2d-folded.ps1']:
    assert com in reports[name], name
assert sum(c == 5 for c in reports['py-per-os-pipe.py'].values()) >= 4
for name in ['behaviors-3b5ee8d954dc71f1.js', 'lVCGkEMBgMoyFynrqkXj6QaKkK4.js']:
    assert not any(c >= 4 for c in reports[name].values()), name
print('Focused assertions passed: numeric flags, COM writes/reads, installers, paths, dependencies')
