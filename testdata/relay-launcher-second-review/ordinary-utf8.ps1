$bytes = [System.Text.Encoding]::UTF8.GetBytes("hello")
$text = [System.Text.Encoding]::UTF8.GetString($bytes)
Write-Output $text
