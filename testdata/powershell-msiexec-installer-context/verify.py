"""WebClient executable-URL/process-start context remains a neutral capability.

The historical MSI exclusion is preserved during relocation; ordinary EXE
installers retain the capability without a hostile dropper claim.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('micro-behaviors/process/create/spawn::'
          'powershell-webclient-executable-url-start-context')

NEGATIVE = """\
$WebClient = New-Object System.Net.WebClient
$WebClient.DownloadFile("https://downloads.example.com/installer/Example.msi", "$env:TEMP\\Example.msi")
$uninstallIds = Find-UninstallGuids -Match "Example"
foreach ($uninstallId in $uninstallIds) {
  Start-Process msiexec.exe -ArgumentList "/x $uninstallId /qn"
}
msiexec.exe /qn /i $env:TEMP\\Example.msi
"""

POSITIVE = """\
$WebClient = New-Object System.Net.WebClient
$WebClient.DownloadFile("https://downloads.example.com/installer/Example.exe", "$env:TEMP\\Example.exe")
Start-Process "$env:TEMP\\Example.exe"
"""


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'msi-installer-negative.ps1': (NEGATIVE, False),
        'plain-exe-positive.ps1': (POSITIVE, True),
    }
    for name, (body, present) in cases.items():
        path = dest / name
        path.write_text(body)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(path)],
            env=dict(os.environ, CLEAVE_VALIDATE='0'),
            text=True, capture_output=True, check=True)
        report = json.loads(result.stdout)
        ids = {t['id'] for entry in report['files'] for t in entry['traits']}
        assert (TARGET in ids) == present, (name, sorted(ids))
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
