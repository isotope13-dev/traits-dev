# Assemble a report in a caller-selected order, then open it in a viewer.
$parts = @('summary', 'details')
$order = @(1,0)
$report = -join ($order | ForEach-Object { $parts[$_] })
([IO.File])::WriteAllText($reportPath, $report)
$info = New-Object System.Diagnostics.ProcessStartInfo
$info.FileName = $viewer
$info.Arguments = $reportPath
$info.CreateNoWindow = $true
$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $info
[void]$proc.Start()
