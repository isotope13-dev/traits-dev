$package = Join-Path $env:TEMP '8e671ad0b13c4d83b641172f2d483a19_Update.msi'
$client = New-Object Net.WebClient
$client.DownloadFile('https://downloads.example.org/client.msi', $package)
Start-Process msiexec.exe -ArgumentList "/i $package /passive /norestart" -Wait
