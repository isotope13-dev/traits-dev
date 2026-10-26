$asset = @'
FOgLmkLEnZ45edK5qkTSIr6RdIY7JmyY1eZsfL1nvwrC92om20uiSZMkD8rNhJIyUOkgHGpVq9AJ5Vg8+aZUEao0AK/dNvagtjSFZk9FP30=
'@
$key = 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8='
$iv = 'AAECAwQFBgcICQoLDA0ODw=='
$a = [System.Security.Cryptography.Aes]::Create()
$a.Mode = [System.Security.Cryptography.CipherMode]::CBC
$a.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
# This example reconstructs data; it never executes the decrypted value.
$a.Key = [Convert]::FromBase64String($key)
$a.IV = [Convert]::FromBase64String($iv)
$d = $a.CreateDecryptor()
$bytes = [Convert]::FromBase64String($asset)
$text = [Text.Encoding]::UTF8.GetString($d.TransformFinalBlock($bytes, 0, $bytes.Length))
Write-Host $text
