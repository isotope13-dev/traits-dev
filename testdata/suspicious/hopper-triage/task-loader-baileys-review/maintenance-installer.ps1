param([Parameter(Mandatory)][string]$ExpectedSha256)
$archive = Join-Path $env:TEMP 'maintenance.zip'
$target = Join-Path $env:LOCALAPPDATA 'Maintenance'
$client = New-Object System.Net.WebClient
$client.DownloadFile('https://updates.example.org/maintenance.zip', $archive)
if ((Get-FileHash $archive -Algorithm SHA256).Hash -ne $ExpectedSha256) {
    throw 'Administrator-pinned digest mismatch'
}
Expand-Archive -Path $archive -DestinationPath $target -Force
$action = New-ScheduledTaskAction -Execute (Join-Path $target 'maintain.exe') -Argument '--check'
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 3)
Write-Output 'Installing the requested three-hour maintenance task'
Register-ScheduledTask -TaskName 'Maintenance' -Action $action -Trigger $trigger -Force
Remove-Item $PSCommandPath -Force
