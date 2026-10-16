Start-Process schtasks.exe -ArgumentList '/Run /TN "\Microsoft\Windows\DiskCleanup\SilentCleanup" /I' -Wait
Start-Process sdclt.exe -ArgumentList '/KickOffElev' -Wait
