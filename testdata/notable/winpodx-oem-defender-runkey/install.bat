@echo off
REM WinPodX guest provisioning: Defender exclusion and HKCU Run launcher.
echo [WinPodX] Adding Windows Defender exclusions...
powershell -NoProfile -Command "try { Add-MpPreference -ExclusionPath 'C:\OEM' -ErrorAction Stop } catch { }" >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v winpodx-agent /t REG_SZ /d "wscript.exe \"C:\Users\Public\winpodx\launchers\hidden-launcher.vbs\" powershell.exe -File C:\OEM\agent.ps1" /f
