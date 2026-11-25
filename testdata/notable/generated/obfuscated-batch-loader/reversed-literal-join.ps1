$name = ('gnirtS46esaBmorF'[-1..-16] -join '')
$value = [Convert]::FromBase64String($name)
[Text.Encoding]::UTF8.GetString($value[0..15])
