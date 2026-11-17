Start-Process -FilePath curl.exe -WindowStyle Hidden -ArgumentList @('-fsSL','https://example.invalid/health')
curl.exe --location https://example.invalid/file
