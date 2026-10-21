$wire = "SGVsbG8sIHdvcmxkIQ=="
$source = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($wire))
Write-Output $source
