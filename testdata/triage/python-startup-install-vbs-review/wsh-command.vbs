Set worker = CreateObject("WScript.Shell")
worker.Run "powershell.exe -NoProfile -Command Write-Output 1", 0, False
