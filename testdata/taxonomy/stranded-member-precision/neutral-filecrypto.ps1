# An ordinary backup transform; no ransom demands or unauthorized targeting.
param($Source, $Backup, $TemporaryFile)
$bytes = [IO.File]::ReadAllBytes($Source)
$algorithm = New-Object System.Security.Cryptography.AesManaged
$encryptor = $algorithm.CreateEncryptor()
$cipher = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length)
[IO.File]::WriteAllBytes($Backup, $cipher)
Remove-Item -Force $TemporaryFile
