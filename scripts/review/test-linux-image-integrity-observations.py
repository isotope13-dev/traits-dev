#!/usr/bin/env python3
"""Check image-customization observations and unrelated command negatives."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PREFIX = 'micro-behaviors/os/kernel/boot::'
SIG = PREFIX + 'sed-remove-module-signature-enforcement-flag'
IMA = PREFIX + 'sed-add-ima-appraisal-off-flag'
MASK = 'micro-behaviors/os/service/disable::shell-mask-update-engine'
source = '''#!/bin/sh
sed -i \\
  -e 's/module.sig_enforce=1//' \\
  -e 's/cros_efi/cros_efi ima_appraise=off/' "$grub"
sudo systemctl mask update-engine
'''
cases = {
    'complete': (source, {SIG, IMA, MASK}),
    'without-signature-expression': (source.replace('sig_enforce=1', 'sig_enforce=0'), {IMA, MASK}),
    'enforce-appraisal': (source.replace('ima_appraise=off', 'ima_appraise=enforce'), {SIG, MASK}),
    'other-service': (source.replace('mask update-engine', 'mask example-engine'), {SIG, IMA}),
    'service-suffix': (source.replace('mask update-engine', 'mask update-engine.service'), {SIG, IMA, MASK}),
    'commented-out': ('\n'.join('# ' + s for s in source.splitlines()) + '\n', set()),
    'restore-not-remove': (source.replace('s/module.sig_enforce=1//', 's/module.sig_enforce=0/1/'), {IMA, MASK}),
    'stop-not-mask': (source.replace('systemctl mask', 'systemctl stop'), {SIG, IMA}),
}
with tempfile.TemporaryDirectory(prefix='image-integrity-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.sh')
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                            check=True, capture_output=True, text=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = {t['id'] for t in report.get('traits', [])} & {SIG, IMA, MASK}
        assert found == cases[name][1], (name, found, cases[name][1])
print('Image-integrity observations distinguish disabling expressions and mask commands')
