$commandPath = 'HKCU:\Software\Classes\mscfile\shell\open\command'
$handler = 'powershell.exe -File C:\admin\view-console.ps1'
New-ItemProperty -Path $commandPath -Name '(Default)' -Value $handler
