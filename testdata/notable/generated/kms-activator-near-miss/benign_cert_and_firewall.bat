@echo off
rem Legitimate vendor application setup and debugging configuration
certutil.exe -addstore "TrustedPublisher" myvendor.cer
netsh advfirewall firewall add rule name="MyApp" dir=in action=allow protocol=TCP localport=8080
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\myapp.exe" /f /v "Debugger" /t REG_SZ /d "vsjitdebugger.exe"
