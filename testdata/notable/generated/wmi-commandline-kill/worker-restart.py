import subprocess
PS = ("Get-CimInstance -ClassName Win32_Process -Filter \"Name='python.exe'\" | "
      "Where-Object {$_.CommandLine -match 'worker'} | Stop-Process -Force")
subprocess.run(["powershell", "-Command", PS])
