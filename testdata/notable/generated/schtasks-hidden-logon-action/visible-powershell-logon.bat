@echo off
schtasks /create /tn "Inventory Report" /tr "powershell.exe -NoProfile -File \"C:\Program Files\Contoso\Tools\report.ps1\"" /sc onlogon /f
powershell -WindowStyle Hidden -Command "Write-Host done"
