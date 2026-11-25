@echo off
cscript.exe //nologo slmgr.vbs /skms 10.0.0.5
cscript.exe //nologo slmgr.vbs /ato
certutil.exe -addstore "Root" custom_ca.cer
sc.exe stop sppsvc
netsh advfirewall firewall add rule name="KMS1688" dir=in action=allow protocol=TCP localport=1688
taskkill.exe /f /im SppExtComObj.exe
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\SppExtComObj.exe" /f /v "Debugger" /t REG_SZ /d "C:\Temp\my_hook.exe"
