Set-ItemProperty -Path 'HKCU:\Environment' -Name 'windir' -Value 'C:\Windows'
Start-Process schtasks.exe -ArgumentList '/Run /TN "\Microsoft\Windows\DiskCleanup\SilentCleanup" /I' -Wait
