Start-Process -FilePath curl.exe -WindowStyle Hidden -ArgumentList @('-s','-o','NUL','https://example.invalid/health')
