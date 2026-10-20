@echo off
REM Download and launch without evasion or an unauthorized action.
curl -fsSL "https://downloads.example.invalid/update.exe" -o "%TEMP%\update.exe"
start "" "%TEMP%\update.exe"
