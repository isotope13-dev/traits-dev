# Inert maintenance-installer control; do not execute this fixture.
$ErrorActionPreference = 'Stop'
$archive = Join-Path $env:TEMP 'maintenance.zip'
$target = Join-Path $env:LOCALAPPDATA 'Maintenance'
Invoke-WebRequest -Uri 'https://updates.example.test/maintenance.zip' -OutFile $archive
if ((Get-FileHash -Path $archive -Algorithm SHA256).Hash -ne $env:EXPECTED_SHA256) {
    throw 'Archive integrity check failed'
}
Expand-Archive -Path $archive -DestinationPath $target -Force
$action = '"' + (Join-Path $target 'Maintenance.exe') + '" --check-updates'
schtasks /create /tn MaintenanceUpdates /sc hourly /mo 3 /tr $action /f
Remove-Item $PSCommandPath -Force
