$text = 'SGVs bG8='
$bytes = [Convert]::FromBase64String([regex]::Replace($text, '\s', ''))
[Text.Encoding]::UTF8.GetString($bytes)
