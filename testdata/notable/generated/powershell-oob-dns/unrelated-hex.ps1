$text="inventory"
$hex = -join ([Text.Encoding]::UTF8.GetBytes($text) | ForEach-Object { $_.ToString("x2") })
Write-Output $hex
[Net.Dns]::GetHostAddresses("$index.$service.corp.example")
