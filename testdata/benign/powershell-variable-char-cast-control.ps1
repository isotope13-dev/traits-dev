$codes = @(72, 101, 108, 108, 111)
$message = -join ($codes | ForEach-Object { [char]$_ })
Write-Output $message
