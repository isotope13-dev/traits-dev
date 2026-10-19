$zone = Get-Content -LiteralPath $file -Stream Zone.Identifier
Set-Content -LiteralPath $report -Value $zone
