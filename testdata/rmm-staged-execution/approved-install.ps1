Invoke-WebRequest -Uri "https://support.example.invalid/ScreenConnect.ClientSetup.msi" -OutFile "C:\Windows\Temp\ClientSetup.msi"
msiexec.exe /i C:\Windows\Temp\ClientSetup.msi /qn
