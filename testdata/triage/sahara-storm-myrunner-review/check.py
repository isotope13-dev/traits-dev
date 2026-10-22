#!/usr/bin/env python3
"""Check name-reference placement and retain real invocation/attack coverage."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CLEAVE = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
NAME = 'micro-behaviors/fs/path/application/executable::mshta-name-reference'
CALL = 'micro-behaviors/process/create/launch::mshta-powershell-call'
REF = NAME
OLD = 'micro-behaviors/process/create/launch::mshta-execution'
CASES = [
    (HERE / 'unrelated-com.vbs', ['micro-behaviors/os/com/automation::mshta-reference-variable-getobject'], ['objectives/execution/interpreter/script/mshta::office-macro-mshta-variable-moniker', 'micro-behaviors/process/script/wsh::wsh-getobject-script-url-profile']),
    (HERE / 'script-moniker.vbs', ['micro-behaviors/os/com/automation::mshta-reference-variable-getobject', 'micro-behaviors/process/script/wsh::wsh-getobject-script-url-profile'], ['objectives/execution/interpreter/script/mshta::office-macro-mshta-variable-moniker']),
    (HERE / 'name.js', [NAME, REF], [CALL, OLD]),
    (HERE / 'invoke.ps1', [CALL], [NAME, OLD]),
    (HERE / 'near-miss.js', [], [NAME, CALL, REF, OLD]),
    (HERE / 'public.bat', [REF, 'objectives/execution/interpreter/script/mshta::batch-background-public-mshta-stage'], [OLD]),
    (ROOT / 'testdata/taxonomy/node-root-truncation/mshta-image.js', [NAME, 'micro-behaviors/process/create/eval::mshta-inline-about-document'], [CALL, OLD]),
    (ROOT / 'testdata/hostile/wsh-reversed-mshta-remote-launch.vbs', ['objectives/execution/interpreter/script/mshta::reversed-mshta-remote-launch', 'objectives/command-and-control/dropper/file-exec/command/script-host-download::wsh-reversed-mshta-hidden-remote-run'], [OLD]),
]
# test-rules evaluates unconsumed composites as well as emitted findings.
def check(case):
    import re
    path, yes, no = case
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(path), '--rules', ','.join(yes + no)], capture_output=True, text=True, env=dict(os.environ, CLEAVE_VALIDATE='0'))
    if result.returncode:
        raise AssertionError(result.stderr + result.stdout)
    states = {trait: state == 'MATCHED' for state, trait in re.findall(r'(?m)^(MATCHED|NOT MATCHED) (\S+)', result.stdout)}
    for trait in yes:
        assert states.get(trait) is True, f'{path.name}: expected {trait}\n{result.stdout}'
    for trait in no:
        assert not states.get(trait, False), f'{path.name}: unexpected {trait}\n{result.stdout}'

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(check, CASES))
print(f'PASS: {len(CASES)} reference, invocation, near-miss and attack cases')
