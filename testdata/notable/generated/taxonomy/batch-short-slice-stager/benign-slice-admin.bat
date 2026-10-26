@echo off
setlocal EnableDelayedExpansion
rem Rotate the first three characters off a status prefix.
set "STAT=OK:200:ready"
set "CODE=!STAT:~0,2!"
set "NUMB=!STAT:~3,3!"
set "FLAG=!STAT:~7,5!"
echo %CODE% %NUMB% %FLAG%
powershell -NoProfile -Command "Get-Date -Format o"
