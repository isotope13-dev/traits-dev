Start-Process powershell.exe -ArgumentList "Get-Date"
New-ItemProperty -Path HKCU:\Software\Example -Name test -Value 1
Start-Process schtasks.exe -ArgumentList "/Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I"
