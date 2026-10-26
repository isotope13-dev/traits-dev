# Fixture: AES-decrypts a config blob and writes it out. No hash gate, no
# ScriptBlock, no obfuscated entry.
function Read-Config {
    $key = [Convert]::FromBase64String('MDEyMzQ1Njc4OUFCQ0RFRjAxMjM0NTY3ODlBQkNERUY=')
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV = [Convert]::FromBase64String('QUJDREVGR0hJSktMTU5PUA==')
    $decryptor = $aes.CreateDecryptor()
    $cipher = [Convert]::FromBase64String('qrvM3T1uQ3h6rC9z7Y9j1U2d5V7h4R6t8P0o3N6k=')
    $plain = $decryptor.TransformFinalBlock($cipher, 0, $cipher.Length)
    [System.IO.File]::WriteAllText('config.json', [System.Text.Encoding]::UTF8.GetString($plain))
    $decryptor.Dispose()
    $aes.Dispose()
}
Read-Config
