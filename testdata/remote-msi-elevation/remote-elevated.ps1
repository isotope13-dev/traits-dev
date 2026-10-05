Start-Process "$PSCommandPath" -Verb RunAs
msiexec.exe /i "https://packages.example.invalid/management.msi" /quiet /norestart
