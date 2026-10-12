$b = [Convert]::FromBase64String($encoded)
$a = New-Object System.Security.Cryptography.AesManaged
$d = $a.CreateDecryptor()
$plain = [Text.Encoding]::UTF8.GetString($d.TransformFinalBlock($b,0,$b.Length))
$plain | ConvertFrom-Json
