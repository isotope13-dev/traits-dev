# Readiness-style prerequisite manifest: collector tool requirements are
# quoted names in a table, verified with Get-Command, never executed.
# Naming recon cmdlets is not running host discovery.
$commandsByCollector = [ordered]@{
    System  = @('whoami.exe', 'w32tm.exe')
    Network = @('Get-NetAdapter', 'Get-NetIPAddress', 'Get-NetRoute', 'Get-NetTCPConnection', 'ipconfig.exe')
}

$commandNames = @($commandsByCollector['Network'])
$missing = @($commandNames | Where-Object { $null -eq (Get-Command -Name $_ -ErrorAction SilentlyContinue) })
if ($missing.Count -eq 0) {
    Write-Output 'All checked collector commands are available.'
}
