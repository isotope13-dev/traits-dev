$download = "$env:TEMP\installer.exe"
Invoke-WebRequest -Uri 'https://downloads.example.invalid/setup.exe' -OutFile $download
Start-Process -FilePath $download -ArgumentList '/S' -Wait
Start-Process -FilePath $existingDaemon -ArgumentList 'serve' -WindowStyle Hidden
