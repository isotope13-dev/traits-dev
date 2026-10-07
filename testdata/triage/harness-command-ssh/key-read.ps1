$dir = Join-Path $env:USERPROFILE ".ssh"
$names = @("id_rsa", "id_ed25519", "id_ecdsa", "id_dsa")
Get-Content (Join-Path $dir $names[0])
