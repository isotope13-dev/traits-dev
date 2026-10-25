#!/usr/bin/env python3
"""Validate saved cleave JSONL; never execute a sample."""
import json
from pathlib import Path
import sys
reports = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    report = json.loads(line)
    file = report['files'][0]
    reports[Path(file['path']).name] = {t['id']: t['crit'] for t in file.get('traits', [])}
node = 'micro-behaviors/process/create/hidden::node-execsync-hidden-ignored-stdio'
hidden = 'objectives/evasion/process/hidden/execution::node-concealed-shortlink-shell-stage'
wsh = 'micro-behaviors/process/create/hidden::wsh-run-hidden-quoted-call'
com = 'objectives/persistence/system/registry/com-hijack::typelib-scriptlet-hijack'
encoded = 'objectives/anti-static/obfuscation/encoding/base64::typelib-base64-scriptlet-concealment'
for name in ['node-reversed-options.js']:
    assert node in reports[name] and hidden in reports[name], name
for name in ['node-split-options.js', 'node-visible.js', 'node-output.js']:
    assert node not in reports[name] and hidden not in reports[name], name
assert node in reports['node-vendor.js'] and hidden not in reports['node-vendor.js']
assert wsh in reports['hidden-scriptlet.ps1']
assert wsh not in reports['visible-scriptlet.ps1']
for name in ['placeholder.ps1', 'boolean-arithmetic.ps1', 'hidden-scriptlet.ps1', 'visible-scriptlet.ps1', 'lower-write.ps1', 'upper-write.ps1', 'mention-write.ps1', 'node-vendor.js', 'typelib-no-write.ps1']:
    assert not any(c >= 4 for c in reports[name].values()), name
write = 'micro-behaviors/fs/write/file/full::powershell-set-content-call'
for name in ['lower-write.ps1', 'upper-write.ps1']:
    assert write in reports[name], name
assert write not in reports['mention-write.ps1']
assert 'metadata/lang/source/literal::cdm-substitution-placeholder' in reports['placeholder.ps1']
assert 'well-known/malware/botnet/powmix::powmix-loader' in reports['powmix-placeholder-loader.ps1']
assert 'objectives/evasion/process/hidden/execution::typelib-scriptlet-hidden-shell' not in reports['typelib-visible.ps1']
for name in ['typelib-plaintext.ps1', 'typelib-no-base64-decoder.ps1']:
    assert encoded not in reports[name], name
assert com in reports['typelib-plaintext.ps1']
print('All focused runtime-trait assertions passed.')
