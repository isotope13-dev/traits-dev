$association = 'HKCU:\Software\Classes\Folder\shell\open\command'
Remove-Item -Path $association -Recurse -Force
Remove-Item -Path 'C:\Temp\outdated.ps1' -Force
