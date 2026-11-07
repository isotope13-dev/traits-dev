@echo off
schtasks /create /tn "Contoso Cleanup" /tr "powershell.exe -WindowStyle Hidden -File \"C:\Program Files\Contoso\Tools\cleanup.ps1\"" /sc daily /st 03:00 /f
