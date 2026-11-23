@echo off
powershell -NoProfile -Command "Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty CurrentRefreshRate"
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce /v Setup /t REG_SZ /d C:\ProgramData\Vendor\setup.exe /f
