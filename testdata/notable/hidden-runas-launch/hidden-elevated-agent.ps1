$arguments = "-WindowStyle Hidden -NoProfile -File `"$PSCommandPath`""
Start-Process -FilePath "powershell.exe" -ArgumentList $arguments -Verb RunAs -WindowStyle Hidden
