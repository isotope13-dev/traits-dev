$key = 0
$numbers = @(87,114,105,116,101,45,79,117,116,112,117,116,32,39,104,105,39)
$text = -join ($numbers | ForEach-Object { [char]($_ -bxor $key) })
& ([scriptblock]::Create($text))
