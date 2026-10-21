$text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($inputText))
Write-Output $text
