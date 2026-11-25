$copyCmd = "Copy-Item 'C:\src\*' 'C:\dst' -Force"
Start-Process powershell -ArgumentList "-NoProfile -Command $copyCmd" -Verb RunAs -Wait -ErrorAction Stop
