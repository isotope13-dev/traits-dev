"""INF-driven CMSTP elevation bypass kit.

Run: python3 testdata/cmstp-inf-bypass-kit/verify.py <scratch-directory>

Unlike the COM-moniker CMSTP bypass, this technique crafts an INF whose
pre-setup section runs attacker commands, kills cmstp so the evil profile
installs cleanly, and disables UAC policy. `cmstp-inf-presetup-bypass-kit`
requires all three legs: a lone setup INF (printer drivers use
RunPreSetupCommands legitimately) or a plain VPN provisioner invoking
cmstp.exe must not convict.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/privilege-escalation/elevation-control/uac-bypass/inf::'
          'cmstp-inf-presetup-bypass-kit')

POSITIVE = """\
[PreSetupCommandsSection]
RunPreSetupCommands=payload.exe /setup
taskkill /IM cmstp.exe /F
cmstp.exe /au evil.inf
reg.exe ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 0 /f
"""

PRINTER_INF_ONLY = """\
[PreSetupCommandsSection]
RunPreSetupCommands=rundll32 printui.dll,PrintUIEntry /ia /f driver.inf
"""

VPN_PROVISIONER_ONLY = """\
cmstp.exe /au corpvpn.inf
"""


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'bypass-kit-positive.bat': (POSITIVE, True),
        'printer-inf-negative.bat': (PRINTER_INF_ONLY, False),
        'vpn-provisioner-negative.bat': (VPN_PROVISIONER_ONLY, False),
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
