function Invoke-PrivescCheck
{
    $services = Get-Service | Where-Object { $_.StartType -eq 'Automatic' }
    $runKeys = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    $tasks = Get-ScheduledTask | Where-Object { $_.State -eq 'Ready' }
    return @($services, $runKeys, $tasks)
}
