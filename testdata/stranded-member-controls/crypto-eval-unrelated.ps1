$aes = New-Object Security.Cryptography.AesManaged
$decryptor = $aes.CreateDecryptor()
$ciphertext = [Convert]::FromBase64String($encoded)
$plain = $decryptor.TransformFinalBlock($ciphertext, 0, $ciphertext.Length)
$secret = [Text.Encoding]::UTF8.GetString($plain)
Write-Output $secret
Invoke-Expression '$env:USERPROFILE'
