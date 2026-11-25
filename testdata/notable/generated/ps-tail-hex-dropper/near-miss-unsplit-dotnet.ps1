Add-Type -AssemblyName 'System.Windows.Forms'
$psi = New-Object System.Diagnostics.ProcessStartInfo('dotnet', '--version')
$proc = [System.Diagnostics.Process]::Start($psi)
$proc.WaitForExit()
