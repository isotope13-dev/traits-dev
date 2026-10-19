# Decrypt data for display; evaluate an unrelated local expression.
$aes = New-Object Security.Cryptography.AesManaged
$decryptor = $aes.CreateDecryptor()
$ciphertext = [Convert]::FromBase64String($encoded)
$plain = $decryptor.TransformFinalBlock($ciphertext, 0, $ciphertext.Length)
Write-Output ([Text.Encoding]::UTF8.GetString($plain))
$payloadStatus = "Write-Output 'ready'"
Invoke-Expression $payloadStatus
