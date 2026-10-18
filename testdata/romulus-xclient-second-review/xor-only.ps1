$key = 23
$numbers = @(97, 98, 99)
$text = -join ($numbers | ForEach-Object { [char]($_ -bxor $key) })
Write-Output $text
