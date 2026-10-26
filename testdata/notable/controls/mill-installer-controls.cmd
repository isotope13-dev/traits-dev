@echo off
REM Minimized vendor empty-machine front door: fetches its own bootstrap
REM from the vendor repo and runs the companion service helper. The
REM download and launch legs stay notable while the suspicious composite
REM stays quiet via the official-installer context.
set "BOOT=%~dp0bootstrap.ps1"
if exist "%BOOT%" goto haveboot
set "BOOT=%TEMP%\mill-bootstrap.ps1"
curl -fsSL "https://gitlab.com/pyginapithon/the-mill/-/raw/main/scripts/bootstrap.ps1" -o "%BOOT%"
:haveboot
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%BOOT%" %*
set "HELPER=%USERPROFILE%\.mill\register-windows-services.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%HELPER%"
