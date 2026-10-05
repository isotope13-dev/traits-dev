$InstallerURL = "https://support.example.invalid/Bin/ScreenConnect.ClientSetup.msi"
$DownloadPath = "C:\Windows\Temp\ClientSetup.msi"
Invoke-WebRequest -Uri $InstallerURL -OutFile $DownloadPath
msiexec.exe /i C:\Windows\Temp\ClientSetup.msi /qn
