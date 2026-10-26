$aes = New-Object Security.Cryptography.AesManaged
$decryptor = $aes.CreateDecryptor()
$ciphertext = [Convert]::FromBase64String($encoded)
Invoke-Expression ([Text.Encoding]::UTF8.GetString($decryptor.TransformFinalBlock($ciphertext, 0, $ciphertext.Length)))
