$env:CURRENT_SCRIPT = $MyInvocation.MyCommand.Path
$env:OLD_CACHE = Join-Path $env:TEMP 'expired-cache.txt'
Remove-Item -LiteralPath $env:OLD_CACHE -Force
