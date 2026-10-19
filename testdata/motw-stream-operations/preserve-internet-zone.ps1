$file = Join-Path $env:TEMP "stream-check.txt"
Set-Content -LiteralPath $file -Value "old text"
Set-Content -LiteralPath "${file}:Zone.Identifier" -Value "[ZoneTransfer]`r`nZoneId=3`r`n"
Set-Content -LiteralPath $file -Value "new text"
$zone = Get-Content -LiteralPath $file -Stream Zone.Identifier -Raw
if ($zone -notmatch "ZoneId=3") { throw "Internet zone was lost" }
