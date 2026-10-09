@echo off
setlocal
set "SCRIPT=%TEMP%\bootstrap-%RANDOM%.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest 'https://example.org/install.ps1' -OutFile $env:SCRIPT"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" %*
set "RESULT=%ERRORLEVEL%"
del /q "%SCRIPT%" >nul 2>nul
exit /b %RESULT%
