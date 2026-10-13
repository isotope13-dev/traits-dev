"""Exercise control binding without executing the PowerShell fixtures."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLICK = 'micro-behaviors/ui/window/automation::powershell-selected-allow-control-click'
APPROVAL = 'objectives/evasion/security-bypass/policy/access-control::powershell-security-dialog-auto-approval'
SOURCE = '''$clickMessage = 0x00f5
function Close-Prompt {
    $chosen = $controls | Where-Object { $_.Caption -match '(?i)allow' } | Select-Object -First 1
    if ($chosen) {
        [void][Native]::SendMessage($chosen.Handle, $clickMessage, [IntPtr]::Zero, [IntPtr]::Zero)
    }
}
function Find-Prompt {
    if ($caption -match '(?i)Security') { return $true }
    [void][Native]::EnumWindows($callback, [IntPtr]::Zero)
}
'''
CASES = [
    ('renamed', SOURCE, True, True),
    ('inline-message', SOURCE.replace('$clickMessage,', '245,'), True, True),
    ('local-message', SOURCE.replace('$clickMessage = 0x00f5\n', '').replace('function Close-Prompt {', 'function Close-Prompt {\n    $clickMessage = 245'), True, True),
    ('deny-target', SOURCE.replace("-match '(?i)allow'", "-match '(?i)deny'"), False, False),
    ('unrelated-handle', SOURCE.replace('$chosen.Handle,', '$other.Handle,'), False, False),
    ('unused-allow', SOURCE.replace('if ($chosen)', "$rejected = $controls | Where-Object { $_.Caption -match '(?i)deny' }; if ($chosen)").replace('$chosen.Handle,', '$rejected.Handle,'), False, False),
    ('reassigned-control', SOURCE.replace('if ($chosen)', '$chosen = $other; if ($chosen)'), False, False),
    ('commented-enumeration', SOURCE.replace('    [void][Native]::EnumWindows', '    # [void][Native]::EnumWindows'), True, False),
    ('commented-security', SOURCE.replace("    if ($caption -match", "    # if ($caption -match"), True, False),
    ('non-click-message', SOURCE.replace('0x00f5', '0x00f1'), False, False),
    ('ordinary-ui', SOURCE.replace('Security', 'Preferences'), True, False),
    ('comments-only', '\n'.join('# '+line for line in SOURCE.splitlines()), False, False),
    ('quoted-example', "$example = @'\n"+SOURCE+"'@\n", False, False),
]

def check(case):
    name, source, clicked, approval = case
    with tempfile.TemporaryDirectory(prefix='sap-triage-control-') as scratch:
        path = Path(scratch) / (name+'.ps1')
        path.write_text(source)
        result = subprocess.run([os.environ.get('CLEAVE','cleave'), '--traits-dir', str(ROOT), '--format', 'json', str(path)], capture_output=True, text=True, check=True,
            env={**os.environ, 'CLEAVE_SKIP_CACHE':'1', 'CLEAVE_NO_UPDATE_CHECK':'1'})
        traits = json.loads(result.stdout)['files'][0]['traits']
        ids = {t['id'] for t in traits}
        assert (CLICK in ids) == clicked, (name, 'click', ids)
        assert (APPROVAL in ids) == approval, (name, 'approval', ids)
        assert not any(t['crit']==5 for t in traits), (name, 'hostile control')
        print(name, 'passed', flush=True)

with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(check, CASES))
print('13 dialog approval controls passed')
