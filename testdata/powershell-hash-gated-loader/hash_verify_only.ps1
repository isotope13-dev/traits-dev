# Fixture: verifies a file digest before use. Hash gate without any
# decryption or dynamic execution.
$hash = [System.Security.Cryptography.SHA256]::Create()
$stream = [System.IO.File]::OpenRead('data.bin')
$actual = [BitConverter]::ToString($hash.ComputeHash($stream)).Replace('-', '').ToLowerInvariant()
$stream.Close()
if ($actual -eq 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb') {
    Write-Host 'checksum ok'
}
