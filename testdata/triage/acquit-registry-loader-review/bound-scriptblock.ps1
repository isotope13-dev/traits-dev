$source = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($inputText))
$work = [ScriptBlock]::Create($source)
& $work
